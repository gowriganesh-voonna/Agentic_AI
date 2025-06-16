from transformers import GPT2Tokenizer, GPT2Model
import torch

# load the tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# load the model

model = GPT2Model.from_pretrained("gpt2")


# 3 . text (input)


text = " I want to play music"



inputs = tokenizer(text , return_tensors = "pt")



with torch.no_grad():
    outputs = model(**inputs)


embeddings = outputs.last_hidden_state


tokens = tokenizer.tokenize(text)


for i , token in enumerate(tokens):
    print(f" Token: {token}")
    print(f"Embedding (768 values):\n{embeddings[0][i]}")
    print("--------------------------------------------------")