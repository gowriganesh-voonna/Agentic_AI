from google import genai
from google.genai import types


# Streaming content means : getting the generated content in smaller parts (chunks) as soon as they are ready, rather than waiting for the entire response to be generated before receiving it. This is particularly useful for large responses or when you want to start processing the content immediately.


client = genai.Client(api_key="AIzaSyC1i5T2p6WfcrgdUtp2t-k799dAoUO3R_o")

response = client.models.generate_content_stream(
    model = "gemini-2.5-flash",
    contents = "Indian stock market news for today",
)
for chunk in response:
    print(chunk.text, end="", flush=True)


    