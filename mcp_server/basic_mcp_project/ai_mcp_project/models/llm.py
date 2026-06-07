from utiles.config import GEMINI_API_KEY
import google.generativeai as genai


genai.configure(api_key=GEMINI_API_KEY)


def generate_content(query, context):

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    Give answer to the following question based on the given context

    Context: {context}

    Question: {query}"""

    response = model.generate_content(prompt)

    return response.text
