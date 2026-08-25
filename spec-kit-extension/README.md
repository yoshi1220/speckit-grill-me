# SpecKit Grill Me

SpecKit Grill Me is a Spec Kit Community Extension for exhaustively
resolving ambiguity and open decisions in an active feature specification
before implementation planning begins.

The extension packages the English, Serena-independent implementations from
`english/base/speckit-grill-me` and `english/base/speckit-grill-with-docs`
without changing the existing standalone Skills.

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

- Scans every material decision point in `spec.md` and tracks its status.
- Investigates facts in the project before asking the user to make a decision.
- Uses dependency-aware rounds and asks one question at a time.
- Accepts unlimited free-form answers and drills down when a choice exposes
  another decision.
- Updates and validates `spec.md` after every accepted answer or established
  fact.
- Rescans until no meaningful ambiguity remains, then asks for explicit user
  satisfaction.
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

Serena is not required.

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
root. Install the dedicated extension ZIP release asset instead:

```bash
specify extension add grill \
  --from https://github.com/yoshi1220/speckit-grill-me/releases/download/v1.0.1/speckit-grill-me-extension-v1.0.1.zip
```

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

## Build the release asset

From the repository root:

```bash
cd spec-kit-extension
zip -r ../speckit-grill-me-extension-v1.0.1.zip \
  extension.yml README.md LICENSE CHANGELOG.md commands
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
```

Attach the ZIP as a GitHub Release asset. Before publishing, test both the local
development install and the release-asset URL on a real initialized project.

## Release test checklist

- The manifest is accepted and `specify extension list` reports two commands.
- Both commands are generated for each intended agent integration.
- Generated command bodies contain the explicit supported Bash prerequisite
  invocation and no unresolved `{SCRIPT}` placeholder.
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

## Community catalog submission

After publishing and testing the release asset, file an update for the existing
`grill` catalog entry through the official
[Extension Submission issue template](https://github.com/github/spec-kit/issues/new?template=extension_submission.yml).
Use the new version and download URL, and state that the submission updates an
existing extension. Do not edit `extensions/catalog.community.json` directly.

Use the following release metadata:

- ID: `grill`
- Name: `SpecKit Grill Me`
- Version: `1.0.1`
- Download URL: the dedicated ZIP release asset above
- Repository: <https://github.com/yoshi1220/speckit-grill-me>
- Documentation: <https://github.com/yoshi1220/speckit-grill-me/tree/main/spec-kit-extension>
- Changelog: <https://github.com/yoshi1220/speckit-grill-me/blob/main/spec-kit-extension/CHANGELOG.md>
- License: `MIT`
- Required Spec Kit version: `>=0.16.2`
- Required tools: Bash on macOS or Linux
- Commands: 2
- Hooks provided: 0

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
