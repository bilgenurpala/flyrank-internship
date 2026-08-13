### 1. Working answer
**MCP primitives—tools, resources, and prompts—differ fundamentally in their operational role and the entity that initiates them**. Prompts are **user-controlled** templates for structured workflows, resources are **application-controlled** passive data sources for context, and tools are **model-controlled** executable functions for performing actions. While all three provide context, tools are unique in their ability to **actively perform operations** like writing to databases or calling APIs.

### 2. Key definitions
*   **Tools**: "Executable functions that AI applications can invoke to perform actions (e.g., file operations, API calls, database queries)". (Quotation)
*   **Resources**: "Data sources that provide contextual information to AI applications (e.g., file contents, database records, API responses)". (Quotation)
*   **Prompts**: "Reusable templates that help structure interactions with language models (e.g., system prompts, few-shot examples)". (Quotation)
*   **MCP Host**: "The AI application that coordinates and manages one or multiple MCP clients". (Quotation)
*   **MCP Client**: "A component that maintains a connection to an MCP server and obtains context from an MCP server for the MCP host to use". (Quotation)
*   **MCP Server**: "A program that provides context to MCP clients," regardless of whether it runs locally or remotely. (Quotation)

### 3. Supported claims
*   **Claim**: Tools are model-controlled.
    *   **Source Reference**:
    *   **Supporting Passage**: "Functions that your LLM can actively call, and decides when to use them based on user requests."
    *   **Confidence**: High.
*   **Claim**: Resources provide read-only access to information.
    *   **Source Reference**:
    *   **Supporting Passage**: "Passive data sources that provide read-only access to information for context... Resources... Application [controls it]."
    *   **Confidence**: High.
*   **Claim**: Prompts require explicit user invocation.
    *   **Source Reference**:
    *   **Supporting Passage**: "They are user-controlled, requiring explicit invocation rather than automatic triggering."
    *   **Confidence**: High.
*   **Claim**: Discovery methods are standardized across all three primitives.
    *   **Source Reference**:
    *   **Supporting Passage**: "Each primitive type has associated methods for discovery ( */list ), retrieval ( */get ), and in some cases, execution ( tools/call )."
    *   **Confidence**: High.
*   **Claim**: Notifications for tool list changes are opt-in.
    *   **Source Reference**:
    *   **Supporting Passage**: "Change notifications are opt-in: the client opens a long-lived subscriptions/listen stream naming the notification types it wants to receive."
    *   **Confidence**: High.

### 4. Important distinctions
*   **Model vs. Application vs. User Control**: The sources explicitly separate primitives based on who triggers them: the **model** for tools, the **application** for resources, and the **user** for prompts.
*   **Active vs. Passive**: Tools are described as "active" because they can "trigger other logic," whereas resources are "passive" data sources.
*   **Read-Only vs. Write**: Resources are "read-only access to information," while tools can "write to databases" or "modify files".
*   **Direct vs. Template Resources**: Sources distinguish between "Direct Resources" with **fixed URIs** and "Resource Templates" with **dynamic URIs** using parameters.
*   **Automatic vs. Explicit Triggering**: Tools can be invoked "automatically" by models during a conversation, while prompts require "explicit invocation" by the user.

### 5. Concrete examples
*   **Tools**: `calculator_arithmetic`, `weather_current`, `searchFlights`, `createCalendarEvent`, and `sendEmail`.
*   **Resources**: `file:///path/to/document.md`, `calendar://events/2024`, `travel://activities/{city}/{category}` (template), and `trips://history/barcelona-2023`.
*   **Prompts**: `plan-vacation`, "Summarize my meetings", and "Draft an email".
*   **Multi-Server Integration**: Using a **Travel Server**, **Weather Server**, and **Calendar Server** together to execute a `plan-vacation` prompt by reading calendar resources and calling flight search tools.
*   **Tool Usage Decision**: An AI choosing to call `checkWeather()` when interpreting a vacation prompt because "weather can affect travel plans". (**Inference**)

### 6. Uncertainties and disagreements
*   **Protocol Versioning Conflicts**: Source 2 is based on an older version (2025-06-18), while Sources 1 and 3 use the latest version (2026-07-28).
*   **Deprecation Discrepancies**: Source 1 explicitly marks **Sampling** and **Logging** as deprecated. Source 2, being older, lists Sampling and Elicitation as standard "Client Features" without mention of deprecation.
*   **Notification Reliability**: Source 1 notes there are "no guarantees that every notification will be sent or received," describing them as "Best Effort".
*   **The Fluidity of "Control"**: While tools are categorized as "model-controlled," Source 3 notes that applications can implement **approval dialogs** or **permission settings**, which introduces a layer of user control over a model-controlled primitive.

### 7. Source coverage
*   **Source 1**: Provided the primary technical architecture, definitions for all primitives, and detailed JSON-RPC message examples for discovery and execution.
*   **Source 2**: Provided the concise **control hierarchy table** that explicitly differentiates the controllers of prompts, resources, and tools.
*   **Source 3**: Provided the detailed "Travel Planning" scenario used to illustrate how the primitives interact in a real-world application, as well as the user interaction models for each.
*   All three sources were utilized to construct this evidence pack.
