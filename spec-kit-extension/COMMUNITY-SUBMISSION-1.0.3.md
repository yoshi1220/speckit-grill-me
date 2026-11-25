# Spec Kit Community Extension Update Submission — v1.0.3

Suggested issue title: `[Extension]: Update SpecKit Grill Me to 1.0.3`

This updates the existing `grill` entry from 1.0.2 to 1.0.3. After publishing
the dedicated ZIP, install it from the Download URL below and fill in
**Testing Details** with your observations. Use the rendered values in the
corresponding form fields and paste only the JSON object into **Proposed
Catalog Entry**. The checkboxes below record the maintainer's confirmations.
[Extension Submission form](https://github.com/github/spec-kit/issues/new?template=extension_submission.yml)

## Extension ID

grill

## Extension Name

SpecKit Grill Me

## Version

1.0.3

## Description

Exhaustively clarify specifications and optionally sync canonical domain knowledge.

## Author

yoshi1220

## Repository URL

<https://github.com/yoshi1220/speckit-grill-me>

## Download URL

<https://github.com/yoshi1220/speckit-grill-me/releases/download/v1.0.3/speckit-grill-me-extension-v1.0.3.zip>

## License

MIT

## Homepage (optional)

<https://github.com/yoshi1220/speckit-grill-me/tree/main/spec-kit-extension>

## Documentation URL (optional)

<https://github.com/yoshi1220/speckit-grill-me/blob/main/spec-kit-extension/README.md>

## Changelog URL (optional)

<https://github.com/yoshi1220/speckit-grill-me/blob/main/spec-kit-extension/CHANGELOG.md>

## Required Spec Kit Version

`>=0.16.2`

## Required Tools (optional)

- bash — required
- Supported platforms: macOS or Linux
- Optional vector matching uses Python 3. Learned embeddings additionally use model2vec and a local model.

## Number of Commands

2

## Number of Hooks (optional)

0

## Tags

clarification, requirements, specification, elicitation, workflow

## Key Features

- Clarify each stated goal through dependency-aware, one-question-at-a-time rounds.
- Shortlist related decisions with TF-IDF or optional offline Model2Vec
  embeddings. Confirm the decision target and scope in the source material.
- Reuse session IDs across categories and rescans, preserve explicit holds,
  and count the answers accepted during the current interview.
- Persist accepted cross-feature terminology and qualifying decisions to
  canonical Markdown with `speckit.grill.with-docs`.

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

Replace the bracketed text with the results of the manual 1.0.3 checks before submitting.

- Environment and real project: [OS, Spec Kit CLI version, agent integration, and a public link or brief project description]
- Public release installation: [version and command count shown by `specify extension list` after installing from the Download URL]
- `speckit.grill.me`: [decision clarified, change observed in `spec.md`, and how the rescan handled that decision]
- `speckit.grill.with-docs`: [cross-feature decision accepted and the corresponding update observed in the canonical Markdown]

## Example Usage

From an initialized project with an active feature specification:

```bash
specify extension add grill \
  --from https://github.com/yoshi1220/speckit-grill-me/releases/download/v1.0.3/speckit-grill-me-extension-v1.0.3.zip
```

In Codex, use the first command to clarify the feature or the second to also
save cross-feature terminology:

```text
$speckit-grill-me Who can approve a refund before settlement?
$speckit-grill-with-docs Clarify what counts as a settled payment.
```

## Proposed Catalog Entry

```json
{
  "grill": {
    "name": "SpecKit Grill Me",
    "id": "grill",
    "description": "Exhaustively clarify specifications and optionally sync canonical domain knowledge.",
    "author": "yoshi1220",
    "version": "1.0.3",
    "download_url": "https://github.com/yoshi1220/speckit-grill-me/releases/download/v1.0.3/speckit-grill-me-extension-v1.0.3.zip",
    "repository": "https://github.com/yoshi1220/speckit-grill-me",
    "homepage": "https://github.com/yoshi1220/speckit-grill-me/tree/main/spec-kit-extension",
    "documentation": "https://github.com/yoshi1220/speckit-grill-me/blob/main/spec-kit-extension/README.md",
    "changelog": "https://github.com/yoshi1220/speckit-grill-me/blob/main/spec-kit-extension/CHANGELOG.md",
    "license": "MIT",
    "category": "process",
    "effect": "read-write",
    "requires": {
      "speckit_version": ">=0.16.2",
      "tools": [{ "name": "bash", "required": true }]
    },
    "provides": { "commands": 2, "hooks": 0 },
    "tags": ["clarification", "requirements", "specification", "elicitation", "workflow"]
  }
}
```

## Additional Context

This updates the existing `grill` catalog entry. The extension lives under
`spec-kit-extension/` in the repository. The dedicated release ZIP places
`extension.yml` at its root and includes both commands, their matching guide,
and the optional Python helper. A SHA-256 checksum accompanies the ZIP.
