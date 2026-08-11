# SpecKit Clarify Grill Me

SpecKit Clarify Grill Me is a Spec Kit Community Extension for exhaustively
resolving ambiguity and open decisions in an active feature specification
before implementation planning begins.

The extension packages the English, Serena-independent implementation from
`english/base/speckit-grill-me` without changing the existing standalone
Skills.

## Command name

- Extension ID: `clarify`
- Command: `grill-me`
- Canonical command ID: `speckit.clarify.grill-me`
- Codex and other skills-mode integrations: `$speckit-clarify-grill-me`
- Dot-command integrations such as Claude Code: `/speckit.clarify.grill-me`

The core command is `speckit.clarify`; this extension adds the distinct,
fully-qualified command `speckit.clarify.grill-me`, so it does not replace or
overwrite the core command.

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

The command may modify only the active feature's `spec.md` and checkbox states
in `checklists/requirements.md`. It does not modify plans, tasks, source code,
or other files.

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
invoke:

```text
$speckit-clarify-grill-me
```

Optional arguments prioritize an area without limiting the rest of the scan:

```text
$speckit-clarify-grill-me Focus on authorization boundaries and failure modes.
```

For integrations that use dotted slash commands, invoke:

```text
/speckit.clarify.grill-me
```

## Install from a release asset

Because the extension lives below `spec-kit-extension/` in this repository, a
GitHub-generated tag archive does not place `extension.yml` at the archive
root. Install the dedicated extension ZIP release asset instead:

```bash
specify extension add clarify \
  --from https://github.com/yoshi1220/speckit-grill-me/releases/download/v1.0.0/speckit-clarify-grill-me-v1.0.0.zip
```

## Workflow and core clarify comparison

Recommended workflow:

```text
speckit.specify
      ↓
speckit.clarify.grill-me
      ↓
speckit.plan
      ↓
speckit.tasks
```

| Behavior | Core `speckit.clarify` | `speckit.clarify.grill-me` |
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
zip -r ../speckit-clarify-grill-me-v1.0.0.zip \
  extension.yml README.md LICENSE CHANGELOG.md commands
```

The resulting ZIP must have this root layout:

```text
extension.yml
README.md
LICENSE
CHANGELOG.md
commands/
└── grill-me.md
```

Attach the ZIP as a GitHub Release asset. Before publishing, test both the local
development install and the release-asset URL on a real initialized project.

## Release test checklist

- The manifest is accepted and `specify extension list` reports one command.
- The command is generated for each intended agent integration.
- The active feature specification is located successfully.
- Questions are asked one at a time and accepted answers update `spec.md`.
- Rescanning and the satisfaction gate complete normally.
- `checklists/requirements.md`, when present, is revalidated without unrelated
  edits.
- `before_clarify` and `after_clarify` hooks behave as documented.
- The core `speckit.clarify` command remains available.
- Removing and reinstalling the extension works.

## Community catalog submission

After publishing and testing the release asset, submit it through the official
[Extension Submission issue template](https://github.com/github/spec-kit/issues/new?template=extension_submission.yml).
Do not edit `extensions/catalog.community.json` directly.

Use the following release metadata:

- ID: `clarify`
- Name: `SpecKit Clarify Grill Me`
- Version: `1.0.0`
- Download URL: the dedicated ZIP release asset above
- Repository: <https://github.com/yoshi1220/speckit-grill-me>
- Documentation: <https://github.com/yoshi1220/speckit-grill-me/tree/main/spec-kit-extension>
- License: `MIT`
- Required Spec Kit version: `>=0.16.2`
- Required tools: Bash on macOS or Linux
- Commands: 1
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

## License

Released under the [MIT License](LICENSE).
