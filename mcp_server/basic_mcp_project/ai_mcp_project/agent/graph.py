from langgraph.graph import StateGraph
from tools.rag_tools import rag_search


def agent_node(state):

    query = state["query"]

    if "add" in query:
        return {"response": "Use add tool  maually via MCP"}

    result = rag_search(query)

    return {"response": result}


graph = StateGraph(dict)

graph.add_node("agent", agent_node)
graph.set_entry_point("agent")

app = graph.compile()
