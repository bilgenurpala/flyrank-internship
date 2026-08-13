# Final Study Note

# Context Engineering for Tool-Using Systems

## Short answer

Prompt engineering is the discrete task of writing and organizing instructions — often system prompts — to guide model behavior, while context engineering is the broader, iterative process of curating the whole set of tokens passed to the model at each turn. The Evidence Pack defines context as "the set of tokens included when sampling from a large-language model (LLM)" and context engineering as strategies for "curating and maintaining the optimal set of tokens" during inference [Effective context engineering for AI agents]. A tool-using system must manage an attention budget spread across system instructions, tool specifications, environmental feedback such as tool results, and dynamically retrieved external data. The pack frames the difference as one of focus: prompting is about "finding the right words," while context engineering is about the broader "configuration of context."

**Note on attribution.** The Evidence Pack's Supported Claims section leaves every per-claim source field blank. Four claims are used throughout this note — that context is a finite resource with diminishing marginal returns; that tool definitions deserve as much prompt engineering attention as overall prompts; that models perform better when each consideration is handled by a separate LLM call; and that just-in-time context loading via lightweight identifiers is more efficient than loading full data objects. All four carry supporting passages in the pack, but the pack does not attribute any of them to a specific source, and its Source Coverage section credits several sources jointly to the same sections. These four claims are therefore cited below as **[Supported Claim, source unattributed in pack]** rather than assigned to a named source.

## Core concepts

**Context** — the set of tokens included when sampling from an LLM [Effective context engineering for AI agents]. Not just the prompt: instructions, tool definitions, external data, and message history all consume the same space.

**Prompt engineering vs. context engineering** — prompting focuses on "finding the right words"; context engineering focuses on the broader "configuration of context." Prompting is a *discrete* task; context engineering is *iterative*, recurring each time a decision is made about what to pass to the model.

**Attention budget** — LLMs draw on an attention budget when parsing large volumes of context, so context "must be treated as a finite resource with diminishing marginal returns" [Supported Claim, source unattributed in pack].

**Context rot** — the pack reports this as a phenomenon in which a model's ability to accurately recall information decreases as the token count in the context window increases. The pack does not identify a token count at which this begins for any particular model, and does not establish it as a measured causal mechanism.

**Compaction** — summarizing a conversation nearing the context window limit and reinitiating a new window with only that summary and critical details.

**Structured note-taking** — recording information outside the immediate conversational flow to carry it across a long horizon; see the Claude plays Pokémon example below.

**MCP host / MCP server** — a host is "the AI application that coordinates and manages one or multiple MCP clients"; a server is "a program that provides context to MCP clients" [Architecture overview - Model Context Protocol]. Local servers use STDIO transport for processes on the same machine; remote servers use Streamable HTTP transport across a network.

**Workflows vs. agents** — workflows orchestrate LLMs through "predefined code paths," whereas agents are systems where LLMs "dynamically direct their own processes and tool usage."

**Upfront retrieval vs. runtime exploration** — the pack identifies a trade-off in which runtime exploration is slower and upfront retrieval is faster. It records this as a separate item from the workflows/agents distinction, and offers no formula for choosing between them.

## How it works

**Organization note:** the Evidence Pack contains no process, pipeline, or prescribed ordering. What follows is my grouping of the pack's supported practices; the arrangement is not drawn from the sources.

- **Instruction altitude.** The pack describes the "right altitude" for prompts as a balance between "brittle" and "vague" guidance, but places this under its own Uncertainties and calls it a subjective "Goldilocks zone." It supplies no method for locating that balance.
- **Tool definition.** "Tool definitions and specifications should be given just as much prompt engineering attention as your overall prompts" [Supported Claim, source unattributed in pack].
- **Just-in-time data loading.** Passing lightweight identifiers such as file paths rather than full data objects lets the model "write targeted queries... without ever loading the full data objects into context," which "keeps the agent focused on relevant subsets" [Supported Claim, source unattributed in pack].
- **Separating compound tasks.** "LLMs generally perform better when each consideration is handled by a separate LLM call, allowing focused attention on each specific aspect" [Supported Claim, source unattributed in pack]. The pack labels this claim *parallelization*, but the supporting passage establishes only that the calls are **separate** — it does not state that they run concurrently.
- **Long-horizon context management.** Compaction and structured note-taking are the two practices the pack describes for work that outruns a single context window. The pack does not state that either prevents recall degradation, and reports no effectiveness results for either.
- **Environmental feedback as context.** Tool results are part of the token set the system must manage, alongside system instructions, tool specifications, and dynamically retrieved external data.

## Concrete example

**Claude Code hybrid model.** Claude Code naively loads `CLAUDE.md` files, while using tools such as `grep` and `glob` to retrieve other files just-in-time. The pack presents this as a hybrid of the two loading approaches; it does not describe the size, relevance, or persistence of the naively loaded files.

**Tool discovery — weather_current.** In the pack's weather_current example, a server provides a "name," a "description," and an "inputSchema" (such as city and units) to a client. This is a single illustrated case, not a stated general rule about every tool.

**One host, multiple servers — Visual Studio Code.** Visual Studio Code acts as an MCP host managing multiple clients, such as a Sentry server and a local filesystem server. This is the pack's concrete instance of one host coordinating more than one server.

**Long-horizon note-taking — Claude plays Pokémon.** An agent that uses structured note-taking to track precise game steps and combat strategies over thousands of turns.

**Tool interface fix — absolute filepaths.** Changing relative paths to absolute paths solved a model failure mode during code editing. The fix was in the tool specification, not the prompt text.

**Inference (labeled):** taken together, the Claude Code and absolute-filepath examples suggest that debugging a tool-using system should begin by inspecting what is in the window and how tools are described, before rewriting instruction text. The Evidence Pack does not recommend this ordering; it is my extrapolation.

## Why it matters for my work

For a backend AI engineering intern, the practical consequence is where effort gets spent when a tool-using service misbehaves. Tool schemas are part of the model-facing surface, and the pack supports giving them as much prompt engineering attention as overall prompts [Supported Claim, source unattributed in pack] — with the weather_current example showing name, description, and inputSchema as the fields a server exposes to a client. Retrieval design is a context decision, since passing identifiers rather than full payloads is what keeps the model working on relevant subsets [Supported Claim, source unattributed in pack]. Where a request bundles several independent considerations, handling each in a separate LLM call is a design option with stated support in the pack [Supported Claim, source unattributed in pack]. For sessions that outrun a context window, compaction and structured note-taking are the long-horizon management practices the pack describes, without any efficacy claim attached. The workflows/agents distinction — predefined code paths versus dynamic self-direction — bears on how much of the context is fixed in advance; the pack draws the distinction but assigns it no priority relative to other design choices.

## What the evidence does not establish

- **No token thresholds.** The pack states that context is finite, but gives no token count at which rot or pollution definitively begins for any particular model.
- **Altitude is subjective.** The "right altitude" for prompts is a balance between brittle and vague, acknowledged as a "Goldilocks zone" rather than a measurable target.
- **MCP does not govern usage.** The protocol defines how context is exchanged; it does not dictate *how* an AI application should use the context it provides.
- **No autonomy formula.** The trade-off between runtime exploration (slower) and upfront retrieval (faster) is identified, but no method is offered for setting the "right level of autonomy" beyond the general advice to "do the simplest thing that works."
- **Attribution gap within the pack.** Every entry in the pack's Supported Claims section has an empty source field. The four claims used in this note cannot be assigned to individual sources from the pack alone.
- **No effectiveness evidence.** The pack contains no benchmarks, evaluation results, or comparative measurements for any practice it describes, including compaction, note-taking, just-in-time loading, and separate calls.
- **No return-value or testing guidance.** The pack describes what a server exposes for tool discovery, but says nothing about what tools return or how tool interfaces should be tested.

## Comprehension checks

1. A teammate reports that their agent handles the first twenty tool calls well and then starts contradicting decisions it made earlier. Using the pack's account of the attention budget and its report of context rot, explain what the pack would and would not let you conclude about the cause — and identify what evidence you would need that the pack does not supply.

2. Given a service that must classify an incoming ticket, extract structured fields from it, and draft a reply, argue for or against handling all three in a single LLM call. Ground your argument in the separate-calls claim and the finite-context claim, and state whether "parallelization" as the pack labels it commits you to running the calls concurrently.

3. You are exposing a database to an agent through an MCP server. Using the weather_current example and the tool-definition claim, explain what the just-in-time principle implies about the inputSchema you would write. Then state plainly what the Evidence Pack does **not** let you conclude here: it contains nothing about tool return values and nothing about how tool interfaces should be tested, so any answer covering those is outside the evidence.

## Change Log

| Critique ID | Action taken | Evidence used |
|---|---|---|
| A1 | Removed all per-claim source labels from the four Supported Claims. Added an explicit attribution note after the Short answer, and replaced the labels with `[Supported Claim, source unattributed in pack]` at every use. Did not reconstruct citations from Source Coverage. | Evidence Pack §3, where each entry reads `**Source**:.` with an empty field; §7 credits multiple sources jointly to sections 3 and 4. |
| A2 | Retained and expanded the attribution-gap bullet in "What the evidence does not establish"; the substantive fix now appears at first use rather than only at the end. | Same as A1. |
| A3 | Deleted "architectural decision rather than a wording decision." Short answer now closes on the pack's own contrast: "finding the right words" vs. "configuration of context." | Evidence Pack §4, Prompting vs. Context Engineering focus. |
| A4 | Removed "small," "always-relevant," and "paid for permanently." The Claude Code entry now states only that `CLAUDE.md` files are loaded naively while other files are retrieved just-in-time via `grep` and `glob`, and notes the pack says nothing about size, relevance, or persistence. | Evidence Pack §5, Claude Code. |
| A5 | Attributed name, description, and inputSchema to the weather_current example and marked it as a single illustrated case rather than a general rule. | Evidence Pack §5, Weather_current Tool. |
| A6 | Added a note that the pack labels the claim "parallelization" while its supporting passage establishes separation, not concurrency. Carried the same qualification into comprehension check 2. | Evidence Pack §3, separate-LLM-call claim heading vs. its supporting passage. |
| A7 | Rewrote the context rot entry as a reported phenomenon with no model-specific threshold and no established causal mechanism. Removed the framing in which degradation triggers compaction. | Evidence Pack §2 (definition, marked Paraphrase); §6, Quantifying "Finite". |
| A8 | Replaced the six numbered steps with an unordered bulleted set of supported practices, prefaced by an explicit note that the ordering was the writer's and that the pack contains no process. | Evidence Pack contains no §presenting a sequence; §§1–7 are definitions, claims, distinctions, examples, uncertainties, coverage. |
| A9 | Moved the "Goldilocks zone" and subjectivity qualifiers to the point where instruction altitude is discussed, and noted the pack files it under Uncertainties. | Evidence Pack §6, Optimal Altitude. |
| A10 | Restated compaction and note-taking as long-horizon context-management practices. Removed "keeps recall from degrading." Removed "any long-running session." | Evidence Pack §2 (Compaction); §5 (Claude plays Pokémon); no efficacy statement appears anywhere in the pack. |
| A11 | Removed the "any long-running session" generalization. | Same as A10. |
| A12 | Separated the workflows/agents distinction from the upfront/runtime trade-off into two Core concepts entries, with no causal statement linking them. | Evidence Pack §4 (Workflows vs. Agents); §6 (Decision Boundaries). |
| A13 | Removed "first architectural fork." The distinction is now stated with an explicit note that the pack assigns it no priority. | Evidence Pack §4; no ordering or ranking appears in the pack. |
| A14 | Rewrote comprehension check 1 to remove the reference to the six steps and to ask what the pack does and does not license as a conclusion, rather than asking for a diagnosis. | Evidence Pack §6, Quantifying "Finite". |
| A15 | Narrowed comprehension check 3 to inputSchema and the tool-definition claim, and stated in the question itself that return values and testing are outside the evidence. Added a matching bullet to "What the evidence does not establish." | Evidence Pack §5 (Weather_current); §3 (tool definitions claim); §5 (Absolute Filepaths, which reports an outcome but no testing method). |
| Coverage — VS Code | Added Visual Studio Code as the pack's concrete case of one MCP host coordinating multiple clients (Sentry server, local filesystem server). | Evidence Pack §5, Visual Studio Code. |
| Coverage — Pokémon | Added Claude plays Pokémon as the source-backed case for structured note-taking over thousands of turns, and added a Core concepts entry for the practice. | Evidence Pack §5, Claude plays Pokémon. |
| Coverage — weather_current | Added as a Concrete example rather than leaving the detail floating in the practices section. | Evidence Pack §5. |
| Coverage — confidence ratings | **Rejected.** The critique suggested surfacing the pack's "Confidence: High" markings. Not applied: the pack gives no basis for those ratings, and reporting them alongside claims whose sources are blank would supply an appearance of precision the pack cannot support. The instruction for this stage also forbids adding confidence the pack cannot support. | Evidence Pack §3 confidence fields; stage instruction. |
| Coverage — Quotation/Paraphrase markers | **Rejected as a required change.** The critique itself marked this optional and not a defect. The distinction is honored in practice; surfacing the markers would add apparatus without changing any claim. | Evidence Pack §2 labels. |
| Coverage — "All sources provided relevant material" | **Rejected.** The critique recommended against adding it; it carries no content bearing on the research question. | Evidence Pack §7. |
| Uncertainty preservation | All four of the pack's original uncertainties retained verbatim in substance; two further limitations added (no effectiveness evidence, no return-value or testing guidance), both statements about what the pack lacks rather than new facts. | Evidence Pack §6; absence of benchmark or return-value content anywhere in the pack. |

## Remaining Limitations

**Unresolved within the Evidence Pack**

- The four Supported Claims remain unattributed. This note now flags that rather than guessing, but the underlying gap is unfixable from the pack — Source Coverage credits multiple sources to the same sections, so no per-claim assignment can be derived.
- Whether "parallelization" in the pack's claim heading was the source's own term or the pack author's label is unknown. The note reports the mismatch between heading and passage without resolving it.
- The pack gives no scope conditions for the just-in-time claim, the separate-calls claim, or compaction. Where each applies, and where it stops applying, is not established.
- Context rot's mechanism, magnitude, and onset are all unspecified. The note treats it as reported rather than demonstrated, which is the most the pack supports.

**Requires human verification against original sources**

- Whether the four claims belong to the sources a reader might assume. The note declines to assign them; a reviewer with the sources should assign them.
- Whether the pack's quotations are accurate and complete. The finite-resource and just-in-time passages both contain ellipses that this note reproduces without knowing what was elided.
- Whether the paraphrased definitions — context rot, compaction, prompt engineering — represent the sources faithfully. The A7 and A10 revisions rest entirely on the pack's wording.
- Whether the pack's stated uncertainties are the sources' actual silences or the pack author's reading. If a source does specify a threshold or an autonomy heuristic, this note's preserved uncertainties would be wrong in a direction not detectable from the pack.
- Whether the sources describe a process that the pack simply did not record. The "How it works" section is labeled as the writer's synthesis on the basis that the pack contains no sequence; this does not rule out one existing upstream.

**Ambiguous points carried forward**

- The weather_current example is generalized nowhere in the note, but a reader may still read it as describing MCP tool discovery generally. Whether that generalization holds is not settled by the pack.
- The labeled inference in the Concrete example section (debug context and tool descriptions before instruction text) is my extrapolation and remains unverified.
- The Claude Code hybrid model is described without any account of why `CLAUDE.md` in particular is loaded naively. The pack states the behavior, not the rationale.

This note has not been verified. Verification against the original sources belongs to the human review gate.