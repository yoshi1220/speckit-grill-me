# Changelog

All notable changes to the SpecKit Grill Me extension are documented in
this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-08-25

### Added

- Added `speckit.grill.with-docs`, packaging the English Serena-independent
  `speckit-grill-with-docs` workflow as a self-contained extension command.

### Changed

- Renamed the extension command from `speckit.grill.grill-me` to
  `speckit.grill.me` to avoid repeating the `grill` namespace in generated
  agent command names.
- Replaced the unresolved `{SCRIPT}` placeholder with the explicit supported
  Bash prerequisite command so Markdown and TOML agent registrations execute
  the same command under Spec Kit 0.16.2.

## [1.0.0] - 2026-08-11

### Added

- Initial Community Extension release.
- Added `speckit.grill.grill-me`, an exhaustive, dependency-aware
  specification clarification command based on the English, Serena-independent
  standalone Skill.
- Added incremental `spec.md` updates, coverage tracking, checklist
  revalidation, and clarify-compatible extension-hook processing.

[1.0.1]: https://github.com/yoshi1220/speckit-grill-me/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/yoshi1220/speckit-grill-me/releases/tag/v1.0.0
