# 🧠 Agentic AI Framework (Gemini Tool Calling)

A minimal **agentic AI framework** that enables a Large Language Model (Google Gemini) to reason step-by-step and **call external tools** using strict JSON schemas and controlled execution.

This project demonstrates how to build a **tool-augmented AI agent** with:
- Deterministic reasoning
- Schema-validated tool calls
- Explicit agent orchestration
- No automatic or unsafe function execution

---

## 📂 Project Structure

.
├── main.py # CLI entry point
├── agent_orchestrator.py # Agent execution loop
├── llm_wrapper.py # Gemini LLM wrapper
├── registry.py # Tool registration & LLM schemas
├── tool_registry.py # Tool registry manager
├── tool_class.py # Tool abstraction
├── schemas.py # Pydantic schemas for tools
├── tools.py # Tool implementations
└── README.md # Documentation


---

## ⚙️ Architecture Overview

**Flow:**

1. User sends a message
2. Agent sends history to LLM
3. LLM responds with strict JSON:
   - Calls a tool **OR**
   - Returns final answer
4. Agent executes the tool
5. Tool result is added to history
6. Loop continues until completion

---

## 🧩 Core Components

### Agent (`agent_orchestrator.py`)
- Maintains conversation history
- Parses LLM JSON responses
- Executes tools
- Enforces maximum steps

### LLM Wrapper (`llm_wrapper.py`)
- Uses **Google Gemini**
- Injects tool metadata into system prompt
- Enforces strict JSON output
- Disables automatic function calling

### Tool Registry (`tool_registry.py`)
- Registers tools dynamically
- Provides tool metadata to the LLM
- Generates type-safe tool name and argument unions

### Tools (`tools.py`)
- Pure Python functions
- No AI logic
- Easy to extend

### Schemas (`schemas.py`)
- Pydantic-validated tool inputs
- Prevents invalid or unsafe calls

---

## 🛠️ Available Tools

| Tool Name | Description |
|---------|------------|
| `add` | Adds two numbers |
| `multiply` | Multiplies two numbers |

---

## 🚀 Getting Started

### 1️⃣ Install Dependencies

```bash
pip install google-generativeai pydantic
2️⃣ Add Gemini API Key
Replace in main.py:

client = genai.Client(api_key="YOUR_API_KEY")
⚠️ Never hard-code API keys in production

3️⃣ Run the Agent
python main.py
💬 Example Interaction
You: add 5 and 7
Answer: 12
You: multiply 6 and 8
Answer: 48
🔒 Safety Guarantees
✅ Tool execution only via registry

✅ Strict JSON responses

✅ Schema-validated inputs

✅ One tool call per step

✅ Deterministic behavior (temperature = 0)

✅ No hidden tool execution

➕ Adding a New Tool
Create function in tools.py

Define input schema in schemas.py

Register tool in registry.py

The agent will automatically detect it.

🎯 Use Cases
Agentic AI systems

AI copilots

Tool-based reasoning workflows

Interview-ready AI architecture demos

Safe LLM execution environments

📌 Notes
This project is intentionally minimal and focused on clarity over complexity.
It is ideal for learning, experimentation, and showcasing agent-tool orchestration.

📜 License
MIT License


---

If you want, I can also:
- Add **diagrams**
- Convert this to **GitHub-style README**
- Add **Docker / .env support**
- Make it **interview-ready explanation**

Just tell me 👍
::contentReference[oaicite:0]{index=0}
