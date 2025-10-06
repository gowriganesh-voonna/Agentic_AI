from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from google.genai import types
 
app = FastAPI()
client = genai.Client()
 
# Request model
class MedicalTextRequest(BaseModel):
    text: str
 
@app.post("/extract-entities")
async def extract_entities(request: MedicalTextRequest):
    prompt = (
        f"Extract all medical entities from the following text. "
        f"List symptoms, diseases, medications, and any other relevant medical terms:\n\n{request.text}"
    )
 
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Part(text=prompt)]
    )
 
    return {"entities": response.text}
 
