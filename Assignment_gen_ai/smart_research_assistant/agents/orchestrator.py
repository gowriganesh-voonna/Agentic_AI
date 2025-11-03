# agents/orchestrator.py
from agents.search_agent import search_agent
from agents.analysis_agent import analyze_agent
from agents.summarizer_agent import summarizer_agent
from models.state_schema import ResearchState


def process_query(user_input: str):
    """Main orchestrator that runs Search → Analyze → Summarize."""
    # Initialize state
    state = ResearchState(topic_query=user_input)

    # Step 1:  Search for documents
    search_output = search_agent(state)
    state.update(search_output)

    # Step 2:  Analyze the content
    analysis_output = analyze_agent(state)
    state.update(analysis_output)

    # Step 3: 🧠 Summarize using Gemini (LangChain)
    summary_output = summarizer_agent(state)

    # ✅ Return final summary, PDF, and references
    return {
        "topic": user_input,
        "summary": summary_output.get("final_summary", ""),
        "pdf_path": summary_output.get("pdf_path", ""),
        "analysis": analysis_output.get("analysis_result", {}),
        "documents": search_output.get("raw_documents", [])
    }
