# SpecKit Grill Me

[Japanese](README.ja.md)

SpecKit Grill Me is a requirements-elicitation skill that thoroughly resolves ambiguity and open decisions in a feature specification before implementation planning begins. It acts as a specification-convergence gate between `specify` and `plan`.

## Origins and attribution

This is an independent project based on two MIT-licensed projects:

- It provides a macOS / Linux + Bash alternative to GitHub [Spec Kit](https://github.com/github/spec-kit)'s `speckit.clarify`, preserving compatibility with its artifacts and side effects.
- It is inspired by the idea behind [`grill-me`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me) from [Matt Pocock's skills](https://github.com/mattpocock/skills): refining a design through thorough questioning.

This is not an official project of GitHub or Matt Pocock and does not imply endorsement by or affiliation with either party.

## Variants

| Language | Investigation and knowledge backend | Skill | Purpose |
| --- | --- | --- | --- |
| English | Ordinary files | [`english/base/speckit-grill-me`](english/base/speckit-grill-me/) | Clarify the active feature specification |
| English | Ordinary files | [`english/base/speckit-grill-with-docs`](english/base/speckit-grill-with-docs/) | Clarify it and persist settled cross-feature knowledge under `docs/domain_knowledge/` by default |
| English | Serena | [`english/with_serena/speckit-grill-me`](english/with_serena/speckit-grill-me/) | Clarify using Serena memory and symbol investigation |
| English | Serena | [`english/with_serena/speckit-grill-with-docs`](english/with_serena/speckit-grill-with-docs/) | Clarify and persist settled knowledge to Serena memories |
| Japanese | Ordinary files | [`japanese/base/speckit-grill-me`](japanese/base/speckit-grill-me/) | Clarify the active feature specification in Japanese |
| Japanese | Ordinary files | [`japanese/base/speckit-grill-with-docs`](japanese/base/speckit-grill-with-docs/) | Clarify and persist settled cross-feature knowledge to ordinary Markdown |
| Japanese | Serena | [`japanese/with_serena/speckit-grill-me`](japanese/with_serena/speckit-grill-me/) | Clarify in Japanese using Serena |
| Japanese | Serena | [`japanese/with_serena/speckit-grill-with-docs`](japanese/with_serena/speckit-grill-with-docs/) | Clarify and persist settled knowledge to Serena memories |

All variants target macOS / Linux + Bash and require a Spec Kit project containing a `.specify/` directory. A `speckit-grill-with-docs` variant also requires the sibling `speckit-grill-me` variant. The `with_serena` variants additionally require Serena.

The language and backend variants reuse the same two skill names. Install only one variant of each skill name in a given skill-discovery root; treat the alternatives as replacements, not as side-by-side skills.

## Community Extension

[`spec-kit-extension`](spec-kit-extension/) packages the English, Serena-independent workflows as the Spec Kit Community Extension `grill`. Release 1.0.1 provides two commands:

- `speckit.grill.me` — exhaustive specification clarification
- `speckit.grill.with-docs` — clarification plus canonical Markdown knowledge synchronization

See the [extension README](spec-kit-extension/README.md) for supported invocation forms, installation from the dedicated release ZIP, and release metadata.

## Differences from `speckit.clarify`

|                      | `speckit.clarify`                           | `speckit-grill-me`                                                                                                                                                                                                                                            |
| -------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Number of questions  | Up to 5                                    | Unlimited                                                                                                                                                                                                                                                     |
| Progression          | One question at a time                     | Rounds based on the frontier—the set of questions that can be answered now—with questions still presented one at a time within each round                                                                                                                     |
| Answer format        | Multiple choice or no more than 5 words    | Labeled choices (A/B/C) plus unlimited free-form answers, with further drill-down after a choice when needed                                                                                                                                                  |
| Iteration            | One scan                                   | Step 1 creates the question candidate pool. Each round draws the currently answerable frontier from that pool. When no askable candidates remain, Step 5 rescans the updated spec.md for newly exposed ambiguity. This repeats until no new frontier emerges. |
| Completion condition | 5 questions answered or ambiguity resolved | Every decision point reaches a final status—Clear / Resolved / Outstanding / Deferred—and the user explicitly confirms satisfaction                                                                                                                           |

SpecKit Grill Me preserves compatibility with clarify's artifacts and side effects. Its internal elicitation and convergence algorithm intentionally differs to achieve deeper clarification.

## License

This project is available under the [MIT License](LICENSE).

The licenses of the source projects have also been verified:

- GitHub Spec Kit — [MIT License](https://github.com/github/spec-kit/blob/main/LICENSE), `Copyright GitHub, Inc.`
- mattpocock/skills — [MIT License](https://github.com/mattpocock/skills/blob/main/LICENSE), `Copyright (c) 2026 Matt Pocock`

Keep the attribution notices above and the MIT License text included in this repository.
