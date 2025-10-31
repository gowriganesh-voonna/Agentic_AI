"""
Routes user messages between:
1. PDF-based chat (via upload_agent)
2. Normal chat (via chat_agent)
3. Web fallback (via web_agent)
4. Document generation requests
"""

from agents.upload_agent import conversation_chain_by_session
from agents.web_agent import fetch_from_web as web_search_fallback
from agents.web_agent import fetch_from_web
from agents.request_detector import detect_document_request, extract_topic_from_request
from utils.memory_utils import build_memory_for_session
from utils.document_generator import generate_document
import os


def is_conversational_message(user_msg: str) -> bool:
    """Check if the user's message is casual conversation."""
    msg_lower = user_msg.lower().strip()
    
    casual_words = {
        "great", "thanks", "thank you", "okay", "ok", "cool", "nice", 
        "awesome", "perfect", "good", "fine", "sure", "yes", "no", 
        "yep", "nope", "yeah", "nah", "alright", "got it", "understood",
        "appreciate it", "appreciate", "noted"
    }
    
    if msg_lower in casual_words:
        return True
    
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


def handle_document_generation(session_id: str, user_msg: str, request_info: dict) -> tuple:
    """
    Generate document based on user request.
    NOW SUPPORTS: PDF content, web search results, or general queries
    Returns: (text_response, file_path or None)
    """
    try:
        action = request_info['action']
        format_type = request_info['format']
        scope = request_info['scope']
        
        content = None
        title = None
        
        # 🔹 Check if user has uploaded a document
        if session_id in conversation_chain_by_session:
            print("📄 Generating document from uploaded PDF...")
            conversation_chain = conversation_chain_by_session[session_id]
            
            # Determine query based on action
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
            else:
                query = "Provide a complete overview of all content in the document with detailed explanations."
            
            # Get content from PDF
            content = conversation_chain.run(query)
            
            # Check if PDF couldn't answer - fallback to web
            if content and any(phrase in content.lower() for phrase in ["i don't know", "not related to the pdf", "cannot find"]):
                print("🌐 PDF couldn't answer, fetching from web...")
                topic = extract_topic_from_request(user_msg)
                if topic:
                    web_content = fetch_from_web(f"{action} {topic}")
                    content = web_content
                    title = f"{action.title()} - {topic.title()} (Web)"
            else:
                topic = extract_topic_from_request(user_msg)
                if topic:
                    title = f"{action.title()} - {topic.title()}"
                else:
                    title = f"Document {action.title()}"
        
        else:
            # 🌐 No PDF uploaded - Use web search or general query
            print("🌐 No PDF uploaded, using web search...")
            topic = extract_topic_from_request(user_msg)
            
            if topic:
                # Search web for the topic
                search_query = f"{action} {topic}" if action else topic
                content = fetch_from_web(search_query)
                title = f"{action.title() if action else 'Information'} - {topic.title()}"
            else:
                # Generic request without specific topic
                content = fetch_from_web(user_msg)
                title = f"{action.title() if action else 'Web Search'} Results"
            
            # Check if web search failed
            if not content or "⚠️" in content or "No relevant" in content:
                return (
                    "⚠️ I couldn't find relevant information to generate the document. Please try with a different query or upload a document first.",
                    None
                )
        
        # 📝 Generate the document file
        if content:
            filepath = generate_document(
                content=content,
                format=format_type,
                title=title or "Generated Document"
            )
            
            preview = content[:500] if len(content) > 500 else content
            
            return (
                f"✅ I've generated your {format_type.upper()} document!\n\n**Preview:**\n{preview}...\n\n"
                f"📥 **Download:** The file is ready at: `{os.path.basename(filepath)}`",
                filepath
            )
        else:
            return ("⚠️ No content available to generate document.", None)
    
    except Exception as e:
        print(f"⚠️ Error in document generation: {e}")
        import traceback
        traceback.print_exc()
        return (f"⚠️ Error generating document: {str(e)}", None)


def orchestrate_conversation(session_id, user_msg):
    """
    Decide how to handle user input:
    - Handle casual conversation naturally
    - Handle document generation (with or without uploaded PDF)
    - Use PDF if uploaded
    - Fall back to web search if needed
    - Support normal chat without requiring document upload
    """
    try:
        # 0️⃣ Handle casual conversational messages
        if is_conversational_message(user_msg):
            print("💬 Detected casual conversation, responding naturally...")
            return get_casual_response(user_msg), None
        
        # 1️⃣ Check if it's a document generation request
        request_info = detect_document_request(user_msg)
        if request_info['is_request']:
            print(f"📄 Detected document generation request: {request_info}")
            return handle_document_generation(session_id, user_msg, request_info)
        
        # 2️⃣ If PDF is uploaded, use it
        if session_id in conversation_chain_by_session:
            print("📚 Using PDF conversation...")
            conversation_chain = conversation_chain_by_session[session_id]
            response = conversation_chain.run(user_msg)
            
            # Check if PDF returned uncertainty
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
            
            cleaned_response = response_lower.replace(".", "").replace(",", "").strip()
            
            # If uncertain, trigger web search
            if any(phrase in cleaned_response for phrase in uncertainty_phrases):
                print("🌐 PDF couldn't answer, falling back to web search...")
                web_info = fetch_from_web(user_msg)
                if "⚠️" in web_info or "No relevant" in web_info:
                    return f"⚠️ Sorry, I couldn't find relevant info in the PDF or web.", None
                return f"The answer is not in the PDF. Here's what I found online:\n\n{web_info}", None
            
            return response, None
        
        # 3️⃣ No PDF uploaded - Use web search directly
        else:
            print("🌐 No PDF uploaded, using web search...")
            web_info = fetch_from_web(user_msg)
            
            if "⚠️" in web_info or "No relevant" in web_info:
                # If web search fails, use normal conversational response
                print("💬 Web search failed, using conversational mode...")
                memory = build_memory_for_session(session_id)
                response = get_conversational_response(session_id, user_msg)
                return response, None
            
            return f"🌐 Here's what I found online:\n\n{web_info}", None

    except Exception as e:
        print("⚠️ Error in orchestrate_conversation:", e)
        import traceback
        traceback.print_exc()
        return f"⚠️ Sorry, I couldn't process that: {e}", None


def process_and_respond(user_msg, chat_history, file, session_id):
    """
    Main bridge called from Gradio UI.
    Handles all user interactions with proper error handling.
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
        import traceback
        traceback.print_exc()
        chat_history.append((user_msg, f"⚠️ Error: {e}"))
        return chat_history, "⚠️ Failed to process request.", None