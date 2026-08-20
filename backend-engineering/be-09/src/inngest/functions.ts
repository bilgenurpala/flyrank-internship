import OpenAI from "openai";
import { inngest } from "@/inngest/client";
import { updateRun } from "@/lib/run-store";
import { nextNodeId, normalizeDecision, validateGraph, type Decision, type WorkflowGraph } from "@/lib/workflow";

type WorkflowEvent = {
  data: {
    runId: string;
    input: string;
    graph: WorkflowGraph;
  };
};

async function decide(prompt: string, input: string): Promise<Decision> {
  if (process.env.DECISION_MODE === "deterministic") {
    return input.toLowerCase().includes("yes") ? "YES" : "NO";
  }
  if (!process.env.OPENAI_API_KEY) throw new Error("OPENAI_API_KEY is required when DECISION_MODE=openai");
  const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  const response = await client.responses.create({
    model: process.env.OPENAI_MODEL ?? "gpt-5-mini",
    instructions: "Evaluate the decision prompt against the user input. Return one decision. Do not add explanation.",
    input: `Decision prompt: ${prompt}\nUser input: ${input}`,
    text: {
      format: {
        type: "json_schema",
        name: "binary_decision",
        strict: true,
        schema: {
          type: "object",
          properties: { decision: { type: "string", enum: ["YES", "NO"] } },
          required: ["decision"],
          additionalProperties: false
        }
      }
    }
  });
  const parsed = JSON.parse(response.output_text) as { decision?: unknown };
  return normalizeDecision(parsed.decision);
}

export const executeDecisionFlow = inngest.createFunction(
  { id: "execute-ai-decision-flow", triggers: { event: "decision-flow/run.requested" }, retries: 1 },
  async ({ event, step }: { event: WorkflowEvent; step: { run: <T>(id: string, callback: () => Promise<T>) => Promise<T> } }) => {
    const { runId, input, graph } = event.data;
    const errors = validateGraph(graph);
    if (errors.length) {
      updateRun(runId, { status: "failed", error: errors.join("; ") });
      throw new Error(errors.join("; "));
    }
    updateRun(runId, { status: "running", error: null });
    let currentNodeId: string | null = graph.startNodeId;
    const order: string[] = [];
    const logs = [];
    try {
      while (currentNodeId) {
        if (order.length >= graph.nodes.length + 1) throw new Error("Traversal stopped because the graph contains a cycle");
        const node = graph.nodes.find((candidate) => candidate.id === currentNodeId);
        if (!node) throw new Error(`Node ${currentNodeId} does not exist`);
        updateRun(runId, { activeNodeId: node.id, order: [...order, node.id] });
        const decision = await step.run(`node-${node.id}`, () => decide(node.data.prompt, input));
        const target = nextNodeId(graph, node.id, decision);
        order.push(node.id);
        logs.push({ nodeId: node.id, label: node.data.label, decision, nextNodeId: target });
        updateRun(runId, { order: [...order], logs: [...logs] });
        currentNodeId = target;
      }
      return updateRun(runId, { status: "done", activeNodeId: null, order, logs });
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown workflow failure";
      updateRun(runId, { status: "failed", activeNodeId: null, order, logs, error: message });
      throw error;
    }
  }
);
