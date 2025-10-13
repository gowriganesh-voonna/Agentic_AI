
import os
import gradio as gr
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
import tempfile
from fastapi import FastAPI , HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware


os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


app= FastAPI(title=".PDF based chatbot")


# CORS (optional, useful for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#  Setup LLM + Embeddings

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)


#  Globals

vector_store = None
conversation_chain = None
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
chat_log = []  # will store chat as list of dicts for gr.Chatbot
last_uploaded_file = None

CUSTOM_PROMPT = """You are a helpful assistant. Use the following context to answer the question.
If the answer is not contained in the context, respond exactly with:
"I don't know, it is not related to the PDF."

Context:
{context}

Question:
{question}

Answer:"""


# -----------------------
# 📄 PDF Loading & Processing
# -----------------------
def load_pdf(file):
    global vector_store, conversation_chain, memory

    if file is None:
        return " No file uploaded."

    #file_path = file.name

    # If file is a string (filepath), just use it directly
    if isinstance(file, str):
        file_path = file

    else:
        # file is file-like object: save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            file_path = tmp.name

    # filename = os.path.basename(file.name)
    # # Save the uploaded file to a temporary path
    # file_path = f"temp_{filename}"
    # with open(file_path, "wb") as f:
    #     f.write(file.read())  # Save uploaded file contents

    loader = PyPDFLoader(file_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    docs = splitter.split_documents(pages)

    # Use FAISS in-memory vector store for speed
    vector_store = FAISS.from_documents(docs, embeddings)
    retriever = vector_store.as_retriever()

    prompt_template = PromptTemplate(
        template=CUSTOM_PROMPT,
        input_variables=["context", "question"]
    )

    # Reset memory each time a new PDF is loaded
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt_template}
    )

    return " PDF loaded and processed successfully!"


# Query Handler

def handle_query(query):
    if not query.strip():
        return " Please ask a valid question."

    if any(word in query.lower() for word in ["exit", "quit", "bye", "goodbye"]):
        return "Thanks! Goodbye "

    if conversation_chain is None:
        return " Please upload and process a PDF first."

    try:
        result = conversation_chain.invoke({"question": query})
        answer = result.get("answer", "")
        if not answer.strip() or "I don't know" in answer:
            fallback = llm.invoke([HumanMessage(content=query)])
            return fallback.content
                                  
        return answer
    except Exception as e:
        return f" Error during query: {e}"


# Process User Interaction

def process_and_respond(message, history, file):
    global chat_log, last_uploaded_file

    status_msg = ""

    # Load new PDF if different from previous
    if file is not None and (last_uploaded_file != file.name):
        status_msg = load_pdf(file)
        chat_log = []
        last_uploaded_file = file.name
        history = []  # reset chat history

    # If no message
    if not message.strip():
        return history + [[message, " Please enter a valid question."]], status_msg or " No input."

    # Get bot response
    response = handle_query(message)

    # Update history
    history.append([message, response])
    return history, status_msg


#  Gradio UI


with gr.Blocks() as demo:
    gr.Markdown("## 🤖 PDF Chatbot (Gemini + RAG)")

    with gr.Row():
        with gr.Column(scale=3):
            file_input = gr.File(label="📎 Upload PDF", file_types=[".pdf"])
        with gr.Column(scale=7):
            status_output = gr.Textbox(label="📂 Status", interactive=False)

    chatbot = gr.Chatbot(label="🗨️ Chat with your PDF", elem_id="chatbot")
    user_msg = gr.Textbox(placeholder="Type your question and press Enter...", label="💬 Your Message", lines=1)

    # Main interaction function
    user_msg.submit(
        fn=process_and_respond,
        inputs=[user_msg, chatbot, file_input],
        outputs=[chatbot, status_output]
    ).then(lambda: "", None, user_msg)  # Clear input after submit


#  Mount Gradio app into FastAPI
gradio_app = gr.mount_gradio_app(app, demo, path="/chat")

# Optional: add endpoint to return Gradio URL
@app.get("/start_chatbot_application")
def chatbot_application():
    return JSONResponse(
        content={"message": "Chatbot is running", "url": "http://localhost:8000/chat"},
        status_code=200
    )
