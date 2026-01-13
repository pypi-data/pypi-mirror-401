import os
import sys
from pathlib import Path

# Ensure we can import the package
sys.path.append(str(Path(__file__).parent / "src"))

from kavi_research_assistant_mcp.server import parse_file, save_research_files_logic

def test_file_parsing():
    # Create test files
    test_dir = Path("test_upload_files")
    test_dir.mkdir(exist_ok=True)
    
    txt_file = test_dir / "test.txt"
    txt_file.write_text("This is a test text file.")
    
    print(f"Testing TXT parsing...")
    txt_content = parse_file(txt_file)
    print(f"TXT Content: {txt_content}")
    assert "test text" in txt_content
    
    # PDF and DOCX would need real files, but we can check if they are recognized
    print("Verification script ran successfully for basic text.")

if __name__ == "__main__":
    try:
        test_file_parsing()
    except Exception as e:
        print(f"Tests failed: {e}")
        sys.exit(1)
