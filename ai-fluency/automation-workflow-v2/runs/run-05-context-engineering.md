# Run 05 — Context Engineering for Tool-Using Systems

## Run Metadata

- Date: 2026-08-13
- Research question: How does context engineering differ from prompt engineering, and what context must a tool-using system manage?
- Manual baseline start/end: Not repeated
- Evidence extraction time: 23.65 seconds
- Workflow start/end: Not timed end-to-end
- Human review time:

## Manual Baseline Output

Not repeated. The comparable manual baseline is recorded in Run 01.

## Evidence Pack

[Raw NotebookLM Evidence Pack](run-05-evidence-pack.md)

## Draft Note

[Raw Claude Draft Note](run-05-draft-note.md)

## Critique Report

[Raw Claude Critique Report](run-05-critique-report.md)

## Final Study Note and Change Log

[Raw Claude Final Study Note](run-05-final-study-note.md)

## Human Review Record

Approved. The reviewer correctly distinguished prompt engineering as the discrete work of writing and organizing instructions from context engineering as the broader, iterative work of curating the complete token set supplied at each turn. She identified the four context categories in the Evidence Pack: system instructions, tool specifications, environmental feedback, and dynamically retrieved external data.

The reviewer explained the finite attention budget, diminishing marginal returns, and just-in-time retrieval without turning context rot into a known causal mechanism or inventing a model-specific threshold. She also kept compaction and structured note-taking as described practices rather than claiming proven effectiveness, preserved the MCP protocol boundary, and explicitly noted that four supported claims remain individually unattributed within the exported Evidence Pack.

Decision: Approved without further revision.

## Observed Failures

- NotebookLM displayed clickable citations in the interface but removed them from the copied response, repeating the export failure.
