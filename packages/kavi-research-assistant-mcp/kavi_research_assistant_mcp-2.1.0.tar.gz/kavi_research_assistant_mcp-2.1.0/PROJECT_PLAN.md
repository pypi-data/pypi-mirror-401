# Kavi Research Assistant - Project Plan

## 🎯 Goal
To provide a robust, reliable, and user-friendly AI Research Assistant that allows users to capture, organize, and synthesize knowledge using local or cloud-based LLMs.

## 🚀 Current Status
**Version**: 2.0 (Premium Edition)
**Core Features**:
- **Dual Backend**: Support for OpenAI (Cloud) and Ollama (Local).
- **Vector Database**: ChromaDB for local embedding storage.
- **MCP Server**: FastMCP implementation for standard protocol connectivity.
- **Web UI**: Gradio-based interface for easy interaction.
- **RAG Functions**: Save, Search, Ask, Summarize.

## 📅 Roadmap

### Phase 1: Foundation (Completed) ✅
- [x] Basic MCP Server setup
- [x] CLI Tools (`save`, `search`)
- [x] OpenAI Integration
- [x] Simple Gradio UI

### Phase 2: Enhanced capabilities (Current) 🚧
- [x] Ollama Integration (Local LLM)
- [x] Topic Management (Create/Delete/List)
- [x] "Ask" functionality (Chat with data)
- [x] "Summarize" functionality
- [ ] Improved Error Handling in UI

### Phase 3: Advanced Features (Planned) 🔮
- [ ] **Multi-Modal Support**: Save images and PDFs directly.
- [ ] **Web Search Integration**: Agent can actively search the web to supplement local data.
- [ ] **Citation & Sourcing**: Better tracking of where data came from.
- [ ] **Export Options**: Export summaries to PDF/Markdown.
- [ ] **Mobile Friendly UI**: Optimize Gradio or build a React/React Native frontend.

## 🛠 Resource Requirements
- **Development**: Python 3.11+
- **Database**: ChromaDB (Local file system)
- **AI Models**:
    - OpenAI API Key (Optional)
    - Ollama (e.g., Llama 3.2, Nomic Embed)
