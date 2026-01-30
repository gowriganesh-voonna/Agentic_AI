import gradio as gr
import uuid
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from agents.orchestrator import process_and_respond
from agents.upload_agent import load_file, load_multiple_files, clear_session_files

app = FastAPI(title="📄 Smart Document Assistant (Enhanced)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Generate persistent session ID
PERSISTENT_SESSION_ID = str(uuid.uuid4())

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🤖 Smart Document Assistant (Enhanced Edition)
        
        **✨ New Features:**
        - 📚 Multi-file upload support
        - 📊 Document comparison
        - 💾 Conversation export
        - 📖 Citation tracking
        - 🖼️ Image extraction & analysis
        
        Upload documents (PDF/DOCX) and unlock powerful AI features!
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
            file_input = gr.File(
                label="📎 Upload Documents (Single or Multiple)", 
                file_types=[".pdf", ".docx"],
                file_count="multiple",
                type="filepath"
            )
            
            # ✅ NEW: Clear button
            with gr.Row():
                clear_btn = gr.Button("🗑️ Clear All Files", variant="secondary", size="sm")
            
            status_output = gr.Textbox(label="📂 Status", interactive=False, lines=3)
        
        with gr.Column(scale=1):
            session_id_box = gr.Textbox(
                label="🔑 Session ID",
                value=PERSISTENT_SESSION_ID,
                info="Keeps your conversation context",
                interactive=False
            )
            
            download_output = gr.File(
                label="📥 Download Generated Document",
                interactive=False,
                visible=True
            )

    chatbot = gr.Chatbot(
        label="🗨️ Chat with your Documents",
        height=450,
        show_label=True
    )

    with gr.Row():
        user_msg = gr.Textbox(
            placeholder="Ask questions, compare documents, export conversation...",
            label="💬 Your Message",
            scale=4
        )
        submit_btn = gr.Button("Send 🚀", scale=1, variant="primary")

    with gr.Accordion("💡 Quick Examples", open=False):
        gr.Markdown("""
        **📄 Questions:**
        - "What is this document about?"
        - "Summarize the key points"
        - "Who is mentioned in this PDF?"
        
        **📊 Comparisons:**
        - "Compare those 2 documents"
        - "What are the differences?"
        - "Compare FastAPI vs Django"
        
        **💾 Export:**
        - "Export conversation as PDF"
        - "Save chat as Word document"
        
        **📥 Document Generation (requires explicit format):**
        - "Summarize this as PDF" ✅
        - "Give me key points as Word document" ✅
        - "Create a summary report in TXT format" ✅
        
        **🔍 Management:**
        - "List my files"
        - "Clear files"
        - "Search for FastAPI"
        """)

    with gr.Accordion("📚 Feature Guide", open=False):
        gr.Markdown("""
        ### 🎯 How It Works:
        
        **✅ Normal Questions** (Just answers, no file generation):
        - "What is MongoDB?" → Answers from PDF
        - "Explain FastAPI in detail" → Detailed explanation
        - "Whose PDF is this?" → Identifies the document
        
        **📥 Document Generation** (Creates downloadable files):
        - Must include BOTH action + format:
          - ✅ "Summarize **as PDF**"
          - ✅ "Explain MongoDB **and give me as Word**"
          - ✅ "Create report **in TXT format**"
        - Or use explicit phrases:
          - ✅ "Give me a file with summary"
          - ✅ "Export this as DOCX"
        
        **📊 Comparisons** (Compares documents):
        - "Compare those documents" → General comparison
        - "Compare X vs Y" → Topic comparison
        - To save comparison: "Compare X vs Y and export as PDF"
        
        **🗑️ Clear Files:**
        - Click the "Clear All Files" button
        - Or type: "Clear files" / "Reset session"
        """)

    def handle_file_upload(files, session_id):
        if files is None:
            return "❌ No files uploaded."
        
        print(f"📤 Uploading files with session_id: {session_id}")
        
        if isinstance(files, list) and len(files) > 1:
            return load_multiple_files(files, session_id)
        else:
            single_file = files[0] if isinstance(files, list) else files
            return load_file(single_file, session_id)
    
    def handle_clear_files(session_id):
        """Clear all files and reset session"""
        result = clear_session_files(session_id)
        return result, []  # Also clear chat history
    
    file_input.upload(
        fn=handle_file_upload,
        inputs=[file_input, session_id_box],
        outputs=[status_output],
    )
    
    # ✅ NEW: Clear button handler
    clear_btn.click(
        fn=handle_clear_files,
        inputs=[session_id_box],
        outputs=[status_output, chatbot]
    )

    def format_for_gradio(history):
        formatted = []
        for h in history:
            if isinstance(h, dict):
                formatted.append(h)
            elif isinstance(h, (list, tuple)) and len(h) == 2:
                formatted.append({"role": "user", "content": h[0]})
                formatted.append({"role": "assistant", "content": h[1]})
        return formatted


    def submit_message(msg, history, file, session_id):
        print(f"💬 Processing message with session_id: {session_id}")
        
        raw_history, status, generated_file = process_and_respond(
            msg, history, file, session_id
        )

        gradio_history = format_for_gradio(raw_history)

        return gradio_history, status, generated_file, ""

    
    submit_btn.click(
        fn=submit_message,
        inputs=[user_msg, chatbot, file_input, session_id_box],
        outputs=[chatbot, status_output, download_output, user_msg]
    )
    
    user_msg.submit(
        fn=submit_message,
        inputs=[user_msg, chatbot, file_input, session_id_box],
        outputs=[chatbot, status_output, download_output, user_msg]
    )

gradio_app = gr.mount_gradio_app(app, demo, path="/chat")

@app.get("/")
def root():
    return {
        "message": "Smart Document Assistant (Enhanced) is running!",
        "version": "2.0",
        "features": [
            "Multi-file upload",
            "Document comparison",
            "Conversation export",
            "Citation tracking",
            "Image extraction",
            "Strict document generation (prevents false triggers)"
        ],
        "chat_url": "/chat"
    }

@app.get("/start_chatbot_application")
def chatbot_application():
    return {"message": "Chatbot is running", "url": "http://localhost:8000/chat"}