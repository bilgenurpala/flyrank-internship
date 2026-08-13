# Run 02 — MCP Tools, Resources, and Prompts

## Run Metadata

- Date:
- Research question: How do MCP tools, resources, and prompts differ in purpose and control?
- Manual baseline start/end: Not repeated
- Evidence extraction time: 36.91 seconds
- Workflow start/end: Complete
- Human review time:

## Manual Baseline Output

Not repeated. The comparable manual baseline is recorded in Run 01.

## Evidence Pack

[Raw NotebookLM Evidence Pack](run-02-evidence-pack.md)

## Draft Note

[Raw Claude Draft Note](run-02-draft-note.md)

## Critique Report

[Raw Claude Critique Report](run-02-critique-report.md)

## Final Study Note and Change Log

[Final Study Note and Change Log](run-02-final-study-note.md)

## Human Review Record

**Comprehension check result:** Passed. In the reviewer's own explanation, MCP tools are model-controlled and called based on the user's request; resources are supplied by the application; and prompts require explicit user invocation. Tools perform actions, resources provide read-only context, and prompts provide reusable templates. The reviewer also correctly explained that resources may use fixed or parameterized URIs and that model-controlled tool use can still be gated by application approval dialogs or permissions.

**Decision:** Approved.

**Reason:** The reviewer accurately explained both the control hierarchy and functional differences, including the important qualification that model-controlled does not mean unsupervised.

## Observed Failures

- NotebookLM displayed clickable citations in the interface but removed them from the copied response, repeating the Run 01 export failure.
