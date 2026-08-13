# Final Study Note

# Workflow vs Agent

## Short answer

The distinction is architectural control. In a workflow, LLMs and tools are orchestrated through predefined code paths; in an agent, LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks (Building Effective AI Agents). Workflows suit well-defined tasks where predictability and consistency matter, while agents suit open-ended problems whose required steps cannot be predicted or hardcoded. Both sit under the broader category of agentic systems, which typically trade increased latency, cost, and a higher risk of unintended consequences for better task performance (Building Effective AI Agents). Agent autonomy additionally introduces the risks of misreading user intent and vulnerability to prompt injection attacks (Trustworthy Agents in Practice).

## Core concepts

**Agentic systems** is the umbrella term covering both prescriptive implementations (workflows) and autonomous ones (agents).

**Workflow** â€” a system where LLMs and tools are orchestrated through predefined code paths (Building Effective AI Agents).

**Agent** â€” a system where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks (Building Effective AI Agents). An agent operates in a **self-directed loop**: planning, acting, observing results, and adjusting until the task is complete or human input is required (Trustworthy Agents in Practice).

**An agent is not just a model.** Agents are composed of the model, the **harness**, the tools, and the environment (Trustworthy Agents in Practice). The harness is the instructions, and the guardrails, that the model operates under.

**Agent-Computer Interface (ACI)** â€” named in the evidence as the surface through which tool documentation matters, but not defined there. Designing effective agents requires prioritizing simplicity, transparency, and thorough tool documentation through the ACI (Building Effective AI Agents).

**Plan Mode** â€” an oversight pattern where the agent shows an intended plan of action up-front for review, rather than asking for step-by-step approval (Trustworthy Agents in Practice).

Two distinctions worth holding separately:

- *Fixed vs. input-dependent subtasks.* In parallelization workflows the subtasks are predefined. In orchestrator-worker workflows the orchestrator determines the subtasks dynamically based on the specific input.
- *Step-level vs. strategic oversight.* Standard interfaces require approval for individual actions; Plan Mode shifts oversight to the overall strategy.

## How it works

The ordering below is this note's organisation, not a sequence stated in the evidence.

1. **Characterize the task.** Workflows are appropriate for well-defined tasks requiring predictability and consistency. Agents are suited for open-ended problems where the required steps cannot be predicted or hardcoded, and are the better option when flexibility and model-driven decision-making are required at scale (Building Effective AI Agents). These are suitability conditions, not a binary test.
2. **For a workflow: use a predefined code path.** Available patterns include prompt chaining, routing, parallelization, and evaluator-optimizer. Note whether subtasks are predefined (parallelization) or determined by an orchestrator from the input (orchestrator-worker).
3. **For an agent: account for all four layers.** An agent comprises the model, the harness (instructions and guardrails), the tools, and the environment (Trustworthy Agents in Practice).
4. **Expect the self-directed loop.** The agent plans, acts, observes results, and adjusts until the task is complete or human input is required.
5. **Prioritize ACI design.** Simplicity, transparency, and thorough tool documentation through the Agent-Computer Interface are named requirements for effective agents (Building Effective AI Agents).
6. **Choose where oversight sits.** Either approval of individual actions, or Plan Mode's up-front review of the intended plan.
7. **Account for the trade-offs.** Agentic systems often trade latency and cost for better task performance (Building Effective AI Agents), and agent autonomy introduces misread intent and prompt injection risk (Trustworthy Agents in Practice).

## Concrete example

Two contrasting source-backed cases:

**Workflow â€” routing.** General customer-service questions are directed to smaller models; complex technical queries are directed to more capable models (Building Effective AI Agents). The destinations are set by the workflow's predefined code path. The evidence does not describe what performs the classification.

**Agent â€” coding agent.** An agent resolves SWE-bench tasks by autonomously editing multiple files based on a pull-request description (Building Effective AI Agents).

The Evidence Pack also lists **subagents** â€” "Claudes" working in parallel on different parts of a complex task. The pack labels the reading that this represents a coordination pattern for scaling agentic work as an **inference**, not a sourced claim, so treat it as such.

## Why it matters for my work

For a backend AI engineering intern, this is a design-time decision that changes what gets built and what has to be guarded against.

- **It sets the default.** Workflows offer higher predictability and consistency for well-defined tasks; agents are the better option when flexibility and model-driven decision-making are required at scale (Building Effective AI Agents). Choosing an agent for a task with enumerable steps buys autonomy the task may not need. The evidence does not establish that agents cost more or run slower than workflows â€” the latency and cost trade-off is stated for agentic systems generally, which includes workflows.
- **Tool documentation is named engineering work.** Simplicity, transparency, and thorough tool documentation through the Agent-Computer Interface are requirements for effective agents (Building Effective AI Agents), so documentation quality is part of the build rather than an afterthought.
- **Agent autonomy adds a risk surface.** Agents can misread user intent and are vulnerable to prompt injection attacks (Trustworthy Agents in Practice). The evidence makes no comparative claim about workflows' exposure to these risks.
- **Oversight placement is a real choice.** Step-level approval and Plan Mode's strategic review are distinct patterns (Trustworthy Agents in Practice).
- **The four-layer composition is worth knowing.** An agent is the model, harness, tools, and environment (Trustworthy Agents in Practice). *Inference: this suggests that when an agent behaves badly, the cause may lie outside the model. The Evidence Pack does not make any claim about debugging or where fixes belong.*

## What the evidence does not establish

- **Terminology is unsettled.** "Agent" is defined in several ways, ranging from fully autonomous systems to prescriptive workflows â€” so the split above is not universally shared vocabulary.
- **No standardized benchmarks.** There is no rigorous industry-wide method for comparing resistance to prompt injection or reliability in surfacing uncertainty. Comparative claims about which system is safer are therefore not backed here.
- **Security is not solved.** Combined defenses such as training, monitoring, and red-teaming are not a guarantee against prompt injection.
- **Goal alignment is open.** Balancing excessive clarification against risky assumptions remains an unsolved problem.
- **No quantities.** No figures for how much latency or cost agentic systems add, and no threshold for when a task is "well-defined enough" for a workflow.
- **No relative cost or security comparison.** The evidence supports neither "agents cost more than workflows" nor "workflows have a smaller threat surface."
- **No definition of the Agent-Computer Interface.** The ACI is named as a design priority but not defined.
- **Citation precision is unverified.** NotebookLM displayed clickable numbered citations in its interface, but its copy-response function removed those markers. The source labels were manually restored from the visible NotebookLM response. Precise citation locations still require human verification against the original sources â€” every label above should be re-checked before this note is cited elsewhere.

## Comprehension checks

1. A teammate proposes an agent for a pipeline whose five steps are identical on every run. Using the suitability conditions in the evidence, argue whether the agent is justified â€” and state what the evidence does *not* let you claim about the relative cost of the two options.
2. Parallelization and orchestrator-worker both split a task into subtasks, yet the Evidence Pack treats the difference as significant. Explain what changes about *who determines* the subtasks, and what that implies about how much can be fixed in code ahead of time.
3. An agent is described as the model, the harness, the tools, and the environment. Explain what the harness contributes that the model alone does not, then state why the evidence does not let you claim which layer to change when an agent misreads user intent.

## Change Log

| Critique ID | Action taken | Evidence used |
|---|---|---|
| C1 | Removed "the model does not choose its own destination." Replaced with a statement that destinations are set by the predefined code path, plus an explicit note that the evidence does not describe what performs the classification. | Pack Â§5 routing example; Â§4 "Workflows follow code-governed steps." |
| C2 | Removed "A predefined path does not have the same surface." Agent risks now stated additively with an explicit note that no comparative claim about workflows is made. | Pack Â§3 agent-risk claim (Trustworthy Agents in Practice). |
| C3 | Removed "docstring" and "shape of a tool's interface." Restated using the Pack's own wording. | Pack Â§3 ACI claim (Building Effective AI Agents). |
| C4 | Removed the binary "agent territory" test. Reframed as suitability conditions and restored the missing scale / model-driven-decision criterion. | Pack Â§1 working answer; Â§3 flexibility-at-scale claim. |
| C5 | Unintended-consequence risk reattributed to agentic systems generally; agent-specific risks kept as misread intent and prompt injection. | Pack Â§1 working answer; Â§3 agent-risk claim. |
| C6 | Removed the implied agent-vs-workflow cost comparison and added an explicit statement that the evidence does not establish it. | Pack Â§3 latency/cost claim, which applies to agentic systems; Â§2 umbrella definition placing workflows inside that category. |
| C7 | Expense-submission example replaced with the SWE-bench coding agent, per the revision instruction. The unsupported runtime-sequencing gloss is gone; the replacement is described without asserting a mechanism the Pack does not state. | Pack Â§5 Coding Agent example. |
| C8 | Four-layer debugging claim retained but explicitly labelled as an inference, with a note that the Pack makes no claim about debugging or fix location. | Pack Â§4 model/harness/tools/environment composition. |
| C9 | ACI definition removed. Now presented as named-but-undefined in the evidence. Added to "What the evidence does not establish." | Pack Â§3 ACI claim; absence of any ACI definition in Â§2. |
| C10 | "How it works" prefaced with a note that the ordering is this note's organisation, not a sourced sequence. Imperative build-procedure framing softened. | Pack Â§4 composition stated descriptively, not as a procedure. |
| C11 | No change. Finding was "acceptable." | â€” |
| C12 | Removed "different products for the user, not just different UIs." Reduced to the Pack's step-level vs. strategic distinction. | Pack Â§4 oversight distinction. |
| C13 | Comprehension check 3 rewritten so it no longer presupposes a debugging framework; it now asks the reader to state why the evidence does not support one. | Pack Â§4 composition; Â§6 goal-alignment uncertainty. |
| C14 | No change. Definitions and distinctions retained as written. | Pack Â§2, Â§4. |
| C15 | Retained all four Pack uncertainties and the citation limitation. Added two bullets recording the newly-identified absences (no relative cost/security comparison; no ACI definition), per C2, C6, and C9. | Pack Â§6; Â§7 evidence limitation. |
| C16 | No change. Source labels retained. | Pack Â§7 source coverage. |
| C17 | No change. Role framing retained without claiming work performed. | â€” |
| Coverage gap â€” SWE-bench | **Applied.** Adopted as the agent example, replacing expense submission. | Pack Â§5 Coding Agent example. |
| Coverage gap â€” prompt chaining, evaluator-optimizer, Computer Use examples | **Rejected as optional.** Marked optional in the critique; adding them would lengthen the note without addressing the research question. Patterns are still named in "How it works." | â€” |
| Coverage gap â€” parallelization example | **Rejected as optional.** Parallelization already appears in the fixed-vs-input-dependent distinction; the guardrail-screening illustration was not required. | â€” |
| Coverage gap â€” "Both sources provided useful and complementary information" | **Rejected.** Meta-observation about Pack assembly, not note content. The critique agreed it should not be added. | â€” |
| Coverage gap â€” confidence ratings | **Rejected as optional.** The Pack rates all five supported claims "High" with no stated basis, so surfacing the ratings would add no discriminating information. Recorded instead under Remaining Limitations. | Pack Â§3 confidence annotations. |

## Remaining Limitations

**Unresolved evidence gaps**

- No quantitative figures for the latency or cost of agentic systems, and no threshold defining "well-defined enough" for a workflow.
- No comparison of relative cost, latency, or security exposure between workflows and agents.
- No definition of the Agent-Computer Interface, only the requirement to prioritize its design.
- No account of what performs routing classification in the routing workflow.
- No claim about failure diagnosis, debugging, or where fixes belong across the four layers.
- No standardized benchmark for prompt-injection resistance or for reliability in surfacing uncertainty.
- The Pack's confidence ratings are all "High" with no stated basis for the assessments.

**Claims requiring human verification against the original sources**

- All three quotations (workflow definition, agent definition, harness definition) â€” wording, boundaries, and whether anything was elided.
- All source-label assignments in this note, since they descend from manually restored labels rather than machine-preserved citations.
- The SWE-bench coding-agent example and the routing example, including their attribution to Building Effective AI Agents.
- The four-layer composition and Plan Mode, including their attribution to Trustworthy Agents in Practice.
- Whether the sources address the questions this note records as unanswered â€” several claims were removed as *unsupported by the Pack*, not as *contradicted by the sources*. Consulting the originals could restore some of them.
- Whether the Evidence Pack omitted material relevant to the research question. This note can only reflect what the Pack captured.

**Ambiguous terminology**

- "Agent" is defined in several ways across the field, from fully autonomous systems to prescriptive workflows. The workflow/agent split used here is one usage among several.
- "Agentic systems" functions as an umbrella including workflows, which makes any claim stated about "agentic systems" ambiguous as to whether it discriminates between the two.
- "Agent-Computer Interface" is used without a definition.
- "Subagents" appears without a sourced explanation of its coordination role; the reading given is labelled an inference in the Pack.

**Lost NotebookLM citation markers**

NotebookLM displayed clickable numbered citations in its interface, but its copy-response function removed those markers. The source labels in the Evidence Pack â€” and therefore every label in this note â€” were manually restored from the visible NotebookLM response rather than carried through mechanically. Precise citation locations remain unestablished. This note has not been verified; verification against the original sources belongs to the human review gate.
