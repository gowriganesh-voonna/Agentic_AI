from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
import os

# Set up embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Initialize Chroma vector store
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db"
)

# Add documents
docs = [
    Document(page_content="LangChain is a framework for building LLM-powered apps.", metadata={"topic": "LangChain"}),
    Document(page_content="Chroma is a vector database for storing embeddings.", metadata={"topic": "Chroma"}),
]

vector_store.add_documents(docs)
vector_store.persist()  # Optional but good for persistence

# Inspect stored vectors
results = vector_store.get()

for doc_id, metadata in zip(results['ids'], results['metadatas']):
    print(f"ID: {doc_id}, Metadata: {metadata}")

# Perform similarity search  (use openai or hugging face transformers)
# query = "What is LangChain?"
# matched_docs = vector_store.similarity_search(query, k=3)

# for i, doc in enumerate(matched_docs):
#     print(f"\nDocument {i+1}:\n{doc.page_content}")

print("\nPersisted document contents:")
for doc in results['documents']:
    print(doc)
