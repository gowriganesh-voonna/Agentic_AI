import os
# from dotenv import load_dotenv, find_dotenv

# print("Path:",find_dotenv())

# load_dotenv(dotenv_path =r" D:\Practice\Agentic_AI\google_gemini\.env")

api_key = os.getenv("GEMINI_API_KEY")

print(api_key)

print("Current working directory:",os.getcwd())