from langchain_core.prompts import PromptTemplate


CUSTOM_PROMPT = """You are a helpful assistant analyzing a document. Use the following context to answer the question accurately.

**Instructions:**
1. If the question asks for a LIST of topics/questions/sections, carefully read through ALL context chunks and compile a COMPLETE list. Don't just list the first few you see.
2. If the context contains numbered questions (like "8. Question..." or "9. Question..."), make sure to include ALL of them when asked for a complete list.
3. If the document is structured with separators (like underscores: ________), recognize that each section is a separate topic.
4. When asked about specific topics (like "FastAPI concepts"), search through ALL context chunks for relevant information.
5. Provide detailed, accurate answers based on the context.
6. If you cannot find the answer in the provided context, respond EXACTLY with: "I don't know, it is not related to the PDF.
7. If the question is count of the topics/sections, ensure you count ALL unique sections from the context."

Context chunks:
{context}

Question: {question}

Answer (be thorough and complete):"""

prompt_template = PromptTemplate(
    template=CUSTOM_PROMPT,
    input_variables=["context", "question"]
)