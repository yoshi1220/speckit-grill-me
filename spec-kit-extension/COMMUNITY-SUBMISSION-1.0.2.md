# Spec Kit Community Extension Update Submission — v1.0.2

Suggested issue title: `[Extension]: Update SpecKit Grill Me to 1.0.2`

Preparation status: the local package, installation, and command registrations
have been validated. The public release and full real-project interview tests
are pending. Complete the unchecked items before submitting this draft through
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

This is the intended public URL; publication and public download verification
have not yet been completed.

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

- [ ] Extension installs successfully via download URL
- [ ] All commands execute without errors
- [x] Documentation is complete and accurate
- [ ] No security vulnerabilities identified
- [ ] Tested on at least one real project

The public download URL and full agent-run interviews have not been tested.
Local installation and registration checks below do not replace those tests or
a security review. No previous release's test results are claimed for 1.0.2.

## Submission Requirements

- [x] Valid `extension.yml` manifest included
- [x] README.md with installation and usage instructions
- [x] LICENSE file included
- [ ] GitHub release created with version tag
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

**Still required:** public-asset installation, full interviews on a real
project, including answer incorporation, consequence confirmation, hooks,
checklists, and canonical-knowledge persistence and recovery; complete the
remaining testing confirmations above only after the corresponding checks.

**Prepared release artifact:**

- ZIP: `speckit-grill-me-extension-v1.0.2.zip`
- SHA-256: `7d01555e2ca2e5f2680aaa076dd7d89b0e364c36facb7fc1b97cc05133067099`
- Checksum file: `speckit-grill-me-extension-v1.0.2.zip.sha256`
- Intended release: <https://github.com/yoshi1220/speckit-grill-me/releases/tag/v1.0.2>

## Example Usage

Install from the public release asset after publication:

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

## Maintainer Release Handoff

1. Review and commit the prepared source and release documents. Merge them to
   `main` so the documentation URLs serve 1.0.2, and select the reviewed release
   commit for the tag. Check out that commit before running the commands below.
2. Rebuild the ZIP using the extension README if any packaged file changes.
   Recompute its SHA-256 and update both the checksum file and this draft's
   artifact and catalog-entry digests.
3. Run the pending real-project interview and review checks. Do not mark them
   complete based only on local package registration.
4. Tag the reviewed release commit, then publish the prepared notes and assets:

   ```bash
   git tag v1.0.2
   git push origin v1.0.2
   gh release create v1.0.2 \
     speckit-grill-me-extension-v1.0.2.zip \
     speckit-grill-me-extension-v1.0.2.zip.sha256 \
     --repo yoshi1220/speckit-grill-me --verify-tag \
     --title "v1.0.2 — Clarification workflow refinement" \
     --notes-file spec-kit-extension/RELEASE-NOTES-1.0.2.md
   ```

5. Download the public ZIP, compare its digest with the prepared checksum, and
   test installation from the exact Download URL in an initialized project.
6. Complete the remaining confirmations, remove preparation-only status and
   handoff text, and submit the updated fields through the official issue
   template. State that this updates the existing `grill` entry.

These publishing and submission commands have not been executed.
