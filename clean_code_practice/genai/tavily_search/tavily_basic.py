
from tavily import TavilyClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

class WebsearchRequest(BaseModel):
    query: str
    max_results: int = 5


def tavily_api_key():
    tavily_key = os.getenv("TAVILY_SEARCH_API")
    if not tavily_key:
        raise ValueError("TAVILY_SEARCH_API environment variable not set")
    return TavilyClient(api_key=tavily_key)

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
        return {"Query": request.query, "Results": response.get("results", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))