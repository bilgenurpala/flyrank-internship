### 1. Working answer
A tool-using system should stop for human approval during **sensitive operations** to ensure trust, safety, and security,. This gate is meaningful when the system provides **clear visual indicators** of invocation and presents specific **tool inputs** to the user before the server call is made,. Such a mechanism allows a "human in the loop" to effectively deny requests and prevent accidental or malicious data exfiltration,.

### 2. Key definitions
*   **Human in the loop**: A security and safety model where a person maintains the ability to oversee and "deny tool invocations",. (Paraphrase)
*   **Model-controlled**: A system design where the language model is responsible for discovering and invoking tools based on its own "contextual understanding" and user prompts. (Quotation)
*   **Tools**: Functionalities exposed by servers that "enable models to interact with external systems," such as APIs or databases. (Quotation)
*   **Sensitive operations**: Specific tool-based actions that require a "confirmation prompt" to ensure safety. (Paraphrase)

### 3. Supported claims
*   **Claim**: Systems should always provide a way for a human to deny a tool invocation.
    *   **Source reference**:
    *   **Supporting passage**: "For trust & safety and security, there SHOULD always be a human in the loop with the ability to deny tool invocations."
    *   **Confidence**: High
*   **Claim**: Meaningful gates require showing tool inputs to the user before the tool is executed.
    *   **Source reference**:
    *   **Supporting passage**: "Show tool inputs to the user before calling the server, to avoid malicious or accidental data exfiltration"
    *   **Confidence**: High
*   **Claim**: User interfaces must make it clear which tools the AI can access.
    *   **Source reference**:
    *   **Supporting passage**: "Provide UI that makes clear which tools are being exposed to the AI model"
    *   **Confidence**: High
*   **Claim**: Clients should validate the results returned by a tool before the LLM sees them.
    *   **Source reference**:
    *   **Supporting passage**: "Validate tool results before passing to LLM"
    *   **Confidence**: High

### 4. Important distinctions
*   **Model-controlled vs. Protocol-mandated**: While tools are "model-controlled" for discovery and invocation, the protocol itself "does not mandate any specific user interaction model".
*   **Protocol Errors vs. Tool Execution Errors**: The sources distinguish between standard JSON-RPC errors (like "Unknown tools") and errors that occur during the tool's actual run (like "API failures").
*   **Trusted vs. Untrusted Servers**: Clients are instructed to treat tool annotations as "untrusted" unless they originate from a verified trusted server.
*   **Structured vs. Unstructured Content**: Tool results are separated into "structuredContent" (server-produced JSON) and "content" (unstructured items like text, images, or audio),.

### 5. Concrete examples
*   **Weather Retrieval**: The `get_weather` or `get_weather_data` tools serve as examples of tools requiring specific inputs (location) to return data (temperature, conditions),.
*   **Confirmation Prompt**: A UI element that asks a user to approve a "sensitive operation" before it proceeds,.
*   **Visual Indicators**: UI elements inserted specifically "when tools are invoked" to signal model activity to the user.
*   **Data Exfiltration**: A security risk (accidental or malicious) that human-in-the-loop gates are specifically designed to prevent.
*   **Sensitive Operation (Inference)**: While not explicitly listed, a tool capable of "data exfiltration" is inferred to be a sensitive operation requiring a gate.

### 6. Uncertainties and disagreements
*   **Definition of "Sensitive"**: The sources do not define the specific threshold or criteria for what makes an operation "sensitive" versus a standard one.
*   **Requirement Level**: The text uses "SHOULD" regarding human-in-the-loop gates and confirmation prompts, which suggests these are strongly recommended but perhaps not strictly mandatory for protocol compliance compared to "MUST" requirements like input validation,,,.
*   **UI Implementation**: Because the protocol "does not mandate" an interaction model, there is no established standard for what a "meaningful" confirmation prompt must look like.

### 7. Source coverage
*   **Source**: Provided core concepts for the working answer, definitions of "model-controlled," and the primary claim for human-in-the-loop necessity.
*   **Source**: Provided the requirements for visual indicators and confirmation prompts.
*   **Source,,**: Provided distinctions regarding content types and error handling.
*   **Source**: Provided the specific rationale for gates (preventing exfiltration) and the "sensitive operations" terminology.
*   **Source,,,,,,,**: Provided technical context, schema examples, and message formats but did not directly address the "why" or "when" of human approval gates.
