# BE-09: Build an AI Decision Flow with React Flow + Inngest

This project is a visual editor and durable executor for binary AI decision workflows. Each React Flow node contains an editable decision prompt. During a run, the graph is traversed through Inngest, each visited node becomes a retriable `step.run()`, and the OpenAI Responses API returns a schema-constrained `YES` or `NO` decision. The selected edge determines the next node.

## Delivered requirements

- Next.js App Router frontend with a configured shadcn-style component layer
- React Flow canvas with add, move, select, connect, and prompt-edit interactions
- Explicit `YES` and `NO` edge data and labels
- Local graph persistence through `localStorage`
- JSON export and import
- Inngest event trigger and one durable step per visited node
- Strict OpenAI Structured Output restricted to `YES | NO`
- Dynamic graph traversal and execution-order tracking
- Active-node and traversed-edge visualization
- Execution log panel with node, decision, and next-node data
- Clear queued, running, done, and failed states

## Architecture

```text
React Flow editor
      |
POST /api/runs
      |
decision-flow/run.requested
      |
Inngest execute-ai-decision-flow
      |
step.run(node-id) -> OpenAI YES/NO -> matching edge -> next node
      |
GET /api/runs/:runId -> visual state and execution logs
```

The in-memory run store exists only to reflect the local Inngest Dev Server run in the frontend. Inngest remains the execution system and its Dev Server is the durable trace. A production deployment would replace the in-memory read model with persistent storage.

## Setup

Requirements: Node.js 20.9 or newer and an OpenAI API key.

```bash
cp .env.example .env.local
npm install
```

Set `OPENAI_API_KEY` in `.env.local`. Keep `DECISION_MODE=openai` for a real AI run.

Start the frontend:

```bash
npm run dev
```

In a second terminal, start the Inngest Dev Server:

```bash
npm run inngest
```

Open:

- Frontend: `http://localhost:3000`
- Inngest Dev Server: `http://localhost:8288`

Edit prompts, choose a start node, connect the `YES` and `NO` handles, enter user input, and select **Run with Inngest**. The canvas highlights the active path while the log panel records traversal order.

## Deterministic local verification

Automated tests never spend API credits. To exercise the complete Inngest traversal without an API call, set this only for local verification:

```bash
DECISION_MODE=deterministic
```

That mode returns `YES` only when the input contains the word `yes`; it is not presented as AI behavior and is not the mode used for an assignment demo.

```bash
npm test
npm run build
```

## Boundaries

- A binary output can make routing auditable, but it does not make the underlying classification correct.
- Prompt quality, model behavior, and input ambiguity still affect decisions.
- The editor rejects missing start nodes, empty prompts, duplicate decision paths, and edges that reference missing nodes.
- Cycles are stopped after the traversal exceeds the node-count guard.
- The frontend run read model is process-local. Restarting Next.js clears it, while Inngest Dev Server retains its own local trace.
- Secrets belong in `.env.local` and are never exposed to the browser or committed.
- There is no authentication, multi-user collaboration, workflow versioning, or production persistence in this assignment scope.
