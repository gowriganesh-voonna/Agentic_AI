from tavily import TavilyClient
import os
from google import genai
from google.genai import types


# Initialize clients
tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_SEARCH_API")
)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Tavily Search
def tavily_search_with_raw_content(query: str) -> dict:

    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        topic="news",
        time_range="w",
        max_results=10,
        include_raw_content=True,
        include_images=False,
        include_answer=True,
    )

    return response


# Extract raw content
def extract_raw_content(response: dict) -> str:

    texts = []

    for item in response.get("results", []):
        raw = item.get("raw_content")

        if raw:
            texts.append(raw)

    return "\n\n".join(texts)


# Generate with Gemini
def generate_content_with_raw_content(query: str, context: str) -> str:

    prompt = f"""
You are given web search content related to:

Query: {query}

Content:
{context}

Based on this information, give a clear and detailed answer.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Part(text=prompt)]
    )

    return response.text


# ---------------- MAIN ----------------

query = "India latest trade deal"

tavily_response = tavily_search_with_raw_content(query)

raw_text = extract_raw_content(tavily_response)

generated_answer = generate_content_with_raw_content(
    query,
    raw_text
)

print("\nGenerated Answer:\n")
print(generated_answer)
