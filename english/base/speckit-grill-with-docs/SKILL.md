---
name: speckit-grill-with-docs
description: Clarify every stated goal in an existing spec-kit feature specification before planning, derive concise requirements and acceptance scenarios, and sync accepted cross-feature terminology, domain knowledge, and qualifying decisions to ordinary Markdown documents. Use docs/domain_knowledge by default without Serena.
argument-hint: 'Specific areas of the specification to examine (optional)'
compatibility: 'Requires macOS / Linux, Bash, and a spec-kit project containing a .specify/ directory'
metadata:
  author: 'yoshi1220'
user-invocable: true
disable-model-invocation: true
---

# SpecKit Grill With Docs

**Required**: First read `../speckit-grill-me/SKILL.md` in full and follow its instructions.

Run the sibling `speckit-grill-me` skill as the **base workflow**. Its language rules, prerequisites, extension hooks, glossary, interview discipline, interrupted completion path, Workflow Steps 1–8, behavior rules, artifacts, and completion conditions all remain in force. Terms used here—including decision point, decision-point status, question candidate pool, frontier, round, design tree, coverage map, request map, core and derived decisions, settlement by consequence, and grounded and agent-introduced elements—have the meanings defined by the base skill.

This skill adds exactly one responsibility: **immediately persist canonical terminology settled during the interview, together with qualifying project-wide business-domain and technical-architecture decisions, to ordinary Markdown documents.** Do not use Serena or `.serena/`, and do not assume either is available.

For this skill, interpret the base behavior rule that permits changes only to spec.md and `checklists/requirements.md` as also permitting the domain-knowledge documents defined below. The prohibition against changing plans, tasks, code, or configuration remains unchanged.

## Applying the base clarification rules

- Keep the design tree, coverage map, and request map in session only. Cover every stated goal's six core facets before drilling down, and apply the base fact gate, dependency order, frozen rounds, evidence requirements, depth limits, and staged thresholds to domain questions too. A need to populate a knowledge artifact is not evidence for another interview question.
- Keep numbered requirements, cited verified premises, derived acceptance scenarios, and undecided behavior under Out of Scope and Limitations in `FEATURE_SPEC`. Knowledge artifacts do not replace these records or the base per-goal coverage and planning-readiness checks. Preserve the single Clarifications Q&A per accepted answer; investigated facts and consequences create no additional Q&A. Apply base Step 4A's single-save exception when decisions share a requirement or depend on each other, so the saved spec never contradicts the accepted answer; process independent knowledge items separately.
- A requirement settled by consequence is not a new user policy decision or a verified unknown fact. Cite its originating accepted decisions and investigated facts in the spec, and do not create a new decision record merely for applying an existing rule. Before the user confirms consequences at the base Step 6 satisfaction gate, their required destination is the spec only; a knowledge update is not yet required to mark those points Resolved. After confirmation, persist any qualifying cross-feature term or rule with the same provenance, verify all affected artifacts, and only then proceed to Step 7. Keep the recording gate for decision records; confirmation alone does not establish a new trade-off.
- Outstanding / Deferred points, situations noted but not asked, unverified assumptions, and unaccepted hypothetical scenarios are not settled domain knowledge. Keep them in the spec and coverage reports as the base requires. Record an agreed extension with its accepted scope, without turning its planning-deferred internal details into knowledge decisions.
- On interruption, preserve consequences already saved in the spec and identify them in the completion report as not confirmed at a satisfaction gate. Do not promote them to canonical knowledge without acceptance. Preserve already accepted, saved, and verified knowledge changes. Persistence failures still follow the failure-handling rules below.

## Document location and initialization

Applicable higher-priority execution instructions and the constitution are non-overridable constraints. Within those constraints, determine the canonical storage location in this order:

1. A storage location explicitly specified by the user in the current session
2. A storage location explicitly specified by agent-facing instructions that apply to the target path, such as `AGENTS.md` or `CLAUDE.md`
3. A location explicitly designated as canonical by project documentation such as a README, CONTEXT file, or documentation convention
4. The default `docs/domain_knowledge/`

If instructions at the same priority conflict, prefer the instruction that is more specific to the target feature or stored subject. If that still does not produce a unique location, do not guess or create files; show the conflicting candidates and their evidence, then ask the user.

After resolving the canonical location, establish these logical path names for the session. They are labels used by this workflow, not shell environment variables:

- `KNOWLEDGE_ROOT` — the resolved canonical knowledge directory. If the winning instruction identifies a context file rather than a directory, use that file's parent directory.
- `CONTEXT_FILE` — the existing entry-point file explicitly designated by the winning instruction or established project convention; otherwise `<KNOWLEDGE_ROOT>/CONTEXT.md`. If the winning instruction identifies a context file, use that file directly.
- `ADR_DIR` — the ADR directory established by the winning instruction or an existing project convention under `KNOWLEDGE_ROOT`; otherwise `<KNOWLEDGE_ROOT>/adr/`.

Resolve these locations once before writing and use the same values throughout the session. If an existing convention yields multiple possible context files or ADR directories and the authority rules do not select one, stop and ask rather than writing to more than one location.

When no alternate canonical storage location is specified, use:

```text
docs/domain_knowledge/
├── CONTEXT.md
├── <domain-topic>.md
└── adr/
    └── 0001-<decision-name>.md
```

- Treat `CONTEXT_FILE` as the canonical entry point to the knowledge base. Keep concise project-specific canonical terms, concept meanings and boundaries, and synonyms to avoid there. Do not put implementation details, feature specifications, working notes, or the history of technical choices there.
- If `CONTEXT_FILE` already exists, preserve its structure and document language and update only the relevant part.
- Create `KNOWLEDGE_ROOT` or `CONTEXT_FILE` only when the first recordable item is settled. Do not pre-create an empty knowledge base.
- A new `CONTEXT_FILE` must use the project's documentation language and contain sections equivalent in meaning to a document title, canonical terms and key concepts, domain boundaries, and related documents. Match headings to the project's documentation language and heading conventions. Keep each term definition to one or two sentences and define what the concept is rather than what it does.
- When one concept has multiple names, choose one canonical term and record the others as `_Avoid_: <synonyms to avoid>`. Do not add general programming vocabulary; include only concepts specific to this project's domain.
- Create `<KNOWLEDGE_ROOT>/<kebab-case-domain-topic>.md` only when the glossary in `CONTEXT_FILE` cannot accurately preserve the relevant boundaries or business rules. A separate document is warranted only when one concept group requires several boundaries, invariants, or business rules whose meaning would be lost in a one- or two-sentence definition in `CONTEXT_FILE`. When in doubt, keep the content in `CONTEXT_FILE`; do not split files merely for the sake of splitting them.
- After creating a topic document, add a relative link and a one-sentence description to the related-documents list in `CONTEXT_FILE`. Do not write broken links, nonexistent evidence, or guessed paths.
- Write decisions that pass the recording gate to `<ADR_DIR>/NNNN-<kebab-case-decision>.md`. Create `ADR_DIR` only when the first ADR is needed.
- If `KNOWLEDGE_ROOT` already uses a different structure or naming convention, preserve it. Do not move, rename, or reorganize unrelated documents.

For item 4 of the base Prerequisites, always read `CONTEXT_FILE` in addition to the ordinary research materials, and read documents under `KNOWLEDGE_ROOT` that relate to the target feature. If `CONTEXT_FILE` does not yet exist, investigate other relevant documents first and then follow the creation rules above.

Use ordinary file search, reading, and editing capabilities. After every write, read the target file back and confirm that the settled content has exactly one canonical definition or decision record in the intended artifact, has not been duplicated as a second canonical record, and has not damaged the existing structure, Markdown, or relative links. Ordinary references to the canonical record, such as links or usage of a defined term, are not duplicates. If the canonical location cannot be read, created, updated, or verified, do not fall back to another location; report the failure and stop.

## Source authority

Use the following authoritative source for each type of content.

| Content | Authoritative source |
| --- | --- |
| Project principles | `.specify/memory/constitution.md`, when present; it constrains all other requirements and decisions |
| Feature-specific requirements and expected behavior | The current `FEATURE_SPEC` and decisions explicitly settled by the user in this session |
| Cross-feature terminology, domain knowledge, and design decisions | The canonical `CONTEXT_FILE`, topic documents under `KNOWLEDGE_ROOT`, and ADRs under `ADR_DIR`, unless the user explicitly settles a change in this session and the new decision has been saved and verified |
| Current implementation state | Primary sources such as code, schemas, migrations, models, interfaces, and tests |

- Do not treat an answer that conflicts with the constitution as settled. Reopen the decision point and confirm a compliant decision. Changing the constitution is outside this skill's scope.
- If the user understands the conflict and retains the decision, mark the point Deferred with a reason. Do not write content that conflicts with the constitution to the spec or domain-knowledge documents as settled information.
- A new user answer has no authority to overwrite existing documents while it remains proposed, ambiguous, or under conflict confirmation. It becomes authoritative only after passing the base conflict discipline and after the spec and all required knowledge documents have been saved and verified.
- Do not treat current implementation facts as desirable requirements or design decisions merely because they exist. When source types conflict, do not silently choose or overwrite one; follow the base conflict-confirmation discipline.

## Separating the spec from domain-knowledge documents

| Content | Write destination |
| --- | --- |
| Requirements, behavior, edge cases, and acceptance criteria specific to this feature | `FEATURE_SPEC`, following base Steps 4A, 4B, and 4C |
| Canonical terms, concepts, and boundaries that apply beyond this feature | `CONTEXT_FILE` or a topic document linked from it under `KNOWLEDGE_ROOT` |
| Business-domain or technical-architecture decisions worth preserving for future readers | `ADR_DIR`, but only when all three recording conditions below are met |

A decision passes the recording gate only when all three conditions hold: (1) reversing it would be materially costly, (2) it would surprise a future reader without context, and (3) real alternatives existed and one was chosen for a reason. If any condition is absent, do not create an ADR.

- Do not maintain the same content as a canonical definition in both the spec and the domain-knowledge documents. Keep cross-feature definitions canonical in the knowledge documents; in the spec, include only the minimum context needed to understand and validate the feature and the feature-specific consequences. Clarifications Q&A lines are audit records, so they do not count as duplicate canonical management and must not be omitted.
- When the same settled matter relates to both terminology or domain knowledge and an ADR, put only the current meaning, boundary, and business rules in the knowledge document, and put only the adoption rationale, alternatives, and trade-offs in the ADR. Do not duplicate the same explanation as canonical information. Use a relative link to show the relationship when useful.
- Keep `CONTEXT_FILE` as a short, declarative glossary and entry point to domain boundaries. Do not mix in implementation details, specifications, scratch notes, or ADR bodies. When detail forms an independent domain topic, move it to a topic document and leave only a short summary and link in `CONTEXT_FILE`.
- A new topic document must have a short stable title, a one-sentence summary at the beginning, boundaries around its concepts and business rules, and relative paths to verified primary sources when such sources exist. A user-settled policy does not require an implementation source; do not invent evidence for it. Put the history of design choices in an ADR, and do not invent content merely to fill an inapplicable section.
- Number a new ADR with four digits by adding one to the highest existing number in `ADR_DIR`. Require a title and one to three sentences covering context, decision, and rationale. Add Status, considered options, or consequences only when they add real value; do not create sections merely to fill a template.
- When replacing an existing ADR, do not delete the old one. Create a new ADR and update the old ADR's Status to `superseded by ADR-NNNN`.
- Persist settled content immediately, one item at a time. If one answer settles several independent terms or decisions, process them separately rather than as a batch. When one settled item requires several artifact types, process them in this order: (1) spec, (2) terminology or concepts in `CONTEXT_FILE`, (3) topic document under `KNOWLEDGE_ROOT`, (4) the related-documents index in `CONTEXT_FILE`, (5) new ADR in `ADR_DIR`, (6) superseded old ADR in `ADR_DIR`, and (7) read-back verification of all affected artifacts. Resolve the decision point only after all required operations succeed. In addition to verifying each file immediately after writing it, use step 7 to verify consistency across the artifacts. Skip artifact types that are not needed.
- When an item incorporated through Step 4A also qualifies for a knowledge document, save and verify the spec first, then save and read back all required knowledge documents before marking the point Resolved.
- Do not promote an implementation fact established only through Step 4B into a business-domain or technical-architecture decision. If it may warrant a project-wide decision, add it to the question candidate pool as a decision for the user and write it only after acceptance.

## Document update discipline

- When updating an existing document, preserve its structure, style, terminology, and link format, changing only the smallest area related to the settled information.
- A terminology record must include the concept's meaning and boundary, its canonical spelling, and synonyms to avoid. Do not mix implementation details or feature-specific working notes into a term definition.
- An ADR must include the decision, scope, and selection rationale. Preserve important rejected alternatives only when they have value for future reconsideration. Do not invent history or alternatives.
- When creating a topic document, treat updating the `CONTEXT_FILE` index as part of the same recording operation. Neither the document alone nor the index alone is complete. ADRs are not required to be linked from `CONTEXT_FILE`.
- When changing a canonical term or domain rule, replace the existing definition so the current state remains unambiguous instead of appending a contradiction. Changes to design decisions follow the ADR supersession rule.

## Persistence failure handling

Updating the spec and the knowledge documents is not a single transaction. If saving or verifying one side of the spec-and-knowledge update, one side of the topic-document-and-`CONTEXT_FILE`-index update, or one side of a new-and-superseded ADR update fails, attach the auxiliary state **Persistence incomplete** to the affected decision point and stop.

Persistence incomplete is not a base decision-point status. If the point was already Resolved, including before a post-confirmation consequence update, preserve its settled value separately and return both its design-tree node and coverage status to Partial in the same operation. Keep the design-tree and coverage-map status Partial until every required file has been saved and verified; do not change it to Resolved.

- On stopping, report the affected decision point, settled content, files already saved and verified, files not yet updated or verified, failure details, and the next recovery operation.
- On resumption, save and verify the incomplete side before asking a new question. Reread the saved side as well and check for duplicates or new conflicts.
- In a new session, compare the latest Clarifications with the related knowledge documents. If the missing side can be reconstructed uniquely, apply it; otherwise, do not guess and ask the user.
- While any Persistence incomplete state remains, do not proceed to a new question, rescan, satisfaction gate, or ordinary completion report. If the user asks to interrupt, report recovery information and stop rather than taking the normal interrupted completion path.

## Additional in-session discipline

- **Raise a conflict with canonical terminology at the first opportunity.** Follow the base conflict-confirmation discipline whether the conflict is found while constructing a question or in an answer: reopen the affected point, preserve its old value, announce the conflict, and put one confirmation decision first in the next round. Do not bundle it with a separate domain decision or insert it into the frozen current frontier.
- **Resolve ambiguous or overloaded language to a canonical term.** Confirm which concept is intended, normalize the spec after its meaning and boundary are settled, and immediately update the knowledge document when required.
- **Probe concept boundaries with concrete scenarios.** Explicitly identify a scenario as hypothetical, and do not persist it as fact or decision before acceptance.
- **Cross-check against code.** When the user's explanation, knowledge documents, and implementation differ, show the primary implementation evidence and ask for confirmation. Do not silently align requirements or canonical documents to the implementation.
- **Handle answers or research that conflict with recorded documents through the base conflict-confirmation discipline.** Update related documents only after the change is settled, and mark the point Resolved only after saving and verification.
- **On the interrupted completion path, preserve settled, saved, and verified document changes and do not write unaccepted content.** Include updated knowledge documents in the completion report.

## Additions to the completion report

Add the following to the base Step 8 completion report:

- The resolved `KNOWLEDGE_ROOT`, `CONTEXT_FILE`, and `ADR_DIR` paths used
- Paths of documents created or updated and their type (context entry point, topic document, or ADR)
- A summary of terms, concepts, and decisions added or changed
- Decision points explicitly raised because they conflicted with recorded information, and whether each was resolved or held
- Consequences confirmed at the satisfaction gate and promoted to knowledge, with their originating decisions or facts; distinguish any consequences left unconfirmed on interruption

## Done When

- [ ] Every Done When condition of the base `speckit-grill-me` is satisfied
- [ ] The workflow used only ordinary file operations and did not depend on Serena or `.serena/`
- [ ] Settled canonical terminology and domain knowledge have been written to and read back from `CONTEXT_FILE` or topic documents under `KNOWLEDGE_ROOT`, and qualifying business-domain and technical-architecture decisions have been written to and read back from `ADR_DIR`
- [ ] Every new topic document has a valid relative link from `CONTEXT_FILE`
- [ ] Every new ADR passes all three recording conditions, has a unique number, and contains only the concise information required
- [ ] Source conflicts have been resolved or terminally classified according to the authority rules and the base conflict discipline
- [ ] Any decision retained despite a constitution conflict is Deferred with a reason, and the conflicting content has not been persisted as settled information
- [ ] No implementation fact from Step 4B was promoted to a design decision without user acceptance
- [ ] The base request coverage, evidence, consequence, numbered-requirement, and acceptance-scenario rules were followed; no unconfirmed consequence or undecided behavior was promoted to canonical knowledge, and every required post-confirmation knowledge update was verified before Step 7
- [ ] No decision point has Persistence incomplete; every point became Resolved only after the spec and all required knowledge documents were saved and verified
- [ ] No canonical definition is managed in both the spec and knowledge documents, while the spec retains enough context to be understood and validated on its own
- [ ] The completion report includes the documents changed and summaries of the terms and decisions recorded
