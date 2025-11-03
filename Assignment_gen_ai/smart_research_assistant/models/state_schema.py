from typing import TypedDict, List, Dict, Optional

class ResearchState(TypedDict, total=False):
    topic_query: str
    raw_documents: List[Dict[str, str]]
    analysis_result: Dict[str, any]
    final_summary: str
    pdf_path: Optional[str]
