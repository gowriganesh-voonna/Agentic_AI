from google import genai
from google.genai import types
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import os


texts = [
    "Samsung A55 is all rounder mobile phone",
    "Indian ocean is the third largest ocean in the world",
    "Indian Army is now having more than 1.4 million active personnel",
]

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.embed_content(
    model ="gemini-embedding-001",
    contents = texts,
    config = types.EmbedContentConfig(task_type = "SEMANTIC_SIMILARITY")
)

# creating an 3*3 matrix to store similarity scores

df = pd.DataFrame(
    cosine_similarity([e.values for e in response.embeddings]),
    index= texts,
    columns = texts
)


print(df)

# to get embeddings all at time
print("Embeddings:", response.embeddings)



