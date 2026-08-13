## Final Study Note

# Human Approval Gates

*Stage: Controlled revision (Run 03) · Sources: `run-03-evidence-pack.md` only · Not verified against original documents*

Notation: **[S]** = stated in the Evidence Pack · **[I]** = my inference from Pack material, not stated there.

## Short answer

**[S] — What makes a gate meaningful.** The Pack ties meaningfulness to **two** conditions: the system gives **clear visual indication that a tool is being invoked**, and it **presents the specific tool inputs to the user before the server call is made**. The stated purpose of the pre-call disclosure is to prevent accidental or malicious **data exfiltration**. The Pack's rationale for the gate overall is trust, safety, and security.

**[S] — When to stop, stated two ways, unreconciled.** The Pack contains two scope statements and does not reconcile them:

- §1 frames the trigger narrowly: approval is required during **sensitive operations**, which are defined as tool actions requiring a "confirmation prompt."
- §3 states it broadly: there SHOULD **always** be a human in the loop with the ability to **deny tool invocations**.

A standing capability to deny every invocation and a prompt that fires on a sensitive subset are different requirements at different scopes. **This note does not resolve which the sources intend.** The Pack does not adjudicate it, and with blank source references there is no way to tell whether the two statements come from one document or from different ones.

**[S] — Requirement level, unsettled.** The passage uses **SHOULD**. Pack §6 reads this as strongly recommended but "**perhaps** not strictly mandatory," contrasting it with what it characterises as MUST requirements — but the Pack quotes no MUST passage and cites no compliance section. The hedge is the Pack's own, and it is not resolved here. **This note does not claim that a gate-free implementation would be compliant**; §3's "always" language cuts directly against that reading.

## Core concepts

| Term | Pack's rendering | Marked as |
|---|---|---|
| **Human in the loop** | A trust/safety/security model in which a person retains the ability to "deny tool invocations" | Paraphrase **[S]** |
| **Model-controlled** | The model discovers and invokes tools from its own "contextual understanding" plus user prompts | Quotation **[S]** |
| **Tools** | Server-exposed functionality that "enable models to interact with external systems" (APIs, databases) | Quotation **[S]** |
| **Sensitive operations** | Tool actions requiring a "confirmation prompt" | Paraphrase **[S]** |

**[S]** A load-bearing distinction sits underneath all four: tools are *model-controlled*, but the protocol "does not mandate any specific user interaction model." Control over invocation and control over approval are separate questions.

**[S]** A fourth term carries weight the Pack never unpacks: §1 says the mechanism allows a human to "**effectively deny requests**." Since the research question asks what makes a gate *meaningful*, the qualifier is directly on point — and the Pack gives no account of what separates effective denial from nominal denial.

**[I]** "Model-controlled" does not mean "unsupervised." It specifies who selects and calls the tool, not who authorises it. Nothing in the Pack licenses reading model-control as the absence of a gate.

## How it works

**[S]** The Pack states four client obligations, each as a separate supported claim:

1. **Tool-exposure UI** — provide UI making clear which tools are exposed to the AI model. *This is a standalone client requirement; the Pack does not tie it to what makes a gate meaningful.*
2. **Invocation indication** — insert visual indicators when tools are invoked. *Meaningfulness condition.*
3. **Pre-call input display** — show tool inputs to the user before calling the server. *Meaningfulness condition.*
4. **Result validation** — validate tool results before passing them to the LLM. *Client-side and automated. The Pack places no person at this point; it is not a human approval gate.*

**[I]** Ordering these into a lifecycle is my reconstruction — the Pack presents them as an unordered list of requirements:

```
model selects tool (model-controlled)
  → [1] tool already visible as exposed          (client requirement)
  → [2] visual indicator fires on invocation      (meaningfulness condition)
  → [3] inputs rendered before dispatch           (meaningfulness condition)
  → server call
  → [4] client validates results                  (automated, not a human gate)
  → results reach the LLM

  deny capability: position UNLOCATED by the Pack — see below
```

**[I]** The diagram deliberately does not place the deny capability. §3 pairs denial with "always," not with input display, so locating it at step 3 would be my invention rather than the Pack's claim. Where in the sequence denial is exercisable is not established.

**[I] — framing is mine.** Three further structural distinctions in the Pack bear on gate design; the Pack does not connect them to gates itself:

- **Result shape** — tool results separate `structuredContent` (server-produced JSON) from `content` (unstructured text, images, audio). This is the only Pack material about what a gate could render *back* to a user after a call, though the Pack never discusses post-call display.
- **Error classes** — protocol/JSON-RPC errors (e.g. unknown tools) are distinguished from tool execution errors (e.g. API failures). **A denied invocation is placed in neither class.** What a client returns on denial is not established.
- **Server trust** — clients are instructed to treat tool annotations as **untrusted unless they originate from a verified trusted server**. The carve-out is part of the rule. The Pack does not say how a server becomes verified, nor what annotations contain.

**[I] — unsupported possibility, flagged as such.** *If* annotations were to carry a sensitivity signal, the untrusted-by-default rule would constrain how a gate could rely on it, and the verified-trusted-server carve-out would govern when it could. **The Pack never says annotations bear on sensitivity at all.** The conditional is stated only to mark the question as open, not as a finding.

## Concrete example

**[S]** The Pack's only worked tool example is weather retrieval: `get_weather` / `get_weather_data`, taking a location as input and returning temperature and conditions.

**[S]** Its only gate examples are generic: a confirmation prompt asking a user to approve a "sensitive operation," and visual indicators inserted "when tools are invoked."

**[I] — constructed illustration, not evidence.** A `get_weather(location: "Ankara")` call whose argument is rendered before dispatch, giving the user a chance to notice that the location field carries more than a city name. **Three separate inventions here:** (a) the Pack never labels weather retrieval as sensitive; (b) the Pack never pairs its tool example with its gate examples; (c) **the exfiltration mechanism — data smuggled through an argument field — is entirely mine.** The Pack names data exfiltration as the risk but describes no mechanism by which it occurs. Use this only to picture the shape of a pre-call display.

**[S]** The Pack flags its own gap here: §5 records "Sensitive Operation (Inference)," noting that no sensitive operation is explicitly listed and that a tool capable of data exfiltration is *inferred* to be one. That inference belongs to the Pack, not to its sources.

## Why it matters for my work

**[I] — This section is application, not evidence. The Pack says nothing about my context.**

Implementing an MCP client, the Pack yields four concrete build items (§How it works) and leaves the trigger condition open. Because "sensitive" is undefined and the two scope statements point in different directions, the gating policy is a decision the Pack cannot make for me.

Options I can imagine — gate every invocation, gate against a locally-maintained list, or gate on some server-supplied signal — are illustrative only. **This is not a closed set, the Pack does not enumerate options, and it gives no basis for ranking them or for calling any of them defensible.** The third would additionally depend on the verified-trusted-server carve-out and on whether annotations carry any sensitivity signal, which the Pack does not say.

Pre-call input rendering is the item I would prioritise, because it is what turns an invocation into something a person can inspect before it leaves the client. That is a working preference, not a Pack requirement, and it does not follow from the Pack that it is the only point at which a person can intervene — §3's deny capability is not located at input display. It also sits alongside, not above, the unresolved SHOULD/MUST question.

## What the evidence does not establish

- **Every source reference in the Pack is blank.** All four supported claims in §3 carry quoted passages with empty source fields. Nothing in this note is traceable to a specific document without returning to the originals. This remains the most serious defect in the chain.
- **Stray comma artefacts** (`security,,` / `made,,` / `audio),`) are residue where citation markers were stripped on export. Their positions are the only surviving trace of where attributions sat, and they are not reliable enough to count or to attribute from.
- **"Sensitive" is undefined.** No threshold, criteria, or enumerated list. Pack §6 says so directly.
- **"Effectively deny" is undefined.** The Pack's own qualifier on denial is never unpacked — no account of timing, of what information suffices, or of what would make a denial nominal rather than effective.
- **The two scope statements are unreconciled** ("always" deny-capable vs. confirmation prompts on sensitive operations). Whether this is a genuine tension in the sources or an artefact of the Pack's assembly cannot be determined with blank references.
- **SHOULD vs MUST is unresolved.** The contrast is the Pack's inference from RFC-style keywords. No MUST passage is quoted and no compliance section is cited; the Pack's reference to input validation as a MUST is its own characterisation, not a source passage.
- **No standard for a "meaningful" prompt.** Because the protocol "does not mandate" an interaction model, nothing establishes what a confirmation prompt must contain, how long it persists, or whether approval can be remembered across calls.
- **No evidence that gates work.** The exfiltration rationale is design intent. Nothing reports effectiveness, bypass rates, or user behaviour at prompts. No exfiltration mechanism is described.
- **Server verification is unspecified**, and annotation contents are unspecified. Whether annotations bear on sensitivity is not addressed either way.
- **Denial handling is unaddressed.** Denial is placed in neither the protocol-error nor the tool-execution-error class.
- **Silent on:** who decides sensitivity, approval persistence and batching, timeouts, auditing, post-call display of results to the user, and any performance or scale claim.
- **§7 states that some sources supplied technical context, schema examples, and message formats without directly addressing the "why" or "when" of human approval gates.** How many, and how much of the evidence base that represents, is not something this note can establish.
- **All four confidence ratings are "High," with no stated basis.** They are the Pack's self-assessment.

## Comprehension checks

1. A colleague proposes gating on a signal supplied by the server itself. Using Pack §4, state the rule that governs server-supplied annotations **including its carve-out** — then identify the prior question the Pack never answers about whether annotations bear on sensitivity at all.
2. Your client renders a confirmation prompt showing the tool name but not its arguments. Argue from the Pack that this fails a stated condition of meaningfulness, name the harm the missing element was meant to prevent, and explain why the Pack cannot tell you whether showing arguments actually prevents it.
3. Pack §3 lists "validate tool results before passing to LLM" among its **supported claims**. Explain why treating this as a *human* gate misreads the evidence, and say what the Pack establishes about who or what performs the check.
4. The Pack says SHOULD, hedges that this is "perhaps not strictly mandatory," and elsewhere says there should **always** be a deny-capable human. Evaluate — do not assume — whether these together permit an implementation with no approval gate. State which specific sentence most resists that reading and what evidence would be needed to settle it.
5. Distinguish the tool-exposure UI requirement from the two meaningfulness conditions. Why does the Pack's structure support treating them differently, and what would be lost by merging them?

## Change Log

| Critique ID | Action taken | Evidence used |
|---|---|---|
| C1 | Applied. Meaningfulness reduced to two conditions (invocation indication, pre-call input display). Tool-exposure UI relocated to §How it works as a standalone client requirement and explicitly marked as not a meaningfulness condition. | Pack §1 (two conditions); §3 (exposure UI as separate supported claim). |
| C2 | Applied. Both scope statements now surfaced in §Short answer, with an explicit statement that the note does not resolve them. Added to §What the evidence does not establish. **Not adjudicated.** | Pack §1 ("sensitive operations", confirmation prompt); §3 ("always… deny tool invocations"). |
| C3 | Applied. Comprehension check 4 rewritten to ask the reader to *evaluate* whether SHOULD permits a gate-free reading, citing both §6's hedge and §3's "always." Presupposition removed. | Pack §6 ("perhaps not strictly mandatory"); §3. |
| C4 | Applied. §6's hedge now carried into §Short answer at first statement of the requirement level. | Pack §6. |
| C5 | Applied. MUST/input-validation contrast now attributed to the Pack's characterisation, with a note that no MUST passage is quoted. | Pack §6; §3 claim 4 (no keyword present). |
| C6 | Applied. The annotations-to-sensitivity link is retained only as an explicitly labelled unsupported possibility, with the imported premise named: the Pack never says annotations bear on sensitivity. | Pack §4 (annotations untrusted rule); Pack silence on annotation contents. |
| C7 | Applied. The verified-trusted-server carve-out restored wherever the trust rule appears, in §How it works and §Why it matters. Added that the Pack does not say how verification is established. | Pack §4. |
| C8 | Applied. Closed list of "three defensible policies" removed. Options now illustrative, explicitly not closed, not ranked, and not called defensible. | Pack silence — no policy options enumerated. |
| C9 | Applied. "Non-negotiable" and "the only one that produces a decision point" both removed. Preference retained as a working preference and reconciled with the unresolved SHOULD reading. | Pack §3 (deny capability not located at input display). |
| C10 | Applied. Deny capability marked UNLOCATED in the lifecycle diagram, with a note that placing it at step 3 would be invention. | Pack §3 ("always" paired with denial, not with input display). |
| C11 | Applied. Comprehension check 3 now correctly labels §3 as "Supported claims." Human/automated separation retained throughout — no substantive change, as the critique marked it acceptable. | Pack §3 claim 4 (client-side). |
| C12 | Applied. Weather example retained as constructed inference with three inventions now itemised, including the exfiltration mechanism, which is explicitly marked as mine. | Pack §5 (weather tools; confirmation prompt; data exfiltration named without mechanism). |
| C13 | Applied. Miscount corrected to three distinctions; the framing that they bear on gate design is now marked **[I]**. | Pack §4. |
| C14 | Applied. "Majority of its sources" and "thinner than the Pack's length suggests" both removed. §7 now reported without quantification, with an explicit statement that the proportion cannot be established. | Pack §7; draft's own finding that comma artefacts are unreliable. |
| C15 | No change required — marked acceptable. Retained. | Pack §3, §4, §6. |
| C16 | No change required — marked acceptable. Quotation/paraphrase markings retained as the Pack assigns them. | Pack §2. |
| C17 | No change required — marked acceptable. Retained. | Pack §5. |
| Coverage gap — structured vs. unstructured content | Added to §How it works as the only Pack material bearing on post-call display, with a note that the Pack never discusses post-call display itself. | Pack §4. |
| Coverage gap — protocol vs. tool execution errors | Added, with the finding that denial falls in neither class and that denial handling is therefore unaddressed. Also added to §What the evidence does not establish. | Pack §4. |
| Coverage gap — "effectively deny requests" | Added to §Core concepts as an unresolved term bearing directly on meaningfulness, and to §What the evidence does not establish. | Pack §1. |
| Coverage gap — Tools definition | Not added as a separate point. The definition remains in the concepts table; the Pack does not connect it to exfiltration stakes, and drawing that connection would be unsupported. | Pack §2. |
| Coverage gap — confidence ratings | No change. Already surfaced in §What the evidence does not establish; critique marked handling adequate. | Pack §3. |

## Remaining Limitations

**Unresolved evidence gaps**

- The **two scope statements remain in conflict** and are not resolved by this note. Whether the Pack recorded a genuine tension in the sources or introduced one during synthesis cannot be determined from the Pack alone. This is the largest unresolved item in the chain, and it determines whether the correct fix was "surface a conflict" or "surface an assembly error."
- **"Sensitive" has no definition**, so the trigger condition for a gate is not operational.
- **"Effectively deny" has no definition**, so the meaningfulness standard is incomplete even where the Pack states conditions.
- **SHOULD vs MUST is unsettled**, resting entirely on the Pack's inference from keywords with no compliance section quoted.
- **Denial handling, approval persistence, timeouts, batching, auditing, and post-call display** are all absent.
- **No effectiveness evidence** of any kind for approval gates; the exfiltration rationale is design intent with no described mechanism.
- **Server verification and annotation contents** are both unspecified.

**Claims requiring human verification against the original sources**

- Every quoted passage in §3 of the Pack, all of which carry **blank source references**.
- Whether SHOULD and MUST appear in the originals with RFC 2119 force.
- Whether the "always deny-capable" and "sensitive operations" statements come from the same document, and at what protocol version.
- Whether "input validation" is in fact a MUST requirement, which the Pack asserts but never quotes.
- Whether the four "High" confidence ratings are warranted; no basis is stated.
- Whether the Pack omitted source material relevant to this research question. Coverage assessments in this chain compare draft to Pack, never draft to sources.

**Ambiguous terminology**

- *Sensitive operation* — trigger, undefined.
- *Effectively deny* — meaningfulness qualifier, undefined.
- *Verified trusted server* — verification procedure unstated.
- *Tool annotations* — contents unstated; relation to sensitivity unaddressed either way.
- *Meaningful* (of a confirmation prompt) — no standard, since the protocol mandates no interaction model.

**Lost NotebookLM citation markers**

The Pack's citation markers were stripped on export, leaving comma artefacts as the only trace of where attributions sat. Their positions are not reliable enough to count, attribute from, or use to reconstruct source boundaries — including quotation boundaries and whether ellipses were dropped. Every finding in the critique chain treats the Pack as ground truth; any loose paraphrase, dropped qualifier, or misassignment inside the Pack passes through unflagged.

**This note is not verified.** Final verification against the original sources belongs to the human review gate.