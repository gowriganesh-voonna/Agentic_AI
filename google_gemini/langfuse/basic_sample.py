import os
from dotenv import load_dotenv
from langfuse import Langfuse, observe
import google.generativeai as genai
import requests

# Load environment variables
load_dotenv()

LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_BASE_URL = os.getenv("LANGFUSE_BASE_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize Langfuse
lf = Langfuse(
    public_key=LANGFUSE_PUBLIC_KEY,
    secret_key=LANGFUSE_SECRET_KEY,
    host=LANGFUSE_BASE_URL,
)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


def tavily_search(query: str):
    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": TAVILY_API_KEY,
            "query": query,
            "max_results": 5,
        },
        headers={"Content-Type": "application/json"},
    )
    return response.json()


@observe(name="topic_info")
def get_topic_info(prompt: str):

    search_data = tavily_search(prompt)

    gemini_prompt = f"""
Explain this topic using real-time search data.

Topic: {prompt}

Search Data: {search_data}

Provide:
- Summary
- Key points
- Real world relevance
"""
    response = model.generate_content(gemini_prompt)
    return response.text


if __name__ == "__main__":
    prompt = input("Enter a topic: ").strip()
    output = get_topic_info(prompt)
    print("\n=== RESULT ===\n")
    print(output)
