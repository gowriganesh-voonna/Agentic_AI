from fastapi import FastAPI, UploadFile , File
from pydantic import BaseModel
from google import genai
from google.genai import types
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import time
import shutil


app = FastAPI()
client = genai.Client()
model = "models/gemini-2.5-flash"

class QueryRequest(BaseModel):
    query : str



@app.post("/analyze-file")
async def analyze_file(file: UploadFile, body :QueryRequest):
    
    #save file temporarily
    tem_path = f"./temp_"