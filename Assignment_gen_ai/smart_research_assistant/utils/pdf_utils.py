from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from datetime import datetime
import os

def generate_pdf(topic: str, summary: str, analysis: dict = None, docs: list = None):
    """Generate a research summary PDF report including analysis and sources."""
    filename = f"research_summary_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join("outputs", filename)

    os.makedirs("outputs", exist_ok=True)
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(f"<b>Research Report: {topic}</b>", styles["Heading1"]))
    story.append(Spacer(1, 12))

    # Summary
    story.append(Paragraph("<b>Summary:</b>", styles["Heading2"]))
    story.append(Paragraph(summary.replace("\n", "<br/>"), styles["Normal"]))
    story.append(Spacer(1, 12))

    # Analysis
    if analysis:
        story.append(Paragraph("<b>Analysis:</b>", styles["Heading2"]))
        for key, value in analysis.items():
            story.append(Paragraph(f"<b>{key}:</b> {value}", styles["Normal"]))
        story.append(Spacer(1, 12))

    # References
    if docs:
        story.append(Paragraph("<b>Reference Documents:</b>", styles["Heading2"]))
        for d in docs:
            title = d.get("title", "Untitled")
            url = d.get("url", "")
            story.append(Paragraph(f"- {title} ({url})", styles["Normal"]))

    doc.build(story)
    return filepath
