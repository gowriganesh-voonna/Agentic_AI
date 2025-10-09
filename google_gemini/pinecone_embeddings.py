from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain.schema import Document





"""
Pinecone is a vector database designed specifically for storing and searching high-dimensional vector embeddings — which are numerical representations of data like text, images, or audio. It's built to support fast, scalable, and efficient similarity search, which is crucial for many AI and machine learning applications.
🧠 What is Pinecone?
- Vector database: Unlike traditional databases that store structured data (like rows and columns), Pinecone stores vectors — arrays of numbers that represent the semantic meaning of data.
- Similarity search: It allows you to find items that are "similar" to a query vector, which is essential for tasks like recommendation systems, semantic search, and question answering.
- Managed infrastructure: Pinecone handles indexing, scaling, and optimization behind the scenes, so developers can focus on building applications without worrying about performance bottlenecks.
🔍 Why are we using Pinecone in this code?
- We're working with LangChain, a framework for building applications powered by language models.
- The PineconeVectorStore is used to store embeddings generated from text (e.g., documents, queries) and retrieve relevant results based on similarity.
- This setup enables semantic search — instead of keyword matching, it finds documents that are conceptually similar to a user's query.

"""

embeddings = GoogleGenerativeAIEmbeddings(
    model = "models/gemini-embedding-001",
    google_api_key = os.getenv("GEMINI_API_KEY")
)

pc = Pinecone(api_key = os.getenv("pinecone"))
index = pc.Index("my-langchain-index")

vector_store = PineconeVectorStore(embedding = embeddings, index = index)

docs =[
     Document(page_content="Quantum computing uses qubits instead of bits.", metadata={"source": "doc1"}),
     Document(page_content="Classical computers use binary logic.", metadata={"source": "doc2"})

]

vector_store.add_documents(docs)



query = "Quantum computing uses qubits instead of bits?"
query_embedding = embeddings.embed_query(query)

# search the vector store
results = vector_store.similarity_search_by_vector(query_embedding,k=5)


# Step 3: Print the results
for i, doc in enumerate(results):
    print(f"\nResult {i+1}")
    print("Content:", doc.page_content)
    print("Metadata:", doc.metadata)


stats = index.describe_index_stats()
print("Total vectors:", stats["total_vector_count"])
