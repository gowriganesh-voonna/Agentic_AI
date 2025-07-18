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
 
-------