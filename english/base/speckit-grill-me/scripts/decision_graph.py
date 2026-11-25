"""Manage the temporary GraphML coverage map for one clarification interview."""

import argparse
import fcntl
import json
import os
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from graphlib import TopologicalSorter
from pathlib import Path


CATEGORIES = (
    "Functional scope and behavior", "Domain and data model", "Interaction and UX flow",
    "Non-functional quality", "Integrations and external dependencies",
    "Edge cases and failure handling", "Constraints and trade-offs",
    "Terminology consistency", "Completion signals", "Other",
)
PRIORITY = ("Missing", "Partial", "Deferred", "Outstanding", "Resolved", "Clear")
OPEN = {"Partial", "Missing"}
FIELDS = {"target", "scope", "categories", "status", "detail", "candidate"}
SNAPSHOTS = {"before_hold", "before_conflict"}
NS = "http://graphml.graphdrawing.org/xmlns"
ET.register_namespace("", NS)
PREFIX = "speckit-grill-me-"


def tag(name):
    return f"{{{NS}}}{name}"


def write_graph(path, nodes, revision, review):
    root = ET.Element(tag("graphml"))
    for field in sorted(FIELDS | SNAPSHOTS | {"review", "revision"}):
        owner = "graph" if field in {"review", "revision"} else "node"
        ET.SubElement(root, tag("key"), {
            "id": field, "for": owner, "attr.name": field, "attr.type": "string",
        })
    graph = ET.SubElement(root, tag("graph"), edgedefault="directed")
    ET.SubElement(graph, tag("data"), key="revision").text = str(revision)
    ET.SubElement(graph, tag("data"), key="review").text = json.dumps(sorted(review))
    for point_id, point in nodes.items():
        node = ET.SubElement(graph, tag("node"), id=point_id)
        for key in sorted(point.keys() - {"parents"}):
            value = point[key]
            if not isinstance(value, str):
                value = json.dumps(value, ensure_ascii=False)
            ET.SubElement(node, tag("data"), key=key).text = value
    for point_id, point in nodes.items():
        for parent in point["parents"]:
            ET.SubElement(graph, tag("edge"), source=parent, target=point_id)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as output:
        temporary = Path(output.name)
        try:
            ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
            output.flush()
            # Validate XML characters before replacing the last readable revision.
            ET.parse(temporary)
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)


def read_graph(path):
    graph = ET.parse(path).getroot().find(tag("graph"))
    metadata = {item.get("key"): item.text for item in graph.findall(tag("data"))}
    nodes = {}
    for node in graph.findall(tag("node")):
        point = {"parents": []}
        for field in node.findall(tag("data")):
            key = field.attrib["key"]
            value = field.text or ""
            point[key] = json.loads(value) if key in SNAPSHOTS or key == "categories" else value
        nodes[node.attrib["id"]] = point
    for edge in graph.findall(tag("edge")):
        nodes[edge.attrib["target"]]["parents"].append(edge.attrib["source"])
    return nodes, int(metadata["revision"]), set(json.loads(metadata["review"]))


def strings(value):
    return (isinstance(value, list)
            and all(isinstance(item, str) and item.strip() for item in value)
            and len(set(value)) == len(value))


def validate(nodes):
    identities = {}
    for point_id, point in nodes.items():
        for key in ("target", "scope", "status", "detail", "candidate"):
            if not isinstance(point.get(key), str):
                raise ValueError(f"{point_id}: expected text for {key}")
        if not point["target"].strip() or not point["scope"].strip():
            raise ValueError(f"{point_id}: supply a decision target and scope")
        identity = (point["target"].strip(), point["scope"].strip())
        if identity in identities:
            raise ValueError(f"{point_id}: same target and scope as {identities[identity]}")
        identities[identity] = point_id
        cats = point.get("categories")
        if not strings(cats) or not cats or set(cats).difference(CATEGORIES):
            raise ValueError(f"{point_id}: expected one or more distinct Glossary categories")
        status = point["status"]
        if status not in PRIORITY:
            raise ValueError(f"{point_id}: unknown status {status}")
        if (status in OPEN) != bool(point["candidate"].strip()):
            raise ValueError(f"{point_id}: only Partial/Missing points must carry a candidate")
        if status not in OPEN and not point["detail"].strip():
            raise ValueError(f"{point_id}: supply the settled result or hold rationale")
        if "before_hold" in point and status not in {"Resolved", "Outstanding", "Deferred"}:
            raise ValueError(f"{point_id}: release before_hold when the point becomes applicable")
        if ("before_conflict" in point and status in {"Resolved", "Clear"}
                and "before_hold" not in point):
            raise ValueError(f"{point_id}: release before_conflict when settling the conflict")
        if not strings(point["parents"]) or set(point["parents"]).difference(nodes):
            raise ValueError(f"{point_id}: invalid or unknown parent IDs")
    return list(TopologicalSorter({i: p["parents"] for i, p in nodes.items()}).static_order())


def descendants(nodes, order, roots):
    affected = set(roots)
    children = []
    for point_id in order:
        if affected.intersection(nodes[point_id]["parents"]):
            affected.add(point_id)
            children.append(point_id)
    return children


def overview(nodes, revision, review, order):
    aggregates = {}
    for category in CATEGORIES:
        statuses = {p["status"] for p in nodes.values() if category in p["categories"]}
        aggregates[category] = next((s for s in PRIORITY if s in statuses), None)
    settled_chain = set()
    ready = []
    for point_id in order:
        point = nodes[point_id]
        if point_id in review or not settled_chain.issuperset(point["parents"]):
            continue
        if point["status"] in OPEN:
            ready.append(point_id)
        elif point["status"] in {"Resolved", "Clear"} and "before_hold" not in point:
            settled_chain.add(point_id)
    return {"revision": revision, "review": [i for i in order if i in review],
            "dependency_ready": ready, "categories": aggregates, "nodes": nodes}


def apply_batch(nodes, revision, review, batch):
    if not isinstance(batch, dict) or batch.keys() - {"revision", "points", "reviewed"}:
        raise ValueError("expected a batch with revision, points and/or reviewed")
    if type(batch.get("revision")) is not int or batch["revision"] != revision:
        raise ValueError("stale or missing revision: show the graph and reconcile before retrying")
    changes = batch.get("points", [])
    reviewed = batch.get("reviewed", [])
    if not isinstance(changes, list) or not strings(reviewed) or not (changes or reviewed):
        raise ValueError("expected point changes or reviewed IDs")
    changed_parents = set()
    changed_links = set()
    touched = set()
    for change in changes:
        if not isinstance(change, dict) or change.keys() - (FIELDS | {
                "new", "id", "parents", "save", "release"}):
            raise ValueError("unknown point field or malformed change")
        if ("id" in change) == ("new" in change):
            raise ValueError("use new to create a point or id to update it")
        create = "new" in change
        point_id = change["new"] if create else change["id"]
        if not isinstance(point_id, str) or not re.fullmatch(r"D[0-9]+", point_id):
            raise ValueError("expected a decision ID such as D001")
        if create == (point_id in nodes) or point_id in touched:
            raise ValueError(f"{point_id}: duplicate creation/update or unknown ID")
        touched.add(point_id)
        point = nodes.setdefault(point_id, {"parents": [], "detail": "", "candidate": ""})
        old = point.copy()
        for action in ("save", "release"):
            if action in change:
                slot = change[action]
                if create or slot not in SNAPSHOTS:
                    raise ValueError(f"{point_id}: invalid snapshot operation")
                if action == "save":
                    point.setdefault(slot, {k: old[k] for k in ("status", "detail", "candidate")})
                elif slot in point:
                    del point[slot]
                else:
                    raise ValueError(f"{point_id}: no snapshot {slot} to release")
        for key in (FIELDS | {"parents"}) & change.keys():
            value = change[key]
            # XML readers normalize CR and CRLF to LF, including inside a decision's identity.
            if isinstance(value, str):
                value = value.replace("\r\n", "\n").replace("\r", "\n")
            point[key] = value
        if not create:
            if point["parents"] != old["parents"]:
                changed_links.add(point_id)
            if any(point.get(k) != old.get(k) for k in
                   ("target", "scope", "status", "detail", "before_hold")):
                changed_parents.add(point_id)
    order = validate(nodes)
    review.update(changed_links)
    review.update(descendants(nodes, order, changed_parents | changed_links))
    if set(reviewed).difference(review):
        raise ValueError("reviewed contains IDs outside the pending descendant review")
    review.difference_update(reviewed)
    return order


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="create a private session and print its GraphML path")
    for name in ("show", "match", "apply", "descendants", "check", "close"):
        sub = commands.add_parser(name)
        sub.add_argument("graph", type=Path)
        if name == "descendants":
            sub.add_argument("id")
        if name == "check":
            sub.add_argument("--interrupted", action="store_true",
                             help="allow an empty graph if stopped before the first scan")
    args = parser.parse_args()
    if args.command == "init":
        folder = Path(tempfile.mkdtemp(prefix=PREFIX, dir="/tmp"))
        path = folder / "decisions.graphml"
        try:
            write_graph(path, {}, 0, set())
        except BaseException:
            folder.rmdir()
            raise
        print(path)
        return
    path = args.graph.absolute()
    if (path.name != "decisions.graphml" or not path.parent.name.startswith(PREFIX)
            or path.parent.parent.resolve() != Path("/tmp").resolve()
            or path.is_symlink() or path.parent.is_symlink()):
        raise ValueError("use the session path returned by init")
    batch = json.load(sys.stdin) if args.command in {"apply", "match"} else None
    # Keep the lock stable across atomic graph replacements by locking the session directory.
    directory = os.open(path.parent, os.O_RDONLY)
    try:
        fcntl.flock(directory, fcntl.LOCK_EX)
        nodes, revision, review = read_graph(path)
        if args.command == "close":
            path.unlink()
            path.parent.rmdir()
            return
        if args.command == "apply":
            order = apply_batch(nodes, revision, review, batch)
            revision += 1
            write_graph(path, nodes, revision, review)
            result = {"revision": revision, "review": [i for i in order if i in review]}
        else:
            order = validate(nodes)
            if args.command == "descendants":
                if args.id not in nodes:
                    raise ValueError(f"unknown decision ID: {args.id}")
                result = descendants(nodes, order, {args.id})
            elif args.command == "check":
                pending = [i for i in order if i in review or nodes[i]["status"] in OPEN]
                if pending or (not nodes and not args.interrupted):
                    raise ValueError(f"incomplete coverage; open or unreviewed: {pending}")
                result = {"revision": revision, "complete": True}
            elif args.command == "show":
                result = overview(nodes, revision, review, order)
    finally:
        os.close(directory)

    if args.command == "match":
        from decision_neighbors import neighbors

        known = [{"id": point_id, "text": point["target"] + "\n" + point["scope"]}
                 for point_id, point in nodes.items()]
        result = {"revision": revision, **neighbors({"known": known, "incoming": batch})}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, ET.ParseError, KeyError, TypeError) as error:
        sys.exit(str(error))
