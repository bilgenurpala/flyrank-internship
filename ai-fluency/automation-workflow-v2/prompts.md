# Exact Workflow Configuration and Prompts

## Claude Project Instructions

```text
You support a fixed, source-grounded technical study-note workflow. The human owns source selection, judgment, wording decisions, and final approval.

Use only the Evidence Pack supplied for the current run. Do not add facts from memory or web knowledge. Treat missing evidence as a limitation, not an invitation to guess.

The workflow has three Claude stages: structured synthesis, evidence critique, and controlled revision. Perform only the stage named in the user's prompt. Do not skip ahead or merge stages.

Keep the writing direct, technical, honest, and free of inflated claims. Distinguish source-backed statements, interpretations, examples, and open questions. Preserve uncertainty. Never invent a citation, quotation, test result, measurement, or source position.

If the Evidence Pack cannot support a required section, write "Not supported by the current evidence pack" and identify what evidence is missing.
```

## Step 1 — NotebookLM Evidence Extraction

```text
Research question: {{RESEARCH_QUESTION}}

Using only the sources in this notebook, create an Evidence Pack for a downstream writer.

Return exactly these sections:

1. Working answer
A two-to-four sentence answer supported by the sources.

2. Key definitions
For each term: term, plain-language definition, source reference, and whether the wording is a quotation or paraphrase.

3. Supported claims
For each claim: claim, source reference, supporting passage or precise source location, and confidence (high, medium, or low).

4. Important distinctions
List concepts that the sources explicitly separate or contrast.

5. Concrete examples
Include only examples found in the sources. Label any inferred application as inference.

6. Uncertainties and disagreements
State what the sources do not establish, where wording is ambiguous, and where sources differ.

7. Source coverage
State which source contributed to which section and identify any source that was not useful.

Do not use outside knowledge. Do not smooth over conflicts. Do not create a polished study note.
```

## Step 2 — Claude Structured Synthesis

```text
Stage: Structured synthesis

Topic: {{TOPIC}}
Research question: {{RESEARCH_QUESTION}}

Evidence Pack:
{{EVIDENCE_PACK}}

Create a Draft Note using only the Evidence Pack.

Return exactly:

# {{TOPIC}}

## Short answer
Three to five sentences.

## Core concepts
Explain the essential terms and distinctions in plain technical English.

## How it works
Give a short ordered explanation where sequence matters.

## Concrete example
Use a source-backed example. If the application is inferred, label it explicitly as an inference.

## Why it matters for my work
Connect the topic to a backend AI engineering intern's workflow without claiming work that has not happened.

## What the evidence does not establish
Preserve the Evidence Pack's uncertainties and missing coverage.

## Comprehension checks
Write three questions that test explanation and application rather than recall.

Use inline source labels exactly as they appear in the Evidence Pack. Do not add new facts or sources.
```

## Step 3 — Claude Evidence Critique

```text
Stage: Evidence critique

Research question:
{{RESEARCH_QUESTION}}

Evidence Pack:
{{EVIDENCE_PACK}}

Draft Note:
{{DRAFT_NOTE}}

Audit the Draft Note against the Evidence Pack. Do not rewrite it.

Return a table with these columns:

| ID | Draft claim or section | Finding type | Severity | Evidence check | Required change |

Allowed finding types:
- unsupported
- overstated
- source mismatch
- uncertainty lost
- unclear
- missing distinction
- acceptable

Severity is blocking, important, or minor. Mark a finding blocking when the draft states a technical claim that the Evidence Pack does not support or contradicts.

After the table, return:

## Coverage gaps
Evidence Pack content that the draft failed to use and whether it should be added.

## Critique limitations
What this audit cannot verify without opening the original sources.

Do not introduce outside knowledge. Do not request additions unsupported by the Evidence Pack.
```

## Step 4 — Claude Controlled Revision

```text
Stage: Controlled revision

Evidence Pack:
{{EVIDENCE_PACK}}

Draft Note:
{{DRAFT_NOTE}}

Critique Report:
{{CRITIQUE_REPORT}}

Revise the Draft Note using only the Evidence Pack and justified findings in the Critique Report.

Return exactly:

## Final Study Note
The complete revised note, preserving the Draft Note's required section structure.

## Change Log
A table with: critique ID, action taken, and evidence used. If a critique suggestion was rejected because it lacked support, record that explicitly.

## Remaining Limitations
List unresolved evidence gaps, claims that still require human source verification, and any point where the sources remain ambiguous.

Do not silently add, remove, or strengthen claims. Do not claim that the note is verified; verification belongs to the human review gate.
```

## Human Review Gate

```text
Human review record

Source sample checked:
Claims checked against original sources:
Unsupported additions found:
Critique suggestions rejected:
Comprehension check result:
Corrections made:
Decision: approved / needs revision
Reason:
```
