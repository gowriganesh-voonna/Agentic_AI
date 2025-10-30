# 📁 File: agents/orchestrator.py
"""
Routes user messages between:
1. PDF-based chat (via upload_agent)
2. Normal chat (via chat_agent)
3. Web fallback (via web_agent)
4. Document generation requests (NEW)
"""

from agents.upload_agent import conversation_chain_by_session  # ✅ For PDF sessions
from agents.chat_agent import get_conversational_response       # ✅ For normal chat
from agents.web_agent import fetch_from_web                     # ✅ For web search
from agents.request_detector import detect_document_request, extract_topic_from_request  # ✅ NEW
from utils.memory_utils import build_memory_for_session         # ✅ For memory handling
from utils.document_generator import generate_document           # ✅ NEW
import os


# 🧠 Detect if message is conversational (not a real question)
def is_conversational_message(user_msg: str) -> bool:
    """
    Check if the user's message is a casual conversation
    (greeting, acknowledgment, appreciation) rather than a question.
    """
    msg_lower = user_msg.lower().strip()
    
    # Single-word casual responses
    casual_words = {
        "great", "thanks", "thank you", "okay", "ok", "cool", "nice", 
        "awesome", "perfect", "good", "fine", "sure", "yes", "no", 
        "yep", "nope", "yeah", "nah", "alright", "got it", "understood",
        "appreciate it", "appreciate", "noted"
    }
    
    # Check if entire message is just a casual word
    if msg_lower in casual_words:
        return True
    
    # Short phrases (under 15 chars) without question marks are likely casual
    if len(msg_lower) < 15 and "?" not in msg_lower and not any(
        word in msg_lower for word in ["what", "how", "why", "when", "where", "who", "which", "tell", "explain", "describe"]
    ):
        return True
    
    return False


def get_casual_response(user_msg: str) -> str:
    """Return a natural conversational response for casual messages."""
    msg_lower = user_msg.lower().strip()
    
    if msg_lower in ["great", "cool", "awesome", "nice", "perfect"]:
        return "Glad to help! Feel free to ask anything else. 😊"
    elif msg_lower in ["thanks", "thank you", "appreciate it"]:
        return "You're welcome! Let me know if you need anything else."
    elif msg_lower in ["okay", "ok", "got it", "understood", "noted"]:
        return "Sure! I'm here if you have more questions."
    elif msg_lower in ["yes", "yeah", "yep"]:
        return "Great! How can I assist you further?"
    elif msg_lower in ["no", "nope", "nah"]:
        return "No problem! Let me know if you need help with something else."
    else:
        return "I'm here to help! Feel free to ask me anything."


# 🆕 Handle document generation requests
def handle_document_generation(session_id: str, user_msg: str, request_info: dict) -> tuple:
    """
    Generate document based on user request.
    Returns: (text_response, file_path or None)
    """
    try:
        action = request_info['action']
        format_type = request_info['format']
        scope = request_info['scope']
        
        # Get content based on scope and action
        if session_id in conversation_chain_by_session:
            # User has uploaded a document
            conversation_chain = conversation_chain_by_session[session_id]
            
            # Determine what content to generate
            if action == 'summarize':
                query = "Provide a comprehensive summary of the entire document with all main topics and key points."
            elif action == 'explain':
                topic = extract_topic_from_request(user_msg)
                if topic:
                    query = f"Explain {topic} in detail from end to end with all information available in the document."
                else:
                    query = "Explain all topics in the document in detail from end to end."
            elif action == 'extract':
                topic = extract_topic_from_request(user_msg)
                if topic:
                    query = f"List and explain all content related to {topic} from the document."
                else:
                    query = "List all topics, sections, and key information from the document."
            elif action == 'rewrite':
                topic = extract_topic_from_request(user_msg)
                if topic:
                    query = f"Rewrite and rephrase all content about {topic} in a clear and professional manner."
                else:
                    query = "Rewrite the entire document content in a clear and professional manner."
            else:  # export, report, or general
                query = "Provide a complete overview of all content in the document with detailed explanations."
            
            # Get the content from the conversation chain
            response = conversation_chain.run(query)
            
            # Determine title
            topic = extract_topic_from_request(user_msg)
            if topic:
                title = f"{action.title()} - {topic.title()}"
            else:
                title = f"Document {action.title()}"
            
            # Generate the document file
            filepath = generate_document(
                content=response,
                format=format_type,
                title=title
            )
            
            return (
                f"✅ I've generated your {format_type.upper()} document!\n\n**Preview:**\n{response[:500]}...\n\n"
                f"📥 **Download:** The file is ready at: `{os.path.basename(filepath)}`",
                filepath
            )
        else:
            return (
                "⚠️ Please upload a document first before requesting document generation.",
                None
            )
    
    except Exception as e:
        print(f"⚠️ Error in document generation: {e}")
        return (f"⚠️ Error generating document: {e}", None)


# ---------------------------------------------------------------------
def orchestrate_conversation(session_id, user_msg):
    """
    Decide how to handle user input:
    - If message is casual conversation, respond naturally without search
    - If it's a document generation request, create the document
    - If PDF uploaded, chat using that
    - If PDF returns "I don't know", trigger web search
    - Otherwise, respond using normal chat memory
    """
    try:
        # 0️⃣ Handle casual conversational messages first
        if is_conversational_message(user_msg):
            print("💬 Detected casual conversation, responding naturally...")
            return get_casual_response(user_msg), None
        
        # 🆕 1️⃣ Check if it's a document generation request
        request_info = detect_document_request(user_msg)
        if request_info['is_request']:
            print(f"📄 Detected document generation request: {request_info}")
            return handle_document_generation(session_id, user_msg, request_info)
        
        # 2️⃣ If this session already has a PDF loaded, use that
        if session_id in conversation_chain_by_session:
            print("📚 Using PDF conversation...")
            conversation_chain = conversation_chain_by_session[session_id]
            response = conversation_chain.run(user_msg)
            
            # 🔍 Check if PDF returned uncertainty
            response_lower = response.lower()
            uncertainty_phrases = [
                "i don't know",
                "not related to the pdf",
                "not in the pdf",
                "unrelated to the pdf",
                "cannot find",
                "no relevant",
                "not mentioned"
            ]
            
            # Clean up response for better matching
            cleaned_response = response_lower.replace(".", "").replace(",", "").strip()
            
            # If uncertain, trigger web search
            if any(phrase in cleaned_response for phrase in uncertainty_phrases):
                print("🌐 PDF couldn't answer, falling back to Tavily web search...")
                web_info = fetch_from_web(user_msg)
                if "⚠️" in web_info or "No relevant" in web_info:
                    return f"⚠️ Sorry, I couldn't find relevant info in the PDF or web.", None
                return f"The answer is not in the PDF. Here's what I found online:\n\n{web_info}", None
            
            return response, None

        # 3️⃣ Otherwise, normal chat mode (Gemini)
        print("💬 Using normal conversational mode...")
        memory = build_memory_for_session(session_id)
        response = get_conversational_response(session_id, user_msg)
        return response, None

    except Exception as e:
        print("⚠️ Error in orchestrate_conversation:", e)
        return f"⚠️ Sorry, I couldn't process that: {e}", None


# ---------------------------------------------------------------------
def process_and_respond(user_msg, chat_history, file, session_id):
    """
    Main bridge called from Gradio UI.
    Sends input through orchestrate_conversation()
    and updates chat UI.
    Now also handles file downloads.
    """
    try:
        response, generated_file = orchestrate_conversation(session_id, user_msg)
        chat_history.append((user_msg, response))
        
        if generated_file:
            status = f"✅ Response generated with downloadable file: {os.path.basename(generated_file)}"
            return chat_history, status, generated_file
        else:
            status = "✅ Response generated successfully."
            return chat_history, status, None
            
    except Exception as e:
        print("⚠️ Error in process_and_respond:", e)
        chat_history.append((user_msg, f"⚠️ Error: {e}"))
        return chat_history, "⚠️ Failed to process request.", None