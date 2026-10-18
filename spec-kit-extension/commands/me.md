---
description: "Clarify every stated goal in a feature specification through focused questions before planning."
---

# SpecKit Grill Me

Purpose: Detect, reduce, and clarify ambiguities and unresolved decisions in the active feature specification.

Following the "Interview discipline (applies to every round)" in this file, perform the same clarification role as the core `speckit.clarify` command, but without a question limit. Detect ambiguities in spec.md, ask **one question at a time in sequence while managing the questions that can be asked now (the frontier) as rounds**, immediately apply each answer to spec.md, and repeat the rounds **until every decision point has reached one of the final statuses—Clear / Resolved / Outstanding / Deferred—and the user is satisfied**.

> **See the Glossary for terms such as design tree, question candidate pool, frontier, round, category, decision-point status, aggregate category status, coverage map, request map, core and derived decisions, settlement by consequence, and grounded and agent-introduced elements.**

**This command must be able to run as an alternative to `speckit.clarify` in a macOS / Linux + Bash environment.** In supported environments, preserve compatibility with clarify's artifacts and side effects by producing them in the same form (`## Clarifications`, incorporation into the relevant sections, validation after every write, revalidation of `checklists/requirements.md`, extension-hook processing, and a completion report with coverage). The internal elicitation and convergence algorithm intentionally differs to achieve deeper clarification.

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

### Extension hooks (same processing as clarify)

If `.specify/extensions.yml` exists, process `hooks.before_clarify` before asking questions and `hooks.after_clarify` before the completion report. If the file is absent or registers no hooks for the phase, skip silently. If it cannot be parsed or is invalid, do not skip silently: tell the user that `.specify/extensions.yml` could not be read, include the parser error, state that no hooks were checked—including mandatory (`optional: false`) hooks—and then continue.

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
| **Deferred** | When holding or interrupting a question or investigation | Intentionally unresolved because it belongs in planning under the deferral rule in the interview discipline, the user deferred it, a required fact is currently unavailable, or the interview was interrupted |

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

### Request map

An in-session list of the **stated goals**: every capability, constraint, and exclusion that the original request in spec.md (and `$ARGUMENTS`) asks for, recorded in the request's own words. For each stated goal, track six **core facets**:

1. **Meaning and unit** — what the goal denotes, including the unit, identity, or key it is counted or recorded by.
2. **Actors and permissions** — who performs it, who may change its results, and at what granularity the actor is recorded (an individual, a role, a location, or a device). Settle who may do what as a rule by kind of operation—for example, recording what physically happened; requesting, accepting, refusing, withdrawing, or closing; correcting; and administering the system, such as settings, designation data, and device registration—rather than as a list of the operations known so far, so that operations settled later fall under it. Ask about one administrative action separately only when the stated goals, verified facts, or accepted decisions require it to differ from the rest of its kind, and do not introduce an administrator role only to complete the permission rules. When a workflow cannot proceed without a designated actor—one person or the holder of a specific role, such as an approver or the person responsible for a budget—this facet also covers how that actor is identified (which source or rule designates them) and, where the workflow can meet them, the **designated-actor cases**: no actor is designated, the actor is absent or replaced while work is pending, one person would hold two roles in the same case (including the requester), and someone acts on the actor's behalf; when a pending case can be reassigned, who authorizes the reassignment and what it does to that case. Settle each as a rule for the role, not per person; an answer may be that the work waits or is refused, so a case does not by itself call for a new mechanism. Who holds a business role is a requirement, not reference-data administration. How designation data is entered or maintained is administration detail unless a stated goal asks users to manage it; do not infer an administrator role, a configuration screen, or role management from the need to identify an actor.
3. **Effect on data and state** — which quantities, records, or states change, at which event or time. When records can be corrected or cancelled, this facet also covers what a correction or cancellation does to the quantities and states that later records—including another party's or device's records—already reflect; settling who may correct does not settle this.
4. **Failure and conflict outcome** — what is recorded and what each party sees when input is invalid, a resource is insufficient, operations collide, or events arrive out of order. When a stated goal describes a workflow with steps or a handoff between parties, this facet also covers the workflow's **standard exceptions**: withdrawal or cancellation before completion, partial fulfilment and how the remainder is closed, non-arrival or loss, receipt or fulfilment that exceeds what was sent or committed, duplicate submission, and operations that cross each other (for example, a cancellation and a shipment recorded at the same time), settled by kind of operation like facet 2. When records are created on more than one device or while disconnected, it also covers which kinds of operation may be recorded while disconnected (one rule by kind, like facet 2), how current the data a party relies on must be—including data recorded at another site or device—and how the party can tell data that is not yet current, how a record is identified and deduplicated, what a party may record when the counterpart's record of the previous step has not yet arrived (for example, a receipt before the shipment record has synchronized), the one basis (a clock or a sequence) that orders all of the goal's records, quantities and workflow states alike, what happens when that basis is unreliable, and what happens when a device is lost or replaced.
5. **Transition from the current state** — when the request mentions existing data, records, or processes: migration of existing values, cutover timing, items in progress at cutover, parallel operation, and rollback.
6. **Verification** — the observable check that shows the goal is met, including a measurable form of any vague quality the goal itself states, such as "immediately", settled once with "no numeric target" offered as a choice; for an exclusion, its line under Out of Scope and Limitations.

A decision point that settles a facet of a stated goal is a **core decision**. A point found later—by drill-down, a decision-derived check, or a rescan—is also a core decision of the facet it affects when its answer would change the quantities or states a stated goal manages (not ones an option added), the operations a party may perform on them, or how current the data a party relies on must be: ask it whatever its depth or the stage, unless an accepted rule entails its answer, and never hold it Outstanding. Classify the element that raises such a point first: a point needed only to administer an agent-introduced element—a role, setting, or operation the agent added—is not core, and the scope-extension and deferral rules apply to it. One decision point may settle the same facet for several stated goals (for example, one permissions decision); do not duplicate it. The standard exceptions of a stated workflow, the items in progress at cutover, and the designated-actor cases of facet 2 are core decisions raised by the stated goal itself; create their candidates as soon as the workflow's steps are settled, even though they become askable only then. Assess each for applicability first: mark an exception that the settled steps make impossible (for example, nothing is sent or counted, so nothing can exceed it) Resolved as Not applicable with that reason, without a question; an exception that is possible but not mentioned in the materials remains applicable. Every other candidate—drill-down, decision-derived check, rescan finding, or follow-up—is a **derived decision** and records the stated goal it descends from and its depth (1 = created from a core answer, 2 = created from a depth-1 answer, and so on). A derived decision must trace to the wording of a stated goal, an investigated fact, or an accepted answer; a situation the agent merely imagines is not a candidate. A derived decision whose answer is entailed by accepted decisions and facts is **settled by consequence** (see the interview discipline) rather than asked. Keep the map in session only, like the design tree. Update it whenever candidates are added or statuses change, and present per-goal coverage at the satisfaction gate and in the completion report.

### Grounded and agent-introduced elements

Classify every capability, role, entity, workflow stage, master-data operation, or quantitative target that an option would add to the specification:

- **Grounded** — a stated goal or an investigated fact calls for a decision about it: the element settles a core facet of a stated goal, or responds to a situation the materials say exists or occurs. Examples: distinguishing variants or versions that the materials say exist but current records do not separate; an approval, reservation, or confirmation step that determines how a stated workflow changes availability or state; deciding who may correct records. A grounded element is an ordinary option. It is not a scope extension, and it is not avoided merely because it adds states, operations, or records.
- **Agent-introduced** — no stated goal or investigated fact calls for it, because it goes beyond what settling the core facets requires. Examples: a provisional-registration and merge mechanism for a rare edge case, an extra administrative role or console, notifications, reporting, or a numeric target for a quality the request does not mention. An element that only handles a situation created by another agent-introduced element is also agent-introduced.

Classify by what the request and the materials say, not by how much the element adds. Deciding not to support a grounded element is a scope-narrowing choice, not a neutral default. See "Recommend the option that best achieves the stated goals" and "Label agent-introduced elements" in the interview discipline.

## Interview discipline (applies to every round)

- **Interview every aspect thoroughly until a shared understanding is reached.** Do not stop at superficial agreement.
- **Freeze the frontier at the start of a round and ask its questions one at a time in order.** Do not present all questions in a round at once. Present one question, wait for its answer, incorporate it, then present the next. Start the next round only after all questions in the current round have been processed. Do not limit the number of questions in a round, and do not add questions midway through it.
- **Move dependent questions to a later round.** Do not include a question whose answer depends on an unresolved question in the same round. Do not build questions on assumed premises. Add it to the frontier in a later round only after its prerequisite is settled.
- **Recalculate the design tree whenever a round ends.** Apply the round's answers to the design tree, then identify question candidates whose unresolved prerequisites previously prevented them from being asked but whose prerequisites are now all settled. Treat these as candidates for the next frontier. Recalculate the frontier only during the round-end processing in Step 3, never midway through a round.
- **Investigate facts instead of asking for them. Finding facts is always the agent's responsibility, not the user's.** Investigate facts available from the codebase, project documents, and existing specs, and exclude them from questions. Ask the user only for **decisions** that only the user can make after ordinary file search (for example, `rg`), file reading, and symbol/reference search have been exhausted. Perform the investigation yourself; do not delegate it to subagents.
- **Do not stop a round while waiting for research.** Treat unfinished research like an unsettled prerequisite. If research cannot finish during the current round, remove only the questions that depend on it from the frontier and return them to the question candidate pool. Add them to a later frontier after research finishes. Continue asking all remaining questions in the current frontier.
- **Ask for one independently selectable decision per question.** If the user could reasonably accept one part and reject another, split those parts into separate candidates and design-tree nodes before freezing the frontier. Keep dependent decisions for later rounds under the existing dependency rules. A choice may include the inseparable consequences of one decision, but do not bundle unrelated policies into a single approval. Continue to incorporate each decision separately if the user volunteers several in one answer, as required by Step 4A.
- **Offer one to three situation-appropriate choices labeled from `A.`.** Offer one choice when there is one best answer and two or three when real trade-offs exist. Give each choice a one- or two-sentence rationale, and always end with a free-form option. The user must be able to accept a non-recommended choice as easily as the recommended one by replying with a single label.
- **Whenever marking an option `**Recommended**`, explain the recommendation.** Put the best-supported option at `A` with `**Recommended**` and state in one or two sentences **why it is preferred to the alternatives**, citing investigated facts, existing implementation, or an assessment of trade-offs. Never apply the marker without a reason.
- **Make the basis of a recommendation visible, with sources.** Before the choices, list the **verified facts**, **accepted decisions**, and **unverified assumptions** used to compare the options, under those three labels. Every verified fact carries its source: a fact identifier, a file path, or Round n, Qk. Anything inferred, estimated, or merely plausible—typical volumes, growth rates, likely input variations, what "usually" happens—is an unverified assumption, never a verified fact, even when it seems obvious. State an absence as "not stated in the materials," not as a fact about the product. Show the concrete benefit and material downside of the recommended outcome. Include one worked example with concrete numbers, labeled as an example, whenever the decision concerns quantities, time, or ordering, and a short example whenever a boundary would otherwise be unclear. If an unconfirmed premise could change the decision, investigate it through the fact gate or settle its upstream decision first. Acceptance of a policy recommendation does not verify an unknown fact, and an illustrative situation is not a requirement unless explicitly accepted. Do not add a separate question merely to recap an already settled answer.
- **Allow free-form answers at any time and at any length.** Welcome answers outside the choices, partial adoption, and conditional answers such as "A, except when X"; treat them directly as decisions.
- **If a selected option requires drill-down, present another choice set later.** When a selection creates new decision points or boundary conditions, add them to the question candidate pool and place them on a later frontier, drilling down until the user is satisfied. When an option adds a state, a separately counted quantity, or a closing operation, state within the option how the state is left, which already accepted operations change the quantity, and whether the awaited event can still be recorded after the closure, as inseparable consequences of that choice, rather than asking them later. Do not bundle a new operation into the option; a new operation that the addition would need is a separate point under the threshold rules.
- **Settle upstream decisions first.** Decisions about scope, actors, or the authoritative source of data affect downstream behavior and edge cases, so bias the early frontiers toward upstream decisions. Before freezing each frontier, and the first one in particular, identify the decisions that constrain several others—when applicable, the cutover method and timing, the authoritative source of data, how responsible actors are designated, where a workflow starts and completes, and the scope of migrated data—and order each before the decisions it constrains, even across facets and stated goals. A decision that depends on one of them, such as the handling of items in progress at cutover, waits until it is settled. Do not place an upstream decision in a frontier while its own prerequisites remain unsettled.
- **Cover every stated goal's core facets before drilling down.** Order each frontier so that core decisions come first across all stated goals, and derived decisions follow; among derived decisions, ask depth-1 items before depth-2 items, ordered by the impact of their stated goal. Do not present a derived decision of depth 2 or more while any stated goal still has an askable core decision, and present one of depth 2 only when it also meets the stage 2 threshold in Step 5, whichever stage the interview is in; otherwise settle it by consequence where the rule below allows, or hold it Outstanding. Settle a derived decision of depth 3 or more by consequence where the rule allows, or hold it Outstanding, unless it makes an answer precise, confirms a conflict with a recorded decision, or the user raised it. A point that the request map classifies as a core decision is not subject to these limits. List every held derived point at the satisfaction gate, and record it under Out of Scope and Limitations when Step 4C requires. Do not ask about context already established by the project materials. Fewer questions are not a completion criterion: retain consequential follow-ups, fact investigation, rescans, and explicit holds under the existing rules, but spend each question on the most consequential unsettled decision of the request rather than on the detail nearest the previous answer.
- **Settle consequences without asking.** When accepted decisions and investigated facts entail the resolution of a derived point—it follows from applying an accepted rule, state, or formula, not merely from finding no other plausible resolution—do not ask: incorporate it through Step 4C as a requirement that cites the decisions it follows from, mention it in the one-line incorporation note, and list it at the satisfaction gate so the user can revise it. Otherwise the point is a question, subject to the depth and threshold rules. A consequence introduces no new capability, actor, state, operation, threshold, boundary, or value; if one would be needed, the point is a question. Never settle by consequence a point that no accepted rule covers: who may perform, approve, change, or correct something, or how actors are recorded (facet 2); which kinds of operation are available under a condition, such as while disconnected; or a state, transition, or terminal outcome that no accepted answer already contains, including the outcome when operations cross each other. Ask these even when one option seems obvious, and recommend that option. Ask permission, availability, and crossing points as rules by kind of operation, as facets 2 and 4 require, so that an operation or crossing settled later falls under the accepted rule by consequence; ask again only for a kind the rule does not cover. A consequence may apply an accepted rule, state, or formula to further cases of the same kind, such as the accepted ordering basis to the order of two later records, or an accepted recount or correction rule to a quantity settled later. Derive it only from accepted answers and investigated facts, never from another consequence.
- **Ask only what the evidence raises.** Create a derived candidate only for a situation that a stated goal's wording, an investigated fact, or an accepted answer says exists or implies ("the materials say shipments may arrive split" qualifies, and so does the remainder that a split shipment may leave). The standard exceptions of a stated workflow, the items in progress at cutover, and the designated-actor cases of facet 2 are raised by the stated goal itself, never merely imagined: settle each applicable one by a question, or by consequence where the rule above allows. Record it as a limitation instead only when the user declines to decide it or it is held under the existing hold rules; never skip the question merely to save a turn. Do not turn a situation whose only basis is speculation into a question, even with a recommendation—for example, a rare external event the materials never mention, such as a carrier delivering to the wrong site. If it seems material, list it at the satisfaction gate under situations noted but not asked and record it in the spec as Step 6 requires; the user can reopen it with option 2.
- **Treat reference-data administration and record layout as operations detail.** How codes, variants, locations, or users are added to or maintained in reference data, which fields a record carries beyond those the stated goals and acceptance scenarios need, and how a screen is laid out are not interview decisions unless a stated goal is about them. This covers how records, including designation data, are entered and maintained, not who holds a business role: which actor a workflow designates belongs to facet 2. If the materials describe how reference data is maintained, cite that process under Verified Premises. Otherwise do not assume that a process exists: hold these points Outstanding, record once under Out of Scope and Limitations that the materials do not describe reference-data administration and this spec does not define it, and make no requirement depend on an undescribed process.
- **Recommend the option that best achieves the stated goals.** Choose the **Recommended** option by how completely and safely it settles the stated goals while respecting the investigated facts and known constraints. Use lower complexity only to choose between options that achieve them equally well; never prefer an option merely because it adds the fewest states, operations, or records. When a stated goal involves a handoff between two parties—one requests and another fulfils—prefer options in which each party's commitment (acceptance or refusal, fulfilment, closure) is an explicit recorded state visible to both, over options that leave a party's obligation implicit. Offer a scope-narrowing option—handling the situation outside the system, or recording a limitation—whenever it is viable, but state which stated goal or investigated fact it leaves unmet and the practical consequence. Recommend narrowing only when every stated goal remains achieved, when the request explicitly excludes the element, or when the user has asked for a narrower scope. Do not recommend ignoring a situation the materials say exists or occurs (for example, variants that are known to be mixed) unless one of those conditions holds. Once an ordering basis for a stated goal is accepted, recommend the same basis for every later ordering or conflict decision of that goal; an option that uses a different basis must say so and state where each basis applies.
- **Label agent-introduced elements and keep their details out of the interview.** Label an option that adds an agent-introduced element as a scope extension, name the stated goal it would serve, and keep at least one option that settles the decision without it. Do not recommend an extension; if no option without the element can achieve a stated goal, the element is grounded, so reclassify it and compare it as an ordinary option. If the user accepts an extension, record it in the spec as an agreed extension with its externally visible behavior, then hold its internal details (sub-states, correction and merge rules, administration operations) as Deferred with the rationale "agreed extension; details belong to planning" instead of drilling into them, unless the user asks. Quantify a vague target that the request itself states (such as "immediately") once, offering "no numeric target" as a choice; do not introduce targets for qualities the request does not mention.
- **Defer to planning only what changes no user-visible behavior.** "Belongs in planning" covers technical realization—storage, synchronization mechanics, algorithms, and internal data layout—whose outcome does not change what users do, see, or when. Cutover timing, parallel operation of old and new records, rollback procedure, approval steps, permissions, and who records what are interview decisions: settle them, or hold them Outstanding / Deferred with a reason other than "planning." A decision without which a stated goal cannot be verified is never deferred to planning.
- **If a conflict with a recorded decision is detected, reopen the affected decision point and confirm it first in the next round.** Whether the conflict comes from a user answer, investigation, or rescan, do not silently overwrite the spec. Perform the following in the same operation:
  1. Return the corresponding design-tree node to unresolved.
  2. Return the same decision point in the coverage map to Partial, preserve its previous status and settled value separately as the "old settled value pending confirmation," and immediately recalculate the aggregate category status.
  3. Say, in one line, "A conflict with a recorded decision was detected; I will confirm it first in the next round." If a user answer triggered the conflict, hold that answer until the conflict is settled.
  4. Add a follow-up question asking whether to keep the old decision or adopt the new information, and make it the first candidate for the next round.
  5. Until the conflict is settled, treat the affected point as an unresolved prerequisite and return the remaining frontier questions that depend on it to the question candidate pool. Finish the current round with only the remaining questions that can still be answered.
  6. Incorporate, save, and validate a conflict settled through user choice via Step 4A; handle an apparent conflict resolved solely by investigated facts via Step 4B. Only after completion, simultaneously settle the design-tree node, change its coverage status to Resolved, discard the preserved old value, and recalculate the aggregate category status. If it remains ambiguous, keep it Partial and continue with a follow-up.
- **Follow up on ambiguous or contradictory answers.** Do not stop until the answer is precise. You may create hypothetical scenarios to probe boundaries, but explicitly label them "hypothetical" in the question. Until the user accepts them, do not treat them as project facts, requirements, or decisions and do not incorporate them into the spec. Add each follow-up to the question candidate pool and confirm it on a later frontier.
- **Do not preview later questions.** Present only the current question. Do not reveal or list the remaining questions in the current round or any future round ahead of time.
- **Do not act on a decision until shared understanding is confirmed.** Incorporate only into spec.md; do not begin plans, tasks, or code.
- **Respect interruption signals such as "stop," "that's enough," or "let's move on for now."** Stop presenting new questions immediately and enter the "Interrupted completion path." Ending the question loop does not mean skipping the checklist, hooks, or completion report.

### Interrupted completion path

If the user asks to stop after the spec has been loaded, perform these steps in order regardless of the interview stage:

1. Do not incorporate any answer that has not yet been accepted. Preserve changes that were accepted, saved, and validated before the interruption.
2. Change every remaining Partial / Missing decision point to Deferred, including the current question, unpresented candidates, candidates blocked by dependencies, unfinished factual research, and points reopened for conflict confirmation. Record the reason as "User interruption" and move corresponding design-tree nodes to terminal hold. Empty the frontier and question candidate pool, then recalculate aggregate category statuses.
3. Do not fill unresolved content by assumption or create new Clarifications Q&A entries. Record under Out of Scope and Limitations, one line per stated goal labeled Undecided (interrupted), the Outstanding or Deferred points and situations noted but not asked that leave that goal's behavior undefined and are not yet recorded, stating only that they are undecided. Then run the final full validation from Step 4C against the saved spec.
4. Skip the Step 5 rescan and Step 6 satisfaction gate, and proceed to checklist revalidation in Step 7.
5. After Step 7, process `hooks.after_clarify` according to the extension-hook rules. Actually invoke required hooks and wait for completion; present optional hooks only as guidance.
6. Issue the Step 8 completion report as "Completed by user interruption." Include the interruption point, decision points deferred with reasons, requirements settled by consequence marked as not confirmed at a satisfaction gate, coverage table, checklist results, hook results, and a recommendation on whether to proceed to planning or rerun this command later.

### Question format

Present questions one at a time in sequence using the following format. Start with the highest-priority askable decision using the choice format below, rather than requiring a general account of the user's goals or experiences first. Use known context to frame concrete options, keep the free-form route available, and honor a user's request to explain their situation; do not assume a missing fact to make an option selectable. Restart numbering at `Q1` for every round so the number itself signals a new round. Give carried-over questions new numbers and state in one line when presenting them that they were carried over from the previous round.

```text
❓ **Q1** - **<Question title>**: <Question text. It may include contextual explanation and multiple paragraphs.>

- Verified facts: <fact (source)>; <fact (source)>
- Accepted decisions: <Round n, Qk — summary>
- Unverified assumptions: <assumption used to compare the options>

➡️
- **A. <Choice>** — **Recommended**. <Reason for recommendation in 1–2 sentences>
- **B. <Choice>** — <Rationale in 1–2 sentences>
- **C. <Choice>** — <Rationale in 1–2 sentences>
- **Free-form** — Another answer, partial adoption, or a conditional answer (unlimited length)
```

Vary the number of choices between one and three according to the situation, but always include the `**Free-form**` line. Omit any of the three basis labels that has no entries; never move an entry to a label it does not belong to. The user may answer the one currently presented question with a single label such as "A" or "B," with "recommended," or in free form. Accept "yes" only when its meaning is unambiguous in the current question. If the user says "skip," carry the question into a later round and renumber it there; if the user says "defer," mark the point Deferred with the reason "user deferred" and do not ask it again unless the user reopens it. Also accept free-form text that addresses a question other than the one currently presented—such as an advance answer to a later question or an explicit revision to a settled decision—and incorporate each decision through Step 4A just like the answer to the current question. Recalculate the frontier only at the end of the round. Numbers are for reference within a round and are not recorded in spec.md; use the Clarifications format in Step 4A. When referring to a question from an earlier round, use "Round n, Qk (<question title or summary>)" and always restate the question content because the number alone is not memorable.

## Workflow

### Step 1. Ambiguity scan

Read the entire spec.md and create an internal coverage map assigning **Clear / Partial / Missing** to every decision point within all categories in the Glossary. Initialize the map only during the first scan. When returning from Step 5, do not recreate the map or reset every point to these three statuses; follow the reconciliation rules in Step 5. Do not assign a status directly to a category. Derive aggregate category status from per-point statuses.

In the same scan, build the **request map**: list every stated goal in the request's own words, then assess its six core facets against the spec and the investigated materials, marking a facet Clear only when existing text already settles it and recording the sentence that does. Create a core-decision candidate for every facet that is Partial / Missing, tagged with its stated goal. A stated capability or constraint whose facets are all Clear still receives an acceptance check through Step 4C.

Create a question candidate from every other Partial / Missing decision point and collect all candidates in the **question candidate pool**. Exclude only matters that "have no material effect on implementation or validation strategy" or "are appropriately deferred to the plan phase under the deferral rule in the interview discipline (retain them in an internal note)." Facts whose answers can be established are investigated and removed in Step 2, not excluded here. **Do not limit the number of questions.**

Do not leave an excluded point as Partial / Missing. Immediately change it in the coverage map to **Outstanding** or **Deferred** according to the Glossary's status definitions, then recalculate its aggregate category status. Step 5's completion condition cannot be reached until every point has a final status.

### Step 2. Fact gate and frontier calculation

Whenever candidates are added to the question candidate pool, apply the **fact gate** below before calculating the frontier to all candidates that have not yet passed it and all candidates whose premises changed because a dependency was settled or for another reason. This applies not only to candidates created by the initial Step 1 scan, but also to follow-ups, drill-downs, decision-derived checks, and rescans.

1. Classify the candidate's answer as either "a fact that investigation can establish" or "a decision the user must make as project policy."
2. Investigate factual candidates yourself in the codebase, project documents, and existing specs. Remove candidates whose answers are established from the question candidate pool. If the investigated fact resolves ambiguous text in the spec, edit only the main spec through **Step 4B**, then change the corresponding point to Resolved after incorporation and validation. Do not add it to Clarifications.
3. Keep a candidate whose factual investigation depends on an unresolved decision or cannot finish during the current round in the pool as "awaiting research." Do not add it to the frontier or turn it into a user question. Reapply the fact gate after its dependency is settled or the research is complete.
4. Reclassify a candidate as a decision only if, after exhausting available sources, it becomes clear that new project policy or requirements must be chosen. If a factual answer exists externally but simply cannot be obtained, do not treat it as a decision. Mark it Outstanding if it has no impact on implementation or validation strategy; otherwise mark it Deferred and record why it could not be investigated.

Apply the threshold at its current stage (see the threshold definition in Step 5) to every candidate that remains a decision after passing the fact gate; a core decision always passes it. Remove any candidate that does not pass it—at stage 1, one whose answer, regardless of the outcome, would not change implementation, data model, task breakdown, test design, UX behavior, operations, or compliance validation. Settle a removed candidate by consequence where the rule allows; otherwise change the corresponding point to Outstanding or Deferred, record it under Out of Scope and Limitations when it leaves a stated goal's behavior undefined, and recalculate aggregate category status.

Associate each remaining decision candidate with the design-tree node it will settle and, through the request map, with its stated goal and depth. Move candidates with **no unresolved prerequisites** from the pool to the frontier, leaving all others in the pool. Sort the frontier as the interview discipline requires: core decisions first across all stated goals—decisions that constrain several others ahead of the rest, then by impact × uncertainty—followed by derived decisions by depth and then by the impact of their stated goal. Number it according to the Question format.

### Step 3. Round loop

Treat the current frontier as one round and proceed with one question and one answer at a time:

1. At the start of a round, announce `Round n (m questions)` in one line. If a round starts with confirmation of a conflict detected in the previous round, include that fact in the announcement, for example: `Round n (m questions) — Starting with confirmation of a conflict with a recorded decision.` Do not preview the question list.
2. Following the Question format, present only the first question in the round and wait for the user's answer. The presentation order is the ordering from Step 2, and numbering begins with Q1 in that order.
3. When the answer arrives, incorporate and save each settled decision via Step 4A, change the corresponding point to Resolved, and only then present the next question. State in one line what the saved file now contains: the requirement and scenario identifiers added or changed, any requirement settled by consequence, and the Clarifications count as "n of n accepted answers." Report the state of the saved file, not the editing steps; an intermediate edit reverted before saving needs no mention. If an answer remains ambiguous or contradictory, create a follow-up in the candidate pool for a later frontier; do not insert it into the current round. State in one line that it was held and why before moving to the next question. Carry skipped questions into a later round and renumber them there; mark deferred ones Deferred as the question format requires. If an answer conflicts with a recorded decision, hold it according to the interview rule for conflicts and put the confirmation follow-up first in the next round.
4. If an existing answer already settles a later question in the round, do not present it; say in one line that it was incorporated as answered based on the existing answer. If the answer invalidates the premise of a later question, immediately apply the Design tree non-applicability rules, change the corresponding point to Resolved, then say in one line that the parent decision made it inapplicable. If an earlier answer in the round rules out an option or changes a fact that a later question would cite, compose that question from the spec as saved, dropping or revising the affected option.
5. After the round's questions are exhausted, perform **round-end processing**: report `Round n complete — x settled, y carried over` in one line, run the **decision-derived check**, recalculate the design tree, return to Step 2, and recalculate the next frontier. During the decision-derived check, compare every decision settled in the round with investigated facts about its applicable scope—target types, differences by screen, list/detail/history views, field composition, required/optional status, and so on—and add any overlooked inconsistency or boundary condition to the candidate pool. Also reconcile the request map: if a settled decision changed the meaning, actors, operations, or state effect of a stated goal—for example, by adding a correction or cancellation—reassess that goal's remaining facets, including facets 3 and 4 for the added operation, and the acceptance checks that cite the decision.

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
2. For every accepted answer, append one line: `- Q: <question> → A: <settled answer>`. When a later accepted answer changes an earlier settled decision, keep the earlier line and append ` → Superseded by <later question summary>: <new result>` to it (in the spec's language), so that no Clarifications line states a decision that the main text no longer contains.
3. Incorporate the settled decision into the main spec according to "Step 4C. Shared incorporation and validation rules."
4. If one answer contains multiple decisions, incorporate, save, and validate each decision separately, except that decisions which change the same requirement or depend on each other are incorporated in one save, so that no saved state contradicts the answer. Keep only one Clarifications Q&A line per accepted answer; do not duplicate the same answer.
5. After each decision has been saved and validated successfully, change its point to Resolved and recalculate aggregate category status.

#### Step 4B. Incorporate a fact established by investigation

1. Do not create `## Clarifications` / `### Session YYYY-MM-DD` and do not append a Q&A line. Clarifications records only the user interview.
2. Incorporate only facts verified from the codebase, project documents, or existing specs into the main spec according to "Step 4C. Shared incorporation and validation rules." Never incorporate assumptions or hypothetical scenarios as facts.
3. Incorporate, save, and validate each verified fact separately.
4. After it has been saved and validated successfully, change the point resolved by that fact to Resolved and recalculate aggregate category status.

#### Step 4C. Shared incorporation and validation rules

1. Incorporate content into the best section:
   - Functional ambiguity → Functional Requirements
   - Actor or action distinctions → User Stories / Actors
   - Data shape → Data Model, preserving the existing field order and keeping constraints concise
   - Non-functional requirement → measurable form under Success Criteria; convert vague adjectives into metrics
   - Edge case → Edge Cases / Error Handling
   - Terminology → normalize to the canonical term throughout the spec; if needed, note `(formerly "X")` once
   - If spec.md has no section suited to the content, **add a standard section heading** at the same level as the existing top-level sections rather than extending the overview prose. Use the project's template names when they exist; otherwise use, written in the spec's language: Actors and Permissions, Functional Requirements, Data and State, Edge Cases and Failure Handling, Non-functional Requirements, Acceptance Criteria, Out of Scope and Limitations, and Verified Premises (facts incorporated through Step 4B, each with its source). Keep the original request text intact except for minimal edits that resolve a contradiction; do not rename, reorder, or merge existing sections.
   - Write every requirement as a numbered, independently testable statement in a list, never as an addition to a prose paragraph. Give identifiers a prefix per section—AP- Actors and Permissions, FR- Functional Requirements, DS- Data and State, EC- Edge Cases and Failure Handling, NFR- Non-functional Requirements, SC- Acceptance Criteria, OS- Out of Scope and Limitations, VP- Verified Premises—and add each new item at the end of its section with the next number, so that reading a section from top to bottom meets its identifiers in order. Never renumber an existing identifier; a gap left by a removed item is expected. Follow the project's template when it defines its own identifiers. Keep each statement to the rule itself—normally one or two sentences—without restating context, rationale, or the question. A requirement settled by consequence cites the decisions it follows from, for example (derived from Round 2, Q1 and F04). Express a state change as an explicit rule: the triggering event, the quantities or states that change, and what each party sees. Record an agreed exclusion, limitation, or agreed extension under Out of Scope and Limitations with its reason; for an exclusion or limitation, also name the stated goal or fact it leaves unmet. Record there as well, one line each and labeled Undecided so that none reads as an agreed exclusion, every situation noted but not asked and every Outstanding or Deferred point that leaves a stated goal's behavior undefined, stating the point, its status, the reason, and whether a user decision or a missing fact would settle it (for example, Undecided (not asked): <situation> — <reason>; needs a user decision), so that the spec alone shows what remains open; remove the line if the point is later resolved.
2. If new content invalidates older ambiguous text, **replace** it rather than appending a duplicate. Leave no conflicting obsolete text. When a later decision qualifies an existing requirement—adds an exception, a condition, or a further case—amend that requirement in place under its identifier rather than adding a second requirement that overrides it from elsewhere; add a new identifier only for a new rule.
3. **Derive an acceptance check from each settled decision that defines behavior, a boundary, or a failure outcome of a stated goal.** Add it under Acceptance Criteria as a numbered scenario (for example SC-004) on one line stating the setup, the action, and the observable result with the fewest quantities that distinguish it, and cite the decision it verifies. Merge scenarios that differ only in their numbers. Do not write scenarios for exclusions or out-of-scope items; Out of Scope and Limitations records those. A stated prohibition—an action that must be refused—is a constraint, not an exclusion: verify it with a scenario showing the refusal. Use only accepted values; example quantities are allowed when labeled as examples and the result does not depend on the specific number. A check adds no requirement: if it would need a threshold, target, or capability that has not been accepted, do not write it—create a question candidate for that value instead, offering "no numeric target" as a choice.
4. **Save spec.md after every incorporation.** Edit in place—insert or replace only the affected lines—rather than rewriting the file, and confirm that the saved diff touches only the intended lines. Do not reorder unrelated sections or alter their heading hierarchy. Keep additions minimal and testable.
5. **Validate after every save**, and run one final full pass after the last round:
   - For Step 4A, re-read the saved file and count the Clarifications lines; there must be exactly one non-duplicated line per accepted answer. If the count differs from the number of answers accepted so far, repair it before presenting the next question. For Step 4B, ensure Clarifications has no diff.
   - Ensure requirement and scenario identifiers are unique within the spec and increase within their section, that no requirement is overridden by a requirement in another section, and that a superseded decision's requirements and scenarios were updated in the same operation.
   - Ensure all records of one stated goal, quantities and workflow states alike, are ordered by one basis, or that the spec states which basis applies where and an acceptance scenario exercises the combination.
   - Ensure no ambiguous text or placeholder that the incorporation should resolve remains.
   - Ensure no invalidated option or conflicting obsolete text remains.
   - Ensure Markdown structure is valid. The only new headings may be the standard sections named above and `## Clarifications` / `### Session YYYY-MM-DD` from Step 4A.
   - Ensure every new requirement is a numbered statement, every acceptance scenario cites an accepted decision and no unaccepted value, and no Clarifications line contradicts the main text without a supersession note.
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
> - **Stage 1 — until core coverage is complete** — Ask about any point whose answer could change implementation, data model, task breakdown, test design, UX behavior, operations, or compliance validation. Step 2 applies this gate from the initial scan.
> - **Stage 2 — from the first round-end at which core coverage is complete, and in any case from the second rescan** — Core coverage is complete when every stated goal's six core facets, including the standard exceptions and the items in progress at cutover, have a final status in the request map. From then on, ask only about a point whose different answers change what a party can do or sees, or change an obligation for data integrity, security, or compliance, in a situation that the request, the materials, or the user's own words describe, such as two devices recording the same event. Do not ask about a point that exists only to maintain a state, quantity, or operation that an option introduced, beyond what that option already states under the drill-down rule—such as a new operation to reduce a quantity it adds, or whether another operation counts it—or that an accepted rule settles by consequence: settle it by consequence where the rule allows, otherwise hold it Outstanding, list it at the Step 6 satisfaction gate, and record it under Out of Scope and Limitations when Step 4C requires. The user can reopen it with option 2. At any stage, always ask a follow-up that makes an answer precise, a confirmation of a conflict with a recorded decision, and any core decision found unsettled—a standard exception, an item in progress at cutover, a designated-actor case, or a point the request map classifies as core—unless an accepted rule entails its answer.

Before leaving Step 5, review the request map together with the Acceptance Criteria. Every stated capability or constraint must have at least one acceptance scenario and every stated exclusion a line under Out of Scope and Limitations, and every settled failure or conflict outcome of a stated goal must be exercised by a scenario—partial completion, retried or duplicate submissions, concurrent actions on the same record, out-of-order events, and reconciliation against records not yet synchronized, when the goal involves them. Derive missing scenarios through Step 4C when the settled decisions suffice; otherwise create candidates for the missing decisions and apply the rescan threshold to them like any other. Also confirm that every standard exception of a stated workflow, the items in progress at cutover, and the designated-actor cases of facet 2 are settled, Not applicable with a reason, or recorded as a limitation. Create core-decision candidates for any that are none of these; the staged rescan threshold does not hold them back, because each changes the behavior of a stated goal.

### Step 6. Satisfaction gate

Once every point is Clear / Resolved / Outstanding / Deferred, first confirm that no Outstanding point would change a stated goal's quantities, states, or permitted operations, or how current its data must be; reclassify any that would as a core decision and return to Step 2. Then record under Out of Scope and Limitations every situation noted but not asked and every hold that leaves a stated goal's behavior undefined, following Step 4C items 1, 4, and 5 without adding a Clarifications line. Then present aggregate category statuses, per-goal coverage of the six core facets from the request map, a per-point summary of Outstanding / Deferred items, the requirements settled by consequence (each with the decisions it follows from), situations noted but not asked, the sections changed in this run, and whether the spec is ready for planning: it is not while a Deferred core decision blocks implementation or acceptance verification. Take every count of saved content—accepted answers, requirements, scenarios—from the saved file. Then use **AskUserQuestion or another interactive UI to present choices and confirm satisfaction**. (If no interactive UI is available, present the same three choices in the normal response and wait for the user's selection.) Do not wait for a free-form "OK." Use this fixed confirmation format every time **at this satisfaction gate only**; it does not apply to Step 3 rounds, which use the question format from the interview discipline.

Always offer these three choices and explain the recommendation:

1. **Finish and proceed** — **Recommended**, because every point has a final status and no unresolved question remains; choosing it also accepts the requirements settled by consequence listed above. When the spec is not ready for planning, say that this choice ends the interview only and that planning should wait until the blocking points can be settled
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
- Number of rounds, questions presented, and accepted answers. Count accepted answers from the saved Clarifications rather than from memory, and state separately any question that was skipped, deferred, or asked again as a follow-up; optionally include a per-round breakdown. The question-and-answer list may refer to Clarifications. List requirements settled by consequence separately.
- Path to the updated spec and the sections changed.
- Checklist before/after pass counts, newly passed and regressed items, and items still failing, listed as areas needing attention.
- Coverage table: show every category's aggregate status as **Resolved** / **Clear** / **Deferred** / **Outstanding**, with a per-point status breakdown for each category. Do not proceed to the completion report if even one Partial / Missing point remains.
- Request map table: every stated goal with the status of each of its six core facets, the acceptance scenarios (for an exclusion, the Out of Scope line) that verify it, and any agreed extension or recorded limitation attached to it.
- If Outstanding / Deferred items remain, recommend whether to proceed to the agent-specific invocation of `speckit.plan` or rerun this command later. A final status is not a settled decision: name each Deferred core decision that blocks implementation or acceptance verification, and while one remains, recommend rerunning this command once it can be settled rather than proceeding to planning.
- Suggested next command, normally the agent-specific invocation of `speckit.plan` (for example, `/speckit.plan`, `/speckit-plan`, or `$speckit-plan`).

## Behavior rules

- This workflow is expected to finish **before** `speckit.plan`. If the user explicitly skips it and proceeds, comply after warning that the risk of downstream rework will increase.
- If no significant ambiguity exists, report "No critical ambiguities detected," provide an aggregate category summary showing all points as Clear, and proceed to the Step 6 satisfaction gate. Do not invent questions.
- Do not ask speculative questions about the technology stack unless they block functional clarification.
- This command may modify only spec.md and `checklists/requirements.md` (and only checkbox states in Step 7). Do not modify plans, tasks, code, or any other file.

## Done When

- [ ] Ambiguities in the spec have been identified, and settled answers and investigated facts have been incorporated and saved in spec.md through Step 4A / 4B respectively, with the final Step 4C validation pass complete.
- [ ] The question candidate pool is empty, with no askable questions, unfinished factual research, or blocked candidates depending on unsettled parents. No question rests on an assumed premise, and no awaiting research or dependency cycle is abandoned. On interruption, every point corresponding to remaining questions and research is explicitly Deferred.
- [ ] Design-tree node statuses match corresponding coverage statuses. No working-unresolved node retains a terminal status, and all unresolved nodes are terminally held upon interruption.
- [ ] Current parent decisions and the applicability of all descendants agree. No child that became applicable again retains an obsolete non-applicable or parent-dependent terminal rationale.
- [ ] Every decision point has reached one of the final statuses—Clear / Resolved / Outstanding / Deferred—and aggregate category statuses have been recalculated.
- [ ] Every stated goal in the request map has all six core facets at a final status, and every stated capability or constraint has at least one acceptance scenario in the spec, every stated exclusion a line under Out of Scope and Limitations. Every standard exception of a stated workflow and every designated-actor case of facet 2 is settled, Not applicable with a reason, or recorded as a limitation, and every situation noted but not asked and every hold that leaves a stated goal's behavior undefined appears under Out of Scope and Limitations.
- [ ] Every agent-introduced element is recorded as an agreed extension or excluded with a reason, and every scope-narrowing choice names the stated goal or fact it leaves unmet. Every requirement settled by consequence cites accepted answers or facts, was listed at the satisfaction gate, and applies an accepted rule to a case of the same kind rather than deciding a point no accepted answer covers. Every reported count of saved content—accepted answers, requirements, scenarios—was taken from the saved file, questions presented and rounds from the session, and nothing was deferred to planning that changes user-visible behavior.
- [ ] Permission, availability, and crossing rules were asked by kind of operation and applied to later operations by consequence. No derived decision of depth 3 or more was asked unless it made an answer precise, confirmed a conflict, or the user raised it; no question after core coverage was complete fell below the stage 2 threshold; no point whose answer would change a stated goal's managed quantities, states, or permitted operations, or how current its data must be, was held Outstanding; and every held derived point was listed at the satisfaction gate.
- [ ] User satisfaction is explicit, except upon interruption.
- [ ] `checklists/requirements.md` has been revalidated against the updated spec, if present.
- [ ] Extension hooks have been processed, skipped, or reported as unreadable according to the rules.
- [ ] A completion report has been issued with rounds, questions presented and accepted answers, changed sections, checklist status, and a coverage table containing aggregate category statuses and per-point breakdowns.
