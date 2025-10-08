from langchain_google_genai import GoogleGenerativeAI
import os

google_api_key = os.getenv("GEMINI_API_KEY")

llm = GoogleGenerativeAI(
    model="gemini-pro",  # Use the working model name
    google_api_key=google_api_key
)

response = llm.invoke("Explain Generative AI vs Agentic AI.")

print(response)
