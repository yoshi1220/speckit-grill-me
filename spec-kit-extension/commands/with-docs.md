---
description: "Exhaustively clarify a feature specification and persist canonical domain knowledge before planning."
---

# SpecKit Grill With Docs

Purpose: Detect, reduce, and clarify ambiguities and unresolved decisions in the active feature specification, while synchronizing settled cross-feature knowledge to canonical Markdown documents.

Following the "Interview discipline (applies to every round)" in this file, perform the same clarification role as the core `speckit.clarify` command, but without a question limit. Detect ambiguities in spec.md, ask **one question at a time in sequence while managing the questions that can be asked now (the frontier) as rounds**, immediately apply each answer to spec.md and persist any qualifying cross-feature knowledge, and repeat the rounds **until every decision point has reached one of the final statuses—Clear / Resolved / Outstanding / Deferred—and the user is satisfied**.

> **See the Glossary for terms such as design tree, question candidate pool, frontier, round, category, decision-point status, aggregate category status, and coverage map.**

**This command must be able to run as an alternative to `speckit.clarify` in a macOS / Linux + Bash environment.** In supported environments, preserve compatibility with clarify's artifacts and side effects by producing them in the same form (`## Clarifications`, incorporation into the relevant sections, validation after every write, revalidation of `checklists/requirements.md`, extension-hook processing, and a completion report with coverage), while adding the canonical knowledge artifacts defined in this command. The internal elicitation and convergence algorithm intentionally differs to achieve deeper clarification.

This compatibility applies to **artifacts and side effects**. It does not mean that this command supports every runtime environment supported by official Spec Kit. Use only the Bash prerequisite script; do not automatically select or fall back to the PowerShell or Python versions.

## Language

**Communicate in English unless the user requests another language.** Keep questions, explanations, progress updates, and spec.md in the same language.

## User Input

```text
$ARGUMENTS
```

If non-empty, treat it as a request to prioritize the specified area for deeper examination.

## Prerequisites

1. Confirm that the environment is macOS / Linux and that both the `bash` command and `.specify/scripts/bash/check-prerequisites.sh` are available. If not, state that the environment is unsupported and stop. Do not switch to an alternative PowerShell or Python script.
2. From the repository root, run `bash .specify/scripts/bash/check-prerequisites.sh --json --paths-only` **exactly once** to obtain `FEATURE_DIR` / `FEATURE_SPEC`. If it does not return JSON, stop and recommend rerunning the agent-specific invocation of `speckit.specify` or checking the active feature environment.
3. If spec.md does not exist, stop and recommend running the agent-specific invocation of `speckit.specify` first. Do not create a new specification here.
4. Read `.specify/memory/constitution.md` (project principles) if it exists. In addition, inspect **only the existing materials relevant to the work at hand** using ordinary file search, file reading, and symbol search:
   - `README*` / `CONTEXT.md` / `CLAUDE.md` / `AGENTS.md` / `documents/**` / `docs/**` — domain terminology, stakeholders, business flows, and design decisions
   - Related existing specs / plans / ADRs — existing requirements, constraints, and accepted or rejected decisions
   - Source code / schemas / migrations / models / interfaces / tests — implemented behavior, data shapes, and boundary conditions
   - Package / build / CI/CD / deployment configuration — technology stack, runtime environment, external integrations, and operational constraints

## Domain-knowledge persistence

In addition to clarifying the feature specification, this command has one extra responsibility: **immediately persist canonical terminology settled during the interview, together with qualifying project-wide business-domain and technical-architecture decisions, to ordinary Markdown documents.** Do not use Serena or `.serena/`, and do not assume either is available.

This command may modify the domain-knowledge artifacts defined below in addition to spec.md and checkbox states in `checklists/requirements.md`. The prohibition against changing plans, tasks, code, configuration, or unrelated files remains unchanged.

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

As part of Prerequisites item 4, always read `CONTEXT_FILE` in addition to the ordinary research materials, and read documents under `KNOWLEDGE_ROOT` that relate to the target feature. If `CONTEXT_FILE` does not yet exist, investigate other relevant documents first and then follow the creation rules above.

Use ordinary file search, reading, and editing capabilities. After every write, read the target file back and confirm that the settled content has exactly one canonical definition or decision record in the intended artifact, has not been duplicated as a second canonical record, and has not damaged the existing structure, Markdown, or relative links. Ordinary references to the canonical record, such as links or usage of a defined term, are not duplicates. If the canonical location cannot be read, created, updated, or verified, do not fall back to another location; report the failure and stop.

## Source authority

Use the following authoritative source for each type of content.

| Content | Authoritative source |
| --- | --- |
| Project principles | `.specify/memory/constitution.md`, when present; it constrains all other requirements and decisions |
| Feature-specific requirements and expected behavior | The current `FEATURE_SPEC` and decisions explicitly settled by the user in this session |
| Cross-feature terminology, domain knowledge, and design decisions | The canonical `CONTEXT_FILE`, topic documents under `KNOWLEDGE_ROOT`, and ADRs under `ADR_DIR`, unless the user explicitly settles a change in this session and the new decision has been saved and verified |
| Current implementation state | Primary sources such as code, schemas, migrations, models, interfaces, and tests |

- Do not treat an answer that conflicts with the constitution as settled. Reopen the decision point and confirm a compliant decision. Changing the constitution is outside this command's scope.
- If the user understands the conflict and retains the decision, mark the point Deferred with a reason. Do not write content that conflicts with the constitution to the spec or domain-knowledge documents as settled information.
- A new user answer has no authority to overwrite existing documents while it remains proposed, ambiguous, or under conflict confirmation. It becomes authoritative only after passing the conflict-confirmation discipline in this command and after the spec and all required knowledge documents have been saved and verified.
- Do not treat current implementation facts as desirable requirements or design decisions merely because they exist. When source types conflict, do not silently choose or overwrite one; follow the conflict-confirmation discipline in this command.

## Separating the spec from domain-knowledge documents

| Content | Write destination |
| --- | --- |
| Requirements, behavior, edge cases, and acceptance criteria specific to this feature | `FEATURE_SPEC`, following Steps 4A, 4B, and 4C |
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

Persistence incomplete is not a decision-point status from the Glossary. Keep the design-tree and coverage-map status Partial until every required file has been saved and verified; do not change it to Resolved.

- On stopping, report the affected decision point, settled content, files already saved and verified, files not yet updated or verified, failure details, and the next recovery operation.
- On resumption, save and verify the incomplete side before asking a new question. Reread the saved side as well and check for duplicates or new conflicts.
- In a new session, compare the latest Clarifications with the related knowledge documents. If the missing side can be reconstructed uniquely, apply it; otherwise, do not guess and ask the user.
- While any Persistence incomplete state remains, do not proceed to a new question, rescan, satisfaction gate, or ordinary completion report. If the user asks to interrupt, report recovery information and stop rather than taking the normal interrupted completion path.

## Additional in-session discipline

- **Raise a conflict with canonical terminology at the first opportunity.** Include a conflict found while constructing a question in that question; if an answer exposes the conflict, add a follow-up to a later round.
- **Resolve ambiguous or overloaded language to a canonical term.** Confirm which concept is intended, normalize the spec after its meaning and boundary are settled, and immediately update the knowledge document when required.
- **Probe concept boundaries with concrete scenarios.** Explicitly identify a scenario as hypothetical, and do not persist it as fact or decision before acceptance.
- **Cross-check against code.** When the user's explanation, knowledge documents, and implementation differ, show the primary implementation evidence and ask for confirmation. Do not silently align requirements or canonical documents to the implementation.
- **Handle answers or research that conflict with recorded documents through the conflict-confirmation discipline in this command.** Update related documents only after the change is settled, and mark the point Resolved only after saving and verification.
- **On the interrupted completion path, preserve settled, saved, and verified document changes and do not write unaccepted content.** Include updated knowledge documents in the completion report.

## Extension hooks (same processing as clarify)

If `.specify/extensions.yml` exists, process `hooks.before_clarify` before asking questions and `hooks.after_clarify` before the completion report. If the file is absent or cannot be parsed, skip it silently.

- Exclude hooks with `enabled: false`; treat an omitted `enabled` as enabled.
- Do not evaluate hooks with a non-empty `condition`; skip them and leave them to HookExecutor.
- Invoke hook command IDs using the current agent's command syntax (for example, `speckit.git.commit` may be `/speckit.git.commit`, `/speckit-git-commit`, or `$speckit-git-commit`).
- `optional: false` → Output `EXECUTE_COMMAND: {command}`, actually invoke that hook in the current agent/session, and wait for it to finish. Do not treat outputting the command as execution.
- `optional: true` → Only present the command, description, and prompt.

## Glossary

The following terms apply throughout this file. All subsequent steps rely on these definitions.

### Design tree

An in-session tree that connects unresolved decisions remaining in the spec through parent-child dependencies. Use it to manage interview progress; do not write it to a file.

- **Node** — One decision. Its session status is either working unresolved (Partial / Missing in coverage), settled (Resolved), or terminally held (Outstanding / Deferred). A terminal hold closes the decision for this interview; it does not mean the product decision itself has been made. A node becomes settled through a user answer or a fact established by investigation.
- **Branch** — A dependency in which a child decision becomes meaningful only after its parent decision is settled. For example, until "Does the scope include X?" (parent) is decided, "What should the X list display?" (child) cannot be answered.

Each item in the question candidate pool is a question intended to settle one decision in this tree. The initial tree takes shape when the candidates created in Step 1 are associated with nodes in Step 2. Thereafter, add a corresponding decision node whenever a candidate is added to the pool, and update node status whenever an answer or fact is settled. Do not create and freeze the tree only once at the beginning.

Whenever a parent node is settled, reassess in both directions whether each of its descendants—not only its immediate children—still applies under the parent's result, or whether a previously inapplicable decision has become applicable again. Before changing a descendant to inapplicable or terminally held because of a parent dependency, preserve its current status, settled value, and question candidate as separate "resumption information."

Do not delete descendants that no longer apply. Keep each as a **Resolved node with the settled result "Not applicable"**, and perform all of the following in the same operation:

- Remove the corresponding question from both the current frontier and the question candidate pool.
- Change the corresponding decision point in the coverage map to Resolved and record a rationale such as "Not applicable because parent decision <decision point> was settled as <result>."
- If obsolete child-decision text remains in the spec, remove or revise it through Step 4A or Step 4B according to the source that settled the parent, then save and validate. Do not add a separate Clarifications Q&A for a child that became inapplicable in addition to the parent answer's Clarifications record.
- Recalculate the design tree and aggregate category statuses.

Conversely, when a changed parent decision makes a descendant that was inapplicable, Outstanding, or Deferred because of that parent applicable again, remove the parent-dependent terminal rationale and do the following:

- If the preserved settled value remains valid under the parent's new result and is already incorporated into and validated against the current spec, keep the node Resolved.
- Otherwise, reassess Partial / Missing from the current spec and the resumption information, then restore the corresponding question candidate. Apply the Step 2 fact gate, impact threshold, and dependency assessment normally to restored candidates.
- Update the reassessed node and coverage statuses in the same operation, then recalculate the design tree and aggregate category statuses.

### Question candidate pool

The complete pool of potential questions for the user, initially created from Partial / Missing decision points during the ambiguity scan in Step 1. It is dynamic: follow-up questions, decision-derived checks, post-decision drill-down, and rescanning in Step 5 can add candidates; investigation can establish that a candidate is factual, and previous answers can invalidate candidates, causing them to be removed.

### Sources of question candidates

Question candidates enter the pool through four paths.

| Source | Description |
| ------ | ----------- |
| **Follow-up question** | Re-ask the same decision until it is precise when an answer is ambiguous or contradictory. Confirmation of a conflict with a recorded decision also uses this form. |
| **Drill-down** | Settle new decision points or boundary conditions created by a selected option, continuing until the user is satisfied. |
| **Decision-derived check** | At the end of a round, compare every settled decision with investigated facts about its applicable scope (such as differences by target type or screen), and add overlooked inconsistencies or boundary conditions. |
| **Rescan** (Step 5) | When no currently askable questions remain, reread the entire updated spec.md and create candidates from ambiguities newly exposed by the answers. |

### Frontier

The set of questions in the candidate pool that have no unresolved prerequisites and **can be answered now**—the leading edge while settling the design tree from its roots. As decisions are settled, candidates that depended on them become eligible to enter the frontier.

A candidate that cannot enter the frontier because it depends on unfinished factual research or an unsettled parent decision is a **blocked candidate**. Keep blocked candidates in the question candidate pool; do not treat them as an absence of candidates. Before entering Step 5, follow each dependency to its source and resolve or terminally hold it through the Step 5 entry gate in Step 3.

### Round

An interview unit corresponding to one frontier. Ask questions one at a time in sequence within a round, and recalculate the frontier after each round ends.

### Categories

The ambiguity scan (Step 1) and coverage report (Step 8) organize decision points into the following ten categories. A category is an aggregate grouping of multiple decision points, not the smallest unit that receives a status. Throughout this file, "all categories" refers to these ten.

- **Functional scope and behavior**: Core goals and success criteria / explicit out-of-scope declarations / role and persona distinctions
- **Domain and data model**: Entities, attributes, and relationships / uniqueness and identity rules / lifecycle and state transitions / expected data volume
- **Interaction and UX flow**: Primary user journeys / error, empty, and loading states / accessibility and localization
- **Non-functional quality**: Performance / scalability / reliability and availability / observability / security and privacy / compliance
- **Integrations and external dependencies**: External services and APIs plus failure modes / input and output formats / protocol and version assumptions
- **Edge cases and failure handling**: Negative scenarios / rate limits / conflict resolution, including concurrent edits
- **Constraints and trade-offs**: Technical constraints / explicit trade-offs and rejected alternatives
- **Terminology consistency**: Canonical terms checked against project documents, existing specs, and code / synonyms to avoid
- **Completion signals**: Testability of acceptance criteria / measurable Definition of Done
- **Other**: TODO and unresolved markers / unquantified vague adjectives such as "robust" or "intuitive"

### Decision points and statuses

Assign status to each individual decision point within a category, not directly to the category. Treat each category checklist item—for example, performance, observability, or security—and every independent decision discovered by scanning as one decision point. If one question contains multiple decisions, update each decision point separately.

| Status | Assign when | Meaning |
| ------ | ----------- | ------- |
| **Clear** | During the Step 1 scan | Already defined well enough; no question is needed |
| **Partial** | During the Step 1 scan or while reopening a settled point | The description or decision is incomplete, or a contradiction is being confirmed. This is an in-progress status that feeds a question or investigation. |
| **Missing** | During the Step 1 scan | Required information is absent. This is an in-progress status that feeds a question or investigation. |
| **Resolved** | After incorporating an answer or investigated fact, or after a parent decision establishes non-applicability | Previously Partial / Missing, now resolved after incorporation and validation in the spec or after recording the reason it does not apply |
| **Outstanding** | When deciding not to ask a question | Still Partial / Missing in substance, but with no material impact on implementation or validation strategy |
| **Deferred** | When holding or interrupting a question or investigation | Intentionally unresolved because it belongs in planning, the user deferred it, a required fact is currently unavailable, or the interview was interrupted |

Partial / Missing are in-progress statuses and must not remain at completion. The completion condition is that **every decision point has reached one of the final statuses: Clear / Resolved / Outstanding / Deferred**.

### Aggregate category status

Derive a category's display status mechanically from all decision points beneath it. Never overwrite or hide per-point statuses with an aggregate status.

1. While work is in progress, use `Missing` if at least one point is Missing; otherwise use `Partial` if at least one point is Partial.
2. If no in-progress status remains, use `Deferred` if at least one point is Deferred.
3. Otherwise, use `Outstanding` if at least one point is Outstanding.
4. Otherwise, use `Resolved` if at least one point is Resolved.
5. Use `Clear` if every point was clear from the beginning.

For example, if Performance is Resolved, Observability is Outstanding, Security is Deferred, and the remaining points are Clear under "Non-functional quality," the aggregate category status is Deferred. However, Steps 6 and 8 must also include the per-point breakdown, including all Outstanding points.

### Coverage map

A list associating the semantic identity of every decision point (category, decision target, and applicable scope) with its current status, settled result or hold rationale, and the aggregate status of its category. Create it during the initial ambiguity scan in Step 1 and update it whenever an answer or investigated fact is incorporated or a status changes. Maintain the same list during rescans in Step 5; do not recreate it. Like the design tree, keep it only in session and do not write it to a file. Update a design-tree node and its corresponding coverage status in the same operation. Never return a node to working unresolved while leaving its coverage status as Clear / Resolved / Outstanding / Deferred; if an old status or value is needed, preserve it separately from current status. Evaluate completion by per-point status. At the satisfaction gate in Step 6, present aggregate category statuses and a per-point summary of Outstanding / Deferred items. In the completion report in Step 8, output aggregate statuses for every category and per-point breakdowns.

## Interview discipline (applies to every round)

- **Interview every aspect thoroughly until a shared understanding is reached.** Do not stop at superficial agreement.
- **Freeze the frontier at the start of a round and ask its questions one at a time in order.** Do not present all questions in a round at once. Present one question, wait for its answer, incorporate it, then present the next. Start the next round only after all questions in the current round have been processed. Do not limit the number of questions in a round, and do not add questions midway through it.
- **Move dependent questions to a later round.** Do not include a question whose answer depends on an unresolved question in the same round. Do not build questions on assumed premises. Add it to the frontier in a later round only after its prerequisite is settled.
- **Recalculate the design tree whenever a round ends.** Apply the round's answers to the design tree, then identify question candidates whose unresolved prerequisites previously prevented them from being asked but whose prerequisites are now all settled. Treat these as candidates for the next frontier. Recalculate the frontier only during the round-end processing in Step 3, never midway through a round.
- **Investigate facts instead of asking for them. Finding facts is always the agent's responsibility, not the user's.** Investigate facts available from the codebase, project documents, and existing specs, and exclude them from questions. Ask the user only for **decisions** that only the user can make after ordinary file search (for example, `rg`), file reading, and symbol/reference search have been exhausted. Perform the investigation yourself; do not delegate it to subagents.
- **Do not stop a round while waiting for research.** Treat unfinished research like an unsettled prerequisite. If research cannot finish during the current round, remove only the questions that depend on it from the frontier and return them to the question candidate pool. Add them to a later frontier after research finishes. Continue asking all remaining questions in the current frontier.
- **Offer one to three situation-appropriate choices labeled from `A.`.** Offer one choice when there is one best answer and two or three when real trade-offs exist. Give each choice a one- or two-sentence rationale, and always end with a free-form option. The user must be able to accept a non-recommended choice as easily as the recommended one by replying with a single label.
- **Whenever marking an option `**Recommended**`, explain the recommendation.** Put the best-supported option at `A` with `**Recommended**` and state in one or two sentences **why it is preferred to the alternatives**, citing investigated facts, existing implementation, or an assessment of trade-offs. Never apply the marker without a reason.
- **Allow free-form answers at any time and at any length.** Welcome answers outside the choices, partial adoption, and conditional answers such as "A, except when X"; treat them directly as decisions.
- **If a selected option requires drill-down, present another choice set later.** When a selection creates new decision points or boundary conditions, add them to the question candidate pool and place them on a later frontier, drilling down until the user is satisfied.
- **Settle upstream decisions first.** Decisions about scope, actors, or the authoritative source of data affect downstream behavior and edge cases, so bias the early frontiers toward upstream decisions.
- **If a conflict with a recorded decision is detected, reopen the affected decision point and confirm it first in the next round.** Whether the conflict comes from a user answer, investigation, or rescan, do not silently overwrite the spec. Perform the following in the same operation:
  1. Return the corresponding design-tree node to unresolved.
  2. Return the same decision point in the coverage map to Partial, preserve its previous status and settled value separately as the "old settled value pending confirmation," and immediately recalculate the aggregate category status.
  3. Say, in one line, "A conflict with a recorded decision was detected; I will confirm it first in the next round." If a user answer triggered the conflict, hold that answer until the conflict is settled.
  4. Add a follow-up question asking whether to keep the old decision or adopt the new information, and make it the first candidate for the next round.
  5. Until the conflict is settled, treat the affected point as an unresolved prerequisite and return the remaining frontier questions that depend on it to the question candidate pool. Finish the current round with only the remaining questions that can still be answered.
  6. Incorporate, save, and validate a conflict settled through user choice via Step 4A; handle an apparent conflict resolved solely by investigated facts via Step 4B. Only after completion, simultaneously settle the design-tree node, change its coverage status to Resolved, discard the preserved old value, and recalculate the aggregate category status. If it remains ambiguous, keep it Partial and continue with a follow-up.
- **Follow up on ambiguous or contradictory answers.** Do not stop until the answer is precise. You may create hypothetical scenarios to probe boundaries, but explicitly label them "hypothetical" in the question. Until the user accepts them, do not treat them as project facts, requirements, or decisions and do not incorporate them into the spec. Add each follow-up to the question candidate pool and confirm it on a later frontier.
- **Do not preview later questions.** Present only the current question. Do not reveal or list the remaining questions in the current round or any future round ahead of time.
- **Do not act on a decision until shared understanding is confirmed.** Incorporate only into spec.md and the canonical domain-knowledge artifacts permitted by this command; do not begin plans, tasks, code, or configuration.
- **Respect interruption signals such as "stop," "that's enough," or "let's move on for now."** Stop presenting new questions immediately and enter the "Interrupted completion path." Ending the question loop does not mean skipping the checklist, hooks, or completion report.

### Interrupted completion path

If the user asks to stop after the spec has been loaded and any decision point has Persistence incomplete, follow the domain-knowledge persistence failure rules and stop; do not enter this path. Otherwise, perform these steps in order regardless of the interview stage:

1. Do not incorporate any answer that has not yet been accepted. Preserve spec and knowledge-document changes that were accepted, saved, and validated before the interruption.
2. Change every remaining Partial / Missing decision point to Deferred, including the current question, unpresented candidates, candidates blocked by dependencies, unfinished factual research, and points reopened for conflict confirmation. Record the reason as "User interruption" and move corresponding design-tree nodes to terminal hold. Empty the frontier and question candidate pool, then recalculate aggregate category statuses.
3. Run the final full validation from Step 4C against the already saved spec. Do not fill unresolved content by assumption or create new Clarifications Q&A entries.
4. Skip the Step 5 rescan and Step 6 satisfaction gate, and proceed to checklist revalidation in Step 7.
5. After Step 7, process `hooks.after_clarify` according to the extension-hook rules. Actually invoke required hooks and wait for completion; present optional hooks only as guidance.
6. Issue the Step 8 completion report as "Completed by user interruption." Include the interruption point, decision points deferred with reasons, coverage table, checklist results, hook results, and a recommendation on whether to proceed to planning or rerun this command later.

### Question format

Present questions one at a time in sequence using the following format. Restart numbering at `Q1` for every round so the number itself signals a new round. Give carried-over questions new numbers and state in one line when presenting them that they were carried over from the previous round.

```text
❓ **Q1** - **<Question title>**: <Question text. It may include contextual explanation and multiple paragraphs.>

➡️
- **A. <Choice>** — **Recommended**. <Reason for recommendation in 1–2 sentences>
- **B. <Choice>** — <Rationale in 1–2 sentences>
- **C. <Choice>** — <Rationale in 1–2 sentences>
- **Free-form** — Another answer, partial adoption, or a conditional answer (unlimited length)
```

Vary the number of choices between one and three according to the situation, but always include the `**Free-form**` line. The user may answer the one currently presented question with a single label such as "A" or "B," with "recommended," or in free form. Accept "yes" only when its meaning is unambiguous in the current question. If the user says "skip" or "defer," carry the question into a later round and renumber it there. Also accept free-form text that addresses a question other than the one currently presented—such as an advance answer to a later question or an explicit revision to a settled decision—and incorporate each decision through Step 4A just like the answer to the current question. Recalculate the frontier only at the end of the round. Numbers are for reference within a round and are not recorded in spec.md; use the Clarifications format in Step 4A. When referring to a question from an earlier round, use "Round n, Qk (<question title or summary>)" and always restate the question content because the number alone is not memorable.

## Workflow

### Step 1. Ambiguity scan

Read the entire spec.md and create an internal coverage map assigning **Clear / Partial / Missing** to every decision point within all categories in the Glossary. Initialize the map only during the first scan. When returning from Step 5, do not recreate the map or reset every point to these three statuses; follow the reconciliation rules in Step 5. Do not assign a status directly to a category. Derive aggregate category status from per-point statuses.

Create a question candidate from every Partial / Missing decision point and collect them in the **question candidate pool**. Exclude only matters that "have no material effect on implementation or validation strategy" or "are appropriately deferred to the plan phase (retain them in an internal note)." Facts whose answers can be established are investigated and removed in Step 2, not excluded here. **Do not limit the number of questions.**

Do not leave an excluded point as Partial / Missing. Immediately change it in the coverage map to **Outstanding** or **Deferred** according to the Glossary's status definitions, then recalculate its aggregate category status. Step 5's completion condition cannot be reached until every point has a final status.

### Step 2. Fact gate and frontier calculation

Whenever candidates are added to the question candidate pool, apply the **fact gate** below before calculating the frontier to all candidates that have not yet passed it and all candidates whose premises changed because a dependency was settled or for another reason. This applies not only to candidates created by the initial Step 1 scan, but also to follow-ups, drill-downs, decision-derived checks, and rescans.

1. Classify the candidate's answer as either "a fact that investigation can establish" or "a decision the user must make as project policy."
2. Investigate factual candidates yourself in the codebase, project documents, and existing specs. Remove candidates whose answers are established from the question candidate pool. If the investigated fact resolves ambiguous text in the spec, edit only the main spec through **Step 4B**, then change the corresponding point to Resolved after incorporation and validation. Do not add it to Clarifications.
3. Keep a candidate whose factual investigation depends on an unresolved decision or cannot finish during the current round in the pool as "awaiting research." Do not add it to the frontier or turn it into a user question. Reapply the fact gate after its dependency is settled or the research is complete.
4. Reclassify a candidate as a decision only if, after exhausting available sources, it becomes clear that new project policy or requirements must be chosen. If a factual answer exists externally but simply cannot be obtained, do not treat it as a decision. Mark it Outstanding if it has no impact on implementation or validation strategy; otherwise mark it Deferred and record why it could not be investigated.

Reapply the same impact threshold used in Step 1 to every candidate that remains a decision after passing the fact gate. Remove any candidate whose answer, regardless of the outcome, would not change implementation, data model, task breakdown, test design, UX behavior, operations, or compliance validation. Change the corresponding point to Outstanding or Deferred and recalculate aggregate category status.

Associate each remaining decision candidate with the design-tree node it will settle. Move candidates with **no unresolved prerequisites** from the pool to the frontier, leaving all others in the pool. Sort the frontier by impact × uncertainty and number it according to the Question format.

### Step 3. Round loop

Treat the current frontier as one round and proceed with one question and one answer at a time:

1. At the start of a round, announce `Round n (m questions)` in one line. If a round starts with confirmation of a conflict detected in the previous round, include that fact in the announcement, for example: `Round n (m questions) — Starting with confirmation of a conflict with a recorded decision.` Do not preview the question list.
2. Following the Question format, present only the first question in the round and wait for the user's answer. The presentation order is the ordering from Step 2, and numbering begins with Q1 in that order.
3. When the answer arrives, incorporate and save each settled decision via Step 4A, change the corresponding point to Resolved, and only then present the next question. If an answer remains ambiguous or contradictory, create a follow-up in the candidate pool for a later frontier; do not insert it into the current round. State in one line that it was held and why before moving to the next question. Carry skipped or deferred questions into a later round and renumber them there. If an answer conflicts with a recorded decision, hold it according to the interview rule for conflicts and put the confirmation follow-up first in the next round.
4. If an existing answer already settles a later question in the round, do not present it; say in one line that it was incorporated as answered based on the existing answer. If the answer invalidates the premise of a later question, immediately apply the Design tree non-applicability rules, change the corresponding point to Resolved, then say in one line that the parent decision made it inapplicable.
5. After the round's questions are exhausted, perform **round-end processing**: report `Round n complete — x settled, y carried over` in one line, run the **decision-derived check**, recalculate the design tree, return to Step 2, and recalculate the next frontier. During the decision-derived check, compare every decision settled in the round with investigated facts about its applicable scope—target types, differences by screen, list/detail/history views, field composition, required/optional status, and so on—and add any overlooked inconsistency or boundary condition to the candidate pool.

After each round—or if the frontier was empty during the initial Step 2—evaluate the following **Step 5 entry gate** from top to bottom:

1. If the frontier contains a candidate, proceed to the next round in Step 3.
2. If factual research remains unfinished, complete it without blocking other askable questions, then reapply the Step 2 fact gate to the result. If research is impossible, terminally classify it as Outstanding / Deferred under the Step 2 rules. Do not proceed to Step 5.
3. If blocked candidates depend on unsettled parent points, trace the dependency of every candidate toward the root, handle them as follows, then return to Step 2. Do not proceed to Step 5.
   - If no candidate in the question candidate pool corresponds to an in-progress parent point, restore a parent candidate from that Partial / Missing point.
   - If the parent is Clear / Resolved but the child remains blocked, reassess applicability. Make applicable children candidates for the next frontier and apply the Design tree non-applicability rules to inapplicable children.
   - If the parent is Deferred, terminally hold as Deferred, with reasons, all descendants that cannot be settled without it. If the parent is Outstanding but has descendants that affect implementation or validation strategy, reopen the parent as Partial and restore its candidate. If the descendants also have no material impact, terminally hold them as Outstanding.
   - If a self-dependency or circular dependency is detected, rebuild the branches because the dependency graph is wrong. If investigated facts alone cannot establish an order, reposition the most upstream decision as a root candidate with no dependency. Do not rescan while retaining a cycle.
   - After changing statuses, recalculate the design tree and aggregate category statuses.
4. Proceed to Step 5 **only when the question candidate pool is empty, no factual research or blocked candidates remain, and every decision point is Clear / Resolved / Outstanding / Deferred**. If these conditions are not met and no actionable candidate can be restored, terminally classify the remaining in-progress points as Deferred with reasons, then evaluate this gate again.

### Step 4. Incorporation procedure: update spec.md immediately

Step 4 does not run sequentially after Step 3. Invoke Step 4A from Step 3 whenever a user answer is settled, and invoke Step 4B from Step 2 whenever an investigated fact resolves ambiguity. Never mix the two paths.

#### Step 4A. Incorporate a user answer

1. On the first answer only, ensure that spec.md contains `### Session YYYY-MM-DD` under `## Clarifications`; if `## Clarifications` does not exist, add it immediately after the spec overview section.
2. For every accepted answer, append one line: `- Q: <question> → A: <settled answer>`.
3. Incorporate the settled decision into the main spec according to "Step 4C. Shared incorporation and validation rules."
4. If one answer contains multiple decisions, incorporate, save, and validate each decision separately. Keep only one Clarifications Q&A line per accepted answer; do not duplicate the same answer.
5. After each decision has been saved and validated successfully in the spec, apply the Domain-knowledge persistence rules when the decision qualifies. Save and read back every required knowledge artifact. Only after every required artifact succeeds, change the point to Resolved and recalculate aggregate category status.

#### Step 4B. Incorporate a fact established by investigation

1. Do not create `## Clarifications` / `### Session YYYY-MM-DD` and do not append a Q&A line. Clarifications records only the user interview.
2. Incorporate only facts verified from the codebase, project documents, or existing specs into the main spec according to "Step 4C. Shared incorporation and validation rules." Never incorporate assumptions or hypothetical scenarios as facts.
3. Incorporate, save, and validate each verified fact separately.
4. After it has been saved and validated successfully, change the point resolved by that fact to Resolved and recalculate aggregate category status.
5. Do not promote an implementation fact established through this path into a project-wide domain or architecture decision. If such a decision is needed, add it to the question candidate pool and persist it only after user acceptance through Step 4A.

#### Step 4C. Shared incorporation and validation rules

1. Incorporate content into the best section:
   - Functional ambiguity → Functional Requirements
   - Actor or action distinctions → User Stories / Actors
   - Data shape → Data Model, preserving the existing field order and keeping constraints concise
   - Non-functional requirement → measurable form under Success Criteria; convert vague adjectives into metrics
   - Edge case → Edge Cases / Error Handling
   - Terminology → normalize to the canonical term throughout the spec; if needed, note `(formerly "X")` once
2. If new content invalidates older ambiguous text, **replace** it rather than appending a duplicate. Leave no conflicting obsolete text.
3. **Save spec.md after every incorporation.** Do not reorder unrelated sections or alter their heading hierarchy. Keep additions minimal and testable.
4. **Validate after every save**, and run one final full pass after the last round:
   - For Step 4A, ensure the Clarifications Session has exactly one non-duplicated line per accepted answer. For Step 4B, ensure Clarifications has no diff.
   - Ensure no ambiguous text or placeholder that the incorporation should resolve remains.
   - Ensure no invalidated option or conflicting obsolete text remains.
   - Ensure Markdown structure is valid. The only new headings may be `## Clarifications` / `### Session YYYY-MM-DD` from Step 4A.
   - Ensure canonical terminology is consistent across every updated section.

### Step 5. Rescan loop

Only after passing the Step 5 entry gate in Step 3, **repeat the Step 1 detection scan against the updated spec.md**, because answers can expose new ambiguities and derived decision points. Rescan **as strictly as the initial run and as though reading the updated spec for the first time**, but do not reset point statuses. Reconcile differences into the existing coverage map in this order:

1. Preserve semantic identity, current status, settled result or hold rationale, and dependencies for every point from before the rescan.
2. Match every detected point to existing points by semantic identity. Treat different wording as the same point when it has the same decision target and applicable scope; do not recreate it as new.
3. Preserve status and rationale for existing Clear / Resolved / Outstanding / Deferred points when the updated spec supports the recorded result and introduces no new scope, boundary condition, or conflict. If a new conflict is detected, do not silently overwrite the recorded final status; send it to the conflict-confirmation flow in "If a conflict with a recorded decision is detected."
4. Classify only genuinely new points with no existing match as Clear / Partial / Missing, and create candidates from new Partial / Missing points. If an existing point is no longer present in the main text, do not delete it automatically: apply the Design tree non-applicability rules if a parent decision made it inapplicable; otherwise treat it as a conflict candidate.
5. Recalculate aggregate category statuses after reconciling the differences.

The acceptance criterion is: "Immediately rerunning this command would produce no new question capable of changing a decision." If new Partial / Missing points appear, the candidate pool is replenished and askable questions emerge, so return to Steps 2–4 for new rounds. Repeat until rescanning produces no new askable question and every point is Clear / Resolved / Outstanding / Deferred.

Avoid an interview that never ends because each rescan continually creates questions from minor details. Maintain strict detection while **raising the threshold for turning findings into questions in stages**.

Check candidates generated by rescanning for semantic duplicates. If a candidate is semantically identical to a point already assigned a final status of Resolved / Outstanding / Deferred, would converge to the same decision, and introduces no new scope, boundary condition, or conflict, do not add it. Treat mere rewordings as duplicates.

> **Threshold definition** — The standard for what an answer must be capable of changing before a candidate becomes a question. Use these two stages:
>
> - **Initial scan through first rescan** — Use the same gate as Step 2. Ask about any point whose answer could change implementation, data model, task breakdown, test design, UX behavior, operations, or compliance validation.
> - **Second and subsequent rescans** — Ask only about points whose answer would change the decision or implementation branch, meaning different choices lead to different designs or implementations. Settle minor points below this threshold—wording details or clarifications that produce the same implementation regardless of answer—as Outstanding, and list them at the Step 6 satisfaction gate. The user can reopen them with option 2.

### Step 6. Satisfaction gate

Once every point is Clear / Resolved / Outstanding / Deferred, present aggregate category statuses, a per-point summary of Outstanding / Deferred items, and the sections changed in this run. Then use **AskUserQuestion or another interactive UI to present choices and confirm satisfaction**. (If no interactive UI is available, present the same three choices in the normal response and wait for the user's selection.) Do not wait for a free-form "OK." Use this fixed confirmation format every time **at this satisfaction gate only**; it does not apply to Step 3 rounds, which use the question format from the interview discipline.

Always offer these three choices and explain the recommendation:

1. **Finish and proceed** — `**Recommended**`, because every point has a final status and no unresolved question remains
2. **Explore an area further** — Ask for the area and specific concern, change the corresponding point (or a new point if necessary) to Partial, add it to the candidate pool, and return to Step 2
3. **Concerns remain, but stop here** — Ask for the area and specific points, then follow the Interrupted completion path from step 2 onward, recording each identified point as Deferred before continuing with Step 7

If the user selects 1, proceed to Step 7.

If the user selects 2, ask a confirmation question requesting a free-form description of the area and concern. After confirming the response, perform option 2 above: make the relevant point Partial, add it to the candidate pool, recalculate aggregate category status, and return to Step 2.

Also accept free-form answers outside the choices, such as directly identifying an additional point, and treat them like option 2 or 3 according to their content.

### Step 7. Revalidate the checklist

If `FEATURE_DIR/checklists/requirements.md` exists, perform the following. If it does not, skip silently.

1. Record as a before snapshot only checkbox lines outside code fences (`- [ ]` / `- [x]` / `- [X]`, allowing indentation for nesting), including each item's current status and text.
2. Reevaluate every item against the **updated spec**. Save changes only for items whose state changes, toggling `[ ]` / `[x]`. Do not alter anything else: headings, metadata, notes, line order, or whitespace. Avoid diff noise.
3. Compare against the before snapshot and produce three lists: **newly passed** (unchecked → checked), **regressed** (checked → unchecked), and **still failing**. Also record before/after pass counts, for example `12/16 → 15/16`.

### Step 8. Completion report

After processing the `after_clarify` hook, report:

- Completion type (normal / user interruption). For an interruption, include where it occurred and that no post-interruption question or answer was incorporated.
- Number of rounds and total questions; optionally include a per-round breakdown. The question-and-answer list may refer to Clarifications.
- Path to the updated spec and the sections changed.
- The resolved `KNOWLEDGE_ROOT`, `CONTEXT_FILE`, and `ADR_DIR`; paths and types of knowledge documents created or updated; and a summary of terms, concepts, and decisions recorded.
- Checklist before/after pass counts, newly passed and regressed items, and items still failing, listed as areas needing attention.
- Coverage table: show every category's aggregate status as **Resolved** / **Clear** / **Deferred** / **Outstanding**, with a per-point status breakdown for each category. Do not proceed to the completion report if even one Partial / Missing point remains.
- If Outstanding / Deferred items remain, recommend whether to proceed to the agent-specific invocation of `speckit.plan` or rerun this command later.
- Suggested next command, normally the agent-specific invocation of `speckit.plan` (for example, `/speckit.plan`, `/speckit-plan`, or `$speckit-plan`).

## Behavior rules

- This workflow is expected to finish **before** `speckit.plan`. If the user explicitly skips it and proceeds, comply after warning that the risk of downstream rework will increase.
- If no significant ambiguity exists, report "No critical ambiguities detected," provide an aggregate category summary showing all points as Clear, and proceed to the Step 6 satisfaction gate. Do not invent questions.
- Do not ask speculative questions about the technology stack unless they block functional clarification.
- This command may modify only spec.md, `checklists/requirements.md` (and only checkbox states in Step 7), and the canonical domain-knowledge artifacts resolved under `KNOWLEDGE_ROOT`, `CONTEXT_FILE`, and `ADR_DIR`. Do not modify plans, tasks, code, configuration, or unrelated files.

## Done When

- [ ] Ambiguities in the spec have been identified, and settled answers and investigated facts have been incorporated and saved in spec.md through Step 4A / 4B respectively, with the final Step 4C validation pass complete.
- [ ] The question candidate pool is empty, with no askable questions, unfinished factual research, or blocked candidates depending on unsettled parents. No question rests on an assumed premise, and no awaiting research or dependency cycle is abandoned. On interruption, every point corresponding to remaining questions and research is explicitly Deferred.
- [ ] Design-tree node statuses match corresponding coverage statuses. No working-unresolved node retains a terminal status, and all unresolved nodes are terminally held upon interruption.
- [ ] Current parent decisions and the applicability of all descendants agree. No child that became applicable again retains an obsolete non-applicable or parent-dependent terminal rationale.
- [ ] Every decision point has reached one of the final statuses—Clear / Resolved / Outstanding / Deferred—and aggregate category statuses have been recalculated.
- [ ] User satisfaction is explicit, except upon interruption.
- [ ] `checklists/requirements.md` has been revalidated against the updated spec, if present.
- [ ] Extension hooks have been processed or skipped according to the rules.
- [ ] A completion report has been issued with rounds, question count, changed sections, checklist status, and a coverage table containing aggregate category statuses and per-point breakdowns.
- [ ] Settled canonical terminology and domain knowledge have been saved and read back from `CONTEXT_FILE` or topic documents under `KNOWLEDGE_ROOT`; qualifying decisions have been saved and read back from `ADR_DIR`.
- [ ] Every new topic document is linked relatively from `CONTEXT_FILE`, and every new ADR passes the three-condition recording gate and uses a unique number.
- [ ] No decision point has Persistence incomplete, and no point became Resolved before every required spec and knowledge artifact was saved and verified.
- [ ] The completion report lists the resolved knowledge locations, changed knowledge documents, and summaries of the terms and decisions recorded.
