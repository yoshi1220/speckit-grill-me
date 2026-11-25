# SpecKit Grill Me

SpecKit Grill Me is a Spec Kit Community Extension for exhaustively
resolving ambiguity and open decisions in an active feature specification
before implementation planning begins.

The extension packages the English, Serena-independent implementations from
`english/base/speckit-grill-me` and `english/base/speckit-grill-with-docs`
without changing the existing standalone Skills.

Version 1.0.3 includes two commands that match decision points
across goals, categories, and rescans. They share a helper installed under
`.specify/extensions/grill/` in the target project.

## Commands

Extension ID: `grill`

| Command | Canonical command ID | Dollar-skill invocation | Hyphenated slash invocation | Dotted slash invocation |
| --- | --- | --- | --- | --- |
| `me` | `speckit.grill.me` | `$speckit-grill-me` | `/speckit-grill-me` | `/speckit.grill.me` |
| `with-docs` | `speckit.grill.with-docs` | `$speckit-grill-with-docs` | `/speckit-grill-with-docs` | `/speckit.grill.with-docs` |

The core command is `speckit.clarify`; this extension uses the separate `grill`
namespace and adds `speckit.grill.me` and `speckit.grill.with-docs`, so it does
not replace or overwrite any core command.

## What it does

- Covers every stated goal's six core facets before drilling down and tracks
  individual decision points in session. Settled requirements are saved in `spec.md`.
- Shortlists similar decisions and checks their source text and scope before
  reusing a session ID. Independently answerable decisions keep separate IDs.
- Investigates facts in the project before asking the user to make a decision.
- Uses dependency-aware rounds and asks one question at a time.
- Accepts unlimited free-form answers and drills down when a choice exposes
  another decision.
- Shows sourced facts, accepted decisions, and explicit assumptions for choices.
- Applies entailed consequences without redundant questions and asks the user to
  confirm them at the satisfaction gate.
- Updates and validates `spec.md` after every accepted answer or established
  fact, keeping concise numbered requirements and derived acceptance scenarios.
- Rescans until no meaningful ambiguity remains, then asks for explicit user
  satisfaction, reporting per-goal coverage and any decisions blocking planning.
- Revalidates `checklists/requirements.md` and processes the same clarify hook
  points as the core command.
- With `speckit.grill.with-docs`, synchronizes settled cross-feature canonical
  terminology and domain knowledge to Markdown documents, and records only
  qualifying design decisions as ADRs.

`speckit.grill.me` may modify only the active feature's `spec.md` and checkbox
states in `checklists/requirements.md`. `speckit.grill.with-docs` may also
modify its resolved canonical knowledge root, which defaults to
`docs/domain_knowledge/`. Neither command modifies plans, tasks, source code,
configuration, or unrelated files.

## Requirements

- Spec Kit `>=0.16.2`
- A project initialized with Spec Kit and an active feature specification
- macOS or Linux
- Bash and `.specify/scripts/bash/check-prerequisites.sh`

Both commands can run the interview without Python by comparing the source
passages directly. The optional TF-IDF matcher uses only the Python 3 standard
library. To compare paraphrases using learned embeddings, install `model2vec` in the
Python environment and set `GRILL_ME_VECTOR_MODEL` to a local Model2Vec
directory suited to the specification’s language. The model loads offline.
If the model cannot score a batch, the helper uses TF-IDF for that batch.

## Install for local development

Run this from an initialized Spec Kit project, replacing the path with the
location of this repository:

```bash
specify extension add --dev /path/to/speckit-grill-me/spec-kit-extension
specify extension list
```

Then verify that your active agent integration exposes the command. For Codex,
invoke either command:

```text
$speckit-grill-me
$speckit-grill-with-docs
```

Optional arguments prioritize an area without limiting the rest of the scan:

```text
$speckit-grill-me Focus on authorization boundaries and failure modes.
$speckit-grill-with-docs Focus on domain terminology and lifecycle boundaries.
```

For Claude Code and other integrations that use hyphenated slash skills,
invoke:

```text
/speckit-grill-me
/speckit-grill-with-docs
```

For integrations that use dotted slash commands, invoke:

```text
/speckit.grill.me
/speckit.grill.with-docs
```

## Install from a release asset

Because the extension lives below `spec-kit-extension/` in this repository, a
GitHub-generated tag archive does not place `extension.yml` at the archive
root. Choose the dedicated ZIP from the [published releases](https://github.com/yoshi1220/speckit-grill-me/releases).
After publication, install v1.0.3 with the following command.

```bash
specify extension add grill \
  --from https://github.com/yoshi1220/speckit-grill-me/releases/download/v1.0.3/speckit-grill-me-extension-v1.0.3.zip
```

To upgrade an existing `grill` installation, add `--force` to the same command.
Run `specify extension list` to confirm version `1.0.3`.

## Workflow and core clarify comparison

Recommended workflow:

```text
speckit.specify
      ↓
speckit.grill.me OR speckit.grill.with-docs
      ↓
speckit.plan
      ↓
speckit.tasks
```

| Behavior | Core `speckit.clarify` | `speckit.grill.me` / `speckit.grill.with-docs` |
| --- | --- | --- |
| Question budget | Up to 5 | No fixed limit |
| Progression | Prioritized queue | Dependency-aware frontiers and rounds |
| Answers | Choice or short phrase | 1–3 choices plus unlimited free-form input |
| Convergence | Stops at the budget or when sufficiently clear | Rescans until every decision point has a final status |
| Completion | Coverage report | Coverage report plus explicit satisfaction gate |

This extension preserves clarify-compatible artifacts and side effects while
using a more exhaustive elicitation algorithm. It is an alternative for cases
where reducing downstream rework is more important than minimizing interview
time.

## Publish version 1.0.3

### 1. Tag the extension release commit

Merge the complete `spec-kit-extension/` package into `main`, including the
1.0.3 manifest, both commands, the matching guide, and the helper. From the
root of a clean checkout of the intended release commit, review the committed
manifest and file list before tagging.

```bash
git show HEAD:spec-kit-extension/extension.yml
git ls-tree -r --name-only HEAD -- spec-kit-extension/
```

If `v1.0.3` already points to this release commit, use the existing tag. If it
identifies a standalone-only release, keep that tag and choose a scoped tag
such as `grill-v1.0.3` for the extension. In that case, update the tag in the
commands and release links throughout the 1.0.3 documents before committing
them. Use `1.0.3` as the version in both the manifest and the submission form.

For a new `v1.0.3` tag, run:

```bash
git tag -a v1.0.3 -m "SpecKit Grill Me 1.0.3" HEAD
git push origin refs/tags/v1.0.3
```

### 2. Build the dedicated ZIP and checksum

Run from the same repository root. The archive reads the files recorded in the tag.

```bash
git -C spec-kit-extension archive --format=zip \
  v1.0.3 -- extension.yml README.md LICENSE CHANGELOG.md \
  commands/me.md commands/with-docs.md references/decision-matching.md \
  scripts/decision_neighbors.py > speckit-grill-me-extension-v1.0.3.zip
shasum -a 256 speckit-grill-me-extension-v1.0.3.zip \
  > speckit-grill-me-extension-v1.0.3.zip.sha256
```

The resulting ZIP must have this root layout:

```text
extension.yml
README.md
LICENSE
CHANGELOG.md
commands/
├── me.md
└── with-docs.md
references/decision-matching.md
scripts/decision_neighbors.py
```

Inspect the file list with `unzip -Z1 speckit-grill-me-extension-v1.0.3.zip`.
For a manual check of the packaged files before publication, extract the ZIP
and use its directory with `specify extension add --dev` in an initialized project.

#### Manual checks on a real project

- The manifest is accepted and `specify extension list` reports two commands.
- Both commands are generated for each intended agent integration.
- Generated command bodies contain the explicit supported Bash prerequisite
  invocation and no unresolved `{SCRIPT}` placeholder.
- Both generated commands can read the installed matching guide, and the helper accepts its JSON example.
- A rescan reuses the ID for the same decision and keeps separate IDs when the scope changes.
- The active feature specification is located successfully.
- Questions are asked one at a time and accepted answers update `spec.md`.
- Rescanning and the satisfaction gate complete normally.
- `checklists/requirements.md`, when present, is revalidated without unrelated
  edits.
- `before_clarify` and `after_clarify` hooks behave as documented.
- `speckit.grill.with-docs` resolves its canonical knowledge locations,
  persists qualifying knowledge, and does not require Serena.
- The core `speckit.clarify` command remains available.
- Removing and reinstalling the extension works.

### 3. Publish the GitHub Release

After the manual checks, publish from the release checkout. This command uses
the pushed tag, the prepared release notes, and both generated assets.

```bash
gh release create v1.0.3 --verify-tag --title "SpecKit Grill Me v1.0.3" \
  --notes-file spec-kit-extension/RELEASE-NOTES-1.0.3.md \
  speckit-grill-me-extension-v1.0.3.zip speckit-grill-me-extension-v1.0.3.zip.sha256
```

Download the ZIP and checksum from the public release into an empty directory.
There, run `shasum -a 256 -c speckit-grill-me-extension-v1.0.3.zip.sha256` and
check for `OK`. In an initialized project, repeat the installation using the
exact URL in [Install from a release asset](#install-from-a-release-asset).

### 4. Submit the community catalog update

Once the public URL installs successfully, file a **new Extension Submission
issue** for the existing `grill` entry. Copy the fields from the submission
draft, including the version `1.0.3`, the tag-pinned ZIP URL, and the results
of your manual checks. Spec Kit calculates `sha256` from the public ZIP.
If you also include the optional digest in the JSON, use the verified 1.0.3 value.
[Submission draft](https://github.com/yoshi1220/speckit-grill-me/blob/v1.0.3/spec-kit-extension/COMMUNITY-SUBMISSION-1.0.3.md) · [Official issue form](https://github.com/github/spec-kit/issues/new?template=extension_submission.yml)

A Spec Kit maintainer applies the `extension-submission` label. The upstream
workflow validates the release and opens a draft catalog PR for maintainer
review. After it merges, use `specify extension search grill` to find the
updated entry. [Official publishing guide](https://github.github.com/spec-kit/extensions/publishing.html)

## Origins and attribution

This is an independent project based on two MIT-licensed projects:

- It provides a macOS/Linux and Bash alternative to GitHub
  [Spec Kit](https://github.com/github/spec-kit)'s `speckit.clarify`, preserving
  compatibility with its artifacts and side effects.
- It is inspired by the `grill-me` workflow from
  [Matt Pocock's skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me).

This is not an official project of GitHub or Matt Pocock and does not imply
endorsement by or affiliation with either party.

Third-party copyright notices:

- GitHub Spec Kit — [MIT License](https://github.com/github/spec-kit/blob/main/LICENSE),
  `Copyright GitHub, Inc.`
- mattpocock/skills — [MIT License](https://github.com/mattpocock/skills/blob/main/LICENSE),
  `Copyright (c) 2026 Matt Pocock`

Keep these attribution notices and the included MIT License text with
redistributions of this extension.

## License

Released under the [MIT License](LICENSE).
