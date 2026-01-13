
import sys
import os
from pathlib import Path

# Add src to path
# sys.path.append(os.path.abspath("src"))

from kavi_research_assistant_mcp.server import ask_research_topic_logic, save_research_data_logic

def test_chat():
    print("Testing chat functionality...")
    
    test_db_path = os.path.expanduser("~/test_kavi_db_chat")
    topic = "test_chat_topic"
    
    config = {
        "LLM_PROVIDER": "ollama",
        "RESEARCH_DB_PATH": test_db_path,
        "OLLAMA_BASE_URL": "http://localhost:11434",
        "OLLAMA_EMBED_MODEL": "nomic-embed-text",
        "OLLAMA_CHAT_MODEL": "llama3.2"
    }
    
    # 1. Save data first so we have something to ask about
    print("Saving test data...")
    content = ["The sky is blue because of Rayleigh scattering.", "Cats are independent animals."]
    save_result = save_research_data_logic(content, topic, config)
    print(f"Save Result: {save_result}")
    
    # 2. Ask question
    print("Asking question...")
    query = "Why is the sky blue?"
    try:
        response = ask_research_topic_logic(query, topic, config)
        print(f"Response: {response}")
    except Exception as e:
        print(f"❌ Error during chat: {e}")

if __name__ == "__main__":
    test_chat()
