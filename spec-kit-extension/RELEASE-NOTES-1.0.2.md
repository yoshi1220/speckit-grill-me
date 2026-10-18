# v1.0.2 — Clarification workflow refinement

This patch release refines the existing `speckit.grill.me` and
`speckit.grill.with-docs` workflows. Command IDs, macOS/Linux and Bash support,
and the Serena-independent backend remain unchanged.

- Cover every stated goal's six core facets before drilling down, including
  applicable workflow exceptions, designated actors, cutover, and disconnected
  operation.
- Ground choices in sourced facts, accepted decisions, and explicit assumptions.
  Keep questions independently selectable and apply depth and impact thresholds.
- Incorporate entailed consequences without redundant questions, preserve their
  provenance, and confirm them at the satisfaction gate.
- Keep concise numbered requirements and derived acceptance scenarios, report
  per-goal coverage, and identify decisions that still block planning.
- Align canonical-knowledge updates with consequence confirmation, next-round
  conflict checks, and recovery of partially saved changes.

## Install

Requires Spec Kit `>=0.16.2` and an initialized project with an active feature
specification.

```bash
specify extension add grill \
  --from https://github.com/yoshi1220/speckit-grill-me/releases/download/v1.0.2/speckit-grill-me-extension-v1.0.2.zip
```

The dedicated ZIP places `extension.yml` at its root. Use this asset rather
than GitHub's generated source archive. A SHA-256 file accompanies the ZIP.

See the [changelog](https://github.com/yoshi1220/speckit-grill-me/blob/v1.0.2/spec-kit-extension/CHANGELOG.md)
for the version history.
