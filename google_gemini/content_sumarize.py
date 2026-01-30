from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from google.genai import types
 
app = FastAPI()
client = genai.Client()
 
# Define the request model
class TextRequest(BaseModel):
    text: str
 
@app.post("/summarize_text")
async def summarize_text(request: TextRequest):
    prompt = f"Summarize the following text:\n{request.text}"
    
    # Generate content using Google GenAI
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Part(text=prompt)]
    )
    
    return {"summary": response.text}



