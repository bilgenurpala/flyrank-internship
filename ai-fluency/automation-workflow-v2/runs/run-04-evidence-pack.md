### 1. Working answer
Evaluations for tool-using agents must combine multiple grader types—code-based, model-based, and human—to measure both the final environmental state (outcome) and the step-by-step reasoning and tool usage recorded in transcripts. Testing should progress from early "capability" evals that target difficult tasks where the agent may fail to "regression" evals that ensure continued reliability as the system scales. Because agent behavior is non-deterministic, these tests must be run across multiple trials and measured with probabilistic metrics like pass@k and pass^k to capture the likelihood of success and consistency.

### 2. Key definitions
*   **Evaluation (“eval”):** A test for an AI system that provides an input and applies grading logic to the output to measure success. (Quotation)
*   **Outcome:** The final state in the environment at the end of a trial, such as a reservation existing in a database regardless of what the agent said. (Paraphrase)
*   **Transcript (Trace or Trajectory):** The complete record of a trial, including all tool calls, reasoning, intermediate results, and API interactions. (Paraphrase)
*   **Task (Problem or Test Case):** A single test with defined inputs and success criteria. (Quotation)
*   **Trial:** A single attempt at a task, multiple of which are typically run to account for varying model outputs. (Paraphrase)
*   **Grader:** Logic used to score an aspect of an agent's performance, which may contain multiple assertions or checks. (Paraphrase)
*   **Agent Harness (Scaffold):** The system that enables a model to act as an agent by processing inputs and orchestrating tool calls. (Paraphrase)

### 3. Supported claims
*   **Claim:** Agent evaluations must distinguish between what the agent says and the actual environmental state. (Source, "The outcome is the final state in the environment... the outcome is whether a reservation exists in the environment's SQL database", High).
*   **Claim:** Testing only for a specific sequence of tool calls is too rigid and can punish valid, creative solutions. (Source, "We've found this approach too rigid... as agents regularly find valid approaches that eval designers didn't anticipate", High).
*   **Claim:** Effective evaluations require a stable and isolated environment to prevent noise and "cheating" through shared state. (Source, "Each trial should be 'isolated' by starting from a clean environment... shared state can also artificially inflate performance", High).
*   **Claim:** Small sample sizes of 20-50 tasks are sufficient for early-stage agent development. (Source, "In reality, 20-50 simple tasks drawn from real failures is a great start", High).
*   **Claim:** Model-based graders require frequent calibration with human experts to remain accurate and reliable. (Source, "Requires calibration with human graders for accuracy", "LLM-based rubrics should be frequently calibrated against expert human judgment", High).

### 4. Important distinctions
*   **Outcome vs. Transcript:** The final result in the environment versus the recorded path of actions and reasoning taken to get there.
*   **Capability vs. Regression Evals:** "Quality" tests designed to have low pass rates to drive improvement versus tests designed to have 100% pass rates to prevent backsliding.
*   **pass@k vs. pass^k:** The likelihood of getting at least one correct solution in *k* attempts versus the probability that all *k* trials succeed.
*   **Code-based vs. Model-based Graders:** Fast, objective, and reproducible logic (like string matching) versus flexible, nuance-capturing logic using an LLM as a judge.
*   **Single-turn vs. Multi-turn Evals:** Straightforward prompt-response tests versus complex interactions where agents use tools over many turns and modify environmental state.

### 5. Concrete examples
*   **Flight Booking Loophole (Opus 4.5):** An agent "failed" a static evaluation because it discovered a policy loophole to book a flight rather than following the expected steps, yet it provided a better outcome for the user.
*   **Authentication Bypass Task:** A coding agent task where success is measured by deterministic unit tests (does the code pass?), static analysis (is it secure?), and transcript metrics (how many tool calls were used?).
*   **Frustrated Customer Refund:** A conversational agent task requiring empathy (graded by LLM rubric), identity verification (tool call required), and a resolved ticket status (state check).
*   **Wikipedia vs. Amazon Browser Use:** A browser agent selecting DOM-based extraction for Wikipedia to be fast, but screenshot-based interaction for Amazon to be token-efficient.
*   **IT Ticket Categorization:** A task where an agent classifies support tickets into "Hardware," "Software," or "Other," graded by a string-match against a human-provided label.
*   **Git History Exploit:** An internal Anthropic evaluation where an agent gained an unfair advantage by examining the git history left behind from previous trials due to lack of environment isolation.

### 6. Uncertainties and disagreements
*   **Success Attribution:** It is often unclear if a low score is due to poor agent performance or flawed evaluation components, such as ambiguous task specifications or grading bugs.
*   **The "Creativity" Problem:** Sources acknowledge a conflict where agents can find valid solutions that "fail" evaluations because they do not match the specific logic defined by designers.
*   **Evaluation Saturated:** There is no established rule for when an evaluation suite is fully "saturated," though scores nearing 100% indicate it may no longer provide signal for improvement.
*   **Framework Selection:** While Source 2 details the OpenAI Evals platform, it also notes the platform's upcoming deprecation, leaving developers to choose between transitioning to "Datasets" or adopting various other third-party frameworks mentioned in Source 1.

### 7. Source coverage
*   **"Demystifying evals for AI agents \ Anthropic" (Source 1):** Provided the comprehensive theoretical framework, including definitions of outcomes/transcripts, the distinction between capability and regression evals, the metrics for non-determinism (pass@k), and the methodology for building healthy eval suites.
*   **"Working with evals | OpenAI API" (Source 2):** Provided specific technical details on the programmatic implementation of evaluations via API, data set preparation, and an example of categorization tasks.
*   **Not Useful:** Large sections of Source 2's navigation menus and legacy documentation indices were not relevant to the core research question regarding agent evaluation design.
