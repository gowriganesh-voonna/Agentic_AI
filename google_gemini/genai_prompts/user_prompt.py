from fastapi import FastAPI , HTTPException, requests


from google import genai
from google.genai import types

from models.schema_validation import TextRequest

app = FastAPI(title="GenAI Prompts")
client = genai.Client()



# Text summarization
@app.post("/summarize_text")
async def summarize_text(request: TextRequest):
    
    prompt = f"Summarize the following text:\n{request.text}"
    
    # Generate content using Google GenAI
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Part(text=prompt)]
    )
    

    return {"summary": response.text}

# Zero shot prompt 
@app.post("/zero_shot")
async def zero_shot_prompt(request : TextRequest):
    if not request.text:
        raise HTTPException(status_code=204, detail= "No text found.")
    prompt = f" Translate the text into German {request.text}"

    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents=[types.Part(text = prompt)]
    )

    return {"Response" : response.text}