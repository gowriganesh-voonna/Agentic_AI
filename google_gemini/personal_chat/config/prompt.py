from langchain_core.prompts import PromptTemplate


CUSTOM_PROMPT = """You are a helpful assistant. Use the following context to answer the question.
If user asks a question related to the PDF, provide a concise and accurate answer based on the context.
If the answer is not contained in the context, respond exactly with:
"I don't know, it is not related to the PDF."

Context:
{context}

Question:
{question}

Answer:"""

prompt_template = PromptTemplate(
    template=CUSTOM_PROMPT,
    input_variables=["context", "question"]
)
# The prompt_template can be imported and used in other modules