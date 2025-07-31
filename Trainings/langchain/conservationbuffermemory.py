from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
 
# Initialize the LLM
llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)
 
# Add memory
memory = ConversationBufferMemory()
 
# Create the conversation chain with memory
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)
 
# Simulate a conversation
print(conversation.run("Hi, I want to start a shoe company."))
print(conversation.run("What should I name it?"))
print(conversation.run("Can you give me a slogan for that name?"))