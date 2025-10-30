import gradio as gr
import uuid
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from agents.orchestrator import process_and_respond
from agents.upload_agent import load_file

app = FastAPI(title="📄 PDF Chatbot (Gemini + RAG)")

# ✅ Allow frontend (Gradio) to connect to FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Build Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🤖 Smart Document Assistant (Gemini + RAG)
        
        Upload documents (PDF/DOCX) and chat with them. Ask for summaries, rewrites, or export as PDF/DOCX/TXT!
        
        **Example requests:**
        - "Summarize this document"
        - "Explain FastAPI in detail and give me as PDF"
        - "Rewrite the MongoDB section as a Word document"
        - "Create a summary report in txt format"
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
            file_input = gr.File(
                label="📎 Upload Document", 
                file_types=[".pdf", ".docx"],
                type="filepath"  # Changed from "binary" to "filepath"
            )
            status_output = gr.Textbox(label="📂 Status", interactive=False, lines=2)
        
        with gr.Column(scale=1):
            session_id_box = gr.Textbox(
                label="🔑 Session ID",
                value=str(uuid.uuid4()),
                info="Keep this constant to resume memory.",
                interactive=True
            )
            
            # ✅ NEW: Download button for generated files
            download_output = gr.File(
                label="📥 Download Generated Document",
                interactive=False,
                visible=True
            )

    chatbot = gr.Chatbot(
        label="🗨️ Chat with your Document",
        height=400,
        show_label=True
    )

    with gr.Row():
        user_msg = gr.Textbox(
            placeholder="Type your question or request (e.g., 'summarize as PDF')...",
            label="💬 Your Message",
            scale=4
        )
        submit_btn = gr.Button("Send 🚀", scale=1, variant="primary")

    # ✅ Example requests
    gr.Examples(
        examples=[
            "What topics are covered in this document?",
            "Summarize the entire document",
            "Explain FastAPI concepts in detail",
            "Give me all MongoDB topics as a PDF",
            "Rewrite this content as a Word document",
            "Create a summary report in txt format"
        ],
        inputs=user_msg,
        label="💡 Try these examples:"
    )

    # ✅ When user uploads a document → process & create vectorstore
    file_input.upload(
        fn=load_file,
        inputs=[file_input, session_id_box],
        outputs=[status_output],
    )

    # ✅ When user sends message → process and potentially generate file
    def submit_message(msg, history, file, session_id):
        history, status, generated_file = process_and_respond(msg, history, file, session_id)
        return history, status, generated_file, ""  # Clear input after submit
    
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

# ✅ Mount Gradio app inside FastAPI
gradio_app = gr.mount_gradio_app(app, demo, path="/chat")

@app.get("/")
def root():
    return {"message": "Smart Document Assistant is running!", "chat_url": "/chat"}

@app.get("/start_chatbot_application")
def chatbot_application():
    return {"message": "Chatbot is running", "url": "http://localhost:8000/chat"}