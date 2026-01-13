
import os
import pytest
from kavi_research_assistant_mcp import server

def test_imports():
    """Test that key components can be imported."""
    from kavi_research_assistant_mcp.server import get_embeddings, get_llm, ask_research_topic, summarize_topic
    assert get_embeddings is not None
    assert get_llm is not None

def test_openai_config(monkeypatch):
    """Test OpenAI configuration (Default)."""
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-mock")
    # Reload server settings or just check factory logic if dynamic
    # Our implementation uses global constants but the factories read globals.
    # We need to monkeypatch the module level variable if possible or rely on re-import.
    # However, server.py reads env vars at module level.
    # To properly test this, we should refactor server.py to read env vars inside functions
    # OR reload the module. For simpler testing, we can just test the factories 
    # IF the factory reads the GLOBAL variable which was set at import time.
    
    # Let's assume we can't easily change the global constant `LLM_PROVIDER` without reload.
    # But wait, `LLM_PROVIDER = os.getenv(...)`. 
    # We can patch `kavi_research_assistant_mcp.server.LLM_PROVIDER`.
    
    monkeypatch.setattr(server, "LLM_PROVIDER", "openai")
    
    llm = server.get_llm()
    emb = server.get_embeddings()
    
    # Check class names as strings to avoid importing specific providers if missing
    assert "OpenAI" in type(llm).__name__
    assert "OpenAI" in type(emb).__name__

def test_ollama_config(monkeypatch):
    """Test Ollama configuration."""
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.setattr(server, "LLM_PROVIDER", "ollama")
    
    llm = server.get_llm()
    emb = server.get_embeddings()
    
    assert "Ollama" in type(llm).__name__
    assert "Ollama" in type(emb).__name__
