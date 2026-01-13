
import gradio as gr
import os
import sys
from pathlib import Path

# Ensure we can import server
sys.path.append(str(Path(__file__).parent.parent))

from kavi_research_assistant_mcp.server import (
    ask_research_topic_logic,
    save_research_data_logic,
    save_research_files_logic,
    summarize_topic_logic,
    list_research_topics_logic,
)
from kavi_research_assistant_mcp.logo_data import LOGO_BASE64

# --- THEME & STYLE ---
theme = gr.themes.Soft(
    primary_hue="purple",
    secondary_hue="pink",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Outfit")],
).set(
    button_primary_background_fill="linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%)",
    button_primary_background_fill_hover="linear-gradient(135deg, #4f46e5 0%, #9333ea 50%, #db2777 100%)",
    button_primary_text_color="white",
    block_title_text_color="#4338ca",
    block_label_text_color="#6b7280",
    input_background_fill="white", 
    block_border_width="1px",
)

custom_css = """
.gradio-container {
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%) !important;
    max_width: 1100px !important;
    padding-top: 10px !important;
}
h1, h2, h3 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
}
h1 {
    font-size: 2rem !important;
    background: linear-gradient(to right, #6366f1, #a855f7, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
h2 {
    font-size: 1.5rem !important;
    color: #4338ca !important;
    margin-bottom: 15px !important;
}
h3 {
    font-size: 1.2rem !important;
    color: #6366f1 !important;
    margin-bottom: 10px !important;
}
.group {
    padding: 12px !important;
    margin-bottom: 15px !important;
    background: white !important;
    border: 1px solid rgba(168, 85, 247, 0.2) !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02) !important;
}
.topic-card {
    background: white;
    border: 1px solid rgba(168, 85, 247, 0.2);
    border-radius: 12px;
    padding: 15px;
    min-width: 200px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s, border-color 0.2s;
    cursor: pointer;
}
.topic-card:hover {
    transform: translateY(-2px);
    border-color: #a855f7;
    background: #f5f3ff;
}
.topic-hull {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin-top: 10px;
}
.topic-title {
    font-weight: 800;
    color: #4338ca;
    font-size: 1.1rem;
    margin-bottom: 5px;
}
.topic-count {
    font-size: 0.85rem;
    color: #9333ea;
    background: #f5f3ff;
    padding: 2px 8px;
    border-radius: 20px;
    display: inline-block;
}
.status-log {
    background: #1e1b4b;
    color: #e879f9;
    padding: 12px;
    border-radius: 8px;
    font-family: 'Fira Code', monospace;
    font-size: 0.85rem;
    border: 1px solid rgba(232, 121, 249, 0.3);
    min-height: 80px;
}
.thinking-log {
    background: #0f172a;
    color: #38bdf8;
    padding: 12px;
    border-radius: 8px;
    font-family: 'Fira Code', monospace;
    font-size: 0.8rem;
    line-height: 1.4;
    border: 1px solid #1e293b;
    max-height: 180px;
    overflow-y: auto;
}
.log-step {
    color: #94a3b8;
    margin-bottom: 2px;
}
.log-success {
    color: #22c55e;
}
.log-tool {
    color: #f59e0b;
    font-weight: bold;
}
.guide-box {
    background: linear-gradient(90deg, #f5f3ff 0%, #fdf2f8 100%);
    border-left: 4px solid #a855f7;
    padding: 12px;
    border-radius: 6px;
    margin-bottom: 12px;
    color: #5b21b6;
}
.footer {
    text-align: center;
    margin-top: 20px;
    padding: 10px;
    color: #64748b;
    font-size: 0.8rem;
    border-top: 1px solid rgba(168, 85, 247, 0.1);
}
"""

# Custom JS for topic clicking
js_script = """
() => {
    window.setTopic = function(name) {
        const hiddenInput = document.getElementById('hidden_topic_setter').querySelector('input');
        hiddenInput.value = name;
        hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
        // Also find the topic name in text and scroll if needed or highlight
        console.log("Topic selected:", name);
    };
}
"""

def update_config(provider, open_key, db_path, ollama_url, ollama_embed):
    """Update system config state."""
    new_config = {
        "LLM_PROVIDER": provider.lower(),
        "OPENAI_API_KEY": open_key,
        "RESEARCH_DB_PATH": db_path,
        "OLLAMA_BASE_URL": ollama_url,
        "OLLAMA_EMBED_MODEL": ollama_embed,
    }
    status = f"✅ Config Updated! Using **{provider}**."
    return new_config, status

def format_chat_history(history, user_input, topic, config):
    """Integrate with ask_research_topic with step-by-step logging"""
    if history is None:
        history = []
        
    if not user_input:
        gr.Warning("Please enter a question first.")
        return history, "", ""
    
    logs = [
        '<div class="log-step">🚀 Initializing Research Session...</div>',
        f'<div class="log-step">📂 Active Topic: <span class="log-tool">{topic}</span></div>'
    ]
    
    try:
        logs.append('<div class="log-step">🔍 Connecting to Local Vector Database...</div>')
        # Simulate steps or just call logic
        logs.append(f'<div class="log-step">🧠 Retriving context for: "{user_input[:40]}..."</div>')
        
        response = ask_research_topic_logic(user_input, topic, config=config)
        
        logs.append('<div class="log-step">⛓️ Running RAG Chain with LLM...</div>')
        logs.append('<div class="log-success">✅ Generation Complete.</div>')
        
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": response})
    except Exception as e:
        logs.append(f'<div class="log-step" style="color: #ef4444;">❌ Error: {str(e)}</div>')
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": f"❌ Error: {str(e)}"})
        
    log_html = f'<div class="thinking-log">{"".join(logs)}</div>'
    return history, "", log_html

def save_data(text, files, topic, config):
    """Integrate with save_research_data and save_research_files"""
    if not text and not files:
        return "⚠️ Please provide either text content or upload files."
    if not topic:
        return "⚠️ Please specify a topic."
    
    results = []
    
    # Handle text content
    if text:
        res_text = save_research_data_logic([text], topic, config=config)
        results.append(f"Text: {res_text}")
    
    # Handle file uploads
    if files:
        # files is a list of gr.FileData or paths depending on Gradio version
        # Usually it's a list of file paths in this context
        res_files = save_research_files_logic(files, topic, config=config)
        results.append(f"Files: {res_files}")
        
    return "\n".join(results)

def refresh_dashboard(config):
    """Get latest stats, format as cards and return topic list"""
    raw_topics = list_research_topics_logic(config=config)
    topic_names = ["default"]
    
    if "No research topics found" in raw_topics or "Error" in raw_topics:
        html = f"<p style='color: #64748b; font-style: italic;'>{raw_topics}</p>"
    else:
        html = '<div class="topic-hull">'
        lines = raw_topics.split('\n')
        for line in lines:
            if not line.strip(): continue
            try:
                name_part = line.split('Topic: ')[1]
                if '(' in name_part:
                    name = name_part.split(' (')[0]
                    count = name_part.split('(')[1].split(')')[0]
                else:
                    name = name_part
                    count = "0 documents"
                
                if name not in topic_names:
                    topic_names.append(name)
                
                html += f"""
                <div class="topic-card" onclick="window.setTopic('{name}')">
                    <div class="topic-title">📁 {name}</div>
                    <div class="topic-count">📊 {count}</div>
                </div>
                """
            except:
                html += f'<div class="topic-card">{line}</div>'
        html += '</div>'
    
    # Return HTML and updated dropdown choices
    return html, gr.update(choices=topic_names), gr.update(choices=topic_names)

def get_default_config():
    """Load defaults from env or fallbacks."""
    return {
        "LLM_PROVIDER": os.getenv("LLM_PROVIDER", "ollama"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "RESEARCH_DB_PATH": os.getenv("RESEARCH_DB_PATH", os.path.expanduser("~/kavi_research_db")),
        "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        "OLLAMA_EMBED_MODEL": os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text"),
    }

def main():
    default_cfg = get_default_config()

    with gr.Blocks(title="Kavi Research Assistant") as demo:
        # State for configuration
        config_state = gr.State(default_cfg)
        
        # Hidden topic setter for JS integration
        hidden_topic = gr.Textbox(visible=False, elem_id="hidden_topic_setter")

        # --- HEADER ---
        with gr.Row(elem_classes="header-row"):
            gr.HTML(f"""
            <div style="display: flex; align-items: center; justify-content: center; padding: 10px; gap: 15px;">
                <img src="data:image/png;base64,{LOGO_BASE64}" style="height: 45px; width: auto;" alt="Kavi Logo">
                <div style="text-align: left;">
                    <h1 style="background: linear-gradient(to right, #6366f1, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.8em; font-weight: 800; margin: 0; line-height: 1;">
                        KAVI RESEARCH
                    </h1>
                    <p style="font-size: 0.85rem; color: #7c3aed; margin: 0; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                        YOUR PREMIUM AI RESEARCH LIBRARIAN
                    </p>
                </div>
            </div>
            """)

        with gr.Tabs():
            # --- TAB 1: ASK RESEARCHER ---
            with gr.TabItem("💬 Ask Researcher", id=0):
                with gr.Row(elem_classes="compact-row"):
                    with gr.Column(scale=1):
                        with gr.Group():
                            gr.Markdown("### 🎯 Search Context")
                            chat_topic = gr.Dropdown(
                                label="Active Topic", 
                                choices=["default"],
                                value="default", 
                                info="Which database should I search?"
                            )
                        
                        with gr.Accordion("📖 Usage Guide", open=False):
                            gr.HTML("""
                            <div class="guide-box">
                                <p style="margin-bottom: 8px;"><strong>Quick Tips:</strong></p>
                                <ol style="padding-left: 20px; font-size: 0.85rem; color: #1e40af;">
                                    <li>Upload data in "Save Knowledge" first.</li>
                                    <li>Select your topic in the dropdown.</li>
                                    <li>Ask Kavi to summarize or find facts.</li>
                                </ol>
                            </div>
                            """)
                        
                        with gr.Accordion("🔍 Thinking Process", open=True):
                            chat_logs = gr.HTML('<div class="thinking-log">System Ready. Waiting for query...</div>')
                    
                    with gr.Column(scale=3):
                        chatbot = gr.Chatbot(
                            label="Research Conversation", 
                            height=380, 
                            avatar_images=(None, "https://kavi.ai/favicon.ico")
                        )
                        with gr.Group():
                            msg = gr.Textbox(
                                label="Your Question", 
                                placeholder="Ask Kavi something...", 
                                lines=1,
                                autofocus=True,
                                scale=4
                            )
                            with gr.Row():
                                clear = gr.Button("🗑️ Clear", variant="secondary", scale=1)
                                ask_btn = gr.Button("🚀 Ask Kavi", variant="primary", scale=2)

                # Wire up events
                msg.submit(format_chat_history, [chatbot, msg, chat_topic, config_state], [chatbot, msg, chat_logs])
                ask_btn.click(format_chat_history, [chatbot, msg, chat_topic, config_state], [chatbot, msg, chat_logs])
                clear.click(lambda: ([], "", '<div class="thinking-log">Logs Cleared.</div>'), None, [chatbot, msg, chat_logs], queue=False)

            # --- TAB 2: SAVE KNOWLEDGE ---
            with gr.TabItem("📥 Save Knowledge", id=1):
                with gr.Row(elem_classes="compact-row"):
                    with gr.Column(scale=2):
                        with gr.Group(elem_classes="group"):
                            gr.Markdown("### 🗂️ 1. Choose Destination")
                            save_topic = gr.Textbox(
                                label="Topic Name", 
                                value="default", 
                                placeholder="e.g. machine-learning",
                                info="Data will be saved into this specific library."
                            )
                        
                        with gr.Tabs():
                            with gr.TabItem("📄 Paste Text"):
                                content_input = gr.TextArea(
                                    label="Text Content", 
                                    placeholder="Paste notes or snippets here...", 
                                    lines=7
                                )
                            with gr.TabItem("📁 Upload Files"):
                                file_input = gr.File(
                                    label="Select Documents",
                                    file_types=[".txt", ".pdf", ".docx"],
                                    file_count="multiple"
                                )
                        
                        save_btn = gr.Button("🚀 Process & Save Data", variant="primary", scale=1)
                    
                    with gr.Column(scale=1):
                        gr.Markdown("### 📡 Activity Log")
                        save_output = gr.HTML("<div class='status-log'>Waiting for input...</div>")
                        
                        with gr.Accordion("💬 Help & Advice", open=True):
                            gr.Markdown("""
                            - **Automatic Deduplication**: Don't worry about saving the same thing twice.
                            - **Topics**: Use one topic per project (e.g., `thesis`, `market-trends`).
                            - **Multi-File**: You can upload a whole folder of PDF papers.
                            """)
                
                # Logic for status update
                def handle_save(text, files, topic, config):
                    status = save_data(text, files, topic, config)
                    return f"<div class='status-log'>{status.replace('\\n', '<br>')}</div>"

                save_btn.click(handle_save, [content_input, file_input, save_topic, config_state], save_output)

            # --- TAB 3: DASHBOARD ---
            with gr.TabItem("📊 Dashboard", id=2):
                with gr.Group(elem_classes="group"):
                    with gr.Row():
                        gr.Markdown("### 📚 Knowledge Inventory")
                        refresh_btn = gr.Button("🔄 Refresh Database", variant="secondary", scale=0)
                    
                    dashboard_output = gr.HTML("<p style='color: #64748b;'>Loading topics...</p>")
                
                with gr.Row(elem_classes="compact-row"):
                    with gr.Column(scale=1):
                        with gr.Group(elem_classes="group"):
                            gr.Markdown("### 📑 Instant Summary")
                            sum_topic = gr.Dropdown(
                                label="Target Topic", 
                                choices=["default"],
                                value="default"
                            )
                            sum_btn = gr.Button("✨ Generate Executive Summary", variant="primary")
                    
                    with gr.Column(scale=2):
                        with gr.Group(elem_classes="group"):
                            gr.Markdown("### 📝 Research Synthesis")
                            sum_output = gr.Markdown("*Summary will be generated using your local data.*")

                # Function to sync topic selection across all dropdowns
                def sync_topics(name):
                    return name, name

                hidden_topic.change(sync_topics, inputs=[hidden_topic], outputs=[chat_topic, sum_topic])

                refresh_btn.click(
                    refresh_dashboard, 
                    inputs=[config_state], 
                    outputs=[dashboard_output, chat_topic, sum_topic]
                )
                sum_btn.click(summarize_topic_logic, inputs=[sum_topic, config_state], outputs=sum_output)
                demo.load(refresh_dashboard, inputs=[config_state], outputs=[dashboard_output, chat_topic, sum_topic])

            # --- TAB 4: SETTINGS ---
            with gr.TabItem("⚙️ Settings", id=3):
                gr.Markdown("### 🛠️ Global Configuration")
                with gr.Row(elem_classes="compact-row"):
                    with gr.Column(scale=1):
                         with gr.Group(elem_classes="group"):
                             gr.Markdown("#### 🧠 AI Engine")
                             provider_in = gr.Radio(
                                    choices=["Ollama", "OpenAI"], 
                                    value=default_cfg["LLM_PROVIDER"].capitalize(), 
                                    label="Select Provider",
                                    info="Switch between local or cloud AI."
                                )
                             gr.Markdown("---")
                             gr.Markdown("Select **Ollama** for privacy and local processing, or **OpenAI** for cloud intelligence.")
                    
                    with gr.Column(scale=2):
                        with gr.Group(elem_classes="group"):
                            gr.Markdown("#### 🔌 Connection Details")
                            
                            # Ollama Group
                            with gr.Group(visible=(default_cfg["LLM_PROVIDER"] == "ollama")) as ollama_group:
                                with gr.Row():
                                    ollama_url_in = gr.Textbox(value=default_cfg["OLLAMA_BASE_URL"], label="Ollama API URL", placeholder="http://127.0.0.1:11434")
                                    ollama_embed_in = gr.Textbox(value=default_cfg["OLLAMA_EMBED_MODEL"], label="Embedding Model", placeholder="nomic-embed-text")
                            
                            # OpenAI Group
                            with gr.Group(visible=(default_cfg["LLM_PROVIDER"] == "openai")) as openai_group:
                                openai_key_in = gr.Textbox(
                                    value=default_cfg["OPENAI_API_KEY"], 
                                    label="OpenAI API Key", 
                                    type="password",
                                    placeholder="sk-..."
                                )
                                gr.Markdown("<small>Your key is stored locally in your session state.</small>")

                with gr.Accordion("📂 Advanced Storage", open=False):
                    db_path_in = gr.Textbox(
                        value=default_cfg["RESEARCH_DB_PATH"], 
                        label="ChromaDB Path",
                        info="Where your knowledge base files are preserved."
                    )

                with gr.Row():
                    update_btn = gr.Button("✨ Apply Changes", variant="primary")
                    config_status = gr.Markdown("")

                # Toggle visibility of connection groups
                def toggle_provider(choice):
                    if choice.lower() == "ollama":
                        return gr.update(visible=True), gr.update(visible=False)
                    else:
                        return gr.update(visible=False), gr.update(visible=True)

                provider_in.change(toggle_provider, inputs=[provider_in], outputs=[ollama_group, openai_group])
                update_btn.click(
                    update_config,
                    inputs=[provider_in, openai_key_in, db_path_in, ollama_url_in, ollama_embed_in],
                    outputs=[config_state, config_status]
                )

        # --- FOOTER ---
        gr.HTML("""
        <div class="footer">
            <p><strong>© 2026 Kavi.ai</strong> • Premium Research Assistant • Built by Machha Kiran</p>
            <p style="margin-top: 4px; opacity: 0.8;">Secure Local Vector Storage • Powered by ChromaDB & Llama 3.2</p>
        </div>
        """)

    demo.launch(
        server_name="0.0.0.0", 
        server_port=7860,
        theme=theme,
        css=custom_css,
        js=js_script
    )

if __name__ == "__main__":
    main()
