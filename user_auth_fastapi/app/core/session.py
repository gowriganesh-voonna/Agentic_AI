# app/core/session_store.py
 
from datetime import datetime, timedelta
from typing import Dict
 
# This dictionary holds the active user sessions temporarily in memory
active_sessions: Dict[str, Dict[str, datetime]] = {}
 
def create_session(user_id: str, token: str, expiry_minutes: int = 60):
    """
    Store a session with token and expiry time (default: 60 minutes)
    """
    active_sessions[user_id] = {
        "token": token,
        "expires": datetime.utcnow() + timedelta(minutes=expiry_minutes)
    }
 
def is_session_active(user_id: str, token: str) -> bool:
    """
    Check if the user session is valid and not expired
    """
    session = active_sessions.get(user_id)
    if not session:
        return False
    if session["token"] != token or datetime.utcnow() > session["expires"]:
        # Cleanup expired or mismatched sessions
        active_sessions.pop(user_id, None)
        return False
    return True
 
def end_session(user_id: str):
    """
    Remove user session manually (logout)
    """
    active_sessions.pop(user_id, None)
 