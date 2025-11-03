# main.py
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver  # ✅ to handle in-memory state
from agents.search_agent import search_agent
from agents.analysis_agent import analyze_agent
from agents.summarizer_agent import summarizer_agent
from models.state_schema import ResearchState


def build_research_workflow():
    """Build the Smart Research Assistant workflow using LangGraph."""
    workflow = StateGraph(ResearchState)

    # Define workflow nodes
    workflow.add_node("search_agent", search_agent)
    workflow.add_node("analyze_agent", analyze_agent)
    workflow.add_node("summarize_agent", summarizer_agent)

    # Define transitions between steps
    workflow.set_entry_point("search_agent")
    workflow.add_edge("search_agent", "analyze_agent")
    workflow.add_edge("analyze_agent", "summarize_agent")
    workflow.add_edge("summarize_agent", END)

    # Add in-memory checkpointing for better state tracking
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def run_research_workflow(topic_query: str):
    checkpointer = MemorySaver()  # simple in-memory checkpoint (no DB needed)
    app = build_research_workflow()
    result = app.invoke(
        {"topic_query": topic_query},
        config={"configurable": {"thread_id": "session_1"}, "checkpointer": checkpointer}
    )
    return result

if __name__ == "__main__":
    workflow = build_research_workflow()

    # ✅ Visualize workflow using Mermaid (creates a PNG)
    graph = workflow.get_graph()
    graph_png = graph.draw_mermaid_png()
    with open("workflow_graph.png", "wb") as f:
        f.write(graph_png)

    print("✅ LangGraph visual saved as: workflow_graph.png")

