# Run 01 — NotebookLM Evidence Pack

## 1. Working answer

The primary distinction lies in architectural control: **workflows** orchestrate LLMs through **predefined code paths**, while **agents** allow LLMs to **dynamically direct their own processes** and tool usage. Workflows are appropriate for well-defined tasks requiring predictability and consistency, whereas agents are suited for open-ended problems where required steps cannot be predicted or hardcoded. While both systems can improve task performance, they typically trade off increased latency, cost, and a higher risk of unintended consequences.

## 2. Key definitions

- **Agentic systems**: A broad category encompassing both prescriptive implementations (workflows) and autonomous systems (agents). (Paraphrase)
- **Workflows**: Systems where "LLMs and tools are orchestrated through predefined code paths". (Quotation)
- **Agents**: Systems where "LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks". (Quotation)
- **Self-directed loop**: A process where an agent operates by planning, acting, observing results, and adjusting until a task is complete or human input is required. (Paraphrase)
- **Harness**: The "instructions, and the guardrails, that the model operates under". (Quotation)
- **Plan Mode**: A feature where an agent shows an "intended plan of action up-front" for user review rather than asking for step-by-step approval. (Paraphrase)

## 3. Supported claims

- **Claim**: Workflows offer higher predictability and consistency for well-defined tasks compared to agents. (Source:; Confidence: High)
- **Claim**: Agents are the better option when flexibility and model-driven decision-making are required at scale. (Source:; Confidence: High)
- **Claim**: Agentic systems often trade latency and cost for better task performance. (Source:; Confidence: High)
- **Claim**: The autonomy of agents introduces new risks, including misreading user intent and vulnerability to prompt injection attacks. (Source:; Confidence: High)
- **Claim**: Designing effective agents requires prioritizing simplicity, transparency, and thorough tool documentation (the Agent-Computer Interface). (Source:; Confidence: High)

## 4. Important distinctions

- **Predefined paths vs. Dynamic direction**: Workflows follow code-governed steps; agents decide how to achieve goals.
- **Fixed subtasks vs. Input-dependent subtasks**: In parallelization workflows, subtasks are pre-defined; in orchestrator-worker workflows, the orchestrator determines subtasks dynamically based on specific input.
- **Step-level oversight vs. Strategic oversight**: Standard interfaces require approval for individual actions, whereas "Plan Mode" shifts oversight to the overall strategy.
- **Model vs. Harness vs. Tools vs. Environment**: Agents are not just models; they are composed of the model (intelligence), harness (instructions/guardrails), tools (applications), and environment (access/deployment context).

## 5. Concrete examples

- **Prompt chaining (Workflow)**: Generating marketing copy and then translating it into a different language.
- **Routing (Workflow)**: Directing general customer service questions to smaller models and complex technical queries to more capable models.
- **Parallelization (Workflow)**: Using one model instance to process a user query while another simultaneously screens it for guardrail violations.
- **Evaluator-optimizer (Workflow)**: An iterative process where one LLM generates a literary translation and another provides critiques for refinement.
- **Coding Agent (Agent)**: Resolving SWE-bench tasks by autonomously editing multiple files based on a pull request description.
- **Computer Use (Agent)**: Claude using a computer to accomplish tasks via a reference implementation.
- **Subagents (Agentic Coordination)**: "Claudes" working in parallel on different parts of a complex task (Inference: This represents a coordination pattern for scaling agentic work).
- **Expense Submission (Agent)**: Planning steps to transcribe receipts, pull data, and autonomously checking company policy when a charge exceeds a nightly cap.

## 6. Uncertainties and disagreements

- **Terminological inconsistency**: The sources note that the term "agent" is defined in several ways by different users, ranging from fully autonomous systems to prescriptive workflows.
- **Lack of standardized benchmarks**: There is currently no rigorous, industry-wide way to compare agent systems regarding their resistance to prompt injection or reliability in surfacing uncertainty.
- **Security limits**: The sources explicitly state that even combined layers of defense (training, monitoring, red-teaming) are "not a guarantee" against prompt injection.
- **The "Unsolved Problem" of Goal Alignment**: Finding the exact balance between an agent pausing too often for clarification (causing friction) and not often enough (risking misinterpretation) remains an unsolved challenge.

## 7. Source coverage

- **"Building Effective AI Agents" (Source 1)**: Primary contributor to architectural distinctions, detailed workflow patterns, and the core principles of simplicity and ACI design.
- **"Trustworthy agents in practice" (Source 2)**: Primary contributor to the definition of the self-directed loop, the four-layer agent composition, specific risks, and control mechanisms like Plan Mode.
- **Non-useful sources**: Both sources provided significant, complementary information.

## Capture Note

NotebookLM displayed clickable numbered citations in the interface. Its copy-response function removed those citation markers and left blank `Source:` fields in the copied Supported Claims section. The screenshot preserves the visible interface state, but this output does not satisfy the intended citation-preserving handoff without manual repair.
