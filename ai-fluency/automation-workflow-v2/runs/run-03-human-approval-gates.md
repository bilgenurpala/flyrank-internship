# Run 03 — Human Approval Gates

## Run Metadata

- Date: 2026-08-13
- Research question: When should a tool-using system stop for human approval, and what makes that gate meaningful?
- Manual baseline start/end: Not repeated
- Evidence extraction time: 29.07 seconds
- Workflow start/end: Not timed end-to-end
- Human review time:

## Manual Baseline Output

Not repeated. The comparable manual baseline is recorded in Run 01.

## Evidence Pack

[Raw NotebookLM Evidence Pack](run-03-evidence-pack.md)

## Draft Note

[Raw Claude Draft Note](run-03-draft-note.md)

## Critique Report

[Raw Claude Critique Report](run-03-critique-report.md)

## Final Study Note and Change Log

[Raw Claude Final Study Note](run-03-final-study-note.md)

## Human Review Record

Approved. The reviewer independently identified the two supported conditions for a meaningful gate: a clear visual indication when a tool is invoked and disclosure of the tool inputs before the server call. She correctly kept the tool-exposure interface separate from those conditions and connected pre-call disclosure to the stated data-exfiltration risk.

The reviewer also identified why the scope question remains unresolved. The Evidence Pack separately describes an always-available human denial capability and confirmation prompts for sensitive operations, does not reconcile those scopes, does not define "sensitive," and exports no usable source references. Without returning to the original documents and their protocol versions, the run cannot determine whether the tension exists in the sources or was introduced when the Evidence Pack was assembled.

Decision: Approved without further revision.

## Observed Failures

- NotebookLM displayed clickable citations in the interface but removed them from the copied response, repeating the export failure.
