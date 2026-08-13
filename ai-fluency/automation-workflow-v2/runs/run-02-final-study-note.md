## Final Study Note

# MCP Primitives: Tools, Resources, and Prompts

## Short answer

The distinction is **who initiates**. Tools are model-controlled: the model decides when to use them **based on user requests**. Resources are application-controlled: the application supplies them as passive context. Prompts are user-controlled: they require explicit invocation rather than automatic triggering. All three provide context; tools are the ones described as able to **actively perform operations** — writing to databases, calling APIs, modifying files.

## Core concepts

**Tools** — executable functions an AI application can invoke to perform actions: file operations, API calls, database queries. The Evidence Pack characterizes them as *active*, in that they can trigger other logic.

**Resources** — passive data sources providing read-only contextual information: file contents, database records, API responses.

**Prompts** — reusable templates that structure interactions with language models: system prompts, few-shot examples.

**The control hierarchy** is the load-bearing distinction: model → tools, application → resources, user → prompts.

**Automatic vs. explicit triggering.** The pack pairs the control hierarchy with a trigger asymmetry: tools can be invoked **automatically** by models during a conversation, while prompts require **explicit invocation** by the user rather than automatic triggering.

**The three architectural roles:**
- *Host* — the AI application that coordinates and manages one or more clients.
- *Client* — maintains a connection to one server and obtains context from it for the host to use.
- *Server* — a program that provides context to clients, whether it runs locally or remotely.

**Direct resources vs. resource templates** — direct resources have fixed URIs; templates have dynamic URIs using parameters.

**Method families** — each primitive type has associated methods for discovery (`*/list`), retrieval (`*/get`), and **in some cases** execution (`tools/call`).

**Change notifications are opt-in** — per the pack, the client opens a long-lived `subscriptions/listen` stream naming the notification types it wants to receive. Delivery is described as **best effort**, with no guarantees that every notification will be sent or received.

**Control is not absolute.** Applications can implement approval dialogs or permission settings, layering user control over a model-controlled primitive.

## How it works

1. **The host runs one or more clients**, each maintaining a connection to a server.
2. **Discover** what a server offers using the `*/list` method family.
3. **Retrieve** using the `*/get` method family. The pack does not specify what each primitive type returns.
4. **Execute** where execution applies — the pack names `tools/call`, and hedges execution as available "in some cases."
5. **Address resources by URI** — fixed for direct resources, parameterized for templates.
6. **Subscribe to change notifications if wanted**, opening the long-lived stream and naming the notification types; treat delivery as best effort.
7. **Interpose approval where the application requires it** — approval dialogs or permission settings can gate tool invocation.

## Concrete example

The pack's **sourced multi-server scenario**: a Travel Server, Weather Server, and Calendar Server used together to execute a `plan-vacation` prompt by **reading calendar resources and calling flight search tools**.

The pack's **separate example lists** — not part of that narrated scenario, and not combined into one here:
- Tools: `calculator_arithmetic`, `weather_current`, `searchFlights`, `createCalendarEvent`, `sendEmail`.
- Resources: `file:///path/to/document.md`, `calendar://events/2024`, `travel://activities/{city}/{category}` (template), `trips://history/barcelona-2023`.
- Prompts: `plan-vacation`, "Summarize my meetings", "Draft an email".

The pack also describes a model choosing to call `checkWeather()` because weather can affect travel plans — explicitly labeled by the pack as an **inference**, not a sourced claim.

## Why it matters for my work

For a backend AI engineering intern building MCP servers, the primitive you choose is a decision about **who pulls the trigger**.

- **Exposing something as a tool puts invocation in the model's hands**, based on user requests and potentially automatic during a conversation. Exposing it as a resource leaves it application-controlled. The pack gives no rule for choosing between them when both are viable.
- **The read/write contrast is descriptive, not a mandate.** The sources describe resources as read-only access to information and tools as capable of writing to databases or modifying files. *Inference: this suggests mutating operations fit the tool shape. The pack states no requirement on server authors, and does not claim `tools/call` is the only path that changes state.*
- **Resource URIs come in two shapes** — fixed, and parameterized templates. *Inference: parameter naming is therefore a design decision with downstream consumers. The pack contains no contract, versioning, or function-signature framing; that analogy has been removed as unsourced.*
- **Notification delivery is opt-in and best effort.** *Inference: a client cannot assume it received every notification. The pack states the reliability characteristic but prescribes nothing about client design.*
- **"Model-controlled" does not mean unsupervised.** Approval dialogs and permission settings sit over tool invocation, which the pack itself flags as blurring the control categories.
- **The pack's sources disagree on protocol version.** *Inference: version selection is worth making explicit in an implementation. The pack records the disagreement but offers no implementation guidance.*

## What the evidence does not establish

- **Individual claims cannot be traced after export.** Pack §7 gives source-level coverage — Source 1 for architecture, definitions, and JSON-RPC message examples; Source 2 for the control hierarchy table; Source 3 for the travel scenario and user interaction models. But every **Source Reference** field in Pack §3 is blank, so no individual supporting passage can be attributed to Source 1, 2, or 3. Coverage exists at the block level; traceability does not exist at the claim level.
- **The version and deprecation disagreement is unresolved.** Sources 1 and 3 use 2026-07-28; Source 2 uses 2025-06-18. Source 1 marks **both Sampling and Logging** as deprecated. Source 2 lists Sampling and Elicitation as standard "Client Features" with no mention of deprecation. The pack explains this by noting Source 2 is **older** — that explanation is the pack's own reading and is not independently verified here.
- **Sampling, Logging, and Elicitation are named but never defined** in the pack.
- **No decision rule for resource vs. tool** when the same data could be served either way.
- **"Application-controlled" is not unpacked** — nothing describes what in the host selects resources, or on what basis.
- **The `*/get` family is stated generically**; the pack does not map it onto specific primitives.
- **No discovery mechanism for valid template parameter values** is described.
- **No coverage in the pack** of transport, authentication, authorization, error handling, pagination, size limits, performance, or scale. These are absences in the pack, not established absences in the original sources.

## Comprehension checks

1. You need to expose a customer's order history to an assistant. Argue for exposing it as a resource using only the control hierarchy — then state precisely why the Evidence Pack does not let you claim that choice is better.
2. A colleague says tools are "the model-controlled primitive, so the user isn't in the loop." Using the pack's note on approval dialogs and its statement that models decide based on user requests, explain why that inference does not follow.
3. Your client caches a server's tool list and subscribes to change notifications. Using only the pack's characterization of notification delivery, state what the pack does and does not tell you about the reliability of that cache — and identify which part of your answer is inference rather than sourced.

## Change Log

| Critique ID | Action taken | Evidence used |
|---|---|---|
| C1 | Retained; rephrased to the pack's wording ("actively perform operations") rather than "only tools execute." | Pack §1. |
| C2 | **Blocking.** Deleted "This is the one path that changes state." Restored the "in some cases" hedge in both Core concepts and How it works. | Pack §3 discovery/retrieval/execution passage. |
| C3 | Converted the mandate to a descriptive contrast plus a labeled inference; removed "has to be a tool." | Pack §4 read-only vs. write. |
| C4 | Removed the public-contract / function-signature analogy. Kept the fixed-vs-template distinction; the design implication is labeled inference. | Pack §4 Direct vs. Template Resources. |
| C5 | "Pin your protocol version" removed as guidance; retained as a labeled inference from the recorded disagreement. | Pack §6 Protocol Versioning Conflicts. |
| C6 | **Blocking.** Removed `list_changed`. Replaced with the pack's own wording on opt-in notifications and the `subscriptions/listen` stream. | Pack §3 notification claim. |
| C7 | Reliability implication relabeled as inference; the sourced statement is the best-effort characteristic alone. | Pack §6 Notification Reliability. |
| C8 | Retained unchanged. | Pack §6. |
| C9 | Restored the pack's age-based explanation of the discrepancy, with an explicit note that it is the pack's reading and not independently verified. Removed "the pack does not adjudicate this." | Pack §6 Deprecation Discrepancies. |
| C10 | Added **Logging** alongside Sampling in the deprecation discrepancy. | Pack §6. |
| C11 | Split the Concrete example into the pack's sourced multi-server scenario and its separate example lists; stopped presenting the merged narration as sourced. | Pack §5. |
| C12 | Retained the inference label on `checkWeather()`. | Pack §5. |
| C13 | Removed the per-primitive mapping of `*/get`; kept the method family as stated and noted the pack does not specify returns. | Pack §3. |
| C14 | Restored "based on user requests" to the tools description in Short answer and Why it matters. | Pack §3 tools claim. |
| C15 | Removed "decides what context to pull in"; resources now described as application-controlled passive context, with the selection mechanism listed as unspecified. | Pack §2, §4. |
| C16 | Rewrote the traceability statement: source-level coverage from §7 acknowledged, claim-level traceability stated as absent. | Pack §3 blank fields; Pack §7. |
| C17 | Absence claims rescoped as absences in the Evidence Pack rather than in the original sources. | Scope of Pack §1–§7. |
| — | Added the automatic-vs-explicit-trigger distinction to Core concepts. | Pack §4 Automatic vs. Explicit Triggering. |

## Remaining Limitations

- **Citation markers were removed on export.** NotebookLM's clickable numbered citations were stripped by its copy function. Combined with the blank **Source Reference** fields in Pack §3, no individual passage in this note can be tied to a specific source. Source-level coverage from Pack §7 is the only attribution available, and it operates at the level of content blocks, not claims.
- **Quoted passages are unverified.** Whether any quotation in the pack is verbatim, complete, or correctly attributed cannot be checked from inside this document. The removal of `list_changed` was possible only because that identifier was absent from the pack — a fabricated or spliced passage that *is* present would be indistinguishable from a faithful one at this layer.
- **Method names are unverified.** `*/list`, `*/get`, `tools/call`, and `subscriptions/listen` are reproduced as the pack states them. Their existence in the protocol has not been confirmed.
- **Version ambiguity persists.** Whether 2026-07-28 exists, whether Source 2's content is genuinely superseded rather than merely older in stated version, and whether Sampling and Logging are in fact deprecated all remain open. The pack's age-based explanation is a plausible reading, not a verified resolution.
- **Elicitation's status is unresolved** — it appears in Source 2's client features and is not addressed by Source 1's deprecation list as recorded.
- **Omissions may be the pack's, not the sources'.** Transport, authentication, authorization, error handling, pagination, limits, and performance may be covered in the originals. This note cannot distinguish a source gap from a summarization gap.
- **The travel scenario's fidelity is unverified.** Whether the pack itself composed it from scattered Source 3 material cannot be determined here.
- **Every inference label in this note marks a reading, not a finding.** None has been checked against the originals.

This note is not verified. Final verification against the original sources belongs to the human review gate.