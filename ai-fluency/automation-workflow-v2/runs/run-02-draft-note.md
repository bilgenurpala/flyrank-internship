I'll run this as **stage 1 — draft note** on the new pack, matching the format from the previous run. Say the word if you wanted the critique stage instead.

---

# MCP Primitives: Tools, Resources, and Prompts

## Short answer

The distinction is **who initiates**. Tools are model-controlled: the LLM decides when to call them. Resources are application-controlled: the host decides what context to pull in. Prompts are user-controlled: they require explicit invocation rather than automatic triggering. All three supply context, but only tools **execute** — writing to databases, calling APIs, modifying files. The rest is read-only or templated.

## Core concepts

**Tools** — executable functions an AI application can invoke to perform actions: file operations, API calls, database queries. The Evidence Pack characterizes them as *active*, in that they can trigger other logic.

**Resources** — passive data sources providing read-only contextual information: file contents, database records, API responses.

**Prompts** — reusable templates that structure interactions with the model: system prompts, few-shot examples.

**The control hierarchy** is the load-bearing distinction. Model → tools. Application → resources. User → prompts.

**The three architectural roles:**
- *Host* — the AI application that coordinates and manages one or more clients.
- *Client* — maintains a connection to one server and obtains context from it for the host.
- *Server* — a program that provides context to clients, whether it runs locally or remotely.

**Direct resources vs. resource templates** — direct resources have fixed URIs (`file:///path/to/document.md`); templates have dynamic URIs with parameters (`travel://activities/{city}/{category}`).

**Method families** — each primitive type has associated methods for discovery (`*/list`), retrieval (`*/get`), and in some cases execution (`tools/call`). The naming is standardized across all three.

**Change notifications are opt-in.** Per the pack, the client opens a long-lived `subscriptions/listen` stream naming the notification types it wants. They are described as *best effort* — no guarantee every notification is sent or received.

## How it works

1. **Host spins up clients.** One client per server connection.
2. **Discover.** The client calls the `*/list` method for each primitive type to learn what the server offers.
3. **Retrieve.** `*/get` fetches the content — a prompt template, a resource's data.
4. **Execute.** For tools only, `tools/call` runs the function. This is the one path that changes state.
5. **Address resources by URI.** Fixed for direct resources; substitute parameters for templates.
6. **Subscribe if you need change notifications** — and treat delivery as best effort rather than guaranteed.
7. **Interpose approval where needed.** The pack notes applications can implement approval dialogs or permission settings over tool calls.

## Concrete example

**Multi-server travel planning.** A user invokes the `plan-vacation` prompt (user-controlled). Executing it draws on three servers — Travel, Weather, Calendar. The host reads calendar resources such as `calendar://events/2024` and `trips://history/barcelona-2023` (application-controlled), fills the template `travel://activities/{city}/{category}` for the destination, then the model calls `searchFlights` and `createCalendarEvent` (model-controlled).

The pack also describes the model choosing to call `checkWeather()` on the reasoning that weather can affect travel plans — but it explicitly labels that as an **inference**, not a sourced claim. Treat it as illustrative only.

## Why it matters for my work

For a backend AI engineering intern building MCP servers, the primitive you choose is a decision about **who pulls the trigger**, not just about data shape.

- **Expose something as a tool and you hand the trigger to the model.** Expose the same data as a resource and the application decides when it enters context. The Evidence Pack does not give a rule for which to prefer when both are viable.
- **The read/write boundary lines up with the primitive boundary.** Resources are read-only by definition in these sources; anything that mutates state has to be a tool.
- **URI design is interface design.** Resource templates take parameters, so the URI scheme is a public contract, same as a function signature.
- **Don't build correctness on notifications.** Opt-in plus best-effort means a client that missed a `list_changed` is a state you have to tolerate, not an edge case.
- **"Model-controlled" is not "unsupervised."** Approval dialogs and permission settings sit on top of tool invocation — the pack itself flags this as blurring the control categories.
- **Pin your protocol version.** The pack's own sources disagree across versions (below), which is itself the lesson.

## What the evidence does not establish

- **The source references are blank.** Every claim in §3 of the pack has an empty **Source Reference** field. The supporting passages are quoted, but nothing in this note can be traced to a specific source without returning to the originals. This is the most serious gap in the pack.
- **The version conflict is unresolved.** Sources 1 and 3 use 2026-07-28; Source 2 uses 2025-06-18. Source 1 marks **Sampling** and **Logging** as deprecated; Source 2 lists Sampling and Elicitation as standard client features. The pack does not adjudicate this, so the current status of Sampling is genuinely open.
- **Sampling and Elicitation are named but never defined.** They appear only in the deprecation dispute.
- **No decision rule for resource vs. tool.** Nothing tells you which to use when the same data could be served either way.
- **"Application-controlled" is not unpacked.** No account of what in the host actually selects resources, or on what basis.
- **Nothing on transport, authentication, authorization, error handling, pagination, or size limits.**
- **No guidance on discovering valid template parameters** — the pack shows `{city}` and `{category}` but not how a client learns the legal values.
- **No performance or scale claims** of any kind.

## Comprehension checks

1. You need to expose a customer's order history to an assistant. Argue for exposing it as a resource rather than a tool using only the control hierarchy in the pack — then state precisely what the pack does *not* let you claim about which choice is better.
2. A colleague says tools are "the model-controlled primitive, so the user isn't in the loop." Using the pack's own note on approval dialogs, explain why that inference doesn't follow, and identify what "model-controlled" actually specifies.
3. Your client caches a server's tool list and subscribes to change notifications. Using the pack's characterization of notification delivery, explain what failure mode your cache must tolerate — and why the pack cannot tell you how often that failure occurs.