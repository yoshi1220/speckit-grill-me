"""Black-box regressions for the English base skill's session helper."""

import json
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


HELPER = (Path(__file__).resolve().parents[1] / "english/base/speckit-grill-me"
          / "scripts/decision_graph.py")
FUNCTIONAL = "Functional scope and behavior"
DATA = "Domain and data model"
EDGE = "Edge cases and failure handling"


def invoke(*args, batch=None):
    return subprocess.run([sys.executable, str(HELPER), *map(str, args)],
                          input=json.dumps(batch), capture_output=True, text=True)


def new(point_id, target, scope, category, *parents):
    return {"new": point_id, "target": target, "scope": scope, "categories": [category],
            "status": "Missing", "candidate": target + "?", "parents": list(parents)}


def resolve(point_id, detail):
    return {"id": point_id, "status": "Resolved", "detail": detail, "candidate": ""}


class Interview(unittest.TestCase):
    def setUp(self):
        result = invoke("init")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.graph = Path(result.stdout.strip())
        self.revision = 0
        self.addCleanup(self.close)

    def close(self):
        result = invoke("close", self.graph)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.graph.parent.exists())

    def run_ok(self, *args, batch=None):
        result = invoke(args[0], self.graph, *args[1:], batch=batch)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def apply(self, *points, reviewed=()):
        result = self.run_ok("apply", batch={"revision": self.revision, "points": points,
                                             "reviewed": reviewed})
        self.revision = result["revision"]
        return result["review"]

    def test_parent_change_restores_descendants_in_dependency_order(self):
        self.apply(new("D001", "Permit delegation", "Absent approver", FUNCTIONAL),
                   new("D002", "Name the delegate", "Approval history", DATA, "D001"),
                   new("D003", "Correct that name", "Approval history", EDGE, "D002"))
        self.assertEqual(self.run_ok("descendants", "D001"), ["D002", "D003"])
        self.assertEqual(self.run_ok("show")["dependency_ready"], ["D001"])

        self.apply(resolve("D001", "Prohibited (Round 1 Q1)."),
                   dict(resolve("D002", "Not applicable under D001."), save="before_hold"),
                   dict(resolve("D003", "Not applicable under D002."), save="before_hold"),
                   reviewed=["D002", "D003"])
        self.assertTrue(self.run_ok("check")["complete"])
        self.assertEqual(self.apply(resolve("D001", "Allowed during absence (Round 2 Q1).")),
                         ["D002", "D003"])
        self.assertNotEqual(invoke("check", self.graph).returncode, 0)
        records = self.run_ok("show")["nodes"]
        updates = [{"id": i, "release": "before_hold", **records[i]["before_hold"]}
                   for i in ("D002", "D003")]
        self.apply(*updates, reviewed=["D002", "D003"])
        state = self.run_ok("show")
        self.assertEqual(state["dependency_ready"], ["D002"])
        self.assertEqual(state["categories"][EDGE], "Missing")
        self.assertEqual(state["nodes"]["D003"]["candidate"], "Correct that name?")
        self.apply(resolve("D002", "Show the delegate (Round 3 Q1)."), reviewed=["D003"])
        self.assertEqual(self.run_ok("show")["dependency_ready"], ["D003"])

    def test_cross_category_identity_conflict_and_independent_decision(self):
        point = new("D001", "Permit self-approval", "Applicant's own request", FUNCTIONAL)
        self.apply(point)
        self.apply(resolve("D001", "Prohibited (FR-1)."))
        duplicate = dict(point, new="D002", categories=[EDGE])
        result = invoke("apply", self.graph, batch={"revision": 2, "points": [duplicate]})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("same target and scope as D001", result.stderr)

        # The interviewer matches a paraphrase to the same target and scope, while
        # withdrawal is independently selectable even for the exact same actor.
        self.apply({"id": "D001", "categories": [FUNCTIONAL, EDGE]},
                   new("D002", "Permit withdrawal", point["scope"], EDGE))
        state = self.run_ok("show")
        self.assertEqual(len(state["nodes"]), 2)
        self.assertEqual(state["nodes"]["D001"]["detail"], "Prohibited (FR-1).")
        self.assertEqual(state["categories"][EDGE], "Missing")
        self.apply({"id": "D001", "save": "before_conflict", "status": "Partial",
                    "candidate": "Which rule applies?", "detail": "FR-2 allows self-approval."})
        state = self.run_ok("show")
        self.assertEqual(state["nodes"]["D001"]["before_conflict"]["detail"], "Prohibited (FR-1).")
        self.assertEqual(state["categories"][FUNCTIONAL], "Partial")
        self.apply(dict(resolve("D001", "Prohibited (Round 2 Q1)."), release="before_conflict"),
                   {"id": "D002", "status": "Deferred", "candidate": "", "detail": "User interruption"})
        self.assertTrue(self.run_ok("check")["complete"])
        self.assertEqual(self.run_ok("show")["categories"][EDGE], "Deferred")

    def test_invalid_batches_and_concurrent_retries_do_not_corrupt_graph(self):
        self.apply(new("D001", "Allow 代理 <approval> & review", "申請", FUNCTIONAL),
                   new("D002", "Record an actor", "History", DATA, "D001"))
        original = self.graph.read_bytes()
        self.assertEqual(ET.fromstring(original).tag, "{http://graphml.graphdrawing.org/xmlns}graphml")
        for patches in [
            [{"id": "D001", "parents": ["D002"]}],
            [resolve("D001", "Allowed."), {"id": "D002", "parents": ["D999"]}],
            [{"id": "D001", "status": "Resolved", "detail": "Allowed."}],
            [{"id": "D001", "categories": ["Typo"]}],
        ]:
            result = invoke("apply", self.graph, batch={"revision": 1, "points": patches})
            self.assertNotEqual(result.returncode, 0, patches)
            self.assertEqual(self.graph.read_bytes(), original)
        batch = {"revision": 1, "points": [resolve("D001", "Allowed.")]}
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: invoke("apply", self.graph, batch=batch), range(2)))
        self.assertEqual(sorted(r.returncode for r in results), [0, 1])
        self.assertIn("stale", next(r.stderr for r in results if r.returncode))
        state = self.run_ok("show")
        self.assertEqual(state["revision"], 2)
        self.assertEqual(state["review"], ["D002"])

    def test_all_prerequisites_must_be_settled(self):
        self.apply(new("D001", "Allow delegation", "All approvals", FUNCTIONAL),
                   new("D002", "Record history", "All approvals", DATA),
                   new("D003", "Record delegate", "History", DATA, "D001", "D002"))
        self.apply(resolve("D001", "Allowed (FR-1)."), reviewed=["D003"])
        self.assertEqual(self.run_ok("show")["dependency_ready"], ["D002"])
        self.apply(resolve("D002", "Recorded (FR-2)."), reviewed=["D003"])
        self.assertEqual(self.run_ok("show")["dependency_ready"], ["D003"])

    def test_pending_snapshots_and_interruption(self):
        self.assertTrue(self.run_ok("check", "--interrupted")["complete"])
        self.assertNotEqual(invoke("check", self.graph).returncode, 0)
        self.apply(new("D001", "Permit self-approval", "Own request", FUNCTIONAL))
        self.apply(resolve("D001", "Prohibited (FR-1)."))
        self.apply({"id": "D001", "save": "before_conflict", "status": "Partial",
                    "candidate": "Can an applicant approve?", "detail": "FR-2 contradicts FR-1."})
        for change in [resolve("D001", "Confirmed (Round 2 Q1)."),
                       {"id": "D001", "save": "before_hold"}]:
            result = invoke("apply", self.graph, batch={"revision": self.revision, "points": [change]})
            self.assertNotEqual(result.returncode, 0)
        self.assertNotEqual(invoke("check", self.graph, "--interrupted").returncode, 0)
        self.apply({"id": "D001", "status": "Deferred", "candidate": "", "detail": "User interruption"})
        self.assertTrue(self.run_ok("check", "--interrupted")["complete"])


if __name__ == "__main__":
    unittest.main()
