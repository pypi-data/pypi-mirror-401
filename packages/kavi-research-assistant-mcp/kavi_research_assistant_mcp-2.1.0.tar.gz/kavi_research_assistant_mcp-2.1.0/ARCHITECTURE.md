# Kavi Research Assistant - System Architecture

## 🏗 High-Level Overview

The Kavi Research Assistant is a modular application built on the **Model Context Protocol (MCP)** standard. It consists of a backend Server (MCP) and a frontend Client (Gradio UI).

```mermaid
graph TD
    User[User] --> UI[Gradio Web UI]
    UI -- Calls Tools --> Server[MCP Server]
    Server -- Embeddings/Chat --> LLM[LLM Provider]
    Server -- R/W --> DB[(ChromaDB)]
    
    subgraph "LLM Provider"
        OpenAI[OpenAI API]
        Ollama[Ollama (Local)]
    end
    
    subgraph "Client Layer"
        UI
        Claude[Claude Desktop]
    end
```

## 🧩 Components

### 1. The MCP Server (`server.py`)
- **Role**: The core logic engine.
- **Framework**: Built using `fastmcp`, exposing tools via the MCP standard.
- **Responsibilities**:
    - Manage Tool definitions (`save_research_data`, `ask_research_topic`, etc.)
    - Handle database connections.
    - Coordinate with LLMs (LangChain).

### 2. The Vector Database (ChromaDB)
- **Role**: Long-term memory storage.
- **Location**: Local filesystem (default: `~/.kavi_research_db` or defined by `RESEARCH_DB_PATH`).
- **Structure**:
    - **Collections**: Each "Research Topic" is a separate ChromaDB collection.
    - **Documents**: Chunks of text with metadata (content hash, source).
    - **Embeddings**: Vector representations of text using OpenAI `text-embedding-3-small` or Ollama `nomic-embed-text`.

### 3. The Web Interface (`ui.py`)
- **Role**: User-friendly interaction layer.
- **Framework**: `Gradio`.
- **Interaction**: Imports logic functions directly from `server.py` to execute tasks (acting as a direct client).
- **Theme**: Custom high-contrast theme ("Ocean") for clarity.

## 🔄 Data Flow

### Saving Data
1. **Input**: User pastes text in UI.
2. **Processing**: Server hashes content to check for duplicates.
3. **Embedding**: Text is converted to vectors via the configured Provider.
4. **Storage**: Vectors + Text saved to ChromaDB topic collection.

### Asking Questions (RAG)
1. **Query**: User asks "What is X?"
2. **Retrieval**: System searches vector DB for top 5 relevant chunks (Cosine Similarity).
3. **Augmentation**: Retrieved chunks are pasted into the System Prompt.
4. **Generation**: LLM (GPT-4o or Llama 3.2) generates an answer based *only* on the context.

## 🛠 Tech Stack
- **Language**: Python 3.11+
- **Server**: FastMCP
- **Orchestration**: LangChain
- **UI**: Gradio
- **Database**: ChromaDB
- **LLMs**: OpenAI, Ollama
