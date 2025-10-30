import tempfile
import time
import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
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

# 🔹 Use Hugging Face embeddings - better model for semantic search
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"  # ✅ Better than MiniLM
)

# 🔹 Session-level stores
vector_store_by_session = {}
conversation_chain_by_session = {}
last_uploaded_file_by_session = {}


def safe_embed_documents(docs, embeddings, delay=0.3):
    """Embed one document at a time to avoid API rate/time issues."""
    for idx, doc in enumerate(docs):
        try:
            print(f"🔹 Embedding chunk {idx+1}/{len(docs)}...")
            embeddings.embed_documents([doc.page_content])
            time.sleep(delay)
        except Exception as e:
            print(f"⚠️ Skipping chunk {idx+1}: {e}")


def load_file(file, session_id: str):
    """
    ✅ Unified function to load either PDF or DOCX file.
    Optimized for Q&A documents and structured content.
    """

    if file is None:
        return "No file uploaded."

    # 🔹 Gradio now passes filepath directly
    file_path = file if isinstance(file, str) else str(file)
    
    if not os.path.exists(file_path):
        return f"❌ File not found: {file_path}"

    print(f"📄 Loading and splitting file ({file_path})...")

    # 🔹 Detect file type
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    else:
        return "❌ Unsupported file type. Please upload PDF or Word (.docx) file."

    # 🔹 Load content
    pages = loader.load()
    
    # ✅ IMPROVED: Better chunking strategy for Q&A documents
    # Larger chunks to keep Q&A pairs together, with overlap for context
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,        # ✅ Increased from 400 to keep complete Q&A together
        chunk_overlap=200,      # ✅ Increased overlap for better context
        separators=[            # ✅ Custom separators for structured documents
            "\n________________________________________\n",  # Question separator
            "\n\n",             # Paragraph break
            "\n",               # Line break
            ". ",               # Sentence break
            " ",                # Word break
        ],
        length_function=len,
    )
    docs = splitter.split_documents(pages)
    
    print(f"📊 Created {len(docs)} chunks from document")

    # 🔹 Perform embeddings
    safe_embed_documents(docs, embeddings)

    # ✅ IMPROVED: Create FAISS with better retrieval settings
    print("🧠 Creating FAISS vector store...")
    vector_store = FAISS.from_documents(docs, embeddings)
    
    # ✅ Configure retriever to fetch more relevant documents
    retriever = vector_store.as_retriever(
        search_type="mmr",           # ✅ Maximum Marginal Relevance for diversity
        search_kwargs={
            "k": 6,                   # ✅ Fetch top 6 chunks (increased from default 4)
            "fetch_k": 20,            # ✅ Fetch 20 candidates before MMR filtering
            "lambda_mult": 0.7        # ✅ Balance between relevance and diversity
        }
    )

    # 🔹 Create conversation chain
    from agents.retrieval_agent import create_conversational_chain
    conversation_chain = create_conversational_chain(llm, retriever, session_id)

    # 🔹 Save session context
    vector_store_by_session[session_id] = vector_store
    conversation_chain_by_session[session_id] = conversation_chain
    last_uploaded_file_by_session[session_id] = getattr(file, "name", file)

    return f"✅ {os.path.basename(file_path)} loaded and processed successfully! ({len(docs)} chunks created)"


# ✅ NEW: Helper to get LLM and retriever for a session
def get_llm_and_retriever(session_id: str):
    """Get the LLM and retriever for a given session."""
    if session_id not in vector_store_by_session:
        raise ValueError(f"No document loaded for session {session_id}")
    
    vector_store = vector_store_by_session[session_id]
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 6,
            "fetch_k": 20,
            "lambda_mult": 0.7
        }
    )
    return llm, retriever