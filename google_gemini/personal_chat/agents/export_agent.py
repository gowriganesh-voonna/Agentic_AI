"""
Conversation Export Agent
Exports chat history in various formats (PDF, DOCX, TXT)
"""

from utils.memory_utils import build_memory_for_session
from utils.document_generator import generate_document
from datetime import datetime
import re
import os


def detect_export_request(user_msg: str) -> dict:
    """Detect if user wants to export conversation"""
    msg_lower = user_msg.lower()
    
    export_keywords = [
        "export conversation", "export chat", "save conversation",
        "save chat", "download conversation", "download chat",
        "export history", "save history", "download history"
    ]
    
    is_export = any(keyword in msg_lower for keyword in export_keywords)
    
    # Detect format
    format_type = None
    if "pdf" in msg_lower or ".pdf" in msg_lower:
        format_type = "pdf"
    elif "word" in msg_lower or "docx" in msg_lower or ".docx" in msg_lower:
        format_type = "docx"
    elif "txt" in msg_lower or "text" in msg_lower or "notepad" in msg_lower:
        format_type = "txt"
    else:
        format_type = "txt"  # Default
    
    return {
        "is_export": is_export,
        "format": format_type,
        "original_message": user_msg
    }


def format_conversation_history(session_id: str, include_metadata: bool = True) -> str:
    """
    Format conversation history into readable text
    """
    try:
        memory = build_memory_for_session(session_id)
        history = memory.load_memory_variables({})
        
        if "chat_history" not in history or not history["chat_history"]:
            return "No conversation history found."
        
        # Build formatted conversation
        conversation_text = ""
        
        if include_metadata:
            conversation_text += f"# Conversation Export\n\n"
            conversation_text += f"**Session ID:** {session_id}\n"
            conversation_text += f"**Export Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            conversation_text += f"**Total Messages:** {len(history['chat_history'])}\n\n"
            conversation_text += "---\n\n"
        
        # Format each message
        message_count = 0
        for msg in history["chat_history"]:
            if hasattr(msg, 'type') and hasattr(msg, 'content'):
                message_count += 1
                
                if msg.type == "human":
                    conversation_text += f"## 👤 User (Message #{message_count // 2 + 1})\n\n"
                    conversation_text += f"{msg.content}\n\n"
                elif msg.type == "ai":
                    conversation_text += f"## 🤖 Assistant\n\n"
                    conversation_text += f"{msg.content}\n\n"
                
                conversation_text += "---\n\n"
        
        # Add footer
        if include_metadata:
            conversation_text += f"\n\n*Exported from Smart Document Assistant*\n"
            conversation_text += f"*Total exchanges: {message_count // 2}*"
        
        return conversation_text
    
    except Exception as e:
        print(f"⚠️ Error formatting conversation: {e}")
        return f"Error formatting conversation: {e}"


def export_conversation(session_id: str, format_type: str = "txt", include_metadata: bool = True) -> tuple:
    """
    Export conversation history to file
    Returns: (status_message, file_path)
    """
    try:
        print(f"📤 Exporting conversation for session {session_id} as {format_type.upper()}...")
        
        # Get formatted conversation
        conversation_text = format_conversation_history(session_id, include_metadata)
        
        if "No conversation history" in conversation_text or "Error" in conversation_text:
            return conversation_text, None
        
        # Generate document
        title = f"Conversation History - {datetime.now().strftime('%Y-%m-%d')}"
        filename = f"conversation_{session_id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_type}"
        
        filepath = generate_document(
            content=conversation_text,
            format=format_type,
            title=title,
            filename=filename
        )
        
        # Count messages
        memory = build_memory_for_session(session_id)
        history = memory.load_memory_variables({})
        message_count = len(history.get("chat_history", [])) // 2
        
        success_message = f"""✅ **Conversation Exported Successfully!**

📊 **Stats:**
- Format: {format_type.upper()}
- Total exchanges: {message_count}
- File size: {os.path.getsize(filepath) / 1024:.1f} KB

📥 **Download:** File is ready at: `{os.path.basename(filepath)}`

The conversation includes all your questions and my responses from this session."""
        
        return success_message, filepath
    
    except Exception as e:
        print(f"⚠️ Error exporting conversation: {e}")
        import traceback
        traceback.print_exc()
        return f"⚠️ Error exporting conversation: {e}", None


def export_conversation_summary(session_id: str, format_type: str = "txt") -> tuple:
    """
    Export a summarized version of the conversation
    """
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from config.settings import GEMINI_API_KEY
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=GEMINI_API_KEY
        )
        
        # Get full conversation
        full_conversation = format_conversation_history(session_id, include_metadata=False)
        
        if "No conversation history" in full_conversation:
            return "⚠️ No conversation to summarize.", None
        
        # Generate summary
        summary_prompt = f"""Summarize this conversation between a user and an AI assistant. 

Provide:
1. **Main Topics Discussed**: List the key topics
2. **Key Questions Asked**: Important questions from the user
3. **Important Answers**: Critical information provided
4. **Action Items**: Any tasks or follow-ups mentioned
5. **Overall Summary**: Brief overview of the conversation

Conversation:
{full_conversation}

Create a well-structured summary:"""
        
        summary_response = llm.invoke(summary_prompt)
        summary = summary_response.content if hasattr(summary_response, 'content') else str(summary_response)
        
        # Format summary document
        summary_text = f"""# Conversation Summary

**Session ID:** {session_id}
**Summary Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

{summary}

---

*This is an AI-generated summary of the conversation.*
*For full conversation history, export the complete chat.*"""
        
        # Generate document
        title = f"Conversation Summary - {datetime.now().strftime('%Y-%m-%d')}"
        filename = f"summary_{session_id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_type}"
        
        filepath = generate_document(
            content=summary_text,
            format=format_type,
            title=title,
            filename=filename
        )
        
        return f"✅ Conversation summary generated as {format_type.upper()}!\n\n📥 Download: `{os.path.basename(filepath)}`", filepath
    
    except Exception as e:
        print(f"⚠️ Error creating summary: {e}")
        return f"⚠️ Error creating summary: {e}", None


def handle_export_request(session_id: str, user_msg: str) -> tuple:
    """
    Main function to handle export requests
    Returns: (response_text, file_path, is_export_request)
    """
    detection = detect_export_request(user_msg)
    
    if not detection["is_export"]:
        return None, None, False
    
    print(f"📤 Detected export request: {detection}")
    
    format_type = detection["format"]
    
    # Check if user wants summary or full export
    if "summary" in user_msg.lower() or "summarize" in user_msg.lower():
        message, filepath = export_conversation_summary(session_id, format_type)
    else:
        message, filepath = export_conversation(session_id, format_type)
    
    return message, filepath, True


import os  # Add this import at the top