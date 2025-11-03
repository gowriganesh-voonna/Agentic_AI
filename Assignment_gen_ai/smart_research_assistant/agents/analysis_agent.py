# agents/analysis_agent.py
from typing import Dict, Any, List
from models.state_schema import ResearchState
from collections import Counter
import re

def extract_keywords(texts: List[str], top_n: int = 10) -> List[str]:
    """Simple keyword extractor using word frequency."""
    words = re.findall(r"\b[a-zA-Z]{4,}\b", " ".join(texts).lower())
    common = Counter(words).most_common(top_n)
    return [w for w, _ in common]

def analyze_agent(state: ResearchState) -> Dict[str, Any]:
    """
    Node: analyze_agent
    Input: {'raw_documents': [...]}
    Output: {'analysis_result': {...}}
    """
    docs = state.get("raw_documents", [])
    all_texts = [d.get("raw_content", "") for d in docs if d.get("raw_content")]

    if not all_texts:
        return {"analysis_result": {"keywords": [], "themes": [], "summary": "No content to analyze"}}

    # Extract simple keywords and themes
    keywords = extract_keywords(all_texts)
    themes = list({word.title() for word in keywords[:5]})

    analysis = {
        "keywords": keywords,
        "themes": themes,
        "num_sources": len(docs)
    }

    return {"analysis_result": analysis}
