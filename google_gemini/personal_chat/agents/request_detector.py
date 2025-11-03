"""
Document Generation Request Detector - FINAL FIXED VERSION
Only triggers on explicit file generation requests with both action + format
"""

import re


def detect_document_request(user_msg: str) -> dict:
    """
    Detect if user is requesting document generation.
    STRICT: Requires explicit format specification AND action/generation phrase
    """
    msg_lower = user_msg.lower().strip()
    
    # ✅ Step 1: Block all questions unless they have explicit generation phrases
    if "?" in msg_lower:
        explicit_gen = ["give me as", "save as", "export as", "download as", "and give in", "and give as"]
        if not any(phrase in msg_lower for phrase in explicit_gen):
            return {
                'is_request': False,
                'action': None,
                'format': None,
                'scope': None,
                'original_message': user_msg
            }
    
    # ✅ Step 2: Block comparison unless explicit export request
    if any(word in msg_lower for word in ["compare", "comparison", "difference"]):
        if not any(word in msg_lower for word in ["export", "save", "download", "generate file", "give me as"]):
            return {
                'is_request': False,
                'action': None,
                'format': None,
                'scope': None,
                'original_message': user_msg
            }
    
    # Define action keywords (STRICT)
    action_keywords = {
        'summarize': ['summarize'],
        'rewrite': ['rewrite', 'rephrase'],
        'extract': ['extract all', 'give those', 'give that', 'give me all'],
        'export': ['export', 'download', 'save as'],
    }
    
    # Define format keywords (VERY STRICT - must have preposition)
    format_patterns = {
        'pdf': [
            r'\bas\s+pdf\b', r'\bin\s+pdf\b', r'\bto\s+pdf\b',
            r'\bpdf\s+format\b', r'\bpdf\s+file\b',
            r'\band\s+give\s+(?:me\s+)?in\s+pdf\b'
        ],
        'docx': [
            r'\bas\s+(?:docx|word)\b', r'\bin\s+(?:docx|word)\b', r'\bto\s+(?:docx|word)\b',
            r'\bword\s+document\b', r'\bword\s+format\b', r'\bdocx\s+file\b',
            r'\band\s+give\s+(?:me\s+)?in\s+(?:docx|word)\b'
        ],
        'txt': [
            r'\bas\s+(?:txt|text)\b', r'\bin\s+(?:txt|text)\b', r'\bto\s+(?:txt|text)\b',
            r'\btext\s+file\b', r'\btxt\s+file\b', r'\bnotepad\b',
            r'\band\s+give\s+(?:me\s+)?in\s+(?:txt|text)\b'
        ],
    }
    
    # Detect action
    detected_action = None
    for action, keywords in action_keywords.items():
        if any(keyword in msg_lower for keyword in keywords):
            detected_action = action
            break
    
    # Detect format (STRICT - must match pattern)
    detected_format = None
    for fmt, patterns in format_patterns.items():
        if any(re.search(pattern, msg_lower) for pattern in patterns):
            detected_format = fmt
            break
    
    # ✅ CRITICAL: Explicit generation phrases that trigger regardless
    explicit_phrases = [
        r'\bgive\s+(?:me\s+)?(?:in|as)\s+(?:pdf|docx|word|txt|text)',
        r'\band\s+give\s+(?:me\s+)?(?:in|as)\s+(?:pdf|docx|word|txt|text)',
        r'\bexport\s+(?:as|to|in)\s+(?:pdf|docx|word|txt|text)',
        r'\bsave\s+(?:as|to|in)\s+(?:pdf|docx|word|txt|text)',
        r'\bdownload\s+(?:as|to|in)\s+(?:pdf|docx|word|txt|text)',
        r'\bcreate\s+(?:a\s+)?(?:pdf|docx|word|txt|text)\s+file',
        r'\bgenerate\s+(?:a\s+)?(?:pdf|docx|word|txt|text)',
        r'\b(?:tell|explain|give|provide)\s+(?:me\s+)?(?:about|info|information)\s+.+?\s+(?:in|as)\s+(?:pdf|docx|word|txt|text)',
        r'\b.+?\s+(?:in|as)\s+(?:pdf|docx|word|txt|text)\s+format',
    ]
    
    has_explicit = any(re.search(pattern, msg_lower) for pattern in explicit_phrases)
    
    # ✅ RULE: Document generation ONLY if:
    # 1. Has explicit generation phrase, OR
    # 2. Has BOTH action AND format
    is_request = has_explicit or (detected_action is not None and detected_format is not None)
    
    # Detect scope
    detected_scope = 'specific_topic'
    if any(word in msg_lower for word in ['entire', 'complete', 'full', 'whole', 'all']):
        detected_scope = 'full_document'
    
    return {
        'is_request': is_request,
        'action': detected_action,
        'format': detected_format or 'txt',
        'scope': detected_scope,
        'original_message': user_msg
    }


def extract_topic_from_request(user_msg: str) -> str:
    """Extract specific topic from request"""
    msg_lower = user_msg.lower()
    
    patterns = [
        r'(?:about|on)\s+(.+?)(?:\s+(?:in|as|and)|$)',
        r'(?:explain|summarize|rewrite)\s+(?:the\s+)?(.+?)(?:\s+(?:in|as|and|section)|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, msg_lower)
        if match:
            topic = match.group(1).strip()
            stopwords = ['this', 'that', 'the', 'a', 'an', 'it', 'pdf', 'document', 'file']
            if topic not in stopwords and len(topic) > 2:
                return topic
    
    return None