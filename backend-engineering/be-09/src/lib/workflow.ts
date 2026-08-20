import type { Edge, Node } from "@xyflow/react";

export type Decision = "YES" | "NO";

export type DecisionNodeData = {
  label: string;
  prompt: string;
};

export type WorkflowGraph = {
  nodes: Node<DecisionNodeData>[];
  edges: Edge[];
  startNodeId: string;
};

export type ExecutionLog = {
  nodeId: string;
  label: string;
  decision: Decision;
  nextNodeId: string | null;
};

export function normalizeDecision(value: unknown): Decision {
  if (typeof value !== "string") throw new Error("Decision must be a string");
  const normalized = value.trim().toUpperCase();
  if (normalized !== "YES" && normalized !== "NO") throw new Error("Model decision must be YES or NO");
  return normalized;
}

export function nextNodeId(graph: WorkflowGraph, nodeId: string, decision: Decision): string | null {
  const edge = graph.edges.find((candidate) => candidate.source === nodeId && candidate.data?.decision === decision);
  return edge?.target ?? null;
}

export function validateGraph(graph: WorkflowGraph): string[] {
  const errors: string[] = [];
  const ids = new Set(graph.nodes.map((node) => node.id));
  if (!ids.has(graph.startNodeId)) errors.push("Start node is missing");
  for (const node of graph.nodes) {
    if (!node.data.prompt.trim()) errors.push(`${node.data.label} has an empty prompt`);
    const outgoing = graph.edges.filter((edge) => edge.source === node.id);
    const decisions = outgoing.map((edge) => edge.data?.decision);
    if (new Set(decisions).size !== decisions.length) errors.push(`${node.data.label} has duplicate decision edges`);
    if (decisions.some((decision) => decision !== "YES" && decision !== "NO")) errors.push(`${node.data.label} has an unlabeled edge`);
  }
  for (const edge of graph.edges) {
    if (!ids.has(edge.source) || !ids.has(edge.target)) errors.push(`Edge ${edge.id} references a missing node`);
  }
  return errors;
}
