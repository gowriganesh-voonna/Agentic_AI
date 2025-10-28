import gradio as gr
import uuid
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from agents.orchestrator import process_and_respond
from agents.upload_agent import load_pdf  # ✅ Import for PDF loading

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
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 PDF Chatbot (Gemini + RAG)")

    with gr.Row():
        file_input = gr.File(label="📎 Upload PDF", file_types=[".pdf"])
        status_output = gr.Textbox(label="📂 Status", interactive=False)

    chatbot = gr.Chatbot(label="🗨️ Chat with your PDF")

    session_id_box = gr.Textbox(
        label="🔑 Session ID",
        value=str(uuid.uuid4()),
        info="Keep this constant to resume memory."
    )

    user_msg = gr.Textbox(
        placeholder="Type your question...",
        label="💬 Your Message"
    )

    # ✅ When user uploads a PDF → process & create vectorstore
    file_input.upload(
        fn=load_pdf,
        inputs=[file_input, session_id_box],
        outputs=[status_output],
    )

    # ✅ When user sends message → use existing session to reply
    user_msg.submit(
        fn=process_and_respond,
        inputs=[user_msg, chatbot, file_input, session_id_box],
        outputs=[chatbot, status_output]
    ).then(lambda: "", None, user_msg)

# ✅ Mount Gradio app inside FastAPI
gradio_app = gr.mount_gradio_app(app, demo, path="/chat")

@app.get("/start_chatbot_application")
def chatbot_application():
    return {"message": "Chatbot is running", "url": "http://localhost:8000/chat"}
