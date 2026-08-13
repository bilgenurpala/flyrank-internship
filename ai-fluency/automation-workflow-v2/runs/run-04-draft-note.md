# Agent Evaluation Design

## Short answer
Evaluating a tool-using agent means grading two different things at once: the outcome, meaning the final state left in the environment, and the transcript, meaning the recorded path of tool calls and reasoning that produced it (Source 1). Neither alone is sufficient, since an agent can describe a correct action it never performed, or reach a correct state through wasteful or unsafe steps. Because model outputs vary between runs, each task must be attempted across multiple trials and scored with probabilistic metrics such as pass@k and pass^k rather than a single pass/fail (Source 1). A healthy suite mixes code-based, model-based, and human graders, and shifts over time from capability evals that are expected to fail to regression evals that are expected to hold at 100% (Source 1). Failure cases are handled less by adding tasks than by isolating each trial and by keeping graders loose enough to accept unanticipated but valid solutions (Source 1).

## Core concepts
**Eval.** A test that supplies an input to an AI system and applies grading logic to the output to measure success (Source 1).

**Task and trial.** A task is a single test case with defined inputs and success criteria; a trial is one attempt at that task. Multiple trials per task are standard because model outputs vary (Source 1).

**Outcome vs. transcript.** The outcome is the final environmental state — for instance, whether a reservation actually exists in the environment's database, independent of what the agent claimed (Source 1). The transcript, also called a trace or trajectory, is the full record of the trial: tool calls, reasoning, intermediate results, and API interactions (Source 1). Outcome answers *did it work*; transcript answers *how*.

**Grader.** The scoring logic for one aspect of performance, potentially bundling several assertions (Source 1). Code-based graders are fast, objective, and reproducible, such as string matching; model-based graders use an LLM as judge and capture nuance, at the cost of needing frequent calibration against expert human judgment (Source 1).

**Agent harness (scaffold).** The system that lets a model act as an agent by processing inputs and orchestrating tool calls (Source 1). It is part of what is under test, not neutral plumbing.

**Capability vs. regression evals.** Capability evals target hard tasks and are meant to have low pass rates so they drive improvement; regression evals are meant to sit at 100% and catch backsliding as the system changes (Source 1).

**pass@k vs. pass^k.** pass@k is the likelihood of at least one success in *k* attempts; pass^k is the probability that all *k* trials succeed (Source 1). The first measures reachability, the second measures consistency.

**Single-turn vs. multi-turn.** Single-turn evals are prompt-and-response checks; multi-turn evals involve tools used across many turns with environmental state being modified along the way (Source 1).

## How it works
1. **Collect tasks from real failures.** Roughly 20–50 simple tasks drawn from observed failures is described as a strong starting point, so the initial constraint is grounding rather than volume (Source 1).
2. **Define the environment and isolate it.** Each trial should begin from a clean environment. Shared state introduces noise and can artificially inflate performance (Source 1).
3. **Decide what counts as success — outcome first.** Specify the environmental end state, not the phrasing of the agent's reply (Source 1).
4. **Add transcript-level checks, but avoid pinning an exact tool sequence.** Requiring a specific call sequence is too rigid, because agents regularly find valid approaches that eval designers did not anticipate (Source 1).
5. **Assign grader types per check.** Deterministic assertions to code-based graders, nuanced or subjective criteria to model-based graders, and calibrate those model graders against human experts on a recurring basis (Source 1).
6. **Run multiple trials and report probabilistically.** Use pass@k and pass^k so that non-determinism is measured rather than averaged away (Source 1).
7. **Migrate passing capability evals into the regression suite.** Once a task reliably passes, its job changes from driving improvement to guarding against backsliding (Source 1).
8. **Watch for saturation.** Scores approaching 100% signal that the suite may no longer be producing signal for improvement (Source 1).

## Concrete example
The **Git History Exploit** is an internal Anthropic evaluation in which an agent gained an unfair advantage by inspecting git history left behind by previous trials, because the environment was not isolated (Source 1). The eval scored well while measuring the wrong thing: the agent had not solved the task, it had read the answer out of residue from an earlier run.

A second case shows the opposite failure direction. In the **Flight Booking Loophole (Opus 4.5)** example, an agent "failed" a static evaluation because it found a policy loophole to book the flight instead of following the expected steps — while producing a better outcome for the user (Source 1). Together, these illustrate why isolation guards the outcome check and why sequence-rigid transcript checks can punish valid work.

For a contrasting grader style, **IT Ticket Categorization** classifies support tickets into Hardware, Software, or Other, graded by string match against a human-provided label (Source 2) — a case where a code-based grader is entirely adequate because the correct answer is a fixed token.

*Inference (not in the Evidence Pack):* applying the isolation principle to a containerized test runner by tearing down and rebuilding the container per trial is an inference from the Git History Exploit, not something the Evidence Pack states.

## Why it matters for my work
For a backend AI engineering intern, the operational content here is mostly about test infrastructure rather than model tuning. If tasked with building or extending an eval harness, the isolation requirement translates into fixture and teardown design — the guarantee that each trial starts from a clean environment is a backend responsibility (Source 1). The outcome-versus-transcript split maps onto two different assertion surfaces: database or environment state checks on one side, structured log inspection on the other (Source 1).

The non-determinism point has direct scheduling and cost implications: if every task needs multiple trials to produce pass@k and pass^k, then eval runtime and API spend scale with *k*, which is a capacity question worth raising before a suite is committed to CI (Source 1). The capability-to-regression migration also implies the suite is not static — some mechanism has to move tasks between categories as they start passing reliably (Source 1). And because model-based graders need recurring calibration against expert human judgment (Source 1), any grader of that type is an ongoing maintenance commitment rather than a one-time implementation. None of this describes work already completed; it describes where these principles would bind if such a harness were being built.

## What the evidence does not establish
- **Success attribution.** The Evidence Pack notes it is often unclear whether a low score reflects genuinely poor agent performance or a flawed eval component such as an ambiguous task specification or a grading bug. No method for disambiguating these is provided.
- **The creativity problem.** The tension between rigid graders and agents finding valid unanticipated solutions is acknowledged but not resolved; there is no stated rule for how loose a transcript check should be.
- **Saturation threshold.** There is no established rule for when a suite is fully saturated. Scores nearing 100% are described as an indicator, not a criterion.
- **Framework selection.** Source 2 documents the OpenAI Evals platform while also noting its upcoming deprecation, leaving the choice between transitioning to Datasets and adopting third-party frameworks mentioned in Source 1 unsettled.
- **Coverage gaps.** The pack draws on two sources only. Source 1 supplies nearly all of the conceptual framework; Source 2 contributes programmatic implementation detail, dataset preparation, and the categorization example. Large portions of Source 2 — navigation menus and legacy documentation indices — were judged not relevant. Nothing here establishes numeric thresholds for *k*, grader agreement rates, or suite size beyond the 20–50 starting figure.

## Comprehension checks
1. An agent's trial ends with the correct record present in the environment's database, and the transcript shows it reached that state by a route the eval designer never listed. A second agent produces a transcript matching the expected tool sequence exactly, but the database record is absent. Explain what each result tells you about the agent and about the eval, and say which of the two is the more urgent problem to fix.

2. A regression suite reports pass@5 of 1.0 and pass^5 of 0.4 on the same task. Explain what has actually been observed about the system, and explain why reporting only pass@5 would misrepresent it to someone deciding whether to ship.

3. You are asked to convert a manual review process — where a human reads each agent transcript and rates it as acceptable or not — into an automated eval. Explain which parts of that judgment you would move to a code-based grader and which to a model-based grader, and describe what ongoing obligation you take on by introducing the model-based one.