import type { ExecutionLog } from "@/lib/workflow";

export type RunState = {
  id: string;
  status: "queued" | "running" | "done" | "failed";
  activeNodeId: string | null;
  order: string[];
  logs: ExecutionLog[];
  error: string | null;
};

const runStore = new Map<string, RunState>();

export function createRun(id: string): RunState {
  const run: RunState = { id, status: "queued", activeNodeId: null, order: [], logs: [], error: null };
  runStore.set(id, run);
  return run;
}

export function getRun(id: string): RunState | undefined {
  return runStore.get(id);
}

export function updateRun(id: string, update: Partial<RunState>): RunState {
  const current = runStore.get(id) ?? createRun(id);
  const next = { ...current, ...update };
  runStore.set(id, next);
  return next;
}
