# Agent Concepts and MCP Basics

## Workflow vs. Agent

The distinction between a workflow and an agent is not a claim about capability. The same model can sit inside either. What separates them is who decides the path.

In a workflow, the path is fixed before the model runs. Steps are enumerated in advance, and each stage receives its input and returns its output according to a shape imposed from outside. The model does useful work at every step, but it never chooses which step comes next.

An agent changes that control boundary. Within limits the designer sets — permitted tools, a turn budget, a stopping condition — the model decides its own next move: which tool to call, whether the task is finished, whether to loop again. Those limits matter, because "agent" does not mean unsupervised. An agent can run under a tighter approval regime than a fully automated workflow.

By that test, the pipeline described here is a workflow — specifically a manually orchestrated one. The sequence never varies, and a human, not the model, advances each stage.

## MCP and Its Primitives

MCP is not a model. It is a connection layer — a standard way for an AI application to reach external systems, so that each new integration does not require a bespoke protocol. It defines three primitives, distinguished by who initiates them.

**Tools** are model-controlled calls: the model decides, mid-conversation, that it needs one and invokes it. **Resources** are application-provided readable context, addressed by URI; the host decides what gets pulled in. **Prompts** are reusable templates invoked by the user rather than triggered automatically.

"Model-controlled" describes initiative, not permission. The application can still gate a tool call behind an approval dialog or a permission setting, and frequently does. Deciding to call is not the same as being allowed to.

The GitHub connector runs in this project made three real calls: fetching `devlog.md`, searching open issues, and querying commits. Each was a tool call — issued when the model needed the data, not selected from a fixed list the application had staged in advance, and not the execution of a stored template.

That matters because plain chat has no such reach. It answers from what is already in the context window; these runs read live repository state at the moment of asking. This demonstrates tool-backed external access, not the full MCP protocol surface — resources and prompts were never exercised.

## My Pipeline and One Agent Upgrade

The pipeline I have been running is fixed: NotebookLM produces an Evidence Pack, a Draft Note is written against it, a Critique audits every claim back to the pack, a Revision applies the findings, and a human reviews the result. The order never changes, and neither do the handoffs — each stage receives a defined artifact and returns a defined one. Two familiar patterns are visible in it: prompt chaining, where one stage's output is the next stage's input, and evaluator-optimizer, where one stage judges what another produced. None of this is automated in code; I advance each step by hand. It is still a workflow, because the model never chooses what comes next.

The upgrade I would make is a revision-loop agent. After the Critique returns, the model reads the severity ratings itself: if any blocking finding remains, it revises again; if none does, it stops and hands off to human review. That is a small change, but it moves one real decision — continue or stop — from me to the model. It introduces an agentic decision loop into the workflow rather than converting the workflow into an agent.

Two guardrails are load-bearing. A turn limit caps the loop, and the Change Log must survive every pass, so each revision stays traceable. Neither removes the central risk: the model may declare its own finding resolved when it has merely rewritten around it. Final approval stays with the human for exactly that reason.

## What I Learned

The clearest thing I take from this is that agentic behaviour is read from the control flow, not from how the interface feels. A system that answers fluently and calls tools can still be a workflow end to end. Tool use alone settles nothing.

MCP made that concrete for me. It gave the model reach it did not have before — but reach is not intelligence. Nothing about the GitHub connector made the model reason better; it only let the model look at things it previously could not see. And the more it can reach, the more the permission, approval, and verification questions do the real work.

So I will not describe the current pipeline as an agent, because it is not one. And I will keep the upgrade narrow enough that I can actually tell whether it helped.
