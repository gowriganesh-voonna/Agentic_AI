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

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

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


# -----------------------
# 📄 PDF Loading & Processing
# -----------------------
def load_pdf(file):
    global vector_store, conversation_chain, memory

    if file is None:
        return "❌ No file uploaded."

    file_path = file.name
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
            return "🤖 I can't find any related information."
        return answer
    except Exception as e:
        return f"❌ Error during query: {e}"


# -----------------------
# 🔄 Process User Interaction
# -----------------------
def process_and_respond(file, query):
    global chat_log, last_uploaded_file

    status_msg = ""

    # Load PDF only if new file is uploaded
    if file is not None:
        if last_uploaded_file != file.name:
            status_msg = load_pdf(file)
            chat_log = []  # reset chat history on new PDF
            last_uploaded_file = file.name

    if not query.strip():
        return "", chat_log, status_msg or "⚠️ Please enter a question."

    response = handle_query(query)

    # Update chat history in Gradio chatbot format (list of dicts with 'role' and 'content')
    chat_log.append({"role": "user", "content": query})
    chat_log.append({"role": "assistant", "content": response})

    return response, chat_log, status_msg


# -----------------------
# 🎨 Gradio UI
# -----------------------
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 PDF Q&A Chatbot with Memory (RAG + Gemini Pro)")

    with gr.Row():
        file_input = gr.File(label="📎 Upload your PDF", file_types=[".pdf"])
        status_output = gr.Textbox(label="📂 PDF Status", interactive=False)

    query_input = gr.Textbox(lines=2, label="💬 Ask a question about the PDF:")
    submit_btn = gr.Button("📤 Submit")

    output = gr.Textbox(label="🤖 Bot Response", lines=6)
    chat_history = gr.Chatbot(label="💬 Chat History", elem_id="chatbot", type="messages")

    submit_btn.click(
        fn=process_and_respond,
        inputs=[file_input, query_input],
        outputs=[output, chat_history, status_output],
        queue=True
    ).then(lambda: "", inputs=None, outputs=query_input)  # Clear query box after submit


# -----------------------
# 🚀 Run
# -----------------------
if __name__ == "__main__":
    demo.launch()
