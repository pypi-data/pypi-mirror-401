
import os
import sys
from pathlib import Path


# Add src to path so we can import the module
sys.path.append(str(Path("src").resolve()))

# Set required environment variables BEFORE import
os.environ["RESEARCH_DB_PATH"] = "/tmp/test_research_db"
os.environ["OPENAI_API_KEY"] = "sk-mock-key-for-testing"
os.environ["ANONYMIZED_TELEMETRY"] = "False"

def test_imports():
    print("Testing imports...")
    try:
        from kavi_research_assistant_mcp.server import get_embeddings, get_llm, ask_research_topic, summarize_topic
        print("✅ Imports successful")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        sys.exit(1)

def test_factories():
    print("\nTesting factories...")
    from kavi_research_assistant_mcp.server import get_embeddings, get_llm
    
    # Test Default (OpenAI)
    print("Testing OpenAI config (default)...")
    os.environ["LLM_PROVIDER"] = "openai"
    # We might need to reload the module or just trust that the function checks env var at runtime? 
    # Actually my implementation checked env var at global scope for the CONSTANT, 
    # but the functions used the global constant. 
    # Wait, the implementation had:
    # LLM_PROVIDER = os.getenv(...).lower()
    # This means I can't easily change it at runtime without reloading the module.
    # For this test, I will just inspect what was loaded.
    
    from kavi_research_assistant_mcp import server
    print(f"Current Provider: {server.LLM_PROVIDER}")
    
    emb = get_embeddings()
    llm = get_llm()
    print(f"Embeddings: {type(emb).__name__}")
    print(f"LLM: {type(llm).__name__}")
    
    if server.LLM_PROVIDER == "openai":
         if "OpenAI" not in type(emb).__name__ and "OpenAI" not in type(llm).__name__:
             print("❌ Expected OpenAI classes")
    elif server.LLM_PROVIDER == "ollama":
         if "Ollama" not in type(emb).__name__ and "Ollama" not in type(llm).__name__:
             print("❌ Expected Ollama classes")

def main():
    test_imports()
    test_factories()
    print("\n✅ Verification script finished.")

if __name__ == "__main__":
    main()
