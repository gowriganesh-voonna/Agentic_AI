# Masterclass : Understanding  Tokens, Embeddings, Models, Language Models, Vectors, FastAPI and Mongodb.

## Overview

In this article, we will cover the following key concepts:

- **Tokens**: The basic units into which text is split for machine processing.
- **Embeddings**: Representing words, sentences or tokens (text ->Tokens -> Embeddings) in a high dimenisonal space.
- **Vector Based Search**: Efficiently searching through embeddings using similarity metrics.
- **Model** : A model like GPT is a powerful language processing system that understands and generates human-like text based on input.It uses billions of parameters trained on vast text data to predict the next word or sentence in a conversation.
- **Language Model (LM)** : LM is a model that predicts the next word or token in a sequence based on the context of previous words. It helps machines understand and generate human-like text.
- **Large Language Model (LLM)** : LLM is a type of language model trained on massive datasets with billions of parameters, capable of understanding, generating, and reasoning with natural language at a much deeper level.
- **FastAPI**- FastAPI is a modern and high-performance Python web framework used to build APIs quickly and efficiently.
- **Mongodb**- MongoDB is a popular, open-source, NoSQL database that stores data in JSON-like documents organized into collections. 


Throughout the article, we'll explore how these components work individually with examples and end of this article we will cover one example covering all components or topics.

By the end of this masterclass, you'll have a foundational understanding and you can able to do real world scenario.

------------------------------------------------------------------------------------------

# Section 1: Tokens :

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

[See more about transformers and Hugging Face](split_content/tokenization_indetail.md)

---
 
### Installation (Required Only Once)
 
Install the `transformers` library using pip:
 
```bash
pip install transformers 
```

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

### Output :
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
8. **What is tokenization, and why is it needs in NLP?**
9. **List three types of tokenization with examples.?**
10. **List three types of tokenization with examples.?**
11. **List two popular models available through the Hugging Face Transformers library?**

-------------------------------------------------------------------------------------------
 
# Section 2 :  Embeddings in GPT-2
 
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
 
--------
## Working Flow
 
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
[see indetail about torch](split_content/temp.md)

---
 
# Section 3: GPT Model Overview
 
**GPT** (Generative Pre-trained Transformer ) is an advanced version of OpenAI's GPT model, designed to understand and generate human-like text using the Transformer architecture.
 
---
 
## 🧠 What is GPT?
 
GPT-2 is a **decoder-only Transformer model** trained to predict the next word in a sentence, given all the previous words (auto-regressive). It has **1.5 billion parameters** and was trained on a large dataset of web text called WebText.
 
---
 
## 🔄 How GPT Works
 
1. **Tokenization**: Text is split into subword tokens.
2. **Embedding**: Tokens are converted into vectors.
3. **Positional Encoding**: Adds information about token order.
4. **Transformer Blocks**: Processes token relationships using self-attention.
5. **Output Layer**: Predicts the next token.
 
---
### Section 4: What is a Language Model (LM)?

### Explanation:
A **Language Model (LM)** predicts the likelihood of a sequence of words or the next word in a sentence. It learns language patterns from large text corpora.

### Example:
- Input: "The capital of France is"
- LM Output: "Paris"

### Examples of Language Models:
| Model Name     | Developer | Description                             |
|----------------|-----------|-----------------------------------------|
| GPT-2          | OpenAI    | Autoregressive LM for text generation   |
| BERT           | Google    | Bidirectional encoder for understanding |
| RoBERTa        | Facebook  | Robust BERT variant                     |

### GPT-2 Example: [click here to see code](codesamples/gpt2_embeddings.py)

----
 
Knowledge check :
 
# Interview Questions: Embeddings & Language Models
 
1. How does GPT-2 generate embeddings? - Describe the process of tokenization and transformer layers.  
2. What is the shape of the output from a transformer model like GPT-2? - Explain `[batch_size, sequence_length, embedding_dim]`.  
3. What does `last_hidden_state` represent in GPT-2 output?  
4. How do you extract sentence-level embeddings from token-level outputs?  
5. How do you use embeddings in downstream tasks like classification or clustering?  
6. How do you visualize high-dimensional embeddings? - Use of t-SNE, PCA, or UMAP.  
7. How do you store and retrieve embeddings efficiently at scale? - Mention FAISS or Annoy.  
8. How does fine-tuning affect embeddings?  
9. How does positional encoding influence embeddings in transformers?  
10. How do transformer attention mechanisms interact with embeddings?  
11. How would you extract GPT-2 embeddings using HuggingFace Transformers in PyTorch?  
12. How would you handle variable-length inputs when generating embeddings?  
13. If your embeddings don’t capture semantic similarity well, how would you improve them?  
14. How would you compare the performance of different embeddings on a task like sentiment analysis?  
15. What is the role of embedding layers in neural networks?
16. Why are pre-trained embeddings useful?
17. What are some commonly used embedding models?
- Word2Vec  
- GloVe  
- FastText  
- BERT  
- GPT
-------------

# Section 4: What is a Large Language Model (LLM)?

### Explanation:
A **Large Language Model (LLM)** is a type of Language Model trained on massive amounts of data with billions of parameters. LLMs can perform multiple language-related tasks such as answering questions, translation, summarization, and coding.

### Example:
- GPT-3 and GPT-4 are examples of LLMs.
- LLMs like GPT-4 can answer complex queries, generate articles, and perform reasoning.

### Examples of LLMs:
| Model        | Developer | Parameters | Notable Use                    |
|--------------|-----------|------------|--------------------------------|
| GPT-3        | OpenAI    | 175B       | Chatbots, creative writing     |
| GPT-4        | OpenAI    | ~1T (est.) | Advanced reasoning, coding     |
| LLaMA 2      | Meta      | 7B - 65B   | Open-source research           |
| Claude       | Anthropic | Proprietary| Safer conversational AI        |

---------

# Section 5 :🔍 Vector-Based Search using GPT-2 Model
 
Vector-based search, also known as **semantic search**, allows you to retrieve documents or responses based on **meaning** rather than exact keyword matches. Though GPT-2 is primarily a language generation model, it can still be leveraged to **generate embeddings** (numerical vector representations of text), which can then be used in vector search.
 
---
 
## ⚙️ How It Works :
 
**Text Input -> Tokenization -> Generate Embeddings using GPT -> Extract Sentence Embedding -> Index Embeddings -> Search with Query -> Return Results**
[check more for work flow](split_content/search_vector.md)

----
 
  ### Installation 
 
  Install the `faiss-cpu` library using pip:
 
    ```bash
    pip install faiss-cpu
    ```

  **faiss** stands for Facebook AI Similarity Search. It is a library developed by Facebook AI Research to perform efficient similarity search and clustering of dense vectors (typically high-dimensional embeddings, like those from NLP or image models).

  #### What faiss Does:
  faiss is mainly used for:
  - Fast nearest neighbor search in large datasets.
  - Similarity search between vectors (e.g., finding the most similar sentences, images, or documents).
  - Clustering of high-dimensional data.
  - Indexing vectors in a memory-efficient and query-optimized way.

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

-------------

Example Code on search_vector 
[click here to see the example code](codesamples/gpt2_search_vector.py)

---
 
# Section 6 : Understanding `GPT2LMHeadModel` in Transformers
 
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

 ### Example GPT2LMHeadModel : [click here for code](codesamples/gpt2LmHeadmodel.py)
----
## Knowledge Check — Interview Questions

1. What is the difference between a model and a language model?
2. What defines a Large Language Model (LLM)?
3. Explain how vectors help in semantic similarity.
4. What is the role of positional embeddings?
5. How does GPT-4 handle more context than GPT-2?
6. Define context window in LLMs.
7. Why do LLMs operate on tokens instead of raw text?
8. Can you extract embeddings from GPT models?
9. Explain last_hidden_state in Huggingface Transformers.
10. What is the importance of transformer architecture in handling vectors?
11. What are attention mechanisms in LLMs?
12. Why is dimensionality important in embeddings?
13. How does token count limit affect LLM performance?
14. Explain padding tokens and their role.
15. How do embeddings contribute to model generalization?

-----------------

#  Section 7:🧠 FastAPI + Uvicorn 
 
## 🚀 What is FastAPI?
 
**FastAPI** is a modern, high-performance web framework for building APIs with Python 3.6+ based on standard Python type hints.
 
### ✨ Key Features:
- Fast: Built on Starlette and Pydantic; one of the fastest Python frameworks.
- Easy: Fewer lines of code, automatic docs generation.
- Type-safe: Type hints help with validation and editor support.
- Async-ready: Built-in support for asynchronous request handling.
 
### ✅ Installation for FastAPI:
```bash
pip install fastapi uvicorn
```
---
 
## 🔥 What is Uvicorn?
 
**Uvicorn** is a lightning-fast ASGI server implementation, used to run FastAPI applications.
 
### 🔧 Role of Uvicorn:
- Acts as the **web server** for FastAPI apps.
- Handles incoming HTTP requests and routes them to FastAPI.
- Supports both synchronous and asynchronous code.

---

### 📘 What is Pydantic in FastAPI?
 
**Pydantic** is a Python library used in FastAPI to **validate and parse data** using Python type annotations. It ensures the data you receive (especially from API requests) is in the correct format, and it automatically handles errors for invalid data types.
 
------------
 
## 🧩 Basic FastAPI Structure
 
```python
from fastapi import FastAPI
 
app = FastAPI()
 
@app.get("/")
def read_root():
    return {"message": "Hello World"}

```
[click here to view crud operations](split_content/fastAPI.md)

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

# Section 8: MongoDB definition and MongoDB Cloud Setup with Atlas
 
## What is MongoDB?
 MongoDB is a **NoSQL**, document-oriented database designed for scalability, performance, and ease of development. It stores data in flexible, JSON-like documents, making it ideal for modern applications.

### Key Features:
- **Document-based**: Stores data as documents with key-value pairs.
- **Schema-less**: Allows flexible and dynamic data structures.
- **Scalable**: Built to scale horizontally across distributed systems.
- **High Performance**: Optimized for fast read and write operations.
- **Cloud Support**: Easily deployable on MongoDB Atlas for cloud-based applications.

## 🏗️ Core Concepts
- **Database**: Container for collections.
- **Collection**: Group of Documents (like Tables in SQL).
- **Document**: BSON (Binary-JSON) format, analogous to a row in RDBMS.
 
### 📄 Document
- The basic unit of data in MongoDB
```json
{
  "name": "Surendra",
  "skills": ["Python", "Django"],
  "age": 22
}
```
## Section 8.1:📌 MongoDB Operations using `pymongo.MongoClient`
 
### [click here to view CRUD operations code](split_content/mongodb.md)

**⚠️ Note**: MongoClient is synchronous and works well with regular (non-async) Python applications like small scripts, command-line tools, or Flask.

----
## Section 8.2 : What is `AsyncIOMotorClient`?
 
`AsyncIOMotorClient` is an **asynchronous MongoDB client** provided by the `motor` library, which is the official async Python driver for MongoDB.
 
It is used to **connect to MongoDB** and perform **non-blocking I/O operations** when working with FastAPI or other async frameworks.
 
### Why Use It?
- Traditional MongoDB drivers like `pymongo` are synchronous and can block the event loop in async applications.
- `AsyncIOMotorClient` allows you to run database operations without blocking other requests, making your FastAPI apps more **efficient and scalable**.
 
### Example Usage:
```python
from motor.motor_asyncio import AsyncIOMotorClient
 
client = AsyncIOMotorClient("your_mongo_uri")
db = client["bookstore"]
```


-------------------

### Section 8.3: FastAPI CRUD API with MongoDB (Async + Pydantic)
***✅ Highlights**:
- Asynchronous CRUD with FastAPI and Motor
 
- Input validation using Pydantic models
 
- Auto-generated Swagger UI for documentation at /docs

[click here to view example code](codesamples/mongodb.py)

### Run FastAPI App:
```
uvicorn main:app --reload
```
 
 
## Knownledge Check :📋 Interview Questions on MongoDB and FastAPI + MongoDB
 
### 🟢 MongoDB Basics
1. What is MongoDB and how is it different from SQL databases?
2. What is a document in MongoDB?
3. What is a collection in MongoDB?
4. What is BSON and how is it related to JSON?
5. How does MongoDB handle indexing?
6. What are the advantages of using MongoDB?
7. How do you perform CRUD operations in MongoDB?
8. How do you query nested documents in MongoDB?
9. What is the `_id` field in MongoDB and can you change it?
10. How do you perform aggregation in MongoDB?
 
### ⚡ FastAPI + MongoDB Integration
11. How do you connect MongoDB with FastAPI?
12. What is `motor` and why do we use `AsyncIOMotorClient`?
13. How do you ensure non-blocking database access in FastAPI?
14. How are MongoDB operations handled asynchronously in FastAPI?
15. How do you define a Pydantic model for MongoDB documents?
16. What challenges did you face while using MongoDB with FastAPI?
17. How do you handle ObjectId conversion between MongoDB and Pydantic models?
18. How do you implement error handling for MongoDB queries in FastAPI?
19. How do you insert a document using FastAPI and Motor?
20. How do you update and delete documents using FastAPI?
21. How do you retrieve a single document by ID in FastAPI?
22. What happens if the document is not found in the database?
23. How do you test MongoDB-based endpoints in FastAPI?
24. How would you secure sensitive database credentials in a FastAPI project?
25. How do you manage database connection lifecycle in FastAPI?
 
---

