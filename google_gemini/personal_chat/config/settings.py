import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY","AIzaSyDgIuCfgQnqE4l_J4EX-ClysACAw7cNq8s")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/rag_chat")
CHAT_HISTORY_TABLE = os.getenv("CHAT_HISTORY_TABLE", "langchain_chat_history")
TAVILY_API_KEY = "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"

def get_db_engine():
    return create_engine(DATABASE_URL)
