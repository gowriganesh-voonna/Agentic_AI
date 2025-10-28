#from langchain.memory import ConversationBufferMemory
#from langchain_community.memory import ConversationBufferMemory
from langchain_core.chat_history import InMemoryChatMessageHistory

from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import SQLChatMessageHistory
from config.settings import get_db_engine, CHAT_HISTORY_TABLE

def build_memory_for_session(session_id: str) -> ConversationBufferMemory:
    db_engine = get_db_engine()
    chat_history = SQLChatMessageHistory(
        connection=db_engine,
        session_id=session_id,
        table_name=CHAT_HISTORY_TABLE
    )
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        chat_memory=chat_history,
        input_key="question",
        output_key="answer"
    )
