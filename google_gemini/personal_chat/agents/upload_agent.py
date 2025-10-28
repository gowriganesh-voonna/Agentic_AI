import tempfile
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from config.prompt import prompt_template
from utils.memory_utils import build_memory_for_session
from config.settings import GEMINI_API_KEY
from langchain_community.embeddings import HuggingFaceEmbeddings

# 🔹 Initialize LLM (Gemini)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY
)

# 🔹 Use Hugging Face embeddings instead of Google ones
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 🔹 Session-level stores
vector_store_by_session = {}
conversation_chain_by_session = {}
last_uploaded_file_by_session = {}


def safe_embed_documents(docs, embeddings, delay=0.5):
    """Embed one document at a time to avoid API rate/time issues."""
    for idx, doc in enumerate(docs):
        try:
            print(f"🔹 Embedding chunk {idx+1}/{len(docs)}...")
            embeddings.embed_documents([doc.page_content])  # Trigger embedding
            time.sleep(delay)
        except Exception as e:
            print(f"⚠️ Skipping chunk {idx+1}: {e}")


def load_pdf(file, session_id: str):
    if file is None:
        return "No file uploaded."

    # 🔹 Save to a temp file
    if isinstance(file, str):
        file_path = file
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            file_path = tmp.name

    print("📄 Loading and splitting PDF...")
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    # 🔹 Split into smaller text chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=100)
    docs = splitter.split_documents(pages)

    # 🔹 Perform embeddings
    safe_embed_documents(docs, embeddings)

    # 🔹 Create FAISS vector store
    print("🧠 Creating FAISS vector store...")
    vector_store = FAISS.from_documents(docs, embeddings)
    retriever = vector_store.as_retriever()

    # 🔹 Create conversation chain
    from agents.retrieval_agent import create_conversational_chain
    conversation_chain = create_conversational_chain(llm, retriever, session_id)

    # 🔹 Save session context
    vector_store_by_session[session_id] = vector_store
    conversation_chain_by_session[session_id] = conversation_chain
    last_uploaded_file_by_session[session_id] = getattr(file, "name", file)

    return "✅ PDF loaded and processed successfully!"
