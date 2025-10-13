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
from fastapi import FastAPI , HTTPException ,UploadFile, File
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel


os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

app= FastAPI(title=".PDF based chatbot")



# -----------------------
# 🔑 Setup LLM + Embeddings
# -----------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

# -----------------------
# 🧠 Globals
# -----------------------
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

class Query(BaseModel):
    query : str

# -----------------------
# 📄 PDF Loading & Processing
# -----------------------
def load_pdf(file):
    global vector_store, conversation_chain, memory

    # Handle both file path or UploadFile object
    if isinstance(file, str):
        file_path = file  # file is already a path
    else:
        # file is file-like object: save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            file_path = tmp.name

    loader = PyPDFLoader(file_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    docs = splitter.split_documents(pages)

    # Use FAISS vector store
    vector_store = FAISS.from_documents(docs, embeddings)
    retriever = vector_store.as_retriever()

    prompt_template = PromptTemplate(
        template=CUSTOM_PROMPT,
        input_variables=["context", "question"]
    )

    # Reset memory for new PDF
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Build new conversation chain
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt_template}
    )

    return "✅ PDF loaded and processed successfully!"


# -----------------------
# 🗣 Query Handler
# -----------------------
def handle_query(query):
    if not query.strip():
        return "⚠️ Please ask a valid question."

    if any(word in query.lower() for word in ["exit", "quit", "bye", "goodbye"]):
        return "Thanks! Goodbye 👋"

    if conversation_chain is None:
        return "⚠️ Please upload and process a PDF first."

    try:
        result = conversation_chain.invoke({"question": query})
        answer = result.get("answer", "")
        if not answer.strip() or "I don't know" in answer:
            fallback = llm.invoke([HumanMessage(content=query)])
            return fallback.content
                                  
        return answer
    except Exception as e:
        return f"❌ Error during query: {e}"


# -----------------------
# 🔄 Process User Interaction
# -----------------------
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
        return history + [[message, "⚠️ Please enter a valid question."]], status_msg or "⚠️ No input."

    # Get bot response
    response = handle_query(message)

    # Update history
    history.append([message, response])
    return history, status_msg




# ✅ Optional: add endpoint to return Gradio URL
@app.post("/query-parameter")
def Query(req:Query):

    #handle query
    response = handle_query(req.query)

    return response



@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Save uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name  # tmp_path is a string

        # Call load_pdf with the string path
        status = load_pdf(tmp_path)

        return {"status": status}
    except Exception as e:
        return {"error": str(e)}


# -----------------------
# 🚀 Run
# -----------------------
# if __name__ == "__main__":
#     demo.launch()
