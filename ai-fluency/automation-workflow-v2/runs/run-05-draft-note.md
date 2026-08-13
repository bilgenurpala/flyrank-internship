# Context Engineering for Tool-Using Systems

## Short answer
Prompt engineering is the discrete task of writing and organizing instructions — often system prompts — to guide model behavior, while context engineering is the broader, iterative process of curating the whole set of tokens passed to the model at each turn [Effective context engineering for AI agents]. Context is defined as "the set of tokens included when sampling from a large-language model (LLM)," and context engineering as strategies for "curating and maintaining the optimal set of tokens" during inference [Effective context engineering for AI agents]. A tool-using system must manage an attention budget spread across system instructions, tool specifications, environmental feedback such as tool results, and dynamically retrieved external data. Because context is a finite resource with diminishing marginal returns, what gets included — and what gets left out or summarized — becomes an architectural decision rather than a wording decision [Effective context engineering for AI agents].

## Core concepts

**Context** — the set of tokens included when sampling from an LLM [Effective context engineering for AI agents]. Not just the prompt: instructions, tool definitions, external data, and message history all consume the same space.

**Prompt engineering vs. context engineering** — prompting focuses on "finding the right words"; context engineering focuses on the broader "configuration of context" [Effective context engineering for AI agents]. Prompting is a *discrete* task; context engineering is *iterative*, recurring every time a decision is made about what to pass to the model [Effective context engineering for AI agents].

**Attention budget** — LLMs draw on a limited attention budget when parsing large volumes of context, so context "must be treated as a finite resource with diminishing marginal returns" [Effective context engineering for AI agents].

**Context rot** — the phenomenon where a model's ability to accurately recall information degrades as the token count in the window grows [Effective context engineering for AI agents].

**Compaction** — summarizing a conversation that is nearing the context window limit, then reinitiating a new window containing only that summary plus critical details [Effective context engineering for AI agents].

**MCP host / MCP server** — a host is "the AI application that coordinates and manages one or multiple MCP clients"; a server is "a program that provides context to MCP clients" [Architecture overview - Model Context Protocol]. Local servers communicate over STDIO transport for processes on the same machine; remote servers use Streamable HTTP transport across a network [Architecture overview - Model Context Protocol].

**Workflows vs. agents** — workflows orchestrate LLMs through "predefined code paths," whereas agents are systems where LLMs "dynamically direct their own processes and tool usage" [Building Effective AI Agents]. This distinction determines how much of the context is decided in advance versus at runtime.

## How it works

Sequence matters here, because each step consumes budget that the later steps still need.

1. **Establish the standing context.** System instructions are written at the right altitude — specific enough not to be vague, general enough not to be brittle [Effective context engineering for AI agents].
2. **Define the tools.** Tool definitions and specifications "should be given just as much prompt engineering attention as your overall prompts" [Building Effective AI Agents]. The server exposes each tool with a name, a description, and an inputSchema, which the client discovers [Architecture overview - Model Context Protocol].
3. **Decide what data enters context and when.** Just-in-time loading passes lightweight identifiers such as file paths rather than full data objects, so "the model can write targeted queries... without ever loading the full data objects into context" [Effective context engineering for AI agents].
4. **Run the turn and absorb environmental feedback.** Tool results return into the same window, so every call both informs the model and spends its budget.
5. **Split where the task is compound.** "LLMs generally perform better when each consideration is handled by a separate LLM call, allowing focused attention on each specific aspect" [Building Effective AI Agents].
6. **Manage the long horizon.** As the window fills and recall degrades, apply compaction or structured note-taking to carry forward only what remains load-bearing [Effective context engineering for AI agents].

## Concrete example

Claude Code uses a **hybrid model**: it naively loads `CLAUDE.md` files into context up front, while retrieving other files just-in-time through tools such as `grep` and `glob` [Effective context engineering for AI agents]. This shows steps 3 and 6 operating together — a small, always-relevant core is paid for permanently, and the much larger repository is reached through identifiers instead of contents.

A second, narrower example: changing relative file paths to absolute paths in a tool's interface resolved a model failure mode during code editing [Building Effective AI Agents]. The fix was in the tool specification, not the prompt.

**Inference (labeled):** these two together suggest that debugging a tool-using system should begin by inspecting what is in the window and how tools are described, before rewriting instruction text. The Evidence Pack does not state this ordering as a recommendation; it is my extrapolation from the two examples above.

## Why it matters for my work

For a backend AI engineering intern, the practical consequence is where effort gets spent when a tool-using service misbehaves. Tool schemas — names, descriptions, and inputSchema fields — are part of the model-facing surface and would deserve the same review as prompt text [Building Effective AI Agents] [Architecture overview - Model Context Protocol]. Retrieval design becomes a context decision, since returning identifiers rather than full payloads is what keeps the window focused [Effective context engineering for AI agents]. Where a request bundles several independent considerations, splitting it across separate LLM calls is a design option with stated support [Building Effective AI Agents]. And on any long-running session, compaction or note-taking is the mechanism that keeps recall from degrading as tokens accumulate [Effective context engineering for AI agents]. Choosing between a workflow and an agent — predefined code paths versus dynamic self-direction — is the first architectural fork, since it fixes how much of the context is determined at build time [Building Effective AI Agents].

## What the evidence does not establish

- **No token thresholds.** The sources state that context is finite, but give no specific token counts at which rot or pollution definitively begins for any particular model.
- **Altitude is subjective.** The "right altitude" for prompts is described as a balance between brittle and vague, and is acknowledged as a "Goldilocks zone" rather than a measurable target.
- **MCP does not govern usage.** The protocol defines how context is exchanged; it does not dictate *how* an AI application should use the context it provides [Architecture overview - Model Context Protocol].
- **No autonomy formula.** The trade-off between runtime exploration (slower) and upfront retrieval (faster) is identified, but no method is offered for setting the "right level of autonomy" beyond the general advice to "do the simplest thing that works."
- **Attribution gap within the pack.** The Supported Claims section of the Evidence Pack leaves its per-claim Source fields blank; the source labels used above for those four claims are drawn from the Source Coverage section, not from the claim entries themselves.
- **Coverage limits.** Three sources contributed; no evaluation results, benchmarks, or comparative measurements appear anywhere in the pack.

## Comprehension checks

1. A teammate reports that their agent handles the first twenty tool calls well and then starts contradicting decisions it made earlier. Using the concepts of attention budget, context rot, and compaction, explain what is likely happening and which of the six steps above you would change first — and say what evidence you would need that the pack does not supply.

2. Given a service that must classify an incoming ticket, extract structured fields from it, and draft a reply, argue for or against handling all three in a single LLM call. Ground your argument in the parallelization claim and in the finite-context claim, and identify which one does more work in your answer.

3. You are exposing a database to an agent through an MCP server. Explain how the just-in-time principle would shape the inputSchema and return value of your tools, and then explain what the absolute-filepath example implies about how you would test those tools — noting where you are extending the sources rather than applying them.