from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent
from langchain_community.tools import TavilySearchResults
from langchain.tools import Tool
from datetime import datetime
import os

# API keys
tavily_key = os.getenv("TAVILY_API_KEY", "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")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyDgIuCfgQnqE4l_J4EX-ClysACAw7cNq8s")

# LLM setup
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY
)

# Custom Tool: Get current time
def get_current_time(tool_input=None):
    """Returns the current system time."""
    return str(datetime.now())


# Define tools
web_tool = TavilySearchResults(tavily_api_key=tavily_key)
custom_tools = [
    web_tool,
    Tool(name="GetCurrentTime", func=get_current_time, description="Returns the current time")
]

# Initialize the agent
agent = initialize_agent(
    tools=custom_tools,
    llm=llm,
    agent_type="zero-shot-react-description",
    handle_parsing_errors=True,
    verbose=True
)

# # Example: Run a prompt
# response = agent.run("What is the current time and latest news about OpenAI?")
# print(response)

while True:
    prompt = input("User> ")
    if prompt.lower() in {"quit","exit"}:
        break
    print(agent.run(prompt))

