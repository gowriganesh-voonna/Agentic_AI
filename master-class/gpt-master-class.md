# Masterclass for GPT-2/4

## Overview

In this article, we will cover the following key concepts:

- **Tokens**: How large language models process text using tokens.
- **Embeddings**: Representing words, sentences or tokens (text ->Tokens -> Embeddings) in a high dimenisonal space.
- **Vector Based Search**: Efficiently searching through embeddings using similarity metrics.
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
Tokens : ['Learning' ,'Python','is','easy'] ```

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
 
**transformers** is a Python library created by Hugging Face. It allows us to:
 
- Load **pre-trained models** (like GPT-2, BERT, etc.)
- Use **pre-trained tokenizers** for converting text to tokens and back
- Easily run inference, text generation, embeddings, and more
 
It's widely used in the AI/NLP industry and supports models from OpenAI, Meta, Google, and others.
 
---
 
### Installation (Required Only Once)
 
Install the `transformers` library using pip:
 
```bash
pip install transformers ```

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

Output :
# Tokens (Subword Units):
# ['Learning', 'ĠPython', 'Ġis', 'Ġvery', 'Ġinteresting', '.']

# Token IDs (Numerical):
# [41730, 11361, 318, 845, 3499, 13]

#  Number of Tokens: 6

# PyTorch Tensor Output:
# {'input_ids': tensor([[41730, 11361,   318,   845,  3499,    13]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1]])}

