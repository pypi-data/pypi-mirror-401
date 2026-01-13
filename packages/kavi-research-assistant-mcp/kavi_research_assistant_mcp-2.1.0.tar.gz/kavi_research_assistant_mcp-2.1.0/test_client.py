
import subprocess
import json
import os
import sys
import time

# Configuration
SERVER_COMMAND = ["uv", "run", "kavi-research-assistant-mcp"]
ENV = os.environ.copy()
ENV["RESEARCH_DB_PATH"] = "/tmp/test_client_db"
# Only set mock key if using OpenAI or if needed to pass validation
if os.getenv("LLM_PROVIDER") != "ollama":
    ENV["OPENAI_API_KEY"] = "sk-mock-key-for-testing"
    ENV["LLM_PROVIDER"] = "openai"
else:
    ENV["LLM_PROVIDER"] = "ollama"
    # Ensure standard ollama ports/models if not set
    if "OLLAMA_CHAT_MODEL" not in ENV:
        ENV["OLLAMA_CHAT_MODEL"] = "llama3.2"

def create_json_rpc_message(method, params=None, id=1):
    msg = {
        "jsonrpc": "2.0",
        "method": method,
        "id": id
    }
    if params:
        msg["params"] = params
    return msg

def run_test_client():
    print(f"🚀 Starting MCP Server: {' '.join(SERVER_COMMAND)}")
    print(f"📂 DB Path: {ENV['RESEARCH_DB_PATH']}")
    
    # Start the server process
    process = subprocess.Popen(
        SERVER_COMMAND,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr, # Pass stderr through
        env=ENV,
        text=True,
        bufsize=0 # Unbuffered
    )

    def send_request(req):
        json_str = json.dumps(req)
        print(f"\n➡️  Request ({req['method']}):")
        # print(f"    {json_str}")
        process.stdin.write(json_str + "\n")
        process.stdin.flush()

    def read_response():
        line = process.stdout.readline()
        if not line:
            return None
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            print(f"⚠️  Received non-JSON line: {line.strip()}")
            return read_response()

    try:
        # 1. Initialize
        init_req = create_json_rpc_message("initialize", {
            "protocolVersion": "2024-11-05", # Example version
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0"}
        }, id=1)
        send_request(init_req)
        
        resp = read_response()
        print(f"⬅️  Response:")
        print(f"    Server Info: {resp.get('result', {}).get('serverInfo', 'Unknown')}")

        # Send initialized notification
        send_request({"jsonrpc": "2.0", "method": "notifications/initialized"})

        # 2. List Tools
        list_req = create_json_rpc_message("tools/list", id=2)
        send_request(list_req)
        resp = read_response()
        tools = resp.get('result', {}).get('tools', [])
        print(f"⬅️  Response: Found {len(tools)} tools")
        for t in tools:
            print(f"    - {t['name']}")

        # 3. Call Tool: save_research_data (Mock Check)
        # Note: This will fail if we don't have real keys, but we want to see the error handled gracefully
        # or see it attempt to save if we are using mocking.
        # Since we set a mock key, it will crash deep in LangChain unless we configured valid mocked LLMs.
        # But let's try it.
        
        print("\n🧪 Testing Tool Execution (Expect OpenAI Error with mock key)...")
        call_req = create_json_rpc_message("tools/call", {
            "name": "save_research_data",
            "arguments": {
                "content": ["AI Agents are autonomous systems."],
                "topic": "test_agents"
            }
        }, id=3)
        send_request(call_req)
        resp = read_response()
        print(f"⬅️  Response:")
        # We expect a text result, likely containing an error message about the API key, but wrapped in MCP format
        content = resp.get('result', {}).get('content', [])
        if content:
            print(f"    {content[0].get('text', '')}")
        else:
            print(f"    {resp}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        print("\n🛑 Terminating server...")
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()

if __name__ == "__main__":
    run_test_client()
