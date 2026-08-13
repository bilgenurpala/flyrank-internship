# Notes — "Building Effective Agents" (Anthropic, Dec 2024)

*Reading notes, ~20 min*

---

## Core claim

Across dozens of teams, the implementations that actually worked did **not** use complex frameworks or specialized libraries. They used simple, composable patterns. Add complexity only when it demonstrably improves outcomes.

## Workflow vs. agent

Anthropic calls everything here "agentic systems" but draws one architectural line:

- **Workflow** — LLMs and tools orchestrated through *predefined code paths*. Predictable, consistent, good for well-defined tasks.
- **Agent** — the LLM *dynamically directs its own process and tool usage*, keeping control over how it gets the task done. Better when flexibility and model-driven decisions are needed at scale.

Important caveat: for many applications neither is needed. A single LLM call, optimized with retrieval and in-context examples, is usually enough. Agentic systems trade latency and cost for task performance — decide if that trade is worth it.

## On frameworks

Mentioned: Claude Agent SDK, AWS Strands Agents SDK, Rivet (drag-and-drop GUI), Vellum.

They simplify the boring parts (calling LLMs, defining/parsing tools, chaining calls) but add abstraction layers that hide the actual prompts and responses → harder to debug, and tempting to over-engineer.

**Advice:** start with the LLM API directly. Many patterns are a few lines of code. If you do use a framework, understand what's underneath — wrong assumptions about the internals are a common source of errors.

---

## Building block: the augmented LLM

The foundation of everything else: an LLM enhanced with **retrieval + tools + memory**. Current models can use these actively — generating their own search queries, picking the right tool, deciding what to retain.

Two things to focus on:
1. Tailor the capabilities to the specific use case
2. Give the model an easy, well-documented interface

MCP (Model Context Protocol) is offered as one way to do this — lets you plug into a growing ecosystem of third-party tools with a simple client.

Rest of the post assumes every LLM call has these augmentations available.

---

## The five workflow patterns

### 1. Prompt chaining
Break the task into a sequence of steps; each LLM call processes the previous one's output. Can add programmatic **gates** at intermediate steps to check the process is still on track.

*Use when:* the task decomposes cleanly into fixed subtasks. Trades latency for accuracy by making each individual call easier.

*Examples:* write marketing copy → translate it. Write an outline → check it against criteria → write the document.

### 2. Routing
Classify the input, send it to a specialized follow-up task. Gives separation of concerns and lets you write more specialized prompts. Without it, optimizing for one input type degrades the others.

*Use when:* there are distinct categories better handled separately, **and** classification can be done accurately (by an LLM or a classic classifier).

*Examples:* customer service triage (general / refund / technical). Routing easy questions to Haiku 4.5 and hard ones to Sonnet 4.5 for cost-performance balance.

### 3. Parallelization
Two variants:
- **Sectioning** — split into independent subtasks, run in parallel
- **Voting** — run the same task several times for diverse outputs

*Use when:* subtasks can be parallelized for speed, or multiple attempts/perspectives raise confidence. Note: for tasks with several considerations, LLMs generally do better when each consideration gets its own call.

*Examples:* guardrails (one instance answers, another screens for inappropriate content — better than one call doing both); automating evals with one call per aspect. Voting: multiple prompts reviewing code for vulnerabilities; content moderation with different vote thresholds to balance false positives/negatives.

### 4. Orchestrator-workers
A central LLM breaks the task down dynamically, delegates to worker LLMs, synthesizes the results.

*Use when:* you can't predict the subtasks in advance. Topographically similar to parallelization — the **key difference is that subtasks aren't pre-defined**, the orchestrator decides them based on the input.

*Examples:* coding products making complex changes across multiple files; search tasks pulling from many sources.

### 5. Evaluator-optimizer
One LLM generates, another evaluates and gives feedback, in a loop.

*Use when:* there are clear evaluation criteria and iterative refinement measurably helps. Two signs of good fit: (a) a human's articulated feedback would demonstrably improve the response, (b) the LLM can produce that same kind of feedback. Analogous to a writer's revision process.

*Examples:* literary translation (nuance the translator misses first pass); complex multi-round search where the evaluator decides whether to keep searching.

---

## Agents

Now viable in production because models got better at: understanding complex inputs, reasoning/planning, reliable tool use, and error recovery.

**Loop:** start from a human command or discussion → plan → act → observe → adjust → repeat. Crucially the agent must get **"ground truth" from the environment at every step** (tool results, code execution output) to assess its own progress. Can pause for human feedback at checkpoints or when blocked.

Terminates on completion, but include stopping conditions (e.g. max iterations) to stay in control.

Implementation is usually straightforward — "just LLMs using tools based on environmental feedback in a loop." Which is exactly why **toolset design and documentation matter so much**.

*Use when:* open-ended problems, unpredictable number of steps, no hardcodable path — and you can trust the model's judgment. Autonomy = higher cost + risk of compounding errors → test extensively in sandboxes with guardrails.

*Their own examples:* the SWE-bench coding agent; the "computer use" reference implementation.

---

## Three core principles for implementing agents

1. **Keep the design simple.**
2. **Prioritize transparency** — explicitly show the agent's planning steps.
3. **Carefully craft the agent-computer interface (ACI)** — thorough tool documentation and testing.

Summary line worth remembering: success isn't building the most sophisticated system, it's building the right one. Start with simple prompts, optimize with good evals, add multi-step agentic systems only when simpler things fall short.

---

## Appendix 1 — where agents pay off

Both cases share: they need conversation *and* action, have clear success criteria, allow feedback loops, and permit meaningful human oversight.

**Customer support** — conversation flow + external data/actions. Tools pull customer data, order history, KB articles; refunds and ticket updates handled programmatically; success measurable via resolution. Some companies charge only for successful resolutions — a real vote of confidence.

**Coding agents** — solutions are verifiable by automated tests, the agent can iterate using test results as feedback, the problem space is well structured, quality is objectively measurable. Anthropic's agents solve real GitHub issues in SWE-bench Verified from the PR description alone. Human review still needed for alignment with broader system requirements.

---

## Appendix 2 — prompt engineering your tools ← the most practically useful part

Tool definitions deserve **as much prompt engineering attention as the main prompt**.

There are usually several ways to specify the same action (diff vs. full file rewrite; markdown vs. JSON for structured output). These look cosmetic and convert losslessly — but some are much harder for a model to *write*. A diff requires knowing the line count for the chunk header before writing the code. JSON requires escaping newlines and quotes.

**Format rules of thumb:**
- Give the model enough tokens to think before it writes itself into a corner
- Keep the format close to what naturally occurs in internet text
- Remove formatting overhead (counting thousands of lines, string-escaping code)

**ACI design — invest as much effort here as you would in HCI:**
- Put yourself in the model's shoes. If you'd have to think hard to use the tool from its description and parameters, so will the model. Good tool definitions include example usage, edge cases, input format requirements, and clear boundaries from other tools.
- Rewrite parameter names/descriptions for obviousness — write it like a docstring for a junior dev. Matters most when you have many similar tools.
- Test empirically: run many example inputs, watch the mistakes, iterate.
- **Poka-yoke** the tools: change the arguments so mistakes become hard to make.

Concrete example: building the SWE-bench agent they spent *more time optimizing tools than the overall prompt*. The model kept messing up relative filepaths after moving out of the root directory → they changed the tool to require absolute paths → flawless use afterwards.

---

## My takeaways

- Default to the simplest thing. "Do I need an agent here or just a better single call?" is the first question, not the last.
- The five workflow patterns are a decent mental checklist to run through before reaching for full autonomy.
- Tool/ACI design is underrated leverage — worth more effort than prompt tweaking in agent systems.
- Ground truth from the environment at every step + explicit stopping conditions = the two things keeping an agent loop honest.
