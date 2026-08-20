import { Handle, Position, type NodeProps } from "@xyflow/react";
import type { DecisionNodeData } from "@/lib/workflow";

export function DecisionNode({ data, selected }: NodeProps & { data: DecisionNodeData }) {
  return (
    <div className={`decision-node ${selected ? "selected" : ""}`}>
      <span className="node-kicker">AI decision</span>
      <strong>{data.label}</strong>
      <p>{data.prompt}</p>
      <Handle type="target" position={Position.Left} />
      <Handle id="yes" type="source" position={Position.Right} style={{ top: "38%", background: "#3ddc97" }} />
      <Handle id="no" type="source" position={Position.Right} style={{ top: "72%", background: "#ff7a59" }} />
      <span className="handle-label yes">YES</span>
      <span className="handle-label no">NO</span>
    </div>
  );
}
