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
 
