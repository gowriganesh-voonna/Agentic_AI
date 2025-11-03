import tempfile
import time
import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from config.prompt import prompt_template
from utils.memory_utils import build_memory_for_session
from config.settings import GEMINI_API_KEY
from langchain_huggingface import HuggingFaceEmbeddings
from datetime import datetime

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY
)

# Use Hugging Face embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

# Session-level stores
vector_store_by_session = {}
conversation_chain_by_session = {}
uploaded_files_by_session = {}


def safe_embed_documents(docs, embeddings, delay=0.3):
    """Embed one document at a time to avoid API rate/time issues."""
    for idx, doc in enumerate(docs):
        try:
            print(f"🔹 Embedding chunk {idx+1}/{len(docs)}...")
            embeddings.embed_documents([doc.page_content])
            time.sleep(delay)
        except Exception as e:
            print(f"⚠️ Skipping chunk {idx+1}: {e}")


def load_single_file(file_path: str):
    """Load a single file and return processed documents with metadata."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Detect file type
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif file_ext == ".docx":
        loader = Docx2txtLoader(file_path)
    elif file_ext == ".txt":
        loader = TextLoader(file_path, encoding='utf-8')
    else:
        raise ValueError(f"Unsupported file type: {file_ext}. Please upload PDF, DOCX, or TXT.")
    
    # Load content
    pages = loader.load()
    
    # Enhanced chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,  # ✅ Increased for better context
        chunk_overlap=300,
        separators=[
            "\n________________________________________\n",
            "\n\n",
            "\n",
            ". ",
            " ",
        ],
        length_function=len,
    )
    
    docs = splitter.split_documents(pages)
    
    # Add enhanced metadata
    filename = os.path.basename(file_path)
    for idx, doc in enumerate(docs):
        doc.metadata.update({
            "source_file": filename,
            "chunk_id": idx,
            "total_chunks": len(docs),
            "upload_time": datetime.now().isoformat(),
            "file_type": file_ext[1:]  # Remove dot
        })
    
    return docs, filename, len(docs)


def load_file(file, session_id: str):
    """
    ✅ FIXED: Properly clears old session data before loading new file
    """
    if file is None:
        return "❌ No file uploaded."
    
    file_path = file if isinstance(file, str) else str(file)
    
    try:
        print(f"📄 Loading file: {file_path}")
        
        # ✅ CRITICAL FIX: Clear old session data first
        if session_id in vector_store_by_session:
            print("🗑️ Clearing previous session data...")
            del vector_store_by_session[session_id]
        if session_id in conversation_chain_by_session:
            del conversation_chain_by_session[session_id]
        if session_id in uploaded_files_by_session:
            del uploaded_files_by_session[session_id]
        
        # Load and process file
        docs, filename, chunk_count = load_single_file(file_path)
        
        # Embed documents
        safe_embed_documents(docs, embeddings)
        
        # Create NEW vector store (not adding to existing)
        print("🧠 Creating fresh FAISS vector store...")
        vector_store = FAISS.from_documents(docs, embeddings)
        vector_store_by_session[session_id] = vector_store
        
        # Configure retriever
        retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 8,
                "fetch_k": 25,
                "lambda_mult": 0.7
            }
        )
        
        # Create conversation chain
        from agents.retrieval_agent import create_conversational_chain
        conversation_chain = create_conversational_chain(llm, retriever, session_id)
        conversation_chain_by_session[session_id] = conversation_chain
        
        # Track uploaded file
        uploaded_files_by_session[session_id] = [{
            "filename": filename,
            "chunks": chunk_count,
            "upload_time": datetime.now().isoformat(),
            "file_path": file_path
        }]
        
        return f"✅ {filename} loaded successfully!\n📊 {chunk_count} chunks created\n🔄 Session reset - ready for new queries"
    
    except Exception as e:
        print(f"⚠️ Error loading file: {e}")
        import traceback
        traceback.print_exc()
        return f"❌ Error loading file: {e}"


def load_multiple_files(files, session_id: str):
    """Load multiple files at once and merge into single vector store"""
    if not files or len(files) == 0:
        return "❌ No files uploaded."
    
    try:
        # ✅ Clear old session data first
        print("🗑️ Clearing previous session data for multi-file upload...")
        if session_id in vector_store_by_session:
            del vector_store_by_session[session_id]
        if session_id in conversation_chain_by_session:
            del conversation_chain_by_session[session_id]
        if session_id in uploaded_files_by_session:
            del uploaded_files_by_session[session_id]
        
        all_docs = []
        file_stats = []
        
        print(f"📚 Loading {len(files)} files...")
        
        for file in files:
            file_path = file if isinstance(file, str) else str(file)
            docs, filename, chunk_count = load_single_file(file_path)
            all_docs.extend(docs)
            
            file_stats.append({
                "filename": filename,
                "chunks": chunk_count,
                "upload_time": datetime.now().isoformat(),
                "file_path": file_path
            })
            
            print(f"✅ Loaded {filename}: {chunk_count} chunks")
        
        # Embed all documents
        print(f"🔹 Embedding {len(all_docs)} total chunks...")
        safe_embed_documents(all_docs, embeddings)
        
        # Create NEW vector store
        print("🧠 Creating fresh FAISS vector store...")
        vector_store = FAISS.from_documents(all_docs, embeddings)
        vector_store_by_session[session_id] = vector_store
        
        # Configure retriever
        retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 10,
                "fetch_k": 30,
                "lambda_mult": 0.7
            }
        )
        
        # Create conversation chain
        from agents.retrieval_agent import create_conversational_chain
        conversation_chain = create_conversational_chain(llm, retriever, session_id)
        conversation_chain_by_session[session_id] = conversation_chain
        
        # Track all uploaded files
        uploaded_files_by_session[session_id] = file_stats
        
        # Generate summary
        total_files = len(file_stats)
        total_chunks = sum(f["chunks"] for f in file_stats)
        file_names = [f["filename"] for f in file_stats]
        
        summary = f"""✅ Successfully loaded {total_files} files!

📁 Files loaded:
{chr(10).join(f"  • {name}" for name in file_names)}

📊 Total chunks created: {total_chunks}
🔄 Session reset - ready for queries across all documents!"""
        
        return summary
    
    except Exception as e:
        print(f"⚠️ Error loading multiple files: {e}")
        import traceback
        traceback.print_exc()
        return f"❌ Error loading files: {e}"


def list_uploaded_files(session_id: str):
    """List all uploaded files for a session"""
    if session_id not in uploaded_files_by_session or not uploaded_files_by_session[session_id]:
        return "📭 No files uploaded yet."
    
    files = uploaded_files_by_session[session_id]
    
    result = f"📚 Uploaded Files ({len(files)} total):\n\n"
    
    for idx, file_info in enumerate(files, 1):
        result += f"{idx}. **{file_info['filename']}**\n"
        result += f"   • Chunks: {file_info['chunks']}\n"
        result += f"   • Uploaded: {file_info['upload_time'][:19]}\n\n"
    
    total_chunks = sum(f["chunks"] for f in files)
    result += f"📊 **Total chunks across all files:** {total_chunks}"
    
    return result


def clear_session_files(session_id: str):
    """Clear all files from a session"""
    cleared = False
    
    if session_id in vector_store_by_session:
        del vector_store_by_session[session_id]
        cleared = True
    if session_id in conversation_chain_by_session:
        del conversation_chain_by_session[session_id]
        cleared = True
    if session_id in uploaded_files_by_session:
        del uploaded_files_by_session[session_id]
        cleared = True
    
    if cleared:
        return "✅ All files and session data cleared. Upload new files to start fresh."
    else:
        return "ℹ️ No files to clear - session was already empty."


def get_llm_and_retriever(session_id: str):
    """Get the LLM and retriever for a given session."""
    if session_id not in vector_store_by_session:
        raise ValueError(f"No document loaded for session {session_id}")
    
    vector_store = vector_store_by_session[session_id]
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 8,
            "fetch_k": 25,
            "lambda_mult": 0.7
        }
    )
    return llm, retriever