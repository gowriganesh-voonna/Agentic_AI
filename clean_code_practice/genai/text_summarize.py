from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
import os
from tavily import TavilyClient


app = FastAPI()


class TextSummarizeRequest(BaseModel):
    text: str
    max_length: int = 200


class TextEntityExtractionRequest(BaseModel):
    text: str

class WebsearchRequest(BaseModel):
    query: str
    max_results: int = 5

def get_api_key():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    else:
        return api_key
    

def tavily_api_key():
    tavily_key = os.getenv("TAVILY_SEARCH_API")
    if not tavily_key:
        raise ValueError("TAVILY_SEARCH_API environment variable not set")
    return TavilyClient(api_key=tavily_key)

client = genai.Client(api_key=get_api_key())

@app.post("/v1/summarize")
async def summarize_text(request: TextSummarizeRequest):

    prompt = f"Summarize the following text content into meaning full, concise points with clear explanations: \n {request.text}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents= [types.Part(text=prompt)]
    )

    return {"Summary":response.text}



@app.post("/extract_medical_entities")
async def extract_medical_entities(request: TextEntityExtractionRequest):
    prompt = f"Extract medical entities from the following text:\n{request.text}"
    
    # Generate content using Google GenAI
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Part(text=prompt)]
    )
    
    return {"entities": response.text}
   


@app.post("/websearch")
async def web_search(request: WebsearchRequest):
    try:
        client = tavily_api_key()


        response = client.search(
            query=request.query,
            max_results=request.max_results,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=False,
        )

        return {"Query": request.query, 
                "Ansewers": response.get("answer", []),
                "Results": response.get("results", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))