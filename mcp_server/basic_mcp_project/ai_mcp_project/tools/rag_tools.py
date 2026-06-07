from rag.retriever import retrieve
from models.llm import generate_content


def rag_search(query: str):

    docs = retrieve(query)
    context = " ".join(docs)

    return generate_content(query, context)
