# Spec Kit Community Extension Update Submission — v1.0.1

Suggested issue title: `[Extension]: Update SpecKit Grill Me to 1.0.1`

Submit this update through the official [Extension Submission issue
template](https://github.com/github/spec-kit/issues/new?template=extension_submission.yml).

## Extension ID

grill

## Extension Name

SpecKit Grill Me

## Version

1.0.1

## Description

Exhaustively clarify specifications and optionally sync canonical domain knowledge.

## Author

yoshi1220

## Repository URL

<https://github.com/yoshi1220/speckit-grill-me>

## Download URL

<https://github.com/yoshi1220/speckit-grill-me/releases/download/v1.0.1/speckit-grill-me-extension-v1.0.1.zip>

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

- Exhaustive clarification with no fixed question limit
- Dependency-aware question frontiers and iterative rounds
- Investigation of project facts before asking the user to decide
- Immediate specification updates and validation after every accepted decision
- Continuous rescanning until all decision points have a terminal status
- Optional synchronization of settled canonical terms and cross-feature domain
  knowledge to ordinary Markdown under a resolved knowledge root
- Restrained topic-document creation, a three-condition ADR gate, and safe
  recovery from partially persisted multi-file updates
- Clarify-compatible artifacts, requirements checklists, and clarification hooks
- Self-contained, Serena-independent commands for multiple agent integrations

## Testing Checklist

- [x] Extension installs successfully via download URL
- [x] All commands execute without errors
- [x] Documentation is complete and accurate
- [x] No security vulnerabilities identified
- [x] Tested on at least one real project

## Submission Requirements

- [x] Valid `extension.yml` manifest included
- [x] README.md with installation and usage instructions
- [x] LICENSE file included
- [x] GitHub release created with version tag
- [x] All command files exist and are properly formatted
- [x] Extension ID follows naming conventions (lowercase-with-hyphens)

## Testing Details

**Tested on:**

- macOS Tahoe 26.6 with Spec Kit v0.16.2 and Claude Code for the accepted
  v1.0.0 real-project workflow
- Linux x86_64 with the Spec Kit extension manifest, installation, command
  registration, and compatibility implementation evaluated at v0.16.2
- Claude Markdown, Gemini TOML, and `.agents` Markdown command registrations

**Test projects:**

- The active macOS Spec Kit project documented in the accepted v1.0.0
  submission: <https://github.com/github/spec-kit/issues/4047>
- An isolated active-feature Spec Kit project used to execute the published
  `speckit.grill.with-docs` command end to end

**Test scenarios:**

1. Retained the accepted real-project coverage of the unchanged base interview
   algorithm and verified its renamed `speckit.grill.me` registration.
2. Validated `extension.yml` as `grill` v1.0.1 with two commands and zero hooks.
3. Verified the dedicated ZIP contains `extension.yml`, `README.md`, `LICENSE`,
   `CHANGELOG.md`, and both command files at the required archive paths.
4. Downloaded the public GitHub Release asset directly from the submitted URL,
   verified its SHA-256, and installed it with the v0.16.2 compatibility check.
5. Confirmed `specify extension list` reports `grill` v1.0.1, two commands, zero
   hooks, and enabled status.
6. Confirmed both commands register for Claude Markdown, Gemini TOML, and
   `.agents` Markdown integrations.
7. Confirmed every generated command contains the explicit
   `bash .specify/scripts/bash/check-prerequisites.sh --json --paths-only`
   invocation with no unresolved `{SCRIPT}` placeholder, and Gemini receives
   `{{args}}`.
8. Executed the published `speckit.grill.with-docs` command against an active
   feature specification. It asked one canonical-term question, incorporated the
   accepted answer into `spec.md`, and created and read back
   `docs/domain_knowledge/CONTEXT.md` without Serena.
9. Confirmed the command did not create an ADR for a terminology choice that
   failed the ADR recording gate.
10. Confirmed a denied write produced `Persistence incomplete` with no partial
    artifact marked Resolved, then recovered after write access was restored.
11. Confirmed the satisfaction gate, strict rescan, completion report, and
    requirements-checklist transition from 2/3 to 3/3.
12. Removed and reinstalled the extension successfully from the packaged ZIP.
13. Ran the official Spec Kit Markdown lint configuration across all extension
    Markdown with zero issues.
14. Scanned the extension source and package for hidden prompt injection and
    unsafe executable content; no findings were identified.
15. Confirmed only the `speckit.grill` namespace is used, so the core
    `speckit.clarify` command is not overwritten.

**Release artifact:**

- SHA-256: `7610eab61cbaccd9f22d12af2caa929c315abf26e66774557cd503654fc1ccb8`
- Release: <https://github.com/yoshi1220/speckit-grill-me/releases/tag/v1.0.1>

## Example Usage

```bash
# Install the extension
specify extension add grill \
  --from https://github.com/yoshi1220/speckit-grill-me/releases/download/v1.0.1/speckit-grill-me-extension-v1.0.1.zip

# Exhaustive specification clarification
$speckit-grill-me

# Clarification plus canonical Markdown knowledge synchronization
$speckit-grill-with-docs

# Dotted slash-command integrations
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
    "version": "1.0.1",
    "download_url": "https://github.com/yoshi1220/speckit-grill-me/releases/download/v1.0.1/speckit-grill-me-extension-v1.0.1.zip",
    "sha256": "7610eab61cbaccd9f22d12af2caa929c315abf26e66774557cd503654fc1ccb8",
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
    ],
    "verified": false,
    "downloads": 0,
    "stars": 0,
    "created_at": "2026-08-11T00:00:00Z",
    "updated_at": "2026-08-25T00:00:00Z"
  }
}
```

## Additional Context

This is an update to the existing `grill` catalog entry, not a new extension.

Version 1.0.1 renames `speckit.grill.grill-me` to `speckit.grill.me` and adds
`speckit.grill.with-docs`. The new command packages the English base,
Serena-independent workflow as a self-contained Community Extension command.
It also uses an explicit Bash prerequisite invocation so the command remains
executable when an agent registration format does not retain YAML script
metadata.

Because `extension.yml` is stored under `spec-kit-extension/` in the repository,
the dedicated GitHub Release asset is used as the download URL. The asset places
`extension.yml` at ZIP root.
