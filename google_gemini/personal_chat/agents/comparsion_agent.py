"""
Document Comparison Agent - FULLY FIXED
Compares content across multiple uploaded documents or topics
"""

from agents.upload_agent import conversation_chain_by_session, uploaded_files_by_session
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GEMINI_API_KEY
import re

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    google_api_key=GEMINI_API_KEY,
    temperature=0.3  # Lower temperature for factual comparison
)


def detect_comparison_request(user_msg: str) -> dict:
    """
    Detect if user is asking for comparison
    """
    msg_lower = user_msg.lower()
    
    comparison_keywords = [
        "compare", "comparison", "difference", "differences", 
        "versus", "vs", "vs.", "contrast", "similar", "similarities",
        "which is better", "what's the difference"
    ]
    
    # ✅ FIX: Must have explicit comparison keywords
    is_comparison = any(keyword in msg_lower for keyword in comparison_keywords)
    
    # ✅ Ignore if it's just a general question
    if is_comparison and len(msg_lower) < 30:
        question_only_words = ["who", "whose", "what", "where", "when", "why", "how"]
        if any(msg_lower.startswith(word) for word in question_only_words):
            is_comparison = False
    
    # Extract topics to compare
    topics = []
    
    # Pattern 1: "compare X and Y"
    pattern1 = r'compare\s+(.+?)\s+(?:and|with|to)\s+(.+?)(?:\s+and\s+|\s*$|\.)'
    match1 = re.search(pattern1, msg_lower)
    if match1:
        topic1 = match1.group(1).strip()
        topic2 = match1.group(2).strip()
        # Ignore generic terms
        if topic1 not in ['those', 'these', 'the', 'documents', 'files'] and \
           topic2 not in ['those', 'these', 'the', 'documents', 'files', 'give', 'response', 'explain']:
            topics = [topic1, topic2]
    
    # Pattern 2: "X vs Y"
    pattern2 = r'(.+?)\s+(?:vs\.?|versus)\s+(.+?)(?:\s+and\s+|\s*$|\.)'
    match2 = re.search(pattern2, msg_lower)
    if match2 and not topics:
        topics = [match2.group(1).strip(), match2.group(2).strip()]
    
    # Pattern 3: "difference between X and Y"
    pattern3 = r'difference[s]?\s+between\s+(.+?)\s+and\s+(.+?)(?:\s+and\s+|\s*$|\.)'
    match3 = re.search(pattern3, msg_lower)
    if match3 and not topics:
        topics = [match3.group(1).strip(), match3.group(2).strip()]
    
    return {
        "is_comparison": is_comparison,
        "topics": topics,
        "original_message": user_msg
    }


def compare_documents(session_id: str, user_msg: str) -> str:
    """
    Compare content across uploaded documents
    """
    try:
        print(f"🔍 Comparing documents for session: {session_id}")
        print(f"📋 Available sessions: {list(conversation_chain_by_session.keys())}")
        print(f"📋 Uploaded files sessions: {list(uploaded_files_by_session.keys())}")
        
        # Check if documents are uploaded
        if session_id not in conversation_chain_by_session:
            return "⚠️ Please upload documents first to perform comparison."
        
        if session_id not in uploaded_files_by_session or len(uploaded_files_by_session[session_id]) < 2:
            return "⚠️ Please upload at least 2 documents to compare."
        
        # Get conversation chain
        conversation_chain = conversation_chain_by_session[session_id]
        
        # Get file names
        files = uploaded_files_by_session[session_id]
        file_names = [f["filename"] for f in files]
        
        print(f"📄 Comparing files: {file_names}")
        
        # Create comparison prompt
        comparison_prompt = f"""You are comparing multiple documents. The user has uploaded these files:
{chr(10).join(f"- {name}" for name in file_names)}

User question: {user_msg}

Please provide a detailed comparison addressing:
1. Main similarities between the documents
2. Key differences
3. Unique points in each document
4. Which document covers which topics better
5. Overall assessment

Format your response clearly with headers and bullet points."""
        
        # ✅ FIX: Use invoke() instead of run()
        result = conversation_chain.invoke({"question": comparison_prompt})
        response = result.get("answer", "").strip()
        
        return f"📊 **Document Comparison**\n\n{response}"
    
    except Exception as e:
        print(f"⚠️ Error in document comparison: {e}")
        import traceback
        traceback.print_exc()
        return f"⚠️ Error performing comparison: {e}"


def compare_topics(session_id: str, topic1: str, topic2: str) -> str:
    """
    Compare specific topics across documents
    """
    try:
        print(f"🔍 Comparing topics: {topic1} vs {topic2}")
        print(f"📋 Session ID: {session_id}")
        print(f"📋 Available sessions: {list(conversation_chain_by_session.keys())}")
        
        # Check if documents are uploaded
        if session_id not in conversation_chain_by_session:
            return "⚠️ Please upload documents first to perform topic comparison."
        
        conversation_chain = conversation_chain_by_session[session_id]
        
        # ✅ Query for first topic using invoke()
        query1 = f"Provide comprehensive information about {topic1} from the documents."
        result1 = conversation_chain.invoke({"question": query1})
        info1 = result1.get("answer", "").strip()
        
        # ✅ Query for second topic using invoke()
        query2 = f"Provide comprehensive information about {topic2} from the documents."
        result2 = conversation_chain.invoke({"question": query2})
        info2 = result2.get("answer", "").strip()
        
        # Create comparison using LLM
        comparison_prompt = f"""Compare these two topics based on the information from the documents:

**Topic 1: {topic1}**
{info1}

**Topic 2: {topic2}**
{info2}

Please provide a structured comparison covering:
1. **Purpose/Use Case**: What each is used for
2. **Key Features**: Main characteristics of each
3. **Advantages**: Strengths of each
4. **Disadvantages**: Weaknesses of each
5. **When to Use**: Best scenarios for each
6. **Conclusion**: Summary and recommendation

Use a clear comparison table format where possible."""
        
        comparison = llm.invoke(comparison_prompt)
        result = comparison.content if hasattr(comparison, 'content') else str(comparison)
        
        return f"""📊 **Comparison: {topic1.title()} vs {topic2.title()}**

{result}

---
*Comparison based on uploaded documents and AI analysis*"""
    
    except Exception as e:
        print(f"⚠️ Error in topic comparison: {e}")
        import traceback
        traceback.print_exc()
        return f"⚠️ Error performing topic comparison: {e}"


def compare_with_table(session_id: str, topic1: str, topic2: str) -> str:
    """
    Generate a comparison table between two topics
    """
    try:
        if session_id not in conversation_chain_by_session:
            return "⚠️ Please upload documents first."
        
        conversation_chain = conversation_chain_by_session[session_id]
        
        # ✅ Use invoke() instead of run()
        query1 = f"List key features and characteristics of {topic1}"
        result1 = conversation_chain.invoke({"question": query1})
        info1 = result1.get("answer", "").strip()

        query2 = f"List key features and characteristics of {topic2}"
        result2 = conversation_chain.invoke({"question": query2})
        info2 = result2.get("answer", "").strip()
        
        # Generate comparison table
        table_prompt = f"""Create a detailed comparison table for {topic1} vs {topic2}.

Information about {topic1}:
{info1}

Information about {topic2}:
{info2}

Generate a markdown table with these columns:
| Aspect | {topic1.title()} | {topic2.title()} |

Compare at least 8-10 important aspects like:
- Purpose
- Performance
- Ease of Use
- Learning Curve
- Community Support
- Use Cases
- Pros
- Cons
- Best For

Make it comprehensive and factual."""
        
        table = llm.invoke(table_prompt)
        result = table.content if hasattr(table, 'content') else str(table)
        
        return f"""📊 **Comparison Table: {topic1.title()} vs {topic2.title()}**

{result}

---
*Based on uploaded documents*"""
    
    except Exception as e:
        return f"⚠️ Error creating comparison table: {e}"


def handle_comparison(session_id: str, user_msg: str) -> tuple:
    """
    Main function to handle comparison requests
    Returns: (response_text, is_comparison)
    """
    detection = detect_comparison_request(user_msg)
    
    if not detection["is_comparison"]:
        return None, False
    
    print(f"📊 Detected comparison request: {detection}")
    
    # If specific topics are detected
    if detection["topics"] and len(detection["topics"]) == 2:
        topic1, topic2 = detection["topics"]
        
        # Check if user wants a table
        if "table" in user_msg.lower():
            response = compare_with_table(session_id, topic1, topic2)
        else:
            response = compare_topics(session_id, topic1, topic2)
    else:
        # General document comparison (for "compare those documents", "compare the files", etc.)
        response = compare_documents(session_id, user_msg)
    
    return response, True