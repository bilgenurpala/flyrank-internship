# Evidence Critique — Draft Note vs Evidence Pack

| ID | Draft claim or section | Finding type | Severity | Evidence check | Required change |
|---|---|---|---|---|---|
| C1 | Concrete example: "The routing rule is fixed; the model does not choose its own destination." | unsupported | blocking | The Pack's routing entry states only the effect. It never says what performs the classification. "Workflows follow code-governed steps" establishes that the path is predefined, not that no model makes the routing decision. | Cut the second clause. Retain only what the Pack licenses: the routing destinations are predefined rather than chosen by the system at runtime. |
| C2 | Why it matters: "A predefined path does not have the same surface." | overstated | blocking | The Pack supports that agent autonomy introduces new risks. It says nothing about a workflow's exposure to those same risks. The draft converts an additive claim into a comparative security claim. | Restate additively and drop any comparison to workflows. |
| C3 | Why it matters: "the shape of a tool's interface and its docstring are part of the deliverable" | unsupported | important | The Pack supports thorough tool documentation through the Agent-Computer Interface. "Docstring" and "shape of the interface" are absent. | Use the Pack's own wording without naming an artifact type. |
| C4 | How it works, step 1: binary enumerable-steps rule | overstated | important | The Pack states suitability, not an exhaustive decision rule, and also names flexibility and model-driven decision-making at scale. | Reframe as suitability and restore the second condition. |
| C5 | Short answer: "agent autonomy adds risk of unintended consequences" | source mismatch | important | The working answer attributes latency, cost, and unintended-consequence risk to both systems. Agent-specific risks are misread intent and prompt injection. | Attribute unintended-consequence risk generally and keep agent-specific risks separate. |
| C6 | Why it matters: an unnecessary agent pays latency and cost | overstated | important | The Pack says agentic systems trade latency and cost, covering workflows too. It does not establish agents cost more than workflows. | Remove the comparison or label it as an unsupported inference. |
| C7 | Expense example runtime sequence | unsupported | important | The Pack lists steps and a condition but does not state that the sequence is determined at runtime. | Label as inference or cut. |
| C8 | Four layers as a debugging/intervention map | unsupported | important | The Pack states composition, not failure localization or where fixes belong. | Label as inference or reduce to composition. |
| C9 | ACI defined as the design surface between agent and tools | unsupported | minor | The Pack names ACI design but does not define it. | Present it as named but undefined, or label the gloss as inference. |
| C10 | Four layers turned into an ordered build procedure | overstated | minor | The Pack describes what an agent is, not a build sequence. | Mark the ordering as the draft's organization, not a sourced sequence. |
| C11 | Individual approvals vs Plan Mode | acceptable | minor | Tracks the Pack's oversight distinction closely. | None. |
| C12 | Oversight approaches are different products, not just UIs | unsupported | minor | This evaluative user-experience claim has no basis in the Pack. | Cut or soften to the supported distinction. |
| C13 | Comprehension check uses four layers as debugging map | unsupported | minor | Inherits C8. | If retained, label the intervention framework as inference. |
| C14 | Core definitions and distinctions | acceptable | — | They track the Pack. | None. |
| C15 | Evidence-limitations section | acceptable | — | Pack uncertainties and citation limitation are preserved accurately. | None. |
| C16 | Source labels | acceptable | — | Assignments are internally consistent with the Pack's source-coverage section. | None. |
| C17 | Design-time framing for an intern | acceptable | — | Connects to the role without asserting completed work. | None. |

## Coverage gaps

- The prompt-chaining, parallelization, and evaluator-optimizer examples are unused but optional.
- The SWE-bench coding-agent example should be considered because it is the clearest agent example for a backend engineering audience and avoids relying on the inferred runtime reading of the expense case.
- The Computer Use example is unused but optional.
- The statement that both sources were useful should not be added because it is meta-commentary.
- Confidence ratings are unused and optional.

No gap is severe enough to make the draft incomplete against the research question.

## Critique limitations

- This audit treats the Evidence Pack as ground truth and cannot establish whether it is faithful to the original sources.
- It cannot verify that quotations are verbatim.
- It cannot verify the manually restored source labels. This is the largest unresolved risk.
- Unsupported findings may be true in the original sources; unsupported does not mean false.
- It cannot find material omitted from the Evidence Pack.
- It cannot determine whether the Pack's High confidence ratings are warranted.

## Preservation note

This file preserves the substance and all finding IDs of the Claude response. Repetitive wording was compacted when transferred from the chat export; the original pasted response remains the raw capture for the session.
