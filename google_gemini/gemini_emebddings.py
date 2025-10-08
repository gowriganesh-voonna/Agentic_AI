from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
embeddings = GoogleGenerativeAIEmbeddings(
    model = "models/gemini-embedding-001",
     )

vector = embeddings.embed_query("google gemini AI ")

print(vector[:5])