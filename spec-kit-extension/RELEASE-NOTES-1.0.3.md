# v1.0.3 — Match clarification decisions across rescans

Both `speckit.grill.me` and `speckit.grill.with-docs` now shortlist related
questions using vector similarity. The interview checks each candidate against
the source passages. For example, refund approvals before and after settlement
keep separate IDs when the policy can differ between those stages.

- Reuse one session ID when multiple goals or categories depend on the same
  decision. Follow-ups and reopened questions retain their original ID.
- Preserve a hold while its reason applies. Count accepted answers from the
  Q&A entries added during the current interview.
- When a knowledge update is interrupted, check what was saved and what the
  user accepted before completing the missing update.

Python is optional for both commands. Without Python, the interview compares
the source passages directly. The default TF-IDF matcher uses only the Python 3
standard library. To find paraphrases with learned embeddings, install
`model2vec` and point `GRILL_ME_VECTOR_MODEL` at a local model directory for
the specification’s language.

## Install

In an initialized Spec Kit project using CLI 0.16.2 or later on macOS or Linux,
install the dedicated extension ZIP.

```bash
specify extension add grill \
  --from https://github.com/yoshi1220/speckit-grill-me/releases/download/v1.0.3/speckit-grill-me-extension-v1.0.3.zip
```

To upgrade an existing installation, add `--force` to the command above.

Run `specify extension list` to confirm that `grill` reports version `1.0.3`
and two commands.

The ZIP includes both commands, the matching guide, and the optional Python
helper. To verify a download, place the ZIP and its accompanying checksum file
in the same directory and run:

```bash
shasum -a 256 -c speckit-grill-me-extension-v1.0.3.zip.sha256
```

For the version history, see the [extension changelog](https://github.com/yoshi1220/speckit-grill-me/blob/v1.0.3/spec-kit-extension/CHANGELOG.md).
