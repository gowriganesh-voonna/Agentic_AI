# agents/chat_agent.py
from agents.retrieval_agent import get_pdf_answer  # ✅ we added this in retrieval_agent.py
from agents.web_agent import fetch_from_web
from utils.memory_utils import build_memory_for_session


def get_conversational_response(session_id: str, question: str):
    """
    Main function used by the chatbot UI.
    It first tries to get an answer from the PDF (via retrieval_agent),
    and if it’s unrelated or not found, falls back to Tavily web search.
    """
    try:
        # 🧠 Step 1 — Build or load memory for the session
        memory = build_memory_for_session(session_id)

        # 🧩 Step 2 — Get PDF-based answer
        pdf_response = get_pdf_answer(session_id, question)
        pdf_response_lower = pdf_response.lower()

        # 🧠 Step 3 — Detect uncertainty to trigger web search
        uncertainty_phrases = [
            "i don't know",
            "not related to the pdf",
            "not in the pdf",
            "unrelated to the pdf",
            "cannot find",
            "no relevant",
            "not mentioned"
        ]

        # 🧠 Normalize and clean up text to ensure proper match
        cleaned_response = pdf_response_lower.replace(".", "").replace(",", "").strip()

        # 🔍 Improved fallback trigger
        if any(phrase in cleaned_response for phrase in uncertainty_phrases) or \
        "i am not sure" in cleaned_response or \
        "i cannot answer" in cleaned_response or \
        "sorry" in cleaned_response:
            print("🌐 Falling back to Tavily web search...")
            web_info = fetch_from_web(question)
            if "⚠️" in web_info or "No relevant" in web_info:
                return f"⚠️ Sorry, I couldn’t find relevant info in the PDF or web."
            return f"The answer is not in the PDF. Here's what I found online:\n\n{web_info}"

        # ✅ Otherwise, return the PDF-based answer
        return pdf_response or "⚠️ No answer generated."

    except Exception as e:
        return f"⚠️ Error during conversation: {e}"
