from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage , AIMessage , SystemMessage
import os

llm= ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    api_key = os.getenv("GEMINI_API_KEY")

)

result = llm.invoke("What is the current year")
print(result.content)

aimessage = AIMessage(
    model = "gemini-2.5-flash",
    api_key = os.getenv("GEMINI_API_KEY"),
    content = "You are AI agent.Can you give about Samsung"

)
#result = aimessage.invoke("You are AI agent.Can you give about Samsung")

print(aimessage.content)


messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What's the capital of France?")
]
response = llm.invoke(messages)
print(response.content)



# multimodal invocation 
message = HumanMessage(
    content = [
        {
            "type" : "text",
            "text" : " explain what is in the image ?"
        },
        {
            "type": "image_url", "image_url": "https://picsum.photos/seed/picsum/200/300"
        },
    
    ]
)

result = llm.invoke([message])
print(result.content)
