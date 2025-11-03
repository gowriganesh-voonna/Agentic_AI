import os
import uuid
from typing import Dict, Any, List
from models.state_schema import ResearchState

try:
    from tavily import TavilyClient
    _HAS_TAVILY = True
except Exception:
    _HAS_TAVILY = False


# Use your API key if available, else fallback to simulated mode
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "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")


# ------------------------------------------------------------------
#  Simulated results (offline fallback)
# ------------------------------------------------------------------
def _simulate_search(query: str) -> List[Dict[str, Any]]:
    """Return simulated results for offline mode."""
    docs = []
    for i in range(1, 6):
        docs.append({
            "id": str(uuid.uuid4())[:8],
            "title": f"Crime Prediction and Machine Learning - Research Paper {i}",
            "url": f"https://example.com/{i}",
            "snippet": f"This study explores how machine learning models such as Random Forest and KNN "
                       f"can be applied to predict and prevent crimes using historical data. (Example {i})",
            "raw_content": f"Machine learning models can predict potential crime hotspots by analyzing "
                           f"historical crime datasets, population demographics, and location-based patterns. "
                           f"This helps law enforcement allocate resources efficiently. (Example {i})",
            "source_domain": "example.com"
        })
    return docs


# ------------------------------------------------------------------
# 🔹 Actual Tavily or LangChain Search
# ------------------------------------------------------------------
def _tavily_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Perform Tavily or fallback to simulated search."""
    try:
        from langchain_community.tools.tavily_search import TavilySearchResults
        tavily = TavilySearchResults(max_results=max_results)
        results = tavily.invoke(query)

        # Handle cases where results come as a string or list
        docs = []
        if isinstance(results, str):
            # Fallback: single string output
            docs.append({
                "id": str(uuid.uuid4())[:8],
                "title": query[:60],
                "url": "",
                "snippet": results[:200],
                "raw_content": results,
                "source_domain": "unknown"
            })
        elif isinstance(results, list):
            for r in results:
                if isinstance(r, str):
                    docs.append({
                        "id": str(uuid.uuid4())[:8],
                        "title": r[:80] + "...",
                        "url": "",
                        "snippet": r,
                        "raw_content": r,
                        "source_domain": "unknown"
                    })
                elif isinstance(r, dict):
                    docs.append({
                        "id": str(uuid.uuid4())[:8],
                        "title": r.get("title") or query,
                        "url": r.get("url", ""),
                        "snippet": r.get("snippet") or r.get("summary") or "",
                        "raw_content": r.get("content") or r.get("text") or "",
                        "source_domain": (r.get("url") or "").split("/")[2] if r.get("url") else "unknown"
                    })
        else:
            # Unexpected output → fallback
            return _simulate_search(query)

        return docs or _simulate_search(query)

    except Exception:
        # If Tavily or langchain_community not working, fallback
        return _simulate_search(query)


# ------------------------------------------------------------------
# Main Search Agent (Node)
# ------------------------------------------------------------------
def search_agent(state: ResearchState) -> dict:
    """Main search node for LangGraph."""
    query = state.get("topic_query", "").strip()
    if not query:
        return {"raw_documents": []}

    docs = _tavily_search(query, max_results=5)
    print(f"[DEBUG] Found {len(docs)} documents for topic '{query}'")

    # Return properly structured documents
    return {"raw_documents": docs}
