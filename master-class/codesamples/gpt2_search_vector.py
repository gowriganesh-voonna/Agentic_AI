# Import required libraries
import torch
from transformers import GPT2Tokenizer, GPT2Model
import faiss
import numpy as np
 
# Import custom exception handling decorator
from utiles.decoratores import handle_exceptions
 
# Load GPT-2 tokenizer and model once globally
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")
model.eval()  # Set the model to evaluation mode (not training)
 
@handle_exceptions
def get_embedding(text):
    """
    Generates an embedding for the input text using GPT-2.
    """
    # Tokenize the input text and convert to tensor format
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    
    # Disable gradient calculations for faster inference
    with torch.no_grad():
        outputs = model(**inputs)  # Forward pass through the model
    
    # Get the last hidden states (token-level embeddings)
    last_hidden_state = outputs.last_hidden_state
    
    # Take the average across all token embeddings to form a sentence-level embedding
    sentence_embedding = last_hidden_state.mean(dim=1).squeeze().numpy()
    
    return sentence_embedding
 
@handle_exceptions
def build_faiss_index(documents):
    """
    Builds a FAISS index from a list of documents.
    """
    # Convert each document into an embedding
    embeddings = np.array([get_embedding(doc) for doc in documents]).astype('float32')
    
    # Determine the dimension of the embeddings
    embedding_dim = embeddings.shape[1]
    
    # Create a FAISS index with L2 distance metric
    index = faiss.IndexFlatL2(embedding_dim)
    
    # Add all embeddings to the FAISS index
    index.add(embeddings)
    
    return index, embeddings
 
@handle_exceptions
def search_documents(query, index, documents, k=3):
    """
    Searches for the top K similar documents to the query.
    """
    # Generate an embedding for the user's query
    query_vec = get_embedding(query).astype('float32').reshape(1, -1)
    
    # Search in the FAISS index for the top K similar vectors
    D, I = index.search(query_vec, k=k)
    
    # Retrieve and return the matching documents
    results = [documents[i] for i in I[0]]
    return results
 
@handle_exceptions
def main():
    """
    Main driver function to demonstrate vector-based search.
    """
    # Sample document corpus
    documents = [
        "The cat is sitting on the mat.",
        "Artificial intelligence is transforming the world.",
        "A dog barked loudly near the house.",
        "Machine learning is a subset of AI.",
        "The sun rises in the east."
    ]
    
    # Build index from the document list
    index, _ = build_faiss_index(documents)
    
    # Example query
    query = "What is machine learning?"
    
    # Perform the vector search
    top_matches = search_documents(query, index, documents, k=3)
    
    # Print the query and matching results
    print("Query:", query)
    print("\nTop Matches:")
    for match in top_matches:
        print("-", match)
 

if __name__ == "__main__":
    main()
 

# Output :
# Query is : I enjoy learning Python

# 0.9990 → Studying Python is enjoyable
# 0.9980 → Python is a powerful language
# 0.9971 → The weather is nice today
# 0.9938 → I love Programing in Java
# 0.9888 → Bananas are rich is potassium