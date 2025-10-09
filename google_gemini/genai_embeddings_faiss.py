from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
import faiss
import numpy as np
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
#create a vectorstore  with sample text
from langchain_core.vectorstores import InMemoryVectorStore


index_file = "embeddings.faiss"

embeddings = GoogleGenerativeAIEmbeddings(
     model = "models/gemini-embedding-001",
     google_api_key = os.getenv("GEMINI_API_KEY")
)


# vector = embeddings.embed_query("Chatgpt is the No.1 model")

# vect_np = np.array(vector,dtype=np.float32).reshape(1,-1)

# dm = vect_np.shape[1]

# if os.path.exists(index_file):
#     index = faiss.read_index(index_file)
#     print(f"Faiss file content : {index.ntotal}")
# else:
#     index = faiss.IndexFlatL2(dm)
#     print("Faiss index file created .")

# #Add new vector 
# index.add(vect_np)

# print(f"Number of vectors in FAISS index: {index.ntotal}")

# faiss.write_index(index, index_file)
# print(f"FAISS index saved to {index_file}")

# vector_store = FAISS(...)

# You create a Langchain FAISS wrapper that connects embeddings and your FAISS index.

# embedding_function=embeddings: tells it how to convert text to embeddings.

# index=index: the actual FAISS index object that stores vectors.

# docstore=InMemoryDocstore(): a small in-memory database to store the original documents or metadata corresponding to each vector.

# index_to_docstore_id={}: a dictionary that maps FAISS vector indices to your documents' IDs in the docstore.

vector = embeddings.embed_query("Hi my name is K pavan kumar")
embedding_dim = len(vector)
index = faiss.IndexFlatL2(embedding_dim)

vector_store = FAISS(
    embedding_function = embeddings,
    index = index,
    docstore = InMemoryDocstore(),
    index_to_docstore_id = {},
)

vect_np = np.array(vector, dtype=np.float32).reshape(1, -1)
index.add(vect_np)

# Link index to document
vector_store.index_to_docstore_id[0] = "doc_0"
vector_store.docstore._dict["doc_0"] = Document(page_content="Hi my name is K pavan kumar")

print(vector_store)

for faiss_id, doc_id in vector_store.index_to_docstore_id.items():
    doc = vector_store.docstore.search(doc_id)
    vector = vector_store.index.reconstruct(faiss_id)
    print(f"\nVector ID: {faiss_id}")
    print(f"Vector: {vector}")
    print(f"Text: {doc.page_content}")


#------ embedding mutiple strings as a batch------------
vectors = embeddings.embed_documents(
    [
        "Dell is the famous laptop brand",
        "Samsung is the No.1 brand selling mobile",
        "Pavan is an SRK college student"
    ]
)

print("length of vectors :",len(vectors))
print("vector index :",vectors[0])


#Indexing and Retrieval
#------------------- indexing and retriving data usig as_retrive-------------
text = "Langchain is the part of LLM . which we use its components and models to process the data."

vectorstore = InMemoryVectorStore.from_texts(
    [text],
    embedding= embeddings
)

# using vectorestore as retrieval
retrival= vectorstore.as_retriever()

# retrieve most similar text
retrieved_document = retrival.invoke("What is langchain")

print(f"Retrieved document  {retrieved_document[0].page_content}")

