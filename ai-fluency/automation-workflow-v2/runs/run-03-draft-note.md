I'll check the project context so the "Why it matters for my work" section isn't generic.# Human Approval Gates

*Stage: Structured synthesis · Sources: `run-03-evidence-pack.md` only*

Notation used throughout: **[S]** = stated in the Evidence Pack · **[I]** = my inference from Pack material, not stated there.

---

## Short answer

**[S]** A tool-using system should stop for human approval during **sensitive operations**, and the stated rationale is trust, safety, and security. The gate is meaningful when three things hold: the interface makes clear which tools are exposed to the model, a visual indicator appears when a tool is invoked, and the specific **tool inputs are shown to the user before the server is called**. The purpose of that pre-call disclosure is to prevent accidental or malicious **data exfiltration**, and the human must retain the ability to **deny** the invocation.

**[S]** The requirement level is **SHOULD**, not MUST. The Pack flags this explicitly: human-in-the-loop gates and confirmation prompts are strongly recommended, while input validation is expressed as a MUST.

**[I]** So the honest one-line answer is narrower than it first appears: the Pack establishes *what a gate must display* far more firmly than *when it must fire*. The trigger condition ("sensitive operations") is named but never defined.

---

## Core concepts

| Term | Pack's rendering | Marked as |
|---|---|---|
| **Human in the loop** | A trust/safety/security model in which a person retains the ability to "deny tool invocations" | Paraphrase **[S]** |
| **Model-controlled** | The model discovers and invokes tools from its own "contextual understanding" plus user prompts | Quotation **[S]** |
| **Tools** | Server-exposed functionality that "enable models to interact with external systems" (APIs, databases) | Quotation **[S]** |
| **Sensitive operations** | Tool actions requiring a "confirmation prompt" | Paraphrase **[S]** |

**[S]** A load-bearing distinction sits underneath all four: tools are *model-controlled*, but the protocol "does not mandate any specific user interaction model." Control over invocation and control over approval are separate questions.

**[I]** "Model-controlled" therefore does not mean "unsupervised." It specifies who selects and calls the tool, not who authorises it. Nothing in the Pack licenses reading model-control as the absence of a gate.

---

## How it works

**[S]** The Pack states four client obligations:

1. Provide UI making clear which tools are exposed to the AI model.
2. Insert visual indicators when tools are invoked.
3. Show tool inputs to the user **before calling the server**.
4. Validate tool results **before passing to LLM**.

**[I]** Ordering these into a lifecycle is my reconstruction — the Pack presents them as a list of requirements, not as a sequence:

```
model selects tool (model-controlled)
  → [1] user can already see this tool is exposed
  → [2] visual indicator fires on invocation
  → [3] inputs rendered — HUMAN GATE — deny is possible here
  → server call
  → [4] client validates results — NOT a human gate
  → results reach the LLM
```

**[S]** Step 4 is a *client-side* check, not a human one. The Pack lists it among the supported claims but never places a person at that point.

**[S]** Two further structural distinctions bear on what a gate can show:

- **Result shape** — tool results separate `structuredContent` (server-produced JSON) from `content` (unstructured text, images, audio).
- **Error classes** — protocol/JSON-RPC errors (e.g. unknown tools) are distinguished from tool execution errors (e.g. API failures).
- **Server trust** — clients are instructed to treat tool annotations as **untrusted** unless they come from a verified trusted server.

**[I]** The trust point has a direct consequence for gate design: if annotations are untrusted by default, a gate cannot safely take a server's own word for whether its operation is sensitive. The Pack does not draw this conclusion, and does not say how verification of a trusted server is established.

---

## Concrete example

**[S]** The Pack's only worked tool example is weather retrieval: `get_weather` / `get_weather_data`, taking a location as input and returning temperature and conditions.

**[S]** Its only gate examples are generic: a confirmation prompt that asks the user to approve a "sensitive operation," and visual indicators inserted "when tools are invoked."

**[I]** Combining them — a `get_weather(location: "Ankara")` call where the client renders the argument before dispatch, giving the user a chance to notice that the location field carries more than a city name — is my construction. **The Pack never labels weather retrieval as sensitive** and never pairs its tool example with its gate examples. Treat this as illustration only.

**[S]** The Pack flags its own gap here in §5: it records "Sensitive Operation (Inference)" as an item, noting that while no sensitive operation is explicitly listed, a tool capable of data exfiltration is *inferred* to be one. That inference belongs to the Pack, not to the sources.

---

## Why it matters for my work

**[I] — This entire section is application, not evidence. The Pack says nothing about my context.**

If I am implementing an MCP client, the Pack yields four concrete build items (tool-exposure UI, invocation indicator, pre-call input rendering, result validation) and one unresolved design decision that it cannot make for me: **what counts as sensitive**. Since the trigger is undefined and the requirement level is SHOULD, I have three defensible policies — gate everything, gate by a locally-maintained allowlist, or gate on server-supplied annotation — and the Pack gives me no basis to rank them. The third is additionally suspect given the untrusted-annotation instruction.

The pre-call input rendering is the item I would treat as non-negotiable, because it is the only one that produces a *decision point*. Exposure UI and invocation indicators are disclosure; result validation is automated. Only step 3 gives a person something to deny.

---

## What the evidence does not establish

- **Every source reference in the Pack is blank.** All four supported claims in §3 carry quoted passages with empty source fields. Nothing in this note is traceable to a specific document without returning to the originals. This is the most serious defect in the chain.
- **Stray comma artefacts** throughout the Pack (`security,,` / `made,,` / `audio),`) are residue where citation markers were stripped on export. Their positions are the only surviving trace of where attributions sat.
- **"Sensitive" is undefined.** No threshold, no criteria, no enumerated list. The Pack says so itself.
- **No standard for a "meaningful" prompt.** Because the protocol "does not mandate" an interaction model, nothing establishes what a confirmation prompt must contain, how long it may persist, or whether approval can be remembered across calls.
- **SHOULD vs MUST is stated but not resolved.** The Pack infers the contrast from RFC-style keywords; it does not quote a compliance section listing which requirements are mandatory.
- **No evidence that gates work.** The exfiltration rationale is stated as design intent. Nothing in the Pack reports effectiveness, bypass rates, or user behaviour at prompts.
- **Server verification is unspecified.** Clients must treat annotations as untrusted "unless from a verified trusted server" — the Pack does not say how trust is verified.
- **Silent on:** who decides sensitivity (user config, server declaration, or model judgement), approval persistence and batching, timeouts, what happens on denial, auditing, and any performance or scale claim.
- **§7 records that the bulk of the sources contributed nothing here.** The Pack states that the majority of its sources supplied schema examples and message formats but "did not directly address the 'why' or 'when' of human approval gates." The evidence base for this research question is thinner than the Pack's length suggests.
- **All four confidence ratings are "High," with no stated basis.** They are the Pack's self-assessment.

---

## Comprehension checks

1. A colleague proposes gating on a `sensitive: true` annotation supplied by the server. Using only the Pack's trust distinction, explain the problem — then state precisely what the Pack does *not* tell you about how to fix it.

2. Your client renders a confirmation prompt showing the tool name but not its arguments. Argue from the Pack that this fails the stated requirement, and identify which specific harm the missing element was meant to prevent. Then explain why the Pack cannot tell you whether showing arguments actually prevents it.

3. The Pack lists "validate tool results before passing to LLM" among its human-in-the-loop claims. Explain why treating this as a *human* gate misreads the evidence, and say what the Pack establishes about who or what performs that check.

4. Given that the Pack's trigger condition is undefined and its requirement level is SHOULD, construct the strongest case that a compliant implementation could ship with **no** approval gate at all — then state which single sentence in the Pack most resists that reading.