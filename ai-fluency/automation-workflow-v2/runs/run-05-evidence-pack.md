### 1. Working answer
Prompt engineering is the discrete task of writing and organizing instructions to achieve optimal model outputs, whereas **context engineering** is an iterative, broader process of curating the holistic set of tokens—including prompts, tool definitions, and message history—passed to a model at each turn. A tool-using system must manage a diverse "attention budget" consisting of system instructions, tool specifications, environmental feedback (such as tool results), and dynamically retrieved external data to maintain coherence and accuracy.

### 2. Key definitions
*   **Context**: "The set of tokens included when sampling from a large-language model (LLM)". (Quotation)
*   **Context Engineering**: Strategies for "curating and maintaining the optimal set of tokens" during inference, including instructions, tools, external data, and history. (Quotation)
*   **Prompt Engineering**: Methods for writing and organizing the specific instructions (often system prompts) intended to guide LLM behavior. (Paraphrase)
*   **Context Rot**: A phenomenon where a model's ability to accurately recall information decreases as the token count in the context window increases. (Paraphrase)
*   **MCP Host**: "The AI application that coordinates and manages one or multiple MCP clients". (Quotation)
*   **MCP Server**: "A program that provides context to MCP clients". (Quotation)
*   **Compaction**: The practice of summarizing a conversation nearing the context window limit and reinitiating a new window with only that summary and critical details. (Paraphrase)

### 3. Supported claims
*   **Claim**: Context is a finite resource with diminishing marginal returns due to LLM architectural constraints.
    *   **Source**:.
    *   **Supporting Passage**: "Context, therefore, must be treated as a finite resource with diminishing marginal returns... LLMs have an 'attention budget' that they draw on when parsing large volumes of context."
    *   **Confidence**: High.
*   **Claim**: Tool definitions and specifications require as much prompt engineering attention as the overall system prompts.
    *   **Source**:.
    *   **Supporting Passage**: "Tool definitions and specifications should be given just as much prompt engineering attention as your overall prompts."
    *   **Confidence**: High.
*   **Claim**: Models perform better when complex tasks are divided into separate LLM calls (parallelization) rather than one call handling all considerations.
    *   **Source**:.
    *   **Supporting Passage**: "LLMs generally perform better when each consideration is handled by a separate LLM call, allowing focused attention on each specific aspect."
    *   **Confidence**: High.
*   **Claim**: Just-in-time context loading (using lightweight identifiers like file paths) is more efficient than loading full data objects upfront.
    *   **Source**:.
    *   **Supporting Passage**: "The model can write targeted queries... without ever loading the full data objects into context... This self-managed context window keeps the agent focused on relevant subsets."
    *   **Confidence**: High.

### 4. Important distinctions
*   **Workflows vs. Agents**: Workflows use "predefined code paths" to orchestrate LLMs, while agents are systems where LLMs "dynamically direct their own processes and tool usage".
*   **Discrete vs. Iterative**: Prompting is a "discrete task," whereas context engineering is "iterative" and occurs each time a decision is made about what to pass to the model.
*   **Local vs. Remote MCP Servers**: Local servers use STDIO transport for processes on the same machine; remote servers use Streamable HTTP transport for communication across a network.
*   **Prompting vs. Context Engineering focus**: Prompting focuses on "finding the right words," while context engineering focuses on the broader "configuration of context".

### 5. Concrete examples
*   **Visual Studio Code**: Acts as an MCP host to manage multiple clients, such as a Sentry server and a local filesystem server.
*   **Claude Code**: Uses a "hybrid model" where it naively loads `CLAUDE.md` files but uses tools like `grep` and `glob` to retrieve other files just-in-time.
*   **Claude plays Pokémon**: An agent that uses structured note-taking to track precise game steps and combat strategies over thousands of turns.
*   **Absolute Filepaths**: An example of tool optimization where changing relative paths to absolute paths solved a model failure mode during code editing.
*   **Weather_current Tool**: A specific tool discovery example showing how a server provides a "name," "description," and "inputSchema" (like city and units) to a client.

### 6. Uncertainties and disagreements
*   **Quantifying "Finite"**: The sources state context is finite but do not provide specific token limits where "rot" or "pollution" definitively begins for any particular model.
*   **Optimal Altitude**: The sources define the "right altitude" for prompts as a balance between "brittle" and "vague" guidance but acknowledge this is a subjective "Goldilocks zone".
*   **Usage Dictation**: The Model Context Protocol (MCP) does not dictate *how* an AI application should use the context it provides; it only defines the protocol for the exchange.
*   **Decision Boundaries**: While identifying a trade-off between runtime exploration (slower) and upfront retrieval (faster), the sources do not offer a formula for determining the "right level of autonomy" beyond the general advice to "do the simplest thing that works".

### 7. Source coverage
*   **Architecture overview - Model Context Protocol**: Contributed to sections 1, 2, 3, 4, 5. Essential for defining the technical architecture of tool-using systems (MCP).
*   **Building Effective AI Agents**: Contributed to sections 3, 4, 5. Useful for architectural distinctions (agents vs. workflows) and tool engineering principles.
*   **Effective context engineering for AI agents**: Contributed to sections 1, 2, 3, 4, 5, 6. The primary source for the conceptual framework of context engineering and long-horizon management techniques.
*   **All sources** provided relevant material for the research question.
