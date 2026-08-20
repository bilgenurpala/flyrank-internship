import { NextResponse } from "next/server";
import { inngest } from "@/inngest/client";
import { createRun } from "@/lib/run-store";
import { validateGraph, type WorkflowGraph } from "@/lib/workflow";

export async function POST(request: Request) {
  const body = await request.json() as { input?: string; graph?: WorkflowGraph };
  if (!body.input?.trim() || !body.graph) return NextResponse.json({ error: "Input and graph are required" }, { status: 400 });
  const errors = validateGraph(body.graph);
  if (errors.length) return NextResponse.json({ error: errors.join("; ") }, { status: 422 });
  const runId = crypto.randomUUID();
  createRun(runId);
  await inngest.send({ name: "decision-flow/run.requested", data: { runId, input: body.input, graph: body.graph } });
  return NextResponse.json({ runId }, { status: 202 });
}
