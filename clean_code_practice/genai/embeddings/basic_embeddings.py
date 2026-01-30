from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# response = client.models.embed_content(
#     model="gemini-embedding-001",
#     contents=["This text is converted to embeddings."],
# )



response = client.models.embed_content(
    model="gemini-embedding-001",
    contents =[
        "SRK is now Autonomous college",
        "India defence stregenth is very powerfull.",
        "Dell laptop are very worst in point of hardware and also in software including service."
    ]
)

# use for loop to get embeddings one by one
for embed in response.embeddings:
    print(embed)


# to get embeddings all at time
print(response.embeddings)