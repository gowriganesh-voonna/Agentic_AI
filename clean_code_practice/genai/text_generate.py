from google import genai # Changed import


# Initialize the client (ensure your API key is set in your environment or passed here)
client = genai.Client(api_key="AIzaSyC1i5T2p6WfcrgdUtp2t-k799dAoUO3R_o")

response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents="Information about 3rd Prime Minister of India"
)

print(response.text)


