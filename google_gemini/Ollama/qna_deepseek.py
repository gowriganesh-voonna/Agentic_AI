from ollama import chat, ChatResponse

model_name = "gemma:2b"

while True:
    prompt = input("You: ")
    if prompt.lower() in ["exit", "quit"]:
        break

    response: ChatResponse = chat(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )

    print("Gemma:", response.message.content)
