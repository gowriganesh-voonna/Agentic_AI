from fastapi import FastAPI , HTTPException, requests


from google import genai
from google.genai import types

from models.schema_validation import TextRequest
import pathlib




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

# Zero shot prompt  endpoint
@app.post("/zero_shot")
async def zero_shot_prompt(request : TextRequest):
    if not request.text:
        raise HTTPException(status_code=204, detail= "No text found.")
    
    #prompt = f" Translate the text into German {request.text}"
    prompt = f"Classify the sentence whether it is an postive,negative or neutral \n Text : {request.text}"

    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents=[types.Part(text = prompt)]
    )

    return {"Response" : response.text}


# few shot promp endpoint
@app.post("/role_based_prompt")
async def role_based_prompt(request : TextRequest):
    if not request.text:
        raise HTTPException(status_code=204, detail= "No text found.")
    
    prompt = f"""System: You are a helpful  assistant.
    User: Hi, I want to know about ice mountains

    Assistant: Ice mountains were formed in cold climates, completely in a frozen state. They melt during summer.
    User: Thank you
    Assistant: Do you want to know anything else?
    User: {request.text}
    Assistant : 
    """

    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents=[types.Part(text = prompt)]
    )

    return {"Response" : response.text}


#few shot prompt
@app.post("/few_shots_prompt")
async def few_shots_prompt(request : TextRequest):

    if not request.text:
        raise HTTPException(status_code=204, detail="Empty response was received.")
    
    prompt = f""" Extract the cities from the text, include state they are in.

    user : vijayawada is having famous  bus stand , railway station.
    Model : vijayawada -Andhra Pradesh
    user : Hyderabad is the heart for IT growth.
    Model : Hyderabad: Telangana
    user   : {request.text}
    Model 
    """

    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents=[types.Part(text = prompt)]
    )

    return {"Response" : response.text}

# chain of thought prompt
@app.get("/chain_of_thought")
async def chain_of_thought_prompt():
    
    prompt = f""" A can finish a work in 18 days and B can do the same work in 15 days. B worked for 10 days and left the job. In how many days, A alone can finish the remaining work 
    """

    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents=[types.Part(text = prompt)]
    )

    if not response.text:
        raise HTTPException(status_code=204,
                            detail="Empty prompt was given")

    return {"Response" : response.text}


