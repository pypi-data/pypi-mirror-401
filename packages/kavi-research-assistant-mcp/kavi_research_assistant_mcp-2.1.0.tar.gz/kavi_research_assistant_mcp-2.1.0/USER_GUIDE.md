# Kavi Research Assistant - User Guide

Welcome to your AI Research Librarian! Follow this simple guide to master your new tool.

## 🚀 Getting Started

### 1. Launch the App
Open your terminal and run:
```bash
uv run kavi-research-ui
```
Then open your browser to: `http://localhost:7860`

### 2. Configure Settings (First Time)
1. Go to the **⚙️ Settings** tab.
2. **LLM Provider**: Choose "OpenAI" (easiest) or "Ollama" (free/local).
    - If **OpenAI**: Enter your API Key (starts with `sk-...`).
    - If **Ollama**: Ensure Ollama is running (`ollama serve`).
3. Click **✅ Update Configuration**.

---

## 📚 How to Use

### 1. Save Research ("Feed the Brain")
Before you can ask questions, you need to save some data.
1. Go to the **📥 Save Knowledge** tab.
2. **Topic Name**: Enter a name for your research bucket (e.g., `neuroscience`, `ai-agents`, `gardening`).
    - *Tip: Use hyphens instead of spaces.*
3. **Content**: Paste your article text, notes, or paper abstract in the large text box.
4. Click **💾 Save to Knowledge Base**.

### 2. Chat with Your Research
Now that you have data, you can talk to it.
1. Go to the **💬 Ask Researcher** tab.
2. **Research Topic**: Enter the *exact* name of the topic you saved earlier (e.g., `neuroscience`).
3. **Your Question**: Type your question (e.g., "What are the key findings in this paper?").
4. Click **🚀 Ask Kavi**.
5. The AI will answer *only* using the information you saved.

### 3. Summarize a Topic
Get a quick overview of everything you've learned.
1. Go to the **📊 Dashboard** tab.
2. Scroll to **📑 Generate Summary**.
3. **Topic to Summarize**: Enter your topic name.
4. Click **✨ Generate Summary**.

### 4. Manage Topics
See what you have stored.
1. Go to the **📊 Dashboard** tab.
2. Click **🔄 Refresh Topic List**.
3. You will see a list of all your topics and how many documents are in each.

---

## ❓ Frequently Asked Questions

**Q: Can I use this without internet?**
A: Yes! Select "Ollama" in settings. You must have [Ollama](https://ollama.com) installed and models pulled (`ollama pull llama3.2`).

**Q: Where is my data?**
A: It is saved on your computer in a folder (default: `~/.kavi_research_db`). It is private and secure.

**Q: My topic isn't found?**
A: Check your spelling. Topic names are case-sensitive. Use the Dashboard to see the exact names.
