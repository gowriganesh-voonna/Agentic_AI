from google import genai
from google.genai import types

client= genai.Client(api_key="AIzaSyC1i5T2p6WfcrgdUtp2t-k799dAoUO3R_o")

response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents="Safety prompt to avoid harmful content generation",
    config=types.GenerateContentConfig(
        safety_settings = [
            types.SafetySetting(
                category = types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold = types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
            ),
        ]


)
)


print(response.text)