# server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import run_research_workflow
from utils.pdf_utils import generate_pdf

app = FastAPI(title="Smart Research Assistant API")

# Allow CORS (for Streamlit frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    topic_query: str


# @app.post("/research")
# def run_research(request: ResearchRequest):
#     """Run the research workflow pipeline."""
#     result = run_research_workflow(request.topic_query)
#     # Generate PDF automatically
#     summary_text = result.get("final_summary", "")
#     pdf_path = generate_pdf(summary_text, request.topic_query)
#     result["pdf_path"] = pdf_path

#     return result
@app.post("/research")
def run_research(request: ResearchRequest):
    """Run the research workflow pipeline."""
    result = run_research_workflow(request.topic_query)

    # Generate PDF automatically
    summary_text = result.get("final_summary", "")
    analysis = result.get("analysis_result", {})
    docs = result.get("raw_documents", [])

    pdf_path = generate_pdf(request.topic_query, summary_text, analysis, docs)
    result["pdf_path"] = pdf_path

    return result
    


@app.get("/")
def root():
    return {"message": "Smart Research Assistant API is running "}
