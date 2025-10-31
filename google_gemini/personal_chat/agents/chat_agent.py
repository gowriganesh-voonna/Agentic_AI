"""
Handles conversational responses using Gemini LLM.
Works with or without uploaded PDFs.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GEMINI_API_KEY
from utils.memory_utils import build_memory_for_session
from agents.web_agent import fetch_from_web

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)


def get_conversational_response(session_id: str, question: str):
    """
    Main conversational function that works WITHOUT requiring a PDF.
    Uses Gemini LLM for general conversation and web search for unknown topics.
    """
    try:
        # Build memory for the session
        memory = build_memory_for_session(session_id)
        
        # Get chat history
        chat_history = memory.load_memory_variables({})
        history_text = ""
        
        if "chat_history" in chat_history and chat_history["chat_history"]:
            for msg in chat_history["chat_history"]:
                if hasattr(msg, 'type'):
                    if msg.type == "human":
                        history_text += f"Human: {msg.content}\n"
                    elif msg.type == "ai":
                        history_text += f"AI: {msg.content}\n"
        
        # Create prompt for Gemini
        prompt = f"""You are a helpful AI assistant. Answer the following question naturally and conversationally.

Previous conversation:
{history_text if history_text else "No previous conversation."}

Current question: {question}

Answer:"""
        
        # Get response from Gemini
        response = llm.invoke(prompt)
        answer = response.content if hasattr(response, 'content') else str(response)
        
        # Save to memory
        memory.save_context(
            {"question": question},
            {"answer": answer}
        )
        
        return answer

    except Exception as e:
        print(f"⚠️ Error in conversational response: {e}")
        import traceback
        traceback.print_exc()
        
        # Fallback to web search
        try:
            print("🌐 Falling back to web search...")
            web_result = fetch_from_web(question)
            return web_result
        except:
            return f"⚠️ Error: {str(e)}"