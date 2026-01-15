# Adeptiv GenAI Tracing SDK

**Adeptiv GenAI** is a lightweight, vendor-neutral **OpenTelemetry tracing SDK** for **LLMs, agents, and AI workflows**.

It captures **latency, execution flow, hashes, and metadata** for all AI use cases.

---

## Key Features

-  **Trace-only observability** (no response normalization)
- Works with **any LLM** (OpenAI, Anthropic, Gemini, local models)
- Supports **chat, summarization, agents, tools, RAG**
- **Sync & async** compatible
- **Enterprise-safe** (hashing, redaction, previews)
- **OpenTelemetry compatible**
---

This ensures **zero lock-in** and **maximum compatibility**.

---

## Installation

```bash

pip install adeptiv-ai-evaluator-sdk

```

# Adeptiv GenAI Tracing SDK


Tracing an LLM Call

```python


SDK configuration

config.api_key = "" #project Key 
config.project_name = "customer-support-bot" # Project Name


from adeptiv_evaluator_sdk import trace_llm

@trace_llm(model="gpt-4o", operation="chat", workflow_id="")
def chat(prompt):
    return llm.invoke(prompt)

chat("Hello world")

```


```python
# Adeptiv GenAI Tracing Agents SDK

from adeptiv_evaluator_sdk import trace_llm

@trace_agent("support_agent", model="gpt-4o",workflow_id="")
async def run_agent(query):
    return await agent.run(query)


```

