
import os
import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """
    Called before the test session starts. 
    Set environment variables required by the server module.
    """
    os.environ["RESEARCH_DB_PATH"] = "/tmp/test_research_db"
    # Set a mock key so OpenAI embeddings don't crash on init if used
    os.environ["OPENAI_API_KEY"] = "sk-mock-key-for-testing"
    os.environ["ANONYMIZED_TELEMETRY"] = "False"
