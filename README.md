# MCP Multi-Server Chatbot

**MCP Multi-Server Chatbot** is a Generative AI project that shows how to connect a single agent to multiple **MCP (Model Context Protocol) servers**.

It uses:

* **LangChain MCP Adapters** - to connect to multiple MCP servers.
* **LangGraph ReAct Agent** - to let the model decide when to use tools vs respond.
* **Groq LLMs** - for fast reasoning and conversation.
* **FastMCP** - to quickly build custom MCP servers (`math` and `weather`).

This project demonstrates how MCP can unify different services (math operations, weather info, etc.) into **one chatbot**.

---

## Features

* Connects to **multiple MCP servers at once**.
* **Math MCP Server (stdio)** → add, subtract, multiply numbers.
* **Weather MCP Server (HTTP)** → fetch simple weather responses.
* Uses **Groq’s Qwen3-32B model** (via `langchain-groq`).
* **LangGraph ReAct agent** → chooses which MCP tool to call automatically.

---


## Setup with `uv`

1. **Initialize the project**

   ```bash
   uv init mcp-multi
   cd mcp-multi
   ```

2. **Create and activate a virtual environment**

   ```bash
   uv venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   uv add langchain-groq
   uv add langchain-mcp-adapters
   uv add langgraph
   uv add python-dotenv
   uv add mcp
   ```

4. **Create a `.env` file** with your Groq API key:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

---

## Explanation of Each File

### 1. `mathserver.py` (stdio MCP server)

* Implements three tools: `add`, `subtract`, `multiply`.
* Uses `stdio` transport - communicates via standard input/output streams.
* Suitable for simple, local tool servers.

Run with:

```bash
uv run python mathserver.py
```

---

### 2. `weather.py` (HTTP MCP server)

* Implements a single tool: `get_weather(city)`.
* Uses `streamable-http` transport - runs as an HTTP server.
* Good for services exposed via APIs.

Run with:

```bash
uv run python weather.py
```

---

### 3. `client.py` (multi-server client)

* Uses **`MultiServerMCPClient`** to connect to both servers:

  * `math` (stdio)
  * `weather` (http)
* Loads all tools from both servers dynamically.
* Wraps them into a **LangGraph ReAct agent** with **Groq LLM**.
* The agent decides whether to:

  * Answer directly using the LLM.
  * Call one of the MCP tools (`add`, `get_weather`, etc.).

Run with:

```bash
uv run python client.py
```

---

## Example Run

1. **Start the servers** in separate terminals:

```bash
uv run python mathserver.py
```

```bash
uv run python weather.py
```

2. **Run the client**:

```bash
uv run python client.py
```

3. **Output**:

<img width="1578" height="1016" alt="image" src="https://github.com/user-attachments/assets/4f8d82ba-f3fc-4b6a-b069-25e83b04b3f0" />


---

## How It Works

1. **MCP Servers**

   * `mathserver.py` exposes math functions.
   * `weather.py` exposes a weather API.

2. **MCP Client**

   * `client.py` connects to both servers at once using `MultiServerMCPClient`.
   * Collects available tools (`add`, `subtract`, `get_weather`, etc.).

3. **ReAct Agent**

   * Uses **Groq LLM** (`qwen3-32b`) as the brain.
   * Applies the **ReAct pattern**:

     * Reason - Decide which tool to call.
     * Act - Call MCP tool.
     * Observe - Take tool output into context.
     * Respond - Give final answer to user.

4. **Transport**

   * `stdio` - Simple, lightweight communication (used by math server).
   * `http` - API-like communication (used by weather server).

