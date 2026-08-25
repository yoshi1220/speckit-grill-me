---
name: speckit-grill-with-docs
description: When Serena is available in a spec-kit project, resolve ambiguity in the current feature specification through unlimited question rounds and persist settled cross-feature terminology and qualifying domain or architecture decisions to Serena memories. Continue until every decision point has a final status and the user agrees.
argument-hint: 'Specific areas of the specification to examine (optional)'
compatibility: 'Requires macOS / Linux, Bash, Serena, and a spec-kit project containing a .specify/ directory'
metadata:
  author: 'yoshi1220'
user-invocable: true
disable-model-invocation: true
---

# SpecKit Grill With Docs

**Required**: First read `../speckit-grill-me/SKILL.md` in full and follow its instructions.

Run the sibling `speckit-grill-me` skill as the **base workflow**. Its language rules, prerequisites, extension hooks, glossary, interview discipline, interrupted completion path, Workflow Steps 1–8, behavior rules, artifacts, and completion conditions all remain in force, including artifact parity as an alternative to the core `speckit.clarify` command. Terms used here—including decision point, decision-point status, question candidate pool, frontier, round, design tree, and coverage map—have the meanings defined in the base glossary.

This skill adds exactly one responsibility: **immediately and correctly persist terminology settled during the interview, together with qualifying business-domain and technical-architecture decisions, to Serena memories.** Every additional rule below exists to support that responsibility.

For this skill, interpret the base behavior rule that permits changes only to spec.md and `checklists/requirements.md` as also permitting the memories in the table below. The prohibition against changing plans, tasks, code, or other files remains unchanged.

## Write destinations

Treat **Serena memories under `.serena/memories/` as the canonical record** for this repository's domain knowledge and technical-architecture decisions. Do not branch on or infer another location.

| Settled content | Write destination |
| --- | --- |
| Definitions of terms and concepts—the ubiquitous language | The relevant section of `.serena/memories/domain/product_domain_knowledge.md`; for a substantial topic, create `.serena/memories/domain/<kebab-slug>.md` |
| Business-domain design decisions | `.serena/memories/domain/`, at the same granularity described above, and only when all three recording conditions below are met |
| Technical-architecture decisions | The relevant section of `.serena/memories/architectures/architecture_patterns.md`; for a substantial topic, create `.serena/memories/architectures/<kebab-slug>.md`, and only when all three recording conditions below are met |

- **Write only to the destinations in this table.** Do not create a separate domain document elsewhere in the repository.
- When it exists, the Serena memories read for item 4 of the base Prerequisites must include **`domain/product_domain_knowledge`**. Also read topic memories related to the target feature so recorded conflicts can be detected. If the primary memory is absent, follow the lazy-initialization rule below.
- Before the initial read, use `list_memories` to determine whether `domain/product_domain_knowledge` exists. If it is absent, treat the existing glossary as empty and create that memory only when the first recordable term or concept is settled; match the project's documentation language and existing memory conventions. Apply the same lazy-creation rule to `architectures/architecture_patterns` when the first qualifying technical-architecture decision requires it. If a listed primary memory cannot be read, stop rather than treating it as absent.
- **Read and write with Serena memory tools.** Use `read_memory` to read, `edit_memory` to update an existing memory, and `write_memory` to create a memory. Derive `memory_name` from the path above by removing `.serena/memories/` and `.md`, for example `domain/<slug>` or `architectures/<slug>`. **Do not include the `.md` extension.** The paths in the table show the physical locations.
- When updating a memory, preserve its existing structure and edit only the relevant section. Give a new topic memory a short, stable decision or concept name and begin it with a one-sentence conclusion. Include related memories and verified primary implementation paths when they exist. Write cross-memory references as `mem:<name>`, for example `mem:domain/vehicle-category-unified-master`. Do not invent nonexistent references or implementation paths.
- Create a topic memory only when one concept group or decision requires several boundaries, invariants, business rules, alternatives, or trade-offs whose meaning would be lost in a concise entry in the primary memory. When in doubt, keep the content in the primary memory; do not split memories merely for the sake of splitting them.
- After every write, call `read_memory` with the same `memory_name` and verify that the settled content has exactly one canonical definition or decision record in the intended memory, has not been duplicated as a second canonical record, and has not damaged the existing structure. Ordinary references to the canonical record or use of a defined term are not duplicates.
- If an existing destination cannot be read or updated, or a required new memory cannot be created, do not write elsewhere. Report the failure and stop.

## Source authority

Use the following authoritative source for each type of content.

| Content | Authoritative source |
| --- | --- |
| Project principles | `.specify/memory/constitution.md`, when present; it constrains all other requirements and decisions |
| Feature-specific requirements and expected behavior | The current `FEATURE_SPEC` and decisions explicitly settled by the user in this session |
| Cross-feature domain terminology and design decisions | Serena memories, unless the user explicitly settles a change in this session and the new decision has been saved and verified |
| Current implementation state | Primary sources such as code, schemas, migrations, and tests |

- Do not treat an answer that conflicts with the constitution as settled. Reopen the decision point and confirm a compliant decision. Changing the constitution is outside this skill's scope.
- If the user understands the constitution conflict and retains the decision, mark the point Deferred with a reason because it cannot be resolved within this skill. Record that a constitution change or exception approval is required first. Do not write the conflicting content to the spec or Serena memory as settled information.
- A new user answer has no authority to overwrite an existing record while it remains proposed, ambiguous, or under conflict confirmation. It becomes authoritative only after passing the base conflict discipline and after Step 4A and every required memory save and verification have completed.
- Do not treat current implementation facts as desirable requirements or design decisions merely because they exist. When source types conflict, do not silently choose or overwrite one; reopen the affected point under the base conflict-confirmation discipline.

## Separating the spec from Serena memories

| Content | Write destination |
| --- | --- |
| Requirements, behavior, edge cases, and acceptance criteria specific to this feature | The `FEATURE_SPEC` obtained by the base prerequisites, following the incorporation and verification rules in base Steps 4A, 4B, and 4C |
| Definitions of terms and concepts that apply beyond this feature | The domain glossary memory listed above |
| A real trade-off decision that is costly to reverse and would make a future reader ask why | The decision-record memory listed above, but only when all three conditions hold: (1) reversing it would be materially costly, (2) it would surprise a future reader without context, and (3) real alternatives existed and one was chosen for a reason |

- Do not maintain the same content as a **canonical definition** in both the spec body and a memory. Put canonical definitions of cross-feature terminology only in Serena memory. The spec may use the term and contain the minimum context and feature-specific constraints needed to understand and validate the feature, but it must not duplicate or redefine the canonical definition. For decisions, write only feature-specific requirements and consequences in the spec and only cross-feature rationale and trade-offs in the decision-record memory. Clarifications Q&A lines required by base Step 4A are audit records, so they do not count as duplicate canonical management and must not be omitted.
- When the same settled matter belongs in both a glossary or concept memory and a decision-record memory, put only the current meaning, boundary, and business rules in the glossary or concept memory, and only the adoption rationale, alternatives, and trade-offs in the decision record. Do not duplicate the same explanation as canonical information; use a `mem:<name>` reference when useful.
- Persist to Serena memory **immediately whenever an item is settled**, just as with the spec. If one answer settles several terms or decisions, write and save each item separately rather than as a batch.
- When one settled item requires several artifacts, process them in this order: (1) spec, (2) glossary or current-domain-knowledge memory, (3) business-domain decision-record memory, (4) technical-architecture decision-record memory, and (5) read-back verification of every affected artifact. Skip artifact types that are not needed and mark the decision point Resolved only after all required operations succeed.
- When an item settled in Step 4A also qualifies for memory, save and verify the spec first, then save and read back the corresponding memory before marking the decision point Resolved or moving to the next question. If memory saving or verification fails, do not mark it Resolved and do not fall back to another location; stop. When the content is feature-specific only, preserve the base Step 4A order.
- Do not promote an implementation fact established only through base Step 4B into a business-domain or technical-architecture decision in Serena memory. If the fact suggests a new cross-feature design decision should be recorded, add it to the question candidate pool as a decision for the user and write it only after acceptance.

### Persistence failure handling

Updating the spec and Serena memories is not a single transaction. If saving or verifying any required artifact fails after another artifact was saved, attach the auxiliary persistence state **Persistence incomplete** to the decision point and stop.

Persistence incomplete is not a base decision-point status. Keep the affected design-tree and coverage-map status Partial until both the spec and all required Serena memories have been saved and verified; do not change it to Resolved.

Treat answer acceptance, saving the spec, saving and verifying memory, and marking the point Resolved as distinct states.

- On stopping, report the affected decision point, settled content, artifacts already saved and verified, artifacts not yet updated or verified, failure details, and the next recovery operation.
- When resuming in the same session, complete every missing save and verification before asking a new question. Reread the saved artifacts too and check for duplicates or new conflicts before marking the point Resolved.
- In a new session, before creating the Step 1 question candidates, compare terms and recordable decisions in the latest Clarifications with the related Serena memories. If the missing side can be reconstructed uniquely from the settled content without conflicting with existing records, apply and verify it. If it conflicts with an existing record, send it through the base conflict-confirmation discipline; if it cannot be reconstructed uniquely, do not guess and ask the user.
- While any Persistence incomplete state remains, do not proceed to a new question, rescan, satisfaction gate, or completion report.
- A stop caused by Persistence incomplete is a technical stop, separate from the base interrupted completion path. If the user asks to interrupt while persistence is incomplete, do not proceed to Step 8 as an ordinary interruption. Report the affected item, completed side, incomplete side, and recovery method, then stop. Resume the normal interview or interrupted completion path only after persistence is complete.

## In-session domain discipline added to `speckit-grill-me`

- **Raise a conflict with the domain glossary immediately.** For example: "The domain glossary defines Cancellation as X, but the current usage appears to mean Y. Which is intended?" Raise it in the first round where it is noticed. Include a conflict discovered while constructing a question in that question; if an answer exposes it, add a follow-up to the question candidate pool for a later round. When a conflict is detected, tell the user in one line that it will be confirmed in a later round.
- **Resolve ambiguous or overloaded language to one canonical term.** When a term in the user's answer or spec may refer to several concepts, add a question that confirms which concept is intended, ask it in a round, and replace the wording with one project-canonical term. For example, if "account" could mean either a customer or a login identity, ask which concept is intended.
- **Settle concept boundaries with concrete scenarios.** When the relationship between two concepts matters, create a concrete boundary scenario rather than asking only in the abstract, add it to the candidate pool, and ask what should happen. Derive the boundary from the answer. For example, for Return and Loan, ask how equipment returned but not yet inspected is treated if it is loaned again.
- **Cross-check against code.** When the user's explanation conflicts with implementation, add a follow-up that shows the conflict. Treat code as the primary source for current implementation facts, but when it differs from memory, follow the conflict discipline rather than silently overwriting memory or the spec.
- **Update the domain glossary as soon as a term is settled.** Record the term's definition—its meaning and boundary, canonical spelling, and synonyms to avoid. Do not write implementation details; the glossary is neither a specification nor working notes. Write only content accepted and settled by the user, never a held answer or premise from a hypothetical scenario.
- **Create a decision record only when all three conditions in the separation table are met.** If any condition is absent, do not create one.
- **Handle answers or research that conflict with recorded memory through the base discipline for conflicts with recorded decisions.** Do not silently overwrite memory. Reopen the point by returning its design-tree node to unresolved, changing its coverage status to Partial, and preserving the old settled value; add a confirmation follow-up and put it first in the next round. If the old decision is retained, discard only the preserved value. If the change is accepted, update the memory before marking the point Resolved.
- **On the base interrupted completion path**, preserve settled and saved memories and do not write unaccepted content. Include memories written in the completion report.

## Additions to the completion report

Add the following to the `speckit-grill-me` Step 8 completion report:

- Paths of memories written, distinguishing updates from new memories
- A summary of terms and decisions added or changed
- Decision points explicitly raised because they conflicted with recorded decisions, when any

## Done When

- [ ] Every Done When condition of `speckit-grill-me` is satisfied
- [ ] Settled terminology and qualifying business-domain and technical-architecture decisions have been written to the destinations above, saved, and verified by reading them back
- [ ] Source conflicts have been resolved or terminally classified according to the authority rules and the base conflict discipline
- [ ] Any decision retained despite a constitution conflict is Deferred with a reason, and the conflicting content has not been persisted as settled information
- [ ] No implementation fact from Step 4B was promoted to a decision in Serena memory without user acceptance
- [ ] No decision point has Persistence incomplete; every point became Resolved only after both the spec and every required Serena memory were saved and verified
- [ ] No canonical definition is managed in both spec.md and Serena memory, while spec.md retains enough context to be understood and validated on its own
- [ ] The completion report includes memories written and summaries of the terms and decisions recorded
