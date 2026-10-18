# Spec Kit Community Extension Update Submission — v1.0.2

Suggested issue title: `[Extension]: Update SpecKit Grill Me to 1.0.2`

Release status: v1.0.2 and its assets are published. Local command registrations,
public downloads, and installation from the published URL have been validated.
Full real-project interview tests remain pending. Complete the unchecked items
before submitting this draft through
the official [Extension Submission issue template](https://github.com/github/spec-kit/issues/new?template=extension_submission.yml).

This updates the existing `grill` catalog entry. Version 1.0.2 is a refinement
of the existing workflows; the command IDs, supported platforms, and required
tools are unchanged.

## Extension ID

grill

## Extension Name

SpecKit Grill Me

## Version

1.0.2

## Description

Exhaustively clarify specifications and optionally sync canonical domain knowledge.

## Author

yoshi1220

## Repository URL

<https://github.com/yoshi1220/speckit-grill-me>

## Download URL

<https://github.com/yoshi1220/speckit-grill-me/releases/download/v1.0.2/speckit-grill-me-extension-v1.0.2.zip>

The published ZIP and checksum were downloaded from their public URLs and
verified against the release artifact. Installation from this exact URL also
succeeded with Spec Kit 0.16.2.

## License

MIT

## Homepage (optional)

<https://github.com/yoshi1220/speckit-grill-me/tree/main/spec-kit-extension>

## Documentation URL (optional)

<https://github.com/yoshi1220/speckit-grill-me/blob/main/spec-kit-extension/README.md>

## Changelog URL (optional)

<https://github.com/yoshi1220/speckit-grill-me/blob/main/spec-kit-extension/CHANGELOG.md>

## Required Spec Kit Version

>=0.16.2

## Required Tools (optional)

- bash — required
- Supported platforms: macOS or Linux
- Serena is not required

## Number of Commands

2

## Number of Hooks (optional)

0

## Tags

clarification, requirements, specification, elicitation, workflow

## Key Features

- Cover all stated goals' six core facets before derived drill-down.
- Use dependency-aware rounds, with one independently selectable question at a
  time and unlimited free-form answers.
- Distinguish sourced facts, accepted decisions, and unverified assumptions.
- Settle entailed consequences without redundant questions and confirm them at
  the satisfaction gate.
- Keep concise numbered requirements, derived acceptance scenarios, per-goal
  coverage, and explicit blockers to planning.
- Synchronize accepted cross-feature knowledge to canonical Markdown, with a
  three-condition ADR gate and recovery of partially saved updates.
- Preserve clarify-compatible artifacts, checklist validation, and extension
  hooks in self-contained, Serena-independent commands.

## Testing Checklist

- [x] Extension installs successfully via download URL
- [ ] All commands execute without errors
- [x] Documentation is complete and accurate
- [ ] No security vulnerabilities identified
- [ ] Tested on at least one real project

Full agent-run interviews have not been tested. The installation and registration
checks below do not replace those tests or a security review. No previous
release's test results are claimed for 1.0.2.

## Submission Requirements

- [x] Valid `extension.yml` manifest included
- [x] README.md with installation and usage instructions
- [x] LICENSE file included
- [x] GitHub release created with version tag
- [x] All command files exist and are properly formatted
- [x] Extension ID follows naming conventions (lowercase-with-hyphens)

## Testing Details

**Tested on:** Linux x86_64, Python 3.14.3, Spec Kit 0.16.2 installed from the
official v0.16.2 source archive in an isolated environment. Claude, Codex, and
Gemini projects were initialized with that CLI's bundled Bash assets.

**Test projects:** temporary initialized fixture projects, not a real user
project. No live agent interview was run during this preparation.

**Completed checks:**

1. The official `ExtensionManifest` validator accepted `grill` v1.0.2 with two
   commands and no provided hooks.
2. The dedicated ZIP passed its integrity check and contains exactly
   `extension.yml`, `README.md`, `LICENSE`, `CHANGELOG.md`, `commands/me.md`, and
   `commands/with-docs.md` at the expected root paths.
3. Development installs succeeded for Claude, Codex, and Gemini integrations.
4. After removal, the packaged ZIP was served from a temporary loopback HTTP
   URL and installed through `specify extension add grill --from ...` for all
   three integrations. The server was stopped after verification.
5. `specify extension list` reported v1.0.2, two commands, zero hooks, and
   enabled status in all three projects.
6. Claude and Codex generated Markdown skills; Gemini generated valid TOML.
   All six rendered bodies matched the packaged source, apart from argument
   substitution and final whitespace. Gemini received `{{args}}`.
7. Every generated command retained the explicit Bash prerequisite invocation,
   without an unresolved `{SCRIPT}` or a dependency on a sibling `SKILL.md`.
8. The Bash prerequisite command resolved each fixture's active feature spec
   through `.specify/feature.json`.
9. Core clarification files were unchanged after removing and reinstalling
   this extension.
10. After publication, the public ZIP and checksum were downloaded and matched
    the released files and tag contents exactly.
11. In a fresh Codex fixture project, `specify extension add grill --from` the
    exact public Download URL succeeded with Spec Kit 0.16.2. Both rendered
    command bodies, enabled status, core clarification preservation, and active
    feature path resolution were verified again.

**Still required:** full interviews on a real project, including answer
incorporation, consequence confirmation, hooks,
checklists, and canonical-knowledge persistence and recovery; complete the
remaining testing confirmations above only after the corresponding checks.

**Published release artifact:**

- ZIP: `speckit-grill-me-extension-v1.0.2.zip`
- SHA-256: `7d01555e2ca2e5f2680aaa076dd7d89b0e364c36facb7fc1b97cc05133067099`
- Checksum file: `speckit-grill-me-extension-v1.0.2.zip.sha256`
- Release: <https://github.com/yoshi1220/speckit-grill-me/releases/tag/v1.0.2>
- Release commit: `17055745602a06b0673d9b888e8646ebd461939e`

## Example Usage

Install from the public release asset:

```bash
specify extension add grill \
  --from https://github.com/yoshi1220/speckit-grill-me/releases/download/v1.0.2/speckit-grill-me-extension-v1.0.2.zip
```

Invoke either command through the active integration:

```text
$speckit-grill-me
$speckit-grill-with-docs
/speckit-grill-me
/speckit-grill-with-docs
/speckit.grill.me
/speckit.grill.with-docs
```

## Proposed Catalog Entry

```json
{
  "grill": {
    "name": "SpecKit Grill Me",
    "id": "grill",
    "description": "Exhaustively clarify specifications and optionally sync canonical domain knowledge.",
    "author": "yoshi1220",
    "version": "1.0.2",
    "download_url": "https://github.com/yoshi1220/speckit-grill-me/releases/download/v1.0.2/speckit-grill-me-extension-v1.0.2.zip",
    "sha256": "7d01555e2ca2e5f2680aaa076dd7d89b0e364c36facb7fc1b97cc05133067099",
    "repository": "https://github.com/yoshi1220/speckit-grill-me",
    "homepage": "https://github.com/yoshi1220/speckit-grill-me/tree/main/spec-kit-extension",
    "documentation": "https://github.com/yoshi1220/speckit-grill-me/blob/main/spec-kit-extension/README.md",
    "changelog": "https://github.com/yoshi1220/speckit-grill-me/blob/main/spec-kit-extension/CHANGELOG.md",
    "license": "MIT",
    "category": "process",
    "effect": "read-write",
    "requires": {
      "speckit_version": ">=0.16.2",
      "tools": [
        {
          "name": "bash",
          "required": true
        }
      ]
    },
    "provides": {
      "commands": 2,
      "hooks": 0
    },
    "tags": [
      "clarification",
      "requirements",
      "specification",
      "elicitation",
      "workflow"
    ]
  }
}
```

Preserve the existing entry's maintainer-managed verification state, counters,
and creation date when applying this metadata update.

## Additional Context

Version 1.0.2 refines the finalized English base workflows in place. It improves
core coverage, evidence and recommendation discipline, consequence handling,
requirements and scenarios, and canonical-knowledge persistence. It introduces
no new command IDs or runtime dependencies.

The dedicated release asset is required because this repository keeps
`extension.yml` under `spec-kit-extension/`; GitHub's generated source archive
does not place it at the ZIP root.

Follow the [publishing guide](https://github.com/github/spec-kit/blob/main/extensions/EXTENSION-PUBLISHING-GUIDE.md)
for the update submission. Do not edit `extensions/catalog.community.json`
directly; maintainers apply the catalog changes through issue triage.

## Release Status and Remaining Submission Work

- The refinement changes were committed, pushed, and merged into `main`.
- Tag `v1.0.2` identifies release commit
  `17055745602a06b0673d9b888e8646ebd461939e`.
- The public release includes the ZIP, SHA-256 file, and prepared release notes.
  Public download and installation checks are complete.
- The Community catalog update has not been submitted. Complete the remaining
  interview and review checks, update their confirmations, and submit the fields
  through the official issue template as an update to the existing `grill` entry.
