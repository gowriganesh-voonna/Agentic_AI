"""
Detects user intent for document generation requests.
Identifies: summarize, rewrite, create report, export, etc.
"""

import re


def detect_document_request(user_msg: str) -> dict:
    """
    Detect if user is requesting document generation.
    
    Returns:
        dict: {
            'is_request': bool,
            'action': str (summarize, rewrite, export, explain, etc.),
            'format': str (pdf, docx, txt, or None),
            'scope': str (full_document, specific_topic, or None)
        }
    """
    msg_lower = user_msg.lower().strip()
    
    # Define action keywords
    action_keywords = {
        'summarize': ['summarize', 'summary', 'summarise', 'brief', 'overview', 'tldr', 'tl;dr'],
        'rewrite': ['rewrite', 'rephrase', 'paraphrase', 'reword', 'recreate'],
        'explain': ['explain', 'elaborate', 'detail', 'clarify', 'describe in detail', 'end to end'],
        'extract': ['extract', 'get all', 'list all', 'give me all', 'show all'],
        'export': ['export', 'download', 'save as', 'convert to', 'generate', 'create document', 'make a file'],
        'report': ['create report', 'generate report', 'make report', 'prepare report'],
    }
    
    # Define format keywords
    format_keywords = {
        'pdf': ['pdf', '.pdf', 'as pdf'],
        'docx': ['docx', 'word', 'doc', '.docx', 'word document'],
        'txt': ['txt', 'text', 'notepad', '.txt', 'text file','in txt','as text', 'text format'],
    }
    
    # Detect action
    detected_action = None
    for action, keywords in action_keywords.items():
        if any(keyword in msg_lower for keyword in keywords):
            detected_action = action
            break
    
    # Detect format
    detected_format = None
    for fmt, keywords in format_keywords.items():
        if any(keyword in msg_lower for keyword in keywords):
            detected_format = fmt
            break
    
    # Detect scope
    detected_scope = 'specific_topic'  # Default
    full_doc_indicators = [
        'entire', 'complete', 'full', 'whole', 'all topics', 
        'everything', 'all content', 'entire document', 'full document'
    ]
    
    if any(indicator in msg_lower for indicator in full_doc_indicators):
        detected_scope = 'full_document'
    
    # Check if it's a document request
    is_request = detected_action is not None or detected_format is not None
    
    # Additional patterns
    generation_patterns = [
        r'give\s+(?:me\s+)?(?:a\s+)?(?:file|document|report)',
        r'create\s+(?:a\s+)?(?:file|document|report)',
        r'generate\s+(?:a\s+)?(?:file|document|report)',
        r'make\s+(?:a\s+)?(?:file|document|report)',
        r'(?:can you|could you)\s+(?:create|make|generate)',
    ]
    
    if any(re.search(pattern, msg_lower) for pattern in generation_patterns):
        is_request = True
        if not detected_action:
            detected_action = 'export'
    
    return {
        'is_request': is_request,
        'action': detected_action,
        'format': detected_format or 'txt',  # Default to txt
        'scope': detected_scope,
        'original_message': user_msg
    }


def extract_topic_from_request(user_msg: str) -> str:
    """
    Extract the specific topic user wants info about.
    E.g., "explain FastAPI" -> "FastAPI"
    """
    msg_lower = user_msg.lower()
    
    # Common patterns
    patterns = [
        r'(?:explain|summarize|rewrite|about)\s+(.+?)(?:\s+(?:in|from|and give)|$)',
        r'(?:give me|create|generate)\s+(?:info|information|details)\s+(?:about|on)\s+(.+?)(?:\s+(?:in|from)|$)',
        r'(?:all|complete)\s+(.+?)\s+(?:topics|info|details|content)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, msg_lower)
        if match:
            return match.group(1).strip()
    
    return None


# Example usage patterns for testing
if __name__ == "__main__":
    test_cases = [
        "summarize this document",
        "rewrite the FastAPI section and give me as PDF",
        "explain MongoDB from end to end",
        "give me all FastAPI topics as a Word document",
        "create a summary report in txt format",
        "can you generate a PDF with all the content?",
        "what is dependency injection?",  # Not a generation request
    ]
    
    for test in test_cases:
        result = detect_document_request(test)
        print(f"\nInput: {test}")
        print(f"Result: {result}")