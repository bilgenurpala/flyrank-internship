# Run 01 — Workflow vs Agent

## Run Metadata

- Date: 2026-08-13
- Research question: What distinguishes a predefined AI workflow from an agent, and when is each appropriate?
- Manual baseline reading time: 15 minutes
- Manual baseline writing time: 20 minutes
- Manual baseline total: 35 minutes
- Evidence extraction start: 2026-08-13 08:09:50 TRT
- Evidence extraction end: 2026-08-13 08:11:16 TRT
- Evidence extraction elapsed time: 1 minute 26 seconds
- Claude structured synthesis timing re-run: 34.29 seconds
- Claude evidence critique timing re-run: 45.59 seconds
- Claude controlled revision timing re-run: 37.87 seconds
- Claude stages total: 117.75 seconds (1 minute 57.75 seconds)
- Measured model execution total: 203.75 seconds (3 minutes 23.75 seconds)
- Workflow start/end: Complete
- Human review time: Not timed

## Manual Baseline Output

Completed in 35 minutes: 15 minutes reading the two selected sources and 20 minutes manually selecting, reorganizing, and editing copied passages into notes. The retained outputs are:

- [Notes — Building Effective Agents](manual-baseline/notes-building-effective-agents.md)
- [Notes — Trustworthy Agents in Practice](manual-baseline/notes-trustworthy-agents-in-practice.md)

The `~20 min` labels inside the notes are informal estimates. The measured baseline used for comparison is 35 minutes total.

## Evidence Pack

[Raw NotebookLM Evidence Pack](run-01-evidence-pack.md)

## Draft Note

[Raw Claude Draft Note](run-01-draft-note.md)

## Critique Report

[Claude Critique Report](run-01-critique-report.md)

## Final Study Note and Change Log

[Final Study Note and Change Log](run-01-final-study-note.md)

## Human Review Record

**Source sample checked:** The workflow/agent distinction and the remaining unsupported sentence in the coding-agent example.

**Claims checked against original sources:** The central architectural distinction was explained correctly from the retained source notes. Precise NotebookLM citation locations remain unverified.

**Unsupported additions found:** The final note added that the pull-request description does not provide the files as a fixed sequence. The Evidence Pack did not explicitly establish this, so the sentence was removed.

**Critique suggestions rejected:** Optional examples and unsupported additions were not added.

**Comprehension check result:** Passed. In the reviewer's own explanation, a workflow follows a predefined orchestration path, while an agent dynamically controls its own process and tool usage. This pipeline is a workflow because NotebookLM → Evidence Pack → Draft Note → Critique → Revision is fixed in advance and each transition is initiated by the human rather than selected by the model. It combines prompt chaining with an evaluator-optimizer stage.

**Important nuance:** The path is manually orchestrated rather than encoded as an automated code path. It still belongs on the workflow side because control does not move to the model.

**Corrections made:** Removed the unsupported fixed-file-sequence sentence from the coding-agent example.

**Decision:** Approved after correction.

**Reason:** The final note now stays within the Evidence Pack, retains its citation limitation, and the reviewer can explain and apply the central distinction without reading the generated answer.

## Observed Failures

- NotebookLM displayed clickable numbered citations, but its copy-response action stripped the citation markers from the exported text. In the Supported Claims section this produced blank `Source:` fields, so the handoff is not self-contained without manual citation repair.
- The original Claude stages were not timed. The recorded Claude durations come from a timing re-run with the same Run 01 input and prompts; they are not reconstructed estimates of the original run.
- Manual handoff, file-storage, and human-review time were not timed, so 3 minutes 23.75 seconds is measured model execution, not total workflow duration.
