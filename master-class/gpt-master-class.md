# Masterclass for GPT-2 and GPT-4

## Overview

In this article, we will cover the following key concepts:

- **Tokens**: How large language models process text using tokens.
- **Embeddings**: Representing words, sentences or tokens (text ->Tokens -> Embeddings) in a high dimenisonal space.
- **Vector Based Search**: Efficiently searching through embeddings using similarity metrics.
- **Model** : A model like GPT is a powerful language processing system that understands and generates human-like text based on input.It uses billions of parameters trained on vast text data to predict the next word or sentence in a conversation.
- **FastAPI**- FastAPI is a modern and high-performance Python web framework used to build APIs quickly and efficiently.
- **Mongodb**- MongoDB is a popular, open-source, NoSQL database that stores data in JSON-like documents organized into collections. 


Throughout the article, we'll explore how these components work individually with examples and end of this article we will cover one example covering all components or topics.

By the end of this masterclass, you'll have a foundational understanding and you can able to do real world scenario.

-------------------------------------------------------------------------------------------

# 1. Tokens :

**Tokens** can be single characters like z or whole words like cat. Long words are broken up into several tokens. The set of all tokens used by the model is called the vocabulary, and the process of splitting text into tokens is called tokenization.

For Example :
```Python :
Text : "Learning Python is easy"
Tokens : ['Learning' ,'Python','is','easy']
 ```

The model doesnt split at just spaces - It uses a special tokenizer like Byte Pair Encoding(BPE) or others depending on the model.

### ❓ Why Tokens are Important? 
The maximum input and output size of GPT models is defined in terms of tokens,not characters or words.

### ❓ Why Are We Using a Tokenizer?
 
Before feeding any text to a model like GPT-2, we must convert it into tokens. This process:
- Helps the model understand and predict language patterns
- Converts readable text into numerical input
- Is required for generating or analyzing text with pre-trained models
 
Instead of writing our own tokenizer from scratch, we use a **pre-built tokenizer** from a well-maintained library — `transformers` by Hugging Face.

###  What is `transformers`?
 
**transformers** is a Python library created by Hugging Face.Transformers are a powerful deep learning architecture designed to handle sequential data like text. They use a mechanism called **self-attention** that allows the model to focus on different parts of the input sentence when generating output. This helps capture the context and relationships between words, even if they are far apart. Transformers are the foundation behind many modern language models, including GPT-2. When we use from transformers import GPT2Tokenizer,GPT2LMHeadModel or GPT2Model, we are importing components built on this architecture, allowing us to tokenize input text and work with pretrained language models effectively. It allows us to:
 
- Load **pre-trained models** (like GPT-2, BERT, etc.)
- Use **pre-trained tokenizers** for converting text to tokens and back
- Easily run inference, text generation, embeddings, and more
 
It's widely used in the AI/NLP industry and supports models from OpenAI, Meta, Google, and others.

---
 
### Installation (Required Only Once)
 
Install the `transformers` library using pip:
 
```bash
pip install transformers 
```
---
## 🤗 What is Hugging Face?
 
**Hugging Face** is a company and open-source platform that provides powerful tools, libraries, and pre-trained models for **Natural Language Processing (NLP)** and **Machine Learning (ML)**.
 
---
 
### 🧠 What Does Hugging Face Offer?
 
- It is best known for the `transformers` library, which gives access to **state-of-the-art models** like:
  - GPT-2, GPT-3, GPT-4
  - BERT, RoBERTa, T5, DistilBERT
- These models can be used for:
  - Text generation
  - Sentiment analysis
  - Translation
  - Text summarization
  - Question answering
 
---
 
### 📦 Key Libraries
 
| Library       | Purpose                                             |
|---------------|------------------------------------------------------|
| `transformers`| Pre-trained transformer models (e.g., GPT, BERT)     |
| `datasets`    | Load, process, and share datasets for ML/NLP         |
| `tokenizers`  | Fast tokenization for text processing                |
 
---
 
### 🌐 Official Website
 
Visit: [https://huggingface.co](https://huggingface.co)
 
--------
## 🧾 What is GPT2Tokenizer?
 
`GPT2Tokenizer` is a class provided by Hugging Face's `transformers` library. It is used to **convert raw text into tokens** (numerical format) that the GPT-2 model can understand and process.
 
---
 
### ⚙️ Purpose of GPT2Tokenizer
 
- **Tokenization:** Breaks input text into smaller units called *tokens*.
- **Encoding:** Converts tokens into integer IDs (model-readable format).
- **Decoding:** Converts model output (IDs) back into human-readable text.
 

---------
###Example:  Tokenizing Text using GPT-2 Tokenizer

```python
from transformers import GPT2Tokenizer
 
# 1. Input Text
text = "Learning Python is very interesting."
 
# 2. Load the pre-trained GPT-2 tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
 
# 3. Tokenize the text and return as PyTorch tensors
# return_tensors="pt" ensures the output is in PyTorch tensor format (used during model inference)
inputs = tokenizer(text, return_tensors="pt")
 
# 4. Get token IDs (numerical representations of tokens)
token_ids = tokenizer.encode(text)
 
# 5. Get tokens (readable subword units)
tokens = tokenizer.tokenize(text)
 
# 6. Print Outputs
print("Tokens (Subword Units):")
print(tokens)
 
print("\nToken IDs (Numerical):")
print(token_ids)
 
print(f"\n Number of Tokens: {len(token_ids)}")
 
print("\nPyTorch Tensor Output:")
print(inputs)

```
-----------

###Output :
Tokens (Subword Units):
['Learning', 'ĠPython', 'Ġis', 'Ġvery', 'Ġinteresting', '.']

Token IDs (Numerical):
[41730, 11361, 318, 845, 3499, 13]

Number of Tokens: 6

 PyTorch Tensor Output:
{'input_ids': tensor([[41730, 11361,   318,   845,  3499,    13]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1]])}

-------------------------------------------------------------------------------

## Knowledge Check on Tokenization : 

 
1. **What is the purpose of the `transformers` library in Python?**
2. **Why do we use the `GPT2Tokenizer.from_pretrained("gpt2")` method?**
3. **What is the difference between `tokenizer.tokenize()` and `tokenizer.encode()`?**
4. **What does `return_tensors="pt"` do in the tokenizer?**
5. **What is the output of `tokenizer(text, return_tensors="pt")` and what is it used for?**
6. **How are tokens and token IDs different? Can you give examples?**
7. **Why might you use PyTorch tensors instead of plain token IDs when working with models?**

-------------------------------------------------------------------------------------------
 
##  Embeddings in GPT-2
 
###  What Are Embeddings?
 
Embeddings are **dense vector representations** of tokens (words or subwords) that allow models like GPT-2 to understand and work with text in a numerical form. Instead of working directly with words, the model converts each token into a high-dimensional vector, capturing **semantic meaning and context**.

 
---
 
###  Why Do We Need Embeddings?
 
- Transformers like GPT-2 cannot process raw text directly.
- **Embeddings transform tokens into vectors** that can be passed to the model.
- These vectors help capture relationships like:
  - "king" - "man" + "woman" ≈ "queen"
- GPT-2 uses embeddings at the **input layer** (token embeddings) and **positional embeddings** to understand both what the words are and where they are in a sentence.
 
---
## 🏗️ Types of Embeddings
 
| Type | Description |
|------|-------------
| **Word Embeddings** | Fixed vectors for each word 
| **Contextual Embeddings** | Vary by sentence context 
| **Sentence Embeddings** | Represent full sentences 
| **Document Embeddings** | Represent paragraphs or docs
 
### Types of Embeddings in GPT-2
 
1. **Token Embeddings** – Represent the actual word/subword tokens.
2. **Positional Embeddings** – Help the model understand the position of each token (since transformers lack built-in sequence understanding).
 
Combined together: Embeddings = Token Embeddings + Positional EMbeddings 

All tokens are embedded into such vectors before being used in attention layers.
 
---
 
## 2. Positional Encodings
 
### 📌 Why Do We Need Them?
 
Transformers do **not know the order** of tokens inherently.  
To add order, **positional encodings** are added to embeddings.
 
These are unique vectors added to token embeddings to indicate position.
 
### 🧪 Example:
 
Suppose:
- Token Embedding for "Chat" = `[0.1, 0.2, 0.3]`
- Positional Encoding for position 1 = `[0.01, 0.02, 0.03]`

then :
Final Input Vector = [0.11, 0.22, 0.33]

So the model now understands **what** the token is and **where** it is in the sentence.
 
---
 
## 🔁 Combined View
 
When input enters the GPT model:
 
1. Text → Tokens
2. Tokens → Token IDs
3. Token IDs → Token Embeddings
4. Token Embeddings + Positional Encodings → Final Input to Transformer

### Installation (Required Only Once)
 
Install the `torch` library using pip:
 
```bash
pip install torch 
```

## 🧠 What is `torch`?
 
`torch` refers to **PyTorch**, an open-source deep learning framework developed by Facebook's AI Research lab. It provides a flexible and efficient platform for building and training neural networks.
 
---
 
## 🚀 Why Is It Required for GPT Models?
 
When working with models like **GPT-2** or **GPT-4** using libraries such as Hugging Face's `transformers`, the underlying computations (like matrix operations, attention mechanisms, and backpropagation) depend on `torch`.
 
The model's architecture and learned weights are built on top of PyTorch tensors, which are similar to NumPy arrays but with GPU acceleration.
 
---
 
## 🛠️ What Does It Do?
 
- Handles **tensor operations** (e.g., dot products, reshaping).
- Performs **automatic differentiation** (used during training).
- Manages **model layers**, attention heads, and activation functions.
- Supports **GPU acceleration** using CUDA (optional).
 
---
 
 
 #  GPT-2 Model Overview
 
**GPT-2** (Generative Pre-trained Transformer 2) is an advanced version of OpenAI's GPT model, designed to understand and generate human-like text using the Transformer architecture.
 
---
 
## 🧠 What is GPT-2?
 
GPT-2 is a **decoder-only Transformer model** trained to predict the next word in a sentence, given all the previous words (auto-regressive). It has **1.5 billion parameters** and was trained on a large dataset of web text called WebText.
 
---
 
## 🔧 Key Features
 
| Feature             | Description                                               |
|---------------------|-----------------------------------------------------------|
| Model Type          | Transformer (decoder-only)                                |
| Parameters          | 1.5 Billion                                               |
| Pre-training Data   | 8 million web pages (no fine-tuning required)             |
| Input               | Text tokens + positional encoding                         |
| Output              | Next-token prediction (language generation)               |
| Architecture        | 48-layer Transformer with self-attention                  |
 
---
 
## 🔄 How GPT-2 Works
 
1. **Tokenization**: Text is split into subword tokens.
2. **Embedding**: Tokens are converted into vectors.
3. **Positional Encoding**: Adds information about token order.
4. **Transformer Blocks**: Processes token relationships using self-attention.
5. **Output Layer**: Predicts the next token.
 
---
 
## 💡 Example for embeddings
```Python
from transformers import GPT2Tokenizer, GPT2Model
import torch
 
# Import your custom exception-handling decorator
from utiles.decoratores import handle_exceptions
 
 
@handle_exceptions
def get_gpt2_embeddings(text: str):
    """
    Tokenizes the input text using GPT2Tokenizer and retrieves token embeddings using GPT2Model.
 
    Args:
        text (str): The input sentence or phrase.
 
    Returns:
        torch.Tensor: The embeddings tensor of shape [1, sequence_length, 768]
    """
    # Load the pre-trained GPT2 tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
 
    # Load the pre-trained GPT2 model (without LM head)
    model = GPT2Model.from_pretrained("gpt2")
 
    # Tokenize the input and convert it to tensor format
    inputs = tokenizer(text, return_tensors="pt")
 
    # Run the model without computing gradients (inference mode)
    with torch.no_grad():
        outputs = model(**inputs)
 
    # Extract the last hidden state (token embeddings)
    embeddings = outputs.last_hidden_state
 
    # Print the shape of the embedding tensor
    print(f"Embeddings shape: {embeddings.shape}")
 
    print(embeddings)
 
 
# Example usage
if __name__ == "__main__":
    get_gpt2_embeddings("GPT-2 embeddings example")

```

output :
Embeddings shape: torch.Size([1, 8, 768])
tensor([[[-0.2023, -0.1084, -0.1990,  ..., -0.1866,  0.0799, -0.0417],
         [ 0.3028, -0.0956,  0.3298,  ...,  0.2122,  0.2060, -0.2252],
         [-0.0335,  0.0473,  0.2137,  ..., -0.0744,  0.4494, -0.0472],
         ...,
         [-0.0941, -0.1020,  1.0095,  ..., -0.4113, -0.6200,  0.1524],
         [ 0.1354, -0.1038, -0.5818,  ...,  0.3190,  0.1542,  0.4927],
         [ 0.0694, -0.3225, -1.1552,  ..., -0.0970,  0.1496,  0.3304]]])

----
 
Knowledge check :
 
# Interview Questions: Embeddings & Language Models
 
### 1. How does GPT-2 generate embeddings? - Describe the process of tokenization and transformer layers.  
### 2. What is the shape of the output from a transformer model like GPT-2? - Explain `[batch_size, sequence_length, embedding_dim]`.  
### 3. What does `last_hidden_state` represent in GPT-2 output?  
### 4. How do you extract sentence-level embeddings from token-level outputs?  
### 5. How do you use embeddings in downstream tasks like classification or clustering?  
### 6. How do you visualize high-dimensional embeddings? - Use of t-SNE, PCA, or UMAP.  
### 7. How do you store and retrieve embeddings efficiently at scale? - Mention FAISS or Annoy.  
### 8. How does fine-tuning affect embeddings?  
### 9. How does positional encoding influence embeddings in transformers?  
### 10. How do transformer attention mechanisms interact with embeddings?  
### 11. How would you extract GPT-2 embeddings using HuggingFace Transformers in PyTorch?  
### 12. How would you handle variable-length inputs when generating embeddings?  
### 13. If your embeddings don’t capture semantic similarity well, how would you improve them?  
### 14. How would you compare the performance of different embeddings on a task like sentiment analysis?  
 
### 15 What is the role of embedding layers in neural networks?
 
### 16 Why are pre-trained embeddings useful?
### 17. What are some commonly used embedding models?
- Word2Vec  
- GloVe  
- FastText  
- BERT  
- GPT
 
 
-------------

# 🔍 Vector-Based Search using GPT-2 Model
 
Vector-based search, also known as **semantic search**, allows you to retrieve documents or responses based on **meaning** rather than exact keyword matches. Though GPT-2 is primarily a language generation model, it can still be leveraged to **generate embeddings** (numerical vector representations of text), which can then be used in vector search.
 
---
 
## ⚙️ How It Works
 
1. **Text Input**
   - You provide textual data (e.g., documents, sentences, or questions).
   
2. **Tokenization**
   - Use GPT-2 tokenizer (from HuggingFace) to convert text into token IDs.
   - Example:
     ```python
     tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
     inputs = tokenizer("example text", return_tensors="pt")
     ```
 
3. **Generate Embeddings using GPT-2**
   - Pass tokenized input into the GPT-2 model to get hidden states:
     ```python
     model = GPT2Model.from_pretrained("gpt2")
     outputs = model(**inputs)
     last_hidden_state = outputs.last_hidden_state
     ```
 
4. **Extract Sentence Embedding**
   - You can average token embeddings to form a fixed-size sentence embedding:
     ```python
     sentence_embedding = last_hidden_state.mean(dim=1)  # shape: [1, embedding_dim]
     ```
 
5. **Index Embeddings**
   - Store embeddings in a **vector index** using libraries like:
     - **FAISS** (Facebook AI Similarity Search)
     - **Annoy** (Approximate Nearest Neighbors)
     - **ScaNN** (Google)
     ```python
     import faiss
     index = faiss.IndexFlatL2(embedding_dim)
     index.add(embedding_matrix)  # add all embeddings to index
     ```
    ### Installation (Required Only Once)
 
    Install the `faiss-cpu` library using pip:
 
    ```bash
    pip install faiss-cpu
    ```
     **faiss** stands for Facebook AI Similarity Search. It is a library developed by Facebook AI Research to perform efficient similarity search and clustering of dense vectors (typically high-dimensional embeddings, like those from NLP or image models).

     #### What faiss Does:
    faiss is mainly used for:
    •	Fast nearest neighbor search in large datasets.
    •	Similarity search between vectors (e.g., finding the most similar sentences, images, or documents).
    •	Clustering of high-dimensional data.
    •	Indexing vectors in a memory-efficient and query-optimized way.



    Example Code for faiss :
    ```Python 
    import faiss
    import numpy as np

    # Create some 128-dimensional vectors
    d = 128
    nb = 1000
    query_vector = 1

    # Generate random vectors
    data = np.random.random((nb, d)).astype('float32')
    query = np.random.random((query_vector, d)).astype('float32')

    # Build index
    index = faiss.IndexFlatL2(d)  # L2 = Euclidean distance
    index.add(data)               # Add data to index

    # Search the nearest 5 neighbors
    D, I = index.search(query, 5)  # D = distances, I = indices
    print("Nearest indices:", I)
    print("Distances:", D)

    ```


 
6. **Search with Query**
   - Encode a query using the same GPT-2 embedding pipeline.
   - Search in the index to retrieve top similar vectors:
     ```python
     D, I = index.search(query_embedding, k=5)  # D = distances, I = indices
     ```
 
7. **Return Results**
   - Map indices back to original documents or responses.
 
---
 
## ✅ Advantages
 
- Captures **semantic similarity** (e.g., "car" and "vehicle" will be close).
- Supports **flexible and fuzzy** matching.
- Can be extended for:
  - FAQ bots
  - Recommendation systems
  - Document retrieval
 
---
 
## ⚠️ Limitations
 
- GPT-2 is **not optimized for embeddings** (unlike BERT or Sentence-BERT).
- Requires **fine-tuning or post-processing** for better performance.
- Larger memory usage due to transformer architecture.
 
---
 
## 🧠 Alternative: Use Better Embedding Models
 
Instead of GPT-2, you can use models specifically trained for embeddings:
- `sentence-transformers/all-MiniLM-L6-v2`
- `bert-base-uncased`
- `text-embedding-ada-002` (OpenAI)
 
---
 
## 📌 Summary
 
| Step             | Action                        |
|------------------|-------------------------------|
| Text             | Provide raw input text        |
| Tokenization     | Use GPT-2 tokenizer           |
| Embedding        | Extract hidden states         |
| Indexing         | Store vectors in FAISS/Annoy  |
| Query            | Search for similar vectors    |
| Result           | Retrieve semantically similar |


-------------

Example Code on search_vector 

```python 
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
 
```
Output :
Query is : I enjoy learning Python

0.9990 → Studying Python is enjoyable
0.9980 → Python is a powerful language
0.9971 → The weather is nice today
0.9938 → I love Programing in Java
0.9888 → Bananas are rich is potassium

----
 
# Understanding `GPT2LMHeadModel` in Transformers
 
##  What is `GPT2LMHeadModel`?
 
`GPT2LMHeadModel` is a variant of GPT-2 used **specifically for language modeling tasks** such as:
- Text generation
- Text completion
- Next word prediction
- Autoregressive generation
 
It adds a **language modeling (LM) head** — a linear layer — on top of the base `GPT2Model` to project hidden states to vocabulary size logits.
 
---
 
## Architecture Overview
 
- **GPT2Model**: Outputs hidden states only.
- **GPT2LMHeadModel**: Adds a linear layer on top to output **logits over vocabulary** — enabling prediction of the next token.

working ->
Input Text → Tokenizer → GPT2Model → Hidden States → LM Head → Logits → Softmax → Next Token Probabilities

 ### Example GPT2LMHeadModel :

 ```python :
 # Import required libraries
from transformers import GPT2Tokenizer, GPT2LMHeadModel  # For loading GPT2 tokenizer and language model
import torch  # For tensor computations
from utiles.decoratores import handle_exceptions
 
# Function to load the GPT-2 tokenizer and language model
@handle_exceptions
def load_model():
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")  # Load pre-trained tokenizer
    model = GPT2LMHeadModel.from_pretrained("gpt2")    # Load pre-trained GPT-2 language model head
    return tokenizer, model
 
# Function to generate text based on a given prompt
@handle_exceptions
def generate_text(prompt, max_len=100):
    tokenizer, model = load_model()  # Load tokenizer and model
 
    # Encode the input prompt into tensor of input IDs
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
 
    # Generate text using the model with sampling
    output_ids = model.generate(
        input_ids,
        max_length=max_len,  # Maximum number of tokens in generated text
        do_sample=True       # Enable sampling for more randomness
    )
 
    # Decode output IDs into readable text
    generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
 
    return generated_text
 
# --- Main Execution ---
if __name__ == "__main__":
    prompt = "Python is used for programming the AI models"
 
    # Print original prompt
    print(f"\nPrompt:\n{prompt}\n")
 
    # Generate and print output text
    generated = generate_text(prompt, max_len=100)
    print(f"Generated Text:\n{generated}")
```
Output : 
Prompt:
Python is used for programming the AI models

Generated Text:
Python is used for programming the AI models using the R programming language. So when we get a data set from Python and use R, it will be in R, using some basic programming language to control the AI model. But there is a bigger problem at play here. We can't make a data set with Python. I can't.

A Data Set with Python: The Problem

To get around this, we need to create an R data set which can manipulate values. By doing

---------------------

# 🧠 FastAPI + Uvicorn + GPT-2 Integration
 
## 🚀 What is FastAPI?
 
**FastAPI** is a modern, high-performance web framework for building APIs with Python 3.6+ based on standard Python type hints.
 
### ✨ Key Features:
- Fast: Built on Starlette and Pydantic; one of the fastest Python frameworks.
- Easy: Fewer lines of code, automatic docs generation.
- Type-safe: Type hints help with validation and editor support.
- Async-ready: Built-in support for asynchronous request handling.
 
---
 
## 🔥 What is Uvicorn?
 
**Uvicorn** is a lightning-fast ASGI server implementation, used to run FastAPI applications.
 
### 🔧 Role of Uvicorn:
- Acts as the **web server** for FastAPI apps.
- Handles incoming HTTP requests and routes them to FastAPI.
- Supports both synchronous and asynchronous code.
### ✅ 1. Building REST APIs
- Create full-featured RESTful APIs with simple decorators.
- Supports HTTP methods like `GET`, `POST`, `PUT`, `DELETE`.
- Ideal for CRUD operations.
 
---
 
### ✅ 2. Serving Machine Learning Models
- Serve trained models (e.g., from TensorFlow, PyTorch, Scikit-learn).
- Accept input via JSON and return predictions.
- Common in real-time AI inference apps.
 
---
 
### ✅ 3. Asynchronous Applications
- Built-in support for `async` and `await`.
- Handle thousands of requests with high performance.
- Suitable for chat apps, streaming data, etc.
 
---
 
### ✅ 4. Auto-Generated API Documentation
- Automatically provides interactive API docs:
  - Swagger UI (`/docs`)
  - ReDoc (`/redoc`)
- Saves time for developers and stakeholders.
 
---
 
### ✅ 5. Input Validation and Serialization
- Uses **Pydantic** for:
  - Type-checking request data
  - Data serialization/deserialization
  - Custom error handling
 
---
 
### ✅ 6. Interactive API Testing
- Easily test endpoints via Swagger UI in the browser.
- Helps in frontend-backend collaboration.
- Allows live interaction with the API without Postman.
 
---
 
### ✅ 7. Secure Authentication & Authorization
- Supports:
  - OAuth2 with password and bearer tokens
  - JWT (JSON Web Tokens)
  - API key headers or query parameters
 
---
 
### ✅ 8. WebSocket Support
- Native WebSocket integration for:
  - Real-time communication
  - Dashboards
  - Multiplayer games
 
---
 
### ✅ 9. Background Task Handling
- Run tasks **after** sending a response.
- Example: sending confirmation emails, logging, etc.
- Helps in optimizing API response times.
 
---
 
### ✅ 10. Microservices & Serverless
- Lightweight for microservice architectures.
- Easy to containerize with **Docker** or deploy with **Kubernetes**.
- Works with AWS Lambda using **Mangum** adapter.
 
---
 
### ✅ 11. Database Integration
- Works with:
  - SQL (via SQLAlchemy)
  - NoSQL (via MongoDB with ODMs)
  - Tortoise ORM and others
- Built-in Dependency Injection simplifies setup.
 
---
 
 
### ✅ Installation:
```bash
pip install fastapi uvicorn
```

#### Run FastAPI app using Uvicorn :
uvicorn main:app --reload

main : filename
app : FastAPI

----

# 📌 FastAPI Endpoints Explained
 
## ✅ What is an Endpoint?
 
An **endpoint** in FastAPI is a **URL path** that your API responds to. When a client (like a browser or frontend app) makes an HTTP request to this path (such as `/login`, `/items/1`), FastAPI runs the corresponding Python function and sends back a response.
 
---
 
## 🧩 Basic FastAPI Structure
 
```python
from fastapi import FastAPI
 
app = FastAPI()
 
@app.get("/")
def read_root():
    return {"message": "Hello World"}

```

### Endpoint URL
if your FastAPI app is running locally using uvicorn like this:
```
uvicorn main:app --reload
```
And your main.py file contains the above code,then your FastAPI server will be live at:
**Base URL**: http://1270.0.0.1:8000
You can access your first endpoint by visting:
**📌 GET Endpoint**:
http://127.0.0.1:8000/
 
🔁 Response:
 
```json

{
  "message": "Hello World"
}
```
---
### 📬 What is Postman?
Postman is a popular tool for testing APIs. It allows you to:
 
- Send different types of HTTP requests like GET, POST, PUT, DELETE
 
- Pass headers, body, parameters easily
 
- View response data in a structured way
 
To test this endpoint using Postman:
 
Open Postman
 
Set the method to GET

### 1. GET Endpoint
**✅ Description**:
Used to retrieve data.
 
Enter the URL: http://127.0.0.1:8000/
 
Click Send
 
You’ll get the response:
 
```json

{
  "message": "Hello World"
}
```
✅ Now you’ve successfully tested your first FastAPI endpoint!
 
----

### 2. GET Endpoint with Path Parameter
**✅ Description**:
Used to retrieve a specific item by its ID or name.
 
🔧 Code:
```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```
🔗 URL:
Copy code
GET http://127.0.0.1:8000/items/5
🔁 Sample Response:
```json
{
  "item_id": 5
}
```
----

### 3. GET with Query Parameters
**✅ Description**:
Retrieve data using parameters in the URL query string.
 
🔧 Code:
```python
@app.get("/search/")
def search_items(q: str = None):
    return {"query": q}
```
🔗 URL:
GET http://127.0.0.1:8000/search/?q=books
🔁 Sample Response:
```json
{
  "query": "books"
}
```
---

### 4. POST Endpoint
**✅ Description**:
Used to create new data.
 
```Code:
from pydantic import BaseModel
 
class Item(BaseModel):
    name: str
    price: float
 
@app.post("/items/")
def create_item(item: Item):
    return {"item_created": item}
```

🔗 URL:

POST http://127.0.0.1:8000/items/
📨 Sample Request Body (Postman - Body → raw → JSON):

```json

{
  "name": "Laptop",
  "price": 75000
}
```

🔁 Sample Response:
```json
{
  "item_created": {
    "name": "Laptop",
    "price": 75000
  }
}
```
----

### 5. PUT Endpoint
**✅ Description**:
Used to update existing data.
 
🔧 Code:
```python
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "updated_item": item}
```

🔗 URL:

PUT http://127.0.0.1:8000/items/2

📨 Sample Request Body:
```json
{
  "name": "Mouse",
  "price": 500
}
```

🔁 Sample Response:
```json
{
  "item_id": 2,
  "updated_item": {
    "name": "Mouse",
    "price": 500
  }
}
```
---

### 6. DELETE Endpoint
**✅ Description**:
Used to delete a resource.
 
🔧 Code:
```python
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"deleted_item_id": item_id}
```

🔗 URL:
DELETE http://127.0.0.1:8000/items/10

🔁 Sample Response:
```json
{
  "deleted_item_id": 10
}
```

🧪 Testing with Postman
Open Postman
 
Choose HTTP method (GET, POST, etc.)
 
Enter the appropriate URL
 
For POST/PUT, go to Body → raw → JSON, and add the request body

## ✅ Summary Table
 
| Method | Endpoint              | Description         |
|--------|-----------------------|---------------------|
| GET    | `/`                   | Basic Hello World   |
| GET    | `/items/{item_id}`    | Get item by ID      |
| GET    | `/search/?q=value`    | Get using query     |
| POST   | `/items/`             | Create new item     |
| PUT    | `/items/{item_id}`    | Update an item      |
| DELETE | `/items/{item_id}`    | Delete an item      |

----

## 🧠 Knowledge Check – FastAPI Endpoints
  
1. **What is an endpoint in FastAPI?**
2. **Which decorator is used to define a GET request in FastAPI?**
3. **What is the default port on which FastAPI runs using Uvicorn?**
4. **How does FastAPI know which function to run when a URL is accessed?**
5. **What would be the output of accessing `/items/42` if `item_id` is returned from the function?**
6. **How do you pass a query parameter in a GET request using FastAPI?**
7. **What's the difference between a path parameter and a query parameter in FastAPI?**
8. **What happens if you define the same route for both GET and POST methods without handling it properly?** 
9. **What is Uvicorn, and why is it used with FastAPI?**
10. **How do you define a POST endpoint that accepts JSON input?**
11. **How can you test your API endpoints using Postman?**
12. **How do you define data validation using Pydantic in a POST request?** 
13. **Explain the use of `@app.put()` and `@app.delete()` decorators.**
14. **Can you create nested routes in FastAPI? Give an example.**
15. **How do you return a custom status code in a response from a FastAPI endpoint?**

---
 
 

