from fastapi import FastAPI
from pydantic import BaseModel    # request for validation
from openai import OpenAI         # client to call GPT Model
import os




# initlaizes fastapi
app = FastAPI(
    title = "GPT3.5 learning",
    version = "1.0.0"
)


# get api key from environment

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# define user schema
class UserMessage(BaseModel):
    message : str


# chat endpoint

@app.post("/chat")
async def chat_with_assisant(input : UserMessage):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[
            {
                "role":"system","content":"You are an helpful assistant."
            },
            {
                "role":"user","content":input.message
            }
        ],
        temperature= 0.6
    ).choices[0].message.content.strip()


    return {"response": response}

