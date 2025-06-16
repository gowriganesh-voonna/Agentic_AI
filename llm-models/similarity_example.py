# get sentence (input) -> get token -> embeddings -> means_embeddings.   (do for two sentences)


from transformers import GPT2Tokenizer,GPT2Model
import torch

import torch.nn.functional as F 

# define token and model
tokenizer=GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")

def get_mean_embeddings(input_text):
    tokens = tokenizer(input_text,return_tensors ="pt")

    with torch.no_grad():
        outputs = model(**tokens)

    embeddings = outputs.last_hidden_state

    mean_embeddings = embeddings.mean(dim=1)

    return mean_embeddings


sentence1 = "Python is very interesting Programming language"

sentence2 = "I am very interesting in Sports"

first_sentence_embeddings = get_mean_embeddings(sentence1)

second_sentence_embeddings = get_mean_embeddings(sentence2)

# print (f"Sentence1 mean embedding : {sentence1} {first_sentence_embeddings}")
# print (f"Sentence2 mean embedding : {sentence1} {second_sentence_embeddings}")


# Compare the COSINE SIMILARITY beteen towo vectors
# It measures how similar two vectors are based on Angle and Not the Size
simiarlity = F.cosine_similarity(first_sentence_embeddings,second_sentence_embeddings).item()

print  (f"Cosine Similarity : {simiarlity:.4f} (1 = Very Similar, 0 = different ) ")
