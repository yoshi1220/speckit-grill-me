# Using the decision graph

Run the helper with Python 3.9+ from the skill installation. The active project can be in a different directory. It uses the standard library. Keep the absolute script path and the session path returned by `init` across shell calls. In the examples, `helper` is the absolute path to `scripts/decision_graph.py` beside this skill’s SKILL.md.

```bash
session=$(python3 "$helper" init)
python3 "$helper" show "$session"
```

## Record the scan

Use one node per independent decision, including points already Clear. Before allocating IDs, run [vector matching](decision-matching.md) on the incoming batch. Use the returned revision when applying the reviewed decisions. The helper rejects exact duplicate target/scope pairs across categories. The interviewer judges paraphrases against the spec. A point may appear under several categories while keeping one ID, one answer and one status.

Send JSON on standard input to `apply`. Supply the revision on which you based the changes. Each batch commits all changes together. A stale revision or invalid batch leaves the graph intact. On failure, read it again and reconcile the outstanding changes with the saved spec before retrying.

```bash
python3 "$helper" apply "$session" <<'JSON'
{
  "revision": 0,
  "points": [
    {"new":"D001","target":"Allow delegate approval","scope":"Pending requests during the approver's absence","categories":["Functional scope and behavior"],"status":"Missing","candidate":"May a delegate approve the request?"},
    {"new":"D002","target":"Identify the recorded approver","scope":"Requests approved by a delegate","categories":["Domain and data model"],"status":"Partial","candidate":"Whose identity appears in the history?","parents":["D001"]}
  ]
}
JSON
```

Use `new` to allocate a permanent ID and `id` to patch an existing point. Omitted fields retain their values. A supplied `parents` or `categories` list replaces that list. Use the Glossary category names exactly. Include actor, operation and conditions in the target/scope pair. Use the interview language for free text. For Partial/Missing, supply the current question or research task in `candidate`. For Clear/Resolved/Outstanding/Deferred, set `candidate` to an empty string and give the decision and evidence reference, or the hold rationale, in `detail`. The graph is temporary. Accepted requirements, Q&A and scenarios belong in spec.md.

## Change a decision

Before changing a parent, `descendants SESSION ID` lists affected IDs in dependency order. Reassess them against all their prerequisites. Save and validate any required spec changes first. Patch the affected decisions together, including candidates, reasons and dependency changes.

```json
{
  "revision": 1,
  "points": [
    {"id":"D001","status":"Resolved","candidate":"","detail":"Delegation is prohibited (Round 1, Q1; FR-001)."},
    {"id":"D002","save":"before_hold","status":"Resolved","candidate":"","detail":"Not applicable because D001 prohibits delegation."}
  ],
  "reviewed":["D002"]
}
```

- `save: "before_hold"` preserves the current status, detail and candidate before recording parent-dependent non-applicability or a hold. Repeated saves preserve the first snapshot. When the point applies again, consult that snapshot and the saved spec, and send `release: "before_hold"` with the reassessed fields. This can restore a still-valid answer or return a candidate to the pool.
- For a conflict on the same ID, use `save: "before_conflict"`, set the status to Partial, put the conflicting evidence in `detail` and the confirmation question in `candidate`. Release this separate snapshot when the conflict is settled through Step 4.
- The helper marks descendants for review when their parent's decision changes. Changing an existing point’s parents also marks that point and its descendants. `reviewed` acknowledges IDs actually reassessed, including unchanged outcomes. Outstanding reviews remain visible in `show` and block `check`.
- `show` returns the full cross-category inventory, aggregates, pending reviews and `dependency_ready` IDs. Each ready point is open and all its ancestors have applicable, settled outcomes. The interviewer still applies the fact gate, impact threshold and round ordering. Keep the current round fixed, remove invalidated questions immediately and admit newly eligible ones at the next round boundary.
- A missing category has a null aggregate. Check its Glossary items during the scan. `check` verifies that the recorded points have final statuses and all descendant reviews have been completed. Verify goal coverage, sources and final report counts using the request map and saved spec as usual.

On interruption, set the remaining Partial / Missing points to Deferred with the interruption reason. Follow the interrupted completion path for pending descendant reviews, then run `check SESSION --interrupted`. This accepts an empty graph if the user stopped before the scan recorded a point. After collecting the final report data, run `python3 "$helper" close "$session"`. Close also on an early exit. A shell ending between questions is normal: keep the graph for the next question. After a hard process kill, the recorded session path can be passed to `close` to discard it.
