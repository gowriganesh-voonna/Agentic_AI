"""
COMPLETE WORKING orchestrator.py - Copy this entire file
"""

from agents.upload_agent import conversation_chain_by_session, list_uploaded_files, clear_session_files
from agents.web_agent import fetch_from_web as web_search_fallback
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


def handle_special_commands(session_id: str, user_msg: str) -> tuple:
    """Handle special commands like 'list files', 'clear files', etc."""
    msg_lower = user_msg.lower().strip()
    
    # List uploaded files
    if any(cmd in msg_lower for cmd in ["list files", "show files", "list documents", "show documents", "my files"]):
        response = list_uploaded_files(session_id)
        return response, None, True
    
    # Clear session files
    if any(cmd in msg_lower for cmd in ["clear files", "delete files", "remove files", "clear documents", "reset session"]):
        response = clear_session_files(session_id)
        return response, None, True
    
    # Search in document
    if msg_lower.startswith("search ") or msg_lower.startswith("find "):
        try:
            from agents.retrieval_agent import search_in_document
            search_term = msg_lower.replace("search ", "").replace("find ", "").strip()
            response = search_in_document(session_id, search_term)
            return response, None, True
        except Exception as e:
            return f"⚠️ Search error: {e}", None, True
    
    return None, None, False


def handle_document_generation(session_id: str, user_msg: str, request_info: dict) -> tuple:
    """Generate document based on user request."""
    try:
        action = request_info['action']
        format_type = request_info['format']
        scope = request_info['scope']
        
        content = None
        title = None
        
        # Check if user has uploaded a document
        if session_id in conversation_chain_by_session:
            print("📄 Generating document from uploaded PDF...")
            conversation_chain = conversation_chain_by_session[session_id]
            
            # Determine query based on action
            if action == 'summarize':
                query = "Provide a comprehensive and detailed summary of the entire document. Include all main topics, key points, important details, and conclusions. Be thorough."
            elif action == 'explain':
                topic = extract_topic_from_request(user_msg)
                if topic:
                    query = f"Provide a comprehensive, detailed explanation of {topic}. Include all relevant information, examples, use cases, and technical details available in the document. If the document doesn't contain information about {topic}, search your knowledge base and provide a thorough explanation anyway."
                else:
                    query = "Provide a detailed explanation of all topics in the document. Include comprehensive information, examples, and technical details."
            elif action == 'extract':
                topic = extract_topic_from_request(user_msg)
                if topic:
                    query = f"Extract and list all content, information, and details related to {topic} from the document. Be thorough and comprehensive."
                else:
                    query = "Extract ALL content from the document. Provide the complete text including all sections, topics, subsections, examples, and details. Do not summarize - give the full content."
            elif action == 'rewrite':
                topic = extract_topic_from_request(user_msg)
                if topic:
                    query = f"Rewrite and rephrase all content about {topic} in a clear and professional manner. Include all details and examples."
                else:
                    query = "Provide the complete content of the entire document, rewritten in clear and professional language. Include ALL sections, topics, and details from start to finish."
            else:
                query = "Provide a complete overview of all content in the document with detailed explanations."
            
            # Get content from PDF using invoke
            result = conversation_chain.invoke({"question": query})
            content = result.get("answer", "").strip()
            
            # Check if PDF couldn't answer - fallback to web
            if content and any(phrase in content.lower() for phrase in ["i don't know", "not related to the pdf", "cannot find"]):
                print("🌐 PDF couldn't answer, fetching from web...")
                topic = extract_topic_from_request(user_msg)
                if topic:
                    web_content = web_search_fallback(f"{action} {topic}")
                    content = web_content
                    title = f"{action.title()} - {topic.title()} (Web)"
            else:
                topic = extract_topic_from_request(user_msg)
                if action and topic:
                    title = f"{action.title()} - {topic.title()}"
                elif action:
                    title = f"Document {action.title()}"
                elif topic:
                    title = f"Information - {topic.title()}"
                else:
                    title = "Generated Document"
        
        else:
            # No PDF uploaded - Use web search
            print("🌐 No PDF uploaded, using web search...")
            topic = extract_topic_from_request(user_msg)
            
            if topic:
                search_query = f"{action} {topic}" if action else topic
                content = web_search_fallback(search_query)
                title = f"{action.title() if action else 'Information'} - {topic.title()}"
            else:
                content = web_search_fallback(user_msg)
                title = f"{action.title() if action else 'Web Search'} Results"
            
            if not content or "⚠️" in content or "No relevant" in content:
                return (
                    "⚠️ I couldn't find relevant information to generate the document. Please try with a different query or upload a document first.",
                    None
                )
        
        # Generate the document file
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
    """Main orchestration logic with all features."""
    try:
        # 0️⃣ Handle casual conversational messages
        if is_conversational_message(user_msg):
            print("💬 Detected casual conversation, responding naturally...")
            return get_casual_response(user_msg), None
        
        # 1️⃣ Handle special commands
        special_response, special_file, is_special = handle_special_commands(session_id, user_msg)
        if is_special:
            return special_response, special_file
        
        # 2️⃣ Handle conversation export
        try:
            from agents.export_agent import handle_export_request
            export_response, export_file, is_export = handle_export_request(session_id, user_msg)
            if is_export:
                return export_response, export_file
        except ImportError:
            print("⚠️ Export agent not available")
        except Exception as e:
            print(f"⚠️ Export error: {e}")
        
        # 3️⃣ Handle document comparison
        try:
            from agents.comparison_agent import handle_comparison
            comparison_response, is_comparison = handle_comparison(session_id, user_msg)
            if is_comparison:
                return comparison_response, None
        except ImportError:
            print("⚠️ Comparison agent not available")
        except Exception as e:
            print(f"⚠️ Comparison error: {e}")
        
        # 4️⃣ Handle image extraction
        try:
            from utils.image_extractor import extract_and_describe_images, format_image_extraction_report, detect_image_extraction_request
            from agents.upload_agent import uploaded_files_by_session
            
            if detect_image_extraction_request(user_msg):
                print("🖼️ Detected image extraction request...")
                
                if session_id not in uploaded_files_by_session or not uploaded_files_by_session[session_id]:
                    return "⚠️ Please upload a document first to extract images.", None
                
                # Get the most recent file
                latest_file = uploaded_files_by_session[session_id][-1]
                file_path = latest_file["file_path"]
                
                # Extract and describe images
                result = extract_and_describe_images(file_path, describe_with_ai=True)
                report = format_image_extraction_report(result)
                
                return report, None
        except ImportError:
            print("⚠️ Image extractor not available")
        except Exception as e:
            print(f"⚠️ Image extraction error: {e}")
        
        # 5️⃣ Check if it's a document generation request
        request_info = detect_document_request(user_msg)
        if request_info['is_request']:
            print(f"📄 Detected document generation request: {request_info}")
            return handle_document_generation(session_id, user_msg, request_info)
        
        # 6️⃣ If PDF is uploaded, use it
        if session_id in conversation_chain_by_session:
            print("📚 Using PDF conversation...")
            conversation_chain = conversation_chain_by_session[session_id]
            
            # Use invoke instead of run
            result = conversation_chain.invoke({"question": user_msg})
            response = result.get("answer", "").strip()
            
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
                web_info = web_search_fallback(user_msg)
                if "⚠️" in web_info or "No relevant" in web_info:
                    return f"⚠️ Sorry, I couldn't find relevant info in the PDF or web.", None
                return f"The answer is not in the PDF. Here's what I found online:\n\n{web_info}", None
            
            # Add simple citations
            if result.get("source_documents"):
                sources = result["source_documents"]
                citations = "\n\n📚 **Sources:**\n"
                seen = set()
                for idx, doc in enumerate(sources[:3], 1):
                    source = doc.metadata.get("source_file", "Unknown")
                    page = doc.metadata.get("page", "N/A")
                    key = f"{source}_{page}"
                    if key not in seen:
                        seen.add(key)
                        citations += f"[{idx}] {source}"
                        if page != "N/A":
                            citations += f" (Page {page})"
                        citations += "\n"
                response += citations
            
            return response, None
        
        # 7️⃣ No PDF uploaded - Use web search directly
        else:
            print("🌐 No PDF uploaded, using web search...")
            web_info = web_search_fallback(user_msg)
            
            if "⚠️" in web_info or "No relevant" in web_info:
                # If web search fails, use conversational mode
                print("💬 Web search failed, using conversational mode...")
                try:
                    from agents.chat_agent import get_conversational_response
                    memory = build_memory_for_session(session_id)
                    response = get_conversational_response(session_id, user_msg)
                    return response, None
                except Exception as e:
                    return f"⚠️ I encountered an error: {e}", None
            
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