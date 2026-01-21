from google import genai
from google.genai import types


client = genai.Client(api_key="AIzaSyC1i5T2p6WfcrgdUtp2t-k799dAoUO3R_o")

response = client.models.generate_content_stream(
    model = "gemini-2.5-flash",
    contents = "Indian stock market news for today",
)
for chunk in response:
    print(chunk.text, end="", flush=True)


    