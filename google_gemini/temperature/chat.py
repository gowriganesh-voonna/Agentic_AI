from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import os
from typing import Optional, List
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="LangChain GenAI API",
    description="FastAPI application with LangChain and Google Generative AI",
    version="1.0.0"
)

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str = Field(..., description="User message to send to the LLM")
    temperature: Optional[float] = Field(None, ge=0.0, le=1.0, description="Temperature for response generation")
    max_tokens: Optional[int] = Field(None, ge=1, le=8000, description="Maximum tokens in response")

class ChatResponse(BaseModel):
    response: str
    model_used: str
    temperature: float

class FewShotRequest(BaseModel):
    message: str = Field(..., description="User query for few-shot learning")
    temperature: Optional[float] = Field(0.5, ge=0.0, le=1.0)

    
class CustomFewShotRequest(BaseModel):
    message: str = Field(..., description="Your query")
    custom_examples: List[dict] = Field(..., description="List of example dicts with 'input' and 'output' keys")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=1.0, description="Response temperature")


# Set your Google API key (set this as environment variable)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyDgIuCfgQnqE4l_J4EX-ClysACAw7cNq8s")

# Few-shot examples for sentiment analysis
examples = [
    {
        "input": "I absolutely loved this movie! It was fantastic!",
        "output": "Sentiment: Positive\nConfidence: High\nReason: The text contains strong positive words like 'absolutely loved' and 'fantastic'."
    },
    {
        "input": "This product is terrible and broke after one day.",
        "output": "Sentiment: Negative\nConfidence: High\nReason: The text contains negative words like 'terrible' and 'broke', indicating dissatisfaction."
    },
    {
        "input": "The weather is okay today, nothing special.",
        "output": "Sentiment: Neutral\nConfidence: Medium\nReason: The text is neither strongly positive nor negative, using neutral language."
    }
]

# Create few-shot prompt template
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\n{output}"
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="You are a sentiment analysis expert. Analyze the sentiment of the following text and provide the sentiment, confidence level, and reason.\n\n",
    suffix="\nInput: {input}\n",
    input_variables=["input"]
)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to LangChain GenAI API",
        "endpoints": {
            "/chat": "POST - Basic chat with LLM",
            "/few-shot-sentiment": "POST - Sentiment analysis with few-shot learning",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "LangChain GenAI API"}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Basic chat endpoint using ChatGoogleGenerativeAI
    
    - **message**: Your message to the LLM
    - **temperature**: Controls randomness (0.0 = deterministic, 1.0 = creative)
    - **max_tokens**: Maximum length of response
    """
    try:
        # Set default temperature if not provided
        temp = request.temperature if request.temperature is not None else 0.7
        max_tok = int(request.max_tokens) if request.max_tokens is not None else 1000
        
        print(f"Request received - Message: {request.message[:50]}...")
        print(f"Temperature: {temp}, Max Tokens: {max_tok}")
        print(f"API Key present: {bool(GOOGLE_API_KEY)}")
        
        # Initialize the LLM - Don't use max_tokens parameter
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=temp
        )
        
        # Create message properly for ChatGoogleGenerativeAI
        messages = [
            HumanMessage(content=request.message)
        ]
        
        # Get response from LLM
        response = llm.invoke(messages)
        
        print(f"Response type: {type(response)}")
        print(f"Response object: {response}")
        
        # Extract content from response
        response_text = ""
        if hasattr(response, "content") and response.content:
            response_text = response.content
        elif isinstance(response, str):
            response_text = response
        else:
            # Try to get the text from the response object
            response_text = str(response)
            print(f"Response as string: {response_text}")
        
        if not response_text or response_text.strip() == "":
            print(f"Empty response detected. Response object: {response}")
            raise HTTPException(status_code=500, detail="LLM returned empty response")
        
        return ChatResponse(
            response=response_text,
            model_used="gemini-2.5-flash",
            temperature=temp
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error details: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.post("/chat-v2", response_model=ChatResponse)
async def chat_endpoint_v2(request: ChatRequest):
    """
    Alternative chat endpoint using direct Google GenAI
    """
    try:
        import google.generativeai as genai
        
        temp = request.temperature if request.temperature is not None else 0.7
        max_tok = int(request.max_tokens) if request.max_tokens is not None else 1000
        
        print(f"V2 Request - Message: {request.message[:50]}...")
        
        # Configure the API
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # Create model directly
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Generate response
        response = model.generate_content(
            request.message,
            generation_config=genai.types.GenerationConfig(
                temperature=temp,
                max_output_tokens=max_tok
            )
        )
        
        print(f"V2 Response object: {response}")
        print(f"V2 Response text: {response.text if hasattr(response, 'text') else 'No text attr'}")
        
        response_text = response.text if hasattr(response, 'text') else str(response)
        
        if not response_text or response_text.strip() == "":
            raise HTTPException(status_code=500, detail="LLM returned empty response")
        
        return ChatResponse(
            response=response_text,
            model_used="gemini-2.5-flash",
            temperature=temp
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in v2: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/few-shot-sentiment")
async def few_shot_sentiment_analysis(request: FewShotRequest):
    """
    Sentiment analysis endpoint using few-shot prompting
    
    - **message**: Text to analyze for sentiment
    - **temperature**: Controls response variability
    """
    try:
        # Initialize the LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=request.temperature
        )
        
        # Format the prompt with few-shot examples
        formatted_prompt = few_shot_prompt.format(input=request.message)
        
        # Get response
        response = llm.invoke(formatted_prompt)
        
        return {
            "input": request.message,
            "analysis": response.content,
            "model": "gemini-2.5-flash",
            "temperature": request.temperature,
            "prompt_type": "few-shot"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in sentiment analysis: {str(e)}")


# @app.post("/custom-few-shot")
# async def custom_few_shot(
#     message: str,
#     custom_examples: List[dict],
#     temperature: float = 0.7
# ):
#     """
#     Custom few-shot learning endpoint where you can provide your own examples
    
#     - **message**: Your query
#     - **custom_examples**: List of example dicts with 'input' and 'output' keys
#     - **temperature**: Response temperature
#     """
#     try:
#         # Create custom few-shot prompt
#         custom_example_prompt = PromptTemplate(
#             input_variables=["input", "output"],
#             template="Q: {input}\nA: {output}"
#         )
        
#         custom_few_shot = FewShotPromptTemplate(
#             examples=custom_examples,
#             example_prompt=custom_example_prompt,
#             prefix="Learn from these examples and answer the following question:\n\n",
#             suffix="\nQ: {input}\nA:",
#             input_variables=["input"]
#         )
        
#         # Initialize LLM
#         llm = ChatGoogleGenerativeAI(
#             model="gemini-2.5-flash",
#             google_api_key=GOOGLE_API_KEY,
#             temperature=temperature
#         )
        
#         # Format and get response
#         formatted_prompt = custom_few_shot.format(input=message)
#         response = llm.invoke(formatted_prompt)
        
#         return {
#             "query": message,
#             "response": response.content,
#             "examples_used": len(custom_examples),
#             "temperature": temperature
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/custom-few-shot")
async def custom_few_shot(request: CustomFewShotRequest):
    """
    Custom few-shot learning endpoint where you can provide your own examples
    
    - **message**: Your query
    - **custom_examples**: List of example dicts with 'input' and 'output' keys
    - **temperature**: Response temperature
    """
    try:
        # Create custom few-shot prompt
        custom_example_prompt = PromptTemplate(
            input_variables=["input", "output"],
            template="Q: {input}\nA: {output}"
        )
        
        custom_few_shot = FewShotPromptTemplate(
            examples=request.custom_examples,
            example_prompt=custom_example_prompt,
            prefix="Learn from these examples and answer the following question:\n\n",
            suffix="\nQ: {input}\nA:",
            input_variables=["input"]
        )
        
        # Initialize LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=request.temperature
        )
        
        # Format and get response
        formatted_prompt = custom_few_shot.format(input=request.message)
        response = llm.invoke(formatted_prompt)
        
        response_text = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "query": request.message,
            "response": response_text,
            "examples_used": len(request.custom_examples),
            "temperature": request.temperature
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


    

if __name__ == "__main__":
    # Run the application
    uvicorn.run(app, host="0.0.0.0", port=8000)