import { describe, expect, it } from "vitest";
import { defaultWorkflow } from "@/lib/default-workflow";
import { nextNodeId, normalizeDecision, validateGraph } from "@/lib/workflow";

describe("decision workflow", () => {
  it("normalizes only YES or NO", () => {
    expect(normalizeDecision(" yes ")).toBe("YES");
    expect(normalizeDecision("NO")).toBe("NO");
    expect(() => normalizeDecision("maybe")).toThrow("YES or NO");
  });

  it("chooses the edge matching the model decision", () => {
    expect(nextNodeId(defaultWorkflow, "support", "YES")).toBe("urgent");
    expect(nextNodeId(defaultWorkflow, "support", "NO")).toBe("sales");
    expect(nextNodeId(defaultWorkflow, "urgent", "NO")).toBeNull();
  });

  it("accepts the default graph", () => {
    expect(validateGraph(defaultWorkflow)).toEqual([]);
  });

  it("rejects missing start nodes and duplicate decision paths", () => {
    const invalid = {
      ...defaultWorkflow,
      startNodeId: "missing",
      edges: [...defaultWorkflow.edges, { id: "duplicate", source: "support", target: "human", data: { decision: "YES" } }]
    };
    expect(validateGraph(invalid)).toContain("Start node is missing");
    expect(validateGraph(invalid).some((error) => error.includes("duplicate decision edges"))).toBe(true);
  });
});
