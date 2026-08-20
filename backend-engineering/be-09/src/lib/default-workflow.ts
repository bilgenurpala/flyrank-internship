import type { WorkflowGraph } from "@/lib/workflow";

export const defaultWorkflow: WorkflowGraph = {
  startNodeId: "support",
  nodes: [
    { id: "support", type: "decision", position: { x: 80, y: 180 }, data: { label: "Support request?", prompt: "Does the user message describe a support request?" } },
    { id: "urgent", type: "decision", position: { x: 430, y: 60 }, data: { label: "Urgent?", prompt: "Does the support request describe an urgent service-impacting problem?" } },
    { id: "sales", type: "decision", position: { x: 430, y: 310 }, data: { label: "Sales lead?", prompt: "Does the user show concrete interest in buying or booking a product?" } },
    { id: "human", type: "decision", position: { x: 780, y: 60 }, data: { label: "Human escalation?", prompt: "Should this urgent request be escalated to a human now?" } },
    { id: "qualified", type: "decision", position: { x: 780, y: 310 }, data: { label: "Qualified lead?", prompt: "Does this sales lead include enough intent and context to qualify?" } }
  ],
  edges: [
    { id: "support-yes", source: "support", target: "urgent", sourceHandle: "yes", data: { decision: "YES" }, label: "YES", animated: true },
    { id: "support-no", source: "support", target: "sales", sourceHandle: "no", data: { decision: "NO" }, label: "NO" },
    { id: "urgent-yes", source: "urgent", target: "human", sourceHandle: "yes", data: { decision: "YES" }, label: "YES", animated: true },
    { id: "sales-yes", source: "sales", target: "qualified", sourceHandle: "yes", data: { decision: "YES" }, label: "YES", animated: true }
  ]
};
