<div align="center">

<img src="assets/logo.png" alt="KAVI RESEARCH" width="200" style="margin-bottom: 20px;">

# KAVI RESEARCH

**Your Premium AI Research Librarian**

[![PyPI version](https://img.shields.io/pypi/v/kavi-research-assistant-mcp.svg)](https://pypi.org/project/kavi-research-assistant-mcp/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by LangChain](https://img.shields.io/badge/Powered%20by-LangChain-2E7D32.svg)](https://langchain.com)
[![Built by kavi.ai](https://img.shields.io/badge/Built%20by-kavi.ai-orange.svg)](https://kavi.ai)

[Features](#features) • [Installation](#installation) • [Configuration](#configuration) • [Usage](#usage) • [Contributing](#contributing)

</div>

---

## 🚀 Overview

<img src="assets/dashboard_preview.png" alt="Kavi Research Dashboard" width="100%" style="margin: 15px 0; border-radius: 10px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">

**KAVI RESEARCH** is a premium Model Context Protocol (MCP) server designed to transform your AI into a dedicated research assistant. 

Stop losing track of important findings. KAVI RESEARCH enables your AI to **save**, **organize**, **search**, and **synthesize** high-volume research materials using a local vector database. Whether you are using **OpenAI** or local **Ollama** models, KAVI RESEARCH keeps your knowledge accessible, private, and secure.

> **Newly Added in v2.1**: Large Document Support! KAVI RESEARCH now automatically chunks massive PDFs and files into manageable semantic segments to bypass LLM context limits.

## ✨ Features

- **🧠 Dual Backend Support**: seamless switching between **OpenAI** (Cloud) and **Ollama** (Local/Private).
- **🗣️ RAG Capabilities**: "Chat" with your research topics using advanced Retrieval-Augmented Generation.
- **📚 Smart Storage**: Automatic content deduplication and vector embedding using ChromaDB.
- **🔍 Semantic Search**: Find what you need using natural language, not just keywords.
- **📂 Topic Organization**: Keep different research streams (e.g., "AI Agents", "React Patterns") isolated and organized.
- **⚡ Fast & Efficient**: Built on `fastmcp` and `langchain` for high performance.

## 📦 Installation

### Recommended: using `uv` (Fastest)

```bash
# Run the AI Agent (MCP Server)
uvx kavi-research-assistant-mcp

# Run the Web UI (Gradio)
uv run kavi-research-ui
```

### Using `pip`

```bash
pip install kavi-research-assistant-mcp
```

## 🎨 Web Interface (UI)

We provide a beautiful, colorful web interface to manage your research.

```bash
uv run kavi-research-ui
```

- **🎓 Ask Researcher**: Chat with your research librarian.
- **💾 Save Knowledge**: Easily paste and save new notes.
- **📊 Dashboard**: View summaries and manage your topics.


## ⚙️ Configuration

You can configure the agent to use either OpenAI (default) or a local Ollama instance.

### Option 1: OpenAI (Default)
Powerful, zero-setup (requires API Key).

```bash
export OPENAI_API_KEY=sk-...
export RESEARCH_DB_PATH=~/research_db
export LLM_PROVIDER=openai
```

### Option 2: Ollama (Local & Private)
Run entirely on your machine. No API keys required.

1. **Pull Models**:
   ```bash
   ollama pull llama3.2
   ollama pull nomic-embed-text
   ```

2. **Configure Environment**:
   ```bash
   export RESEARCH_DB_PATH=~/research_db
   export LLM_PROVIDER=ollama
   # Optional overrides
   # export OLLAMA_BASE_URL=http://localhost:11434
   ```

### Claude Desktop Setup
Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "kavi-research": {
      "command": "uvx",
      "args": ["kavi-research-assistant-mcp"],
      "env": {
        "RESEARCH_DB_PATH": "/Users/username/research_db",
        "OPENAI_API_KEY": "sk-..." 
      }
    }
  }
}
```

## 🛠️ MCP Tool Reference

Model Context Protocol (MCP) allows Kavi to act as a bridge between your AI and a private knowledge base. Below are the tools provided:

### 1. 📥 Data Ingestion
*   **`save_research_data(content: List[str], topic: str)`**: Saves raw text or snippets. 
    *   *Usecase*: Saving paper abstracts or news headlines.
*   **`save_research_files(file_paths: List[str], topic: str)`**: Parses and vectorizes documents.
    *   *Supported Formats*: `.pdf`, `.txt`, `.docx`.
    *   *Usecase*: Ingesting a folder of research PDF papers.

### 2. 🔍 Knowledge Retrieval & RAG
*   **`ask_research_topic(query: str, topic: str)`**: Answers questions using **Retrieval Augmented Generation**.
    *   *Usecase*: "What does my research say about Agentic Workflows?"
*   **`summarize_topic(topic: str)`**: Generates a high-level executive summary of an entire library.
    *   *Usecase*: Periodic review of a project topic.

### 3. 📋 Management
*   **`list_research_topics()`**: Returns a list of all libraries and their document counts.
*   **`search_research_data(query: str, topic: str)`**: Performs raw semantic similarity search for specific chunks.

---

## 🧪 Testing & Usage Steps

### Step 1: Initialize the Environment
Ensure your preferred LLM backend is running. For Ollama:
```bash
ollama serve
ollama pull llama3.2
ollama pull nomic-embed-text
```

### Step 2: Launch the Assistant
You can interact via the **MCP Inspector** (Command Line) or the **Web UI**.

**To test via MCP Inspector:**
```bash
npx @modelcontextprotocol/inspector uv run kavi-research-assistant-mcp
```
Once the inspector opens in your browser, you can manually trigger tools like `list_research_topics`.

### Step 3: Populate with Knowledge
Ask your AI (via Claude Desktop or the UI) to save information:
> *"Save the following text to my 'ai-market' topic: [Your Text Here]"*

### Step 4: Validate RAG (The "Proof of Work")
Ask a question that **only** your saved data could answer:
> *"Based on my 'ai-market' data, what was the projected growth for 2026?"*

### Step 5: Dashboard Review
Open the UI to see your topic cards visualized gracefully.
```bash
uv run kavi-research-ui
```

---

## 💡 Typical Usecase Scenarios

1.  **Academic Research**: Upload 50 PDF papers into a topic called `thesis`. Use `ask_research_topic` to find contradictions or common methodologies across all papers.
2.  **Market Intelligence**: Save daily news snippets about competitors into `competitor-intel`. Every Friday, run `summarize_topic` to get a weekly briefing.
3.  **Code Library**: Save documentation for obscure libraries into `dev-docs`. Use Kavi to answer "How do I implement X using Y?" without the LLM hallucinating.

---

## 👨‍💻 Author & Credits

**Machha Kiran**
- 📧 Email: [machhakiran@gmail.com](mailto:machhakiran@gmail.com)
- 🐙 GitHub: [@machhakiran](https://github.com/machhakiran)

**Branding:**
- Copyright © 2025 **kavi.ai**. All rights reserved.
- `kavi.ai` and the Kavi logo are trademarks of [kavi.ai](https://kavi.ai).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ by the kavi.ai team</sub>
</div>
