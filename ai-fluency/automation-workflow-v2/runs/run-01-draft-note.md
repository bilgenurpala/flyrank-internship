# Workflow vs Agent

## Short answer

The distinction is architectural control. In a workflow, LLMs and tools are orchestrated through predefined code paths; in an agent, LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks (Building Effective AI Agents). Workflows suit well-defined tasks where predictability and consistency matter, while agents suit open-ended problems whose required steps cannot be predicted or hardcoded. Both sit under the broader category of agentic systems. Neither is free: agentic systems typically trade latency and cost for better task performance (Building Effective AI Agents), and agent autonomy adds risk of unintended consequences.

## Core concepts

**Agentic systems** is the umbrella term covering both prescriptive implementations (workflows) and autonomous ones (agents).

**Workflow** — a system in which the sequence of LLM calls and tool invocations is fixed in code ahead of time. The code decides what happens next.

**Agent** — a system in which the model decides what happens next. It runs a **self-directed loop**: plan, act, observe results, adjust, and continue until the task is complete or human input is required (Trustworthy Agents in Practice).

**An agent is not just a model.** It is composed of four layers: the model, the **harness** (the instructions, and the guardrails, that the model operates under), the tools, and the environment (Trustworthy Agents in Practice).

**Agent-Computer Interface (ACI)** — the design surface between the agent and its tools. Building effective agents means prioritizing simplicity, transparency, and thorough tool documentation at this interface (Building Effective AI Agents).

**Plan Mode** — an oversight pattern where the agent shows an intended plan of action up-front for review, rather than asking for approval at each individual step (Trustworthy Agents in Practice).

Two distinctions worth holding separately:

- *Fixed vs. input-dependent subtasks.* In parallelization workflows the subtasks are predefined. In orchestrator-worker workflows the orchestrator determines the subtasks dynamically from the specific input.
- *Step-level vs. strategic oversight.* Standard interfaces gate each action; Plan Mode moves the checkpoint up to the overall strategy.

## How it works

1. **Characterize the task.** If the steps can be enumerated in advance, a workflow is available to you. If they cannot be predicted or hardcoded, you are in agent territory.
2. **For a workflow: fix the path in code.** Choose a pattern — prompt chaining, routing, parallelization, evaluator-optimizer — and encode the transitions. Control stays with the code.
3. **For an agent: define the four layers.** Select the model, write the harness (instructions and guardrails), specify and document the tools, and establish the environment.
4. **Let the agent run its loop.** It plans, acts, observes the result, adjusts, and repeats until the task is done or it needs human input.
5. **Place oversight deliberately.** Either approve individual actions, or use Plan Mode to review the strategy up-front.
6. **Accept the trade.** Expect higher latency and cost, and, for agents specifically, exposure to misread intent and prompt injection (Trustworthy Agents in Practice).

## Concrete example

Two contrasting source-backed cases:

**Workflow — routing.** General customer-service questions go to smaller models; complex technical queries go to more capable models (Building Effective AI Agents). The routing rule is fixed; the model does not choose its own destination.

**Agent — expense submission.** Given a receipt, the agent plans its own steps: transcribe the receipt, extract the data, and check company policy when a charge exceeds a nightly cap (Trustworthy Agents in Practice). The policy check is conditional on what the extraction turns up, so the step sequence is determined at runtime rather than written in advance.

The Evidence Pack also lists **subagents** — multiple "Claudes" working in parallel on different parts of a complex task. The pack labels the reading that this represents a coordination pattern for scaling agentic work as an **inference**, not a sourced claim, so treat it as such.

## Why it matters for my work

For a backend AI engineering intern, this is primarily a design-time decision that changes what you build and what you have to guard against.

- **It sets the default.** Workflows offer higher predictability and consistency for well-defined tasks; agents are the better option when flexibility and model-driven decision-making are required at scale (Building Effective AI Agents). Reaching for an agent on a task with enumerable steps buys autonomy you did not need and pays for it in latency and cost.
- **Tool documentation becomes engineering work, not an afterthought.** Simplicity, transparency, and thorough tool documentation through the Agent-Computer Interface are named as requirements for effective agents (Building Effective AI Agents). For a backend engineer, that means the shape of a tool's interface and its docstring are part of the deliverable.
- **The threat model changes.** Agent autonomy introduces misreading user intent and vulnerability to prompt injection (Trustworthy Agents in Practice). A predefined path does not have the same surface.
- **Oversight is a design parameter.** Step-level approval and Plan Mode are different products for the user, not just different UIs.
- **The four-layer composition tells you where to intervene.** When an agent behaves badly, the fix may live in the harness, the tools, or the environment rather than the model.

## What the evidence does not establish

- **Terminology is unsettled.** "Agent" is defined in several ways across the field, ranging from fully autonomous systems to prescriptive workflows — so the clean split above is not universally shared vocabulary.
- **No standardized benchmarks.** There is no rigorous industry-wide method for comparing resistance to prompt injection or reliability in surfacing uncertainty. Comparative claims about which system is *safer* are therefore not backed here.
- **Security is not solved.** Combined defenses — training, monitoring, red-teaming — are not a guarantee against prompt injection.
- **Goal alignment is open.** Balancing excessive clarification against risky assumptions remains unsolved.
- **No quantities.** The pack gives no figures for how much latency or cost agentic systems add, and no thresholds for when a task is "well-defined enough" for a workflow.
- **Citation precision is unverified.** NotebookLM's clickable numbered citations were stripped by its copy function; source labels were manually restored from the visible response. Precise citation locations still require human verification against the original sources — so every label above should be re-checked before the note is cited elsewhere.

## Comprehension checks

1. A teammate proposes an agent for a pipeline whose five steps are identical on every run. Using the predictability/flexibility trade-off, argue whether the agent is justified — and name specifically what is being paid for the autonomy.
2. Parallelization and orchestrator-worker both split a task into subtasks, yet the Evidence Pack treats the difference as significant. Explain what changes about *who decides* the subtasks, and why that shifts where a failure would originate.
3. An agent with file and network tools misreads a user's intent and takes a damaging action. Using the four-layer composition (model, harness, tools, environment), explain which layers you would examine and what a fix at each layer would look like — then state why the Evidence Pack cannot tell you whether your fix worked better than an alternative.
