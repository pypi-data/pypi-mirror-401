# 📖 API Reference

A comprehensive guide to all parameters and classes in the AICCEL framework.

## 1. Core Agent API

### `Agent` Class
The primary interface for building and running AI agents.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`provider`** | `LLMProvider` | ✅ | LLM backend (Gemini, OpenAI, Groq). |
| **`tools`** | `List[Tool]` | `None` | Tools the agent can use. |
| **`name`** | `str` | `"Agent"` | Unique name for logs and orchestration. |
| **`instructions`**| `str` | `""` | System prompt / persona. |
| **`description`** | `str` | `""` | Agent capabilities for `AgentManager`. |
| **`config`** | `AgentConfig`| `None` | Operational settings (see below). |
| **`memory`** | `Memory` | `Buffer` | Conversation history manager. |

---

### `AgentConfig` Dataclass
Operating settings for agents.

| Field | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`verbose`** | `bool` | `False` | Enable detailed thinking & tool logs. |
| **`timeout`** | `float` | `60.0` | Max seconds per generation. |
| **`safety_enabled`**| `bool` | `False` | Enable transformer-based Jailbreak guard. |
| **`lightweight`** | `bool` | `False` | Disable heavy model loading (GLiNER/Rerank). |
| **`max_retries`** | `int` | `3` | Retries on network failure. |

---

## 2. Orchestration API

### `AgentManager` Class
Manages and routes queries to multiple agents.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`llm_provider`** | `LLMProvider` | ✅ | Provider for routing and synthesis. |
| **`agents`** | `List[Agent]` | `None` | Managed agents. |
| **`verbose`** | `bool` | `False` | Log routing and execution details. |
| **`instructions`**| `str` | `None` | Routing-specific instructions. |
| **`max_tasks`** | `int` | `5` | Max sub-tasks allowed per query. |

---

## 3. Data & Analysis API

### `Pandora` Class
Autonomous data transformation engine.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`llm`** | `LLMProvider` | ✅ | Provider for code generation. |
| **`max_retries`** | `int` | `4` | Max self-correction attempts. |
| **`verbose`** | `bool` | `True` | Log detailed thoughts & code. |
| **`execution_mode`**| `str` | `"local"` | `"local"`, `"subprocess"`, or `"service"`. |
| **`safety_enabled`**| `bool` | `False` | Run jailbreak check on input. |

---

## 4. Security & Privacy API

### `EntityMasker` (ia `mask_text`)
Protect sensitive data before LLM transmission.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`text`** | `str` | ✅ | Input text to mask. |
| **`remove_person`** | `bool` | `True` | Mask person names. |
| **`remove_email`** | `bool` | `True` | Mask email addresses. |
| **`remove_phone`** | `bool` | `True` | Mask phone numbers. |
| **`remove_id`** | `bool` | `False` | Mask IDs (Passport, PAN, etc.) |

---

## 5. Workflow API

### `WorkflowExecutor` Class
Executes DAG-based agent pipelines.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`max_iterations`**| `int` | `100` | Safety limit for loops/retries. |
| **`timeout`** | `float` | `300.0` | Max seconds for full execution. |
| **`checkpoint_enabled`** | `bool` | `True` | Allow recovery from failures. |
| **`quiet`** | `bool` | `False` | Minimal logging. |
