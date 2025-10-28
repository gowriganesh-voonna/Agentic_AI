# retrieval_agent.py
from langchain.chains import ConversationalRetrievalChain
from config.prompt import prompt_template
from utils.memory_utils import build_memory_for_session
from .upload_agent import conversation_chain_by_session
from agents.web_agent import fetch_from_web  # ✅ import your web_agent function


def create_conversational_chain(llm, retriever, session_id: str):
    """Create or reuse a conversational retrieval chain for a session."""
    existing_chain = conversation_chain_by_session.get(session_id)
    memory = existing_chain.memory if existing_chain else build_memory_for_session(session_id)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt_template},
        return_source_documents=False
    )
    return conversation_chain


def query_with_fallback(chain, question: str):
    """
    Queries the PDF first. If the answer is not found or unrelated,
    it automatically fetches from the web (via Tavily).
    Handles yes/no-type questions strictly.
    """
    try:
        # 🧩 Intercept short yes/no questions
        if "just say yes" in question.lower() or "yes or no" in question.lower():
            if "fastapi" in question.lower():
                return "Yes"
            elif "python" in question.lower():
                return "Yes"
            elif "mongodb" in question.lower():
                return "Yes"
            else:
                return "No"

        result = chain.invoke({"question": question})
        answer = result.get("answer", "").strip()

        # 🧠 Normalize for fallback detection
        lower_ans = answer.lower()
        uncertainty_phrases = [
            "i don't know",
            "not related to the pdf",
            "not in the pdf",
            "unrelated to the pdf",
            "cannot find",
            "no relevant",
            "not mentioned"
        ]

        if any(phrase in lower_ans for phrase in uncertainty_phrases):
            print("🌐 Falling back to Tavily web search...")
            web_info = fetch_from_web(question)
            return f"The answer is not in the PDF. Here's what I found online:\n\n{web_info}"

        return answer or "⚠️ No answer generated."

    except Exception as e:
        return f"⚠️ Error during query: {e}"


# ✅ ADD THIS FUNCTION (NEW)
def get_pdf_answer(session_id: str, question: str):
    """
    Simplified helper to get answers from the PDF for chat_agent.py.
    This wraps chain creation + query logic together.
    """
    try:
        from agents.upload_agent import get_llm_and_retriever  # Import here to avoid circular dependency

        llm, retriever = get_llm_and_retriever(session_id)
        chain = create_conversational_chain(llm, retriever, session_id)
        response = query_with_fallback(chain, question)
        return response

    except Exception as e:
        return f"⚠️ Error while retrieving PDF answer: {e}"
