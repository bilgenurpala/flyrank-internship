"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  Background,
  Controls,
  MarkerType,
  MiniMap,
  ReactFlow,
  ReactFlowProvider,
  addEdge,
  useEdgesState,
  useNodesState,
  type Connection,
  type Edge,
  type Node
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { Download, Play, Plus, RotateCcw, Upload } from "lucide-react";
import { DecisionNode } from "@/components/decision-node";
import { Button } from "@/components/ui/button";
import { defaultWorkflow } from "@/lib/default-workflow";
import type { DecisionNodeData, WorkflowGraph } from "@/lib/workflow";
import type { RunState } from "@/lib/run-store";

const STORAGE_KEY = "be-09-decision-flow";

function Editor() {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node<DecisionNodeData>>(defaultWorkflow.nodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>(defaultWorkflow.edges.map((edge) => ({ ...edge, markerEnd: { type: MarkerType.ArrowClosed } })));
  const [startNodeId, setStartNodeId] = useState(defaultWorkflow.startNodeId);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(defaultWorkflow.startNodeId);
  const [edgeDecision, setEdgeDecision] = useState<"YES" | "NO">("YES");
  const [input, setInput] = useState("My production account is locked and customers cannot log in.");
  const [run, setRun] = useState<RunState | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInput = useRef<HTMLInputElement>(null);
  const nodeTypes = useMemo(() => ({ decision: DecisionNode }), []);

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) return;
    try {
      const graph = JSON.parse(saved) as WorkflowGraph;
      setNodes(graph.nodes);
      setEdges(graph.edges.map((edge) => ({ ...edge, markerEnd: { type: MarkerType.ArrowClosed } })));
      setStartNodeId(graph.startNodeId);
    } catch {
      localStorage.removeItem(STORAGE_KEY);
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ nodes, edges, startNodeId }));
  }, [nodes, edges, startNodeId]);

  useEffect(() => {
    if (!run || run.status === "done" || run.status === "failed") return;
    const timer = window.setInterval(async () => {
      const response = await fetch(`/api/runs/${run.id}`);
      if (response.ok) setRun(await response.json());
    }, 700);
    return () => window.clearInterval(timer);
  }, [run]);

  useEffect(() => {
    if (!run) return;
    setNodes((current) => current.map((node) => ({
      ...node,
      className: run.activeNodeId === node.id ? "node-active" : run.order.includes(node.id) ? "node-complete" : ""
    })));
    setEdges((current) => current.map((edge) => ({
      ...edge,
      className: run.logs.some((log) => log.nodeId === edge.source && log.nextNodeId === edge.target) ? "edge-active" : ""
    })));
  }, [run, setEdges, setNodes]);

  const onConnect = useCallback((connection: Connection) => {
    const decision = connection.sourceHandle === "no" ? "NO" : edgeDecision;
    setEdges((current) => addEdge({ ...connection, id: `${connection.source}-${decision.toLowerCase()}-${connection.target}`, label: decision, data: { decision }, animated: decision === "YES", markerEnd: { type: MarkerType.ArrowClosed } }, current));
  }, [edgeDecision]);

  function addNode() {
    const id = `node-${crypto.randomUUID().slice(0, 8)}`;
    setNodes((current) => [...current, { id, type: "decision", position: { x: 160 + current.length * 36, y: 140 + current.length * 28 }, data: { label: `Decision ${current.length + 1}`, prompt: "Write a binary decision prompt." } }]);
    setSelectedNodeId(id);
  }

  function updateSelected(field: keyof DecisionNodeData, value: string) {
    if (!selectedNodeId) return;
    setNodes((current) => current.map((node) => node.id === selectedNodeId ? { ...node, data: { ...node.data, [field]: value } } : node));
  }

  async function execute() {
    setError(null);
    setRun(null);
    const response = await fetch("/api/runs", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ input, graph: { nodes, edges, startNodeId } }) });
    const body = await response.json();
    if (!response.ok) {
      setError(body.error ?? "Workflow could not start");
      return;
    }
    setRun({ id: body.runId, status: "queued", activeNodeId: null, order: [], logs: [], error: null });
  }

  function exportGraph() {
    const blob = new Blob([JSON.stringify({ nodes, edges, startNodeId }, null, 2)], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "decision-flow.json";
    link.click();
    URL.revokeObjectURL(link.href);
  }

  async function importGraph(file: File) {
    try {
      const graph = JSON.parse(await file.text()) as WorkflowGraph;
      if (!Array.isArray(graph.nodes) || !Array.isArray(graph.edges) || !graph.startNodeId) throw new Error("Invalid workflow JSON");
      setNodes(graph.nodes);
      setEdges(graph.edges.map((edge) => ({ ...edge, markerEnd: { type: MarkerType.ArrowClosed } })));
      setStartNodeId(graph.startNodeId);
      setSelectedNodeId(graph.startNodeId);
      setError(null);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Import failed");
    }
  }

  const selected = nodes.find((node) => node.id === selectedNodeId);

  return (
    <main>
      <header className="topbar">
        <div><span className="eyebrow">BE-09 · Backend AI Engineering</span><h1>AI Decision Flow</h1></div>
        <div className="toolbar">
          <Button variant="secondary" size="sm" onClick={addNode}><Plus size={16} /> Add node</Button>
          <Button variant="secondary" size="sm" onClick={exportGraph}><Download size={16} /> Export</Button>
          <Button variant="secondary" size="sm" onClick={() => fileInput.current?.click()}><Upload size={16} /> Import</Button>
          <input ref={fileInput} hidden type="file" accept="application/json" onChange={(event) => event.target.files?.[0] && importGraph(event.target.files[0])} />
          <Button variant="secondary" size="sm" onClick={() => { setNodes(defaultWorkflow.nodes); setEdges(defaultWorkflow.edges.map((edge) => ({ ...edge, markerEnd: { type: MarkerType.ArrowClosed } }))); setStartNodeId(defaultWorkflow.startNodeId); }}><RotateCcw size={16} /> Reset</Button>
        </div>
      </header>
      <section className="workspace">
        <div className="canvas-panel">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            nodeTypes={nodeTypes}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeClick={(_event, node) => setSelectedNodeId(node.id)}
            fitView
          >
            <Background gap={20} size={1} />
            <MiniMap pannable zoomable />
            <Controls />
          </ReactFlow>
        </div>
        <aside className="sidebar">
          <section className="panel">
            <span className="panel-label">Selected node</span>
            {selected ? <>
              <label>Label<input value={selected.data.label} onChange={(event) => updateSelected("label", event.target.value)} /></label>
              <label>Decision prompt<textarea rows={4} value={selected.data.prompt} onChange={(event) => updateSelected("prompt", event.target.value)} /></label>
              <label>Start node<select value={startNodeId} onChange={(event) => setStartNodeId(event.target.value)}>{nodes.map((node) => <option key={node.id} value={node.id}>{node.data.label}</option>)}</select></label>
              <label>New edge type<select value={edgeDecision} onChange={(event) => setEdgeDecision(event.target.value as "YES" | "NO")}><option>YES</option><option>NO</option></select></label>
            </> : <p>Select a node on the canvas.</p>}
          </section>
          <section className="panel run-panel">
            <span className="panel-label">Execution</span>
            <label>User input<textarea rows={4} value={input} onChange={(event) => setInput(event.target.value)} /></label>
            <Button onClick={execute} disabled={!input.trim() || run?.status === "queued" || run?.status === "running"}><Play size={16} /> Run with Inngest</Button>
            {error && <p className="error">{error}</p>}
            {run && <div className="run-summary"><span className={`status status-${run.status}`}>{run.status}</span><code>{run.id}</code>{run.error && <p className="error">{run.error}</p>}</div>}
          </section>
          <section className="panel logs-panel">
            <span className="panel-label">Execution logs</span>
            {!run?.logs.length && <p>No visited nodes yet.</p>}
            <ol>{run?.logs.map((log) => <li key={`${log.nodeId}-${log.decision}`}><strong>{log.label}</strong><span>{log.decision} → {log.nextNodeId ?? "END"}</span></li>)}</ol>
          </section>
        </aside>
      </section>
    </main>
  );
}

export function WorkflowEditor() {
  return <ReactFlowProvider><Editor /></ReactFlowProvider>;
}
