## Final Study Note

# Agent Evaluation Design

### Short answer
Evaluating a tool-using agent means grading two things: the outcome, meaning the final state left in the environment at the end of a trial, and the transcript, meaning the complete record of tool calls, reasoning, and intermediate results that produced it (Source 1). The Evidence Pack states these must be measured together, and that doing so requires combining multiple grader types — code-based, model-based, and human (Source 1). Because agent behavior is non-deterministic, tasks must be run across multiple trials and measured with probabilistic metrics such as pass@k and pass^k rather than a single pass/fail (Source 1). Testing should progress from early capability evals that target difficult tasks where the agent may fail, toward regression evals that ensure continued reliability as the system scales (Source 1). For failure cases the Evidence Pack supports three requirements: drawing tasks from real failures, isolating each trial from earlier ones, and avoiding transcript checks that demand a specific sequence of tool calls (Source 1).

### Core concepts
**Eval.** A test for an AI system that provides an input and applies grading logic to the output to measure success (Source 1, quotation).

**Task (problem or test case).** A single test with defined inputs and success criteria (Source 1, quotation). **Trial:** a single attempt at a task, multiple of which are typically run to account for varying model outputs (Source 1, paraphrase).

**Outcome vs. transcript.** The outcome is the final state in the environment at the end of a trial — for example, whether a reservation exists in the environment's SQL database, regardless of what the agent said (Source 1, paraphrase). The transcript, also called a trace or trajectory, is the complete record of the trial, including all tool calls, reasoning, intermediate results, and API interactions (Source 1, paraphrase). The Evidence Pack states that agent evaluations must distinguish between what the agent says and the actual environmental state (Source 1).

**Grader.** Logic used to score an aspect of an agent's performance, which may contain multiple assertions or checks (Source 1, paraphrase). The Evidence Pack names three grader types — code-based, model-based, and human (Source 1). Code-based graders are fast, objective, and reproducible, such as string matching; model-based graders are flexible and capture nuance by using an LLM as a judge (Source 1). Model-based graders require calibration with human graders for accuracy, and LLM-based rubrics should be frequently calibrated against expert human judgment (Source 1).

**Capability vs. regression evals.** Capability evals are quality tests designed to have low pass rates in order to drive improvement; regression evals are designed to have 100% pass rates to prevent backsliding (Source 1).

**pass@k vs. pass^k.** pass@k is the likelihood of getting at least one correct solution in *k* attempts; pass^k is the probability that all *k* trials succeed (Source 1).

**Single-turn vs. multi-turn evals.** Single-turn evals are straightforward prompt-response tests. Multi-turn evals cover complex interactions where agents use tools over many turns and modify environmental state (Source 1). Because multi-turn trials change the environment, they bear directly on the isolation requirement: each trial should start from a clean environment, since shared state introduces noise and can artificially inflate performance (Source 1).

The Evidence Pack also defines the **agent harness (scaffold)** as the system that enables a model to act as an agent by processing inputs and orchestrating tool calls (Source 1, paraphrase). It does not state what role the harness plays in evaluation, so nothing further is claimed about it here.

### How it works
1. **Collect tasks from real failures.** The Evidence Pack states that 20–50 simple tasks drawn from real failures is a great start for early-stage agent development (Source 1).
2. **Isolate each trial.** Each trial should start from a clean environment; shared state introduces noise and can artificially inflate performance (Source 1).
3. **Define success against the environmental outcome.** Specify the final state in the environment rather than what the agent reports (Source 1).
4. **Add transcript-level checks without pinning an exact tool sequence.** Testing only for a specific sequence of tool calls is too rigid, as agents regularly find valid approaches that eval designers didn't anticipate (Source 1).
5. **Assign grader types per check.** Use code-based graders where the logic is objective and reproducible, model-based graders where nuance is required, and calibrate model-based rubrics frequently against expert human judgment (Source 1).
6. **Run multiple trials and report probabilistically.** Use pass@k and pass^k so that non-determinism is measured rather than collapsed into a single result (Source 1).
7. **Let the suite progress from capability toward regression evals.** Testing should progress from early capability evals that target difficult tasks where the agent may fail, to regression evals that ensure continued reliability as the system scales (Source 1). This is stated as a progression of the suite over the development lifecycle; the Evidence Pack describes no procedure for reclassifying individual tasks.
8. **Treat saturation as an open question.** The Evidence Pack states there is no established rule for when an evaluation suite is fully saturated, though scores nearing 100% indicate it may no longer provide signal for improvement (Source 1).

### Concrete example
**Authentication Bypass Task.** A coding agent task where success is measured on three layers at once: deterministic unit tests (does the code pass?), static analysis (is it secure?), and transcript metrics (how many tool calls were used?) (Source 1). This is the Evidence Pack's clearest single-task illustration of outcome, static-analysis, and transcript checks operating together.

**Frustrated Customer Refund.** A conversational agent task requiring empathy graded by an LLM rubric, identity verification requiring a tool call, and a resolved ticket status checked as state (Source 1). It shows a model-based grader working alongside a state check on the same task.

**Git History Exploit.** An internal Anthropic evaluation in which an agent gained an unfair advantage by examining the git history left behind from previous trials, due to lack of environment isolation (Source 1).

**Flight Booking Loophole (Opus 4.5).** An agent "failed" a static evaluation because it discovered a policy loophole to book a flight rather than following the expected steps, yet it provided a better outcome for the user. *(Source attribution is an inference: the Evidence Pack labels no examples by source, and its source-coverage section assigns the theoretical framework to Source 1.)*

**IT Ticket Categorization.** An agent classifies support tickets into "Hardware," "Software," or "Other," graded by a string-match against a human-provided label (Source 2).

*Inference (not in the Evidence Pack):* applying the isolation requirement by tearing down and rebuilding a container per trial is an inference drawn from the Git History Exploit, not something the Evidence Pack states.

### Why it matters for my work
For a backend AI engineering intern, the supported content here concerns how an eval suite is structured rather than how a model is tuned. Two Evidence Pack requirements bear most directly on backend work: each trial should start from a clean environment (Source 1), and outcome checks should target the environmental state rather than the agent's reported answer (Source 1). The outcome/transcript distinction defines what there is to check — the final environment state on one side, the recorded tool calls and reasoning on the other (Source 1). The calibration requirement on model-based graders is likewise ongoing rather than one-time, since LLM-based rubrics should be frequently calibrated against expert human judgment (Source 1).

*Implementation inferences (not stated in the Evidence Pack):* translating the isolation requirement into fixture and teardown design, and translating the outcome/transcript split into two distinct assertion surfaces — state assertions against the environment, and structured inspection of the recorded trial — are inferences about how these requirements might be built, not source claims.

*Further inference (not stated in the Evidence Pack, and carrying no source label):* if every task requires multiple trials to produce pass@k and pass^k, eval runtime and API spending would scale with the number of trials, raising capacity and scheduling questions before a suite is placed in continuous integration. The Evidence Pack says nothing about runtime, cost, capacity, or CI.

Nothing above describes work already completed; it describes where these requirements would apply if such a harness were being built.

### What the evidence does not establish
- **Success attribution.** It is often unclear whether a low score is due to poor agent performance or flawed evaluation components, such as ambiguous task specifications or grading bugs (Source 1).
- **The "creativity" problem.** Sources acknowledge a conflict where agents can find valid solutions that "fail" evaluations because they do not match the specific logic defined by designers (Source 1). The conflict is stated but not resolved, and no rule is given for how loose a transcript check should be.
- **Saturation.** There is no established rule for when an evaluation suite is fully saturated; scores nearing 100% are given as an indicator, not a criterion (Source 1).
- **Framework selection.** Source 2 details the OpenAI Evals platform while also noting the platform's upcoming deprecation, leaving developers to choose between transitioning to "Datasets" or adopting various other third-party frameworks mentioned in Source 1.
- **Agent harness.** The Evidence Pack defines the harness but does not state what role it plays in evaluation.
- **Coverage.** The Evidence Pack draws on two sources. Source 1 supplied the theoretical framework — outcome/transcript definitions, the capability/regression distinction, the non-determinism metrics, and suite-building methodology. Source 2 supplied programmatic implementation detail, dataset preparation, and a categorization example. Large sections of Source 2 (navigation menus and legacy documentation indices) were judged not relevant. No numeric threshold for *k*, no grader agreement rate, and no suite size beyond the 20–50 early-stage starting figure appear anywhere in the pack.

### Comprehension checks
1. An agent's trial ends with the correct record present in the environment's database, and the transcript shows it reached that state by a route the eval designer never listed. A second agent produces a transcript matching the expected tool sequence exactly, but the database record is absent. Explain what each result tells you about the agent and about the eval, and identify which Evidence Pack requirement each case bears on.
2. A suite reports pass@5 of 1.0 and pass^5 of 0.4 on the same task. Using the Evidence Pack's definitions, explain what has been observed about the system, and explain why reporting only pass@5 would misrepresent it to someone deciding whether to ship.
3. You are asked to convert a manual review process — where a human reads each agent transcript and rates it acceptable or not — into an automated eval. Explain which parts of that judgment you would route to a code-based grader and which to a model-based grader, and describe what ongoing obligation the Evidence Pack attaches to introducing a model-based grader.

## Change Log

| Critique ID | Action taken | Evidence used |
|---|---|---|
| C-01 | Removed "Neither alone is sufficient" and the "wasteful or unsafe steps" rationale from the Short answer. Retained the supported requirement that outcome and transcript be measured together using multiple grader types. | §1 (combine grader types; measure outcome and transcript); §3 Claim 1 (what the agent says vs. environmental state). |
| C-02 | Removed the comparison prioritizing isolation and grader flexibility over adding tasks. The Short answer now lists task sourcing, isolation, and transcript-check flexibility as three requirements with no ranking. | §3 Claims 2, 3, 4 — each stated independently; the Evidence Pack contains no ranking among them. |
| C-03 | Deleted "It is part of what is under test, not neutral plumbing." Retained only the §2 definition, and recorded the Evidence Pack's silence on the harness's evaluative role under "What the evidence does not establish." | §2 Agent Harness (Scaffold) definition; absence of any Evidence Pack statement on harness evaluation. |
| C-04 | Added human graders to the grader definition so that the calibration requirement resolves against a defined term. | §1 (code-based, model-based, and human); §3 Claim 5. |
| C-05 | Retained the pass@k / pass^k entry as defined; dropped the non-Pack gloss "reachability." | §4 definitions. |
| C-06 | Retained the 20–50 figure with its early-stage-development scope. Removed the added gloss "the initial constraint is grounding rather than volume." | §3 Claim 4. |
| C-09 | Replaced per-task migration with suite-level progression from capability toward regression evals, and stated that no task-reclassification procedure appears in the Evidence Pack. Removed the "some mechanism has to move tasks between categories" claim from "Why it matters." No migration mechanism invented. | §1 (progression from capability to regression evals); §4 (the two types distinguished by intended pass rates). |
| C-10 | Qualified saturation in step 8 with the Evidence Pack's statement that no established rule exists. | §6 Evaluation Saturated. |
| C-11 | Reduced the Git History Exploit to an unfair advantage caused by git history left behind from previous trials under lack of isolation. Removed the claims that the eval scored well, that the answer was present in the history, and that the agent had not solved the task. | §5 Git History Exploit. |
| C-12 | Removed the (Source 1) label from the Flight Booking Loophole example and marked its attribution explicitly as an inference. Retained Source 1 on the Anthropic-internal Git History Exploit and Source 2 on IT Ticket Categorization, both resting on §7's source-coverage descriptions. | §5 (no source labels on examples); §7 source coverage. |
| C-13 | Removed "entirely adequate" and the added explanation about fixed-token answers; the example now reports only the grading method described. | §5 IT Ticket Categorization. |
| C-14 | Marked runtime, API spending, capacity, and CI as inference in a labeled block with no source attribution, and stated that the Evidence Pack says nothing on these topics. | §1 and §4 support only the multiple-trials premise; no Evidence Pack content on cost, runtime, capacity, or CI. |
| C-15 | Moved fixture design, teardown, structured-log inspection, and assertion surfaces into a labeled implementation-inference block with no source labels. Source labels retained only on the isolation and outcome/transcript requirements themselves. | §3 Claim 3 (isolation); §4 (outcome vs. transcript). |
| C-16 | No change; the statement that no work is being claimed as completed was retained. | Stage constraint; no Evidence Pack conflict. |
| C-17 | No change of substance; all four §6 uncertainties and the §7 coverage note remain, with the creativity and saturation bullets carrying their hedges explicitly. | §6; §7. |
| C-18 | Restored (quotation) / (paraphrase) markers on definitions carried from §2. Confidence ratings not restored: all five §3 claims are rated High uniformly, so per-claim tagging adds no discrimination. Recorded as partial application rather than rejection. | §2 markers; §3 uniform High ratings. |
| C-19 | Comprehension checks retained; questions 1 and 3 now anchor explicitly to Evidence Pack requirements so both test application rather than recall. | §3 Claims 1, 3, 5; §4 definitions. |
| Coverage gap — Authentication Bypass | Added as the lead concrete example. | §5 Authentication Bypass Task. |
| Coverage gap — Frustrated Customer Refund | Added briefly as the only Evidence Pack illustration of a model-based grader operating alongside a state check. | §5 Frustrated Customer Refund. |
| Coverage gap — multi-turn / state modification | Connected the single-turn vs. multi-turn distinction to environmental-state modification and to the isolation requirement. | §4 (multi-turn agents modify environmental state); §3 Claim 3. |
| Coverage gap — Wikipedia vs. Amazon | **Rejected.** The critique marked this optional. The Evidence Pack presents it as a tool-strategy choice framed by speed and token efficiency; linking it to the "too rigid" claim would be this note's own connection, not a stated one. Omitted rather than added under an inference label. | §5 Wikipedia vs. Amazon Browser Use; §3 Claim 2 — no stated link between them. |
| Coverage gap — Source 2 body contribution | **Rejected as an addition.** The critique itself judged no addition required, since §7 assigns the framework to Source 1. Source 2's contribution remains the categorization example and the coverage note. | §7 source coverage. |

## Remaining Limitations

**Unresolved evidence gaps.** The Evidence Pack sets no numeric threshold for *k*, no target agreement rate between model-based and human graders, no calibration frequency beyond "frequently," and no suite size beyond the 20–50 early-stage starting figure. It gives no rule for how loose a transcript check should be, no method for separating poor agent performance from a flawed eval component, and no established saturation criterion. It says nothing about what role the agent harness plays in evaluation, and nothing about eval runtime, cost, capacity, or continuous integration — which is why those consequences appear only as labeled inference.

**Requiring human source verification.** Whether the Evidence Pack's quotations are accurate to Source 1 and Source 2, and whether the ellipses in §3 omit qualifying conditions — particularly around the 20–50 task figure and the isolation claim. Whether the §2 paraphrased definitions preserve the originals' scope, including the harness definition. Whether the six §5 examples originate where this note's labels place them: §5 carries no source labels, so the Flight Booking attribution is marked as inference, and the Git History and IT Ticket attributions rest on §7's general descriptions rather than explicit per-example labels. Whether the "High" confidence ratings in §3 were assigned by a stated method.

**Points where the sources remain ambiguous.** The framework-selection question is unresolved within the Evidence Pack itself: Source 2 documents the OpenAI Evals platform while noting its upcoming deprecation, and the pack does not indicate whether this has since changed. Because §7 records that large sections of Source 2 were set aside as not relevant, silence in the Evidence Pack is not evidence of silence in the underlying sources — the gaps listed above are Evidence Pack gaps, not established source gaps.

This note has not been verified against the original sources; verification belongs to the human review gate.