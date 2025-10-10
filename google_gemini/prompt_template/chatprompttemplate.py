from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import FewShotPromptTemplate,PromptTemplate

chat_template = ChatPromptTemplate.from_messages([
    ("system","You are an helpfull assistant."),
    ("human","Translate '{text}' to '{language}'")
])

# Format the prompt with actual values

formatted_prompt = chat_template.format_messages(
    text = "Hello, how are you ?",
    language = "French"
)

# Print the formatted prompt
for message in formatted_prompt:
    print(f"{message.type} : {message.content}")


examples = [
    {"input":"2+2","output":"4"},
    {"input":"3+5","output":"8"}
]

example_prompt = PromptTemplate.from_template("Input : {input}\n Output : {output}")

few_shot = FewShotPromptTemplate(
    examples = examples,
    example_prompt = example_prompt,
    prefix = "Solve the following problems:",
    suffix = "Input : {input} \n Output:",
    input_variables=["input"]
)

print(few_shot.format(input="7+6"))
