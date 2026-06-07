from fastapi import FastAPI
from agent.graph import app as agent_app

api = FastAPI()


@api.get("/")
def home():
    return {"message": "AI MCP RAG Server Running"}


@api.post("/ask")
def ask(query: str):
    result = agent_app.invoke({"query": query})
    return {"response": result}
