# from google import genai

# client = genai.Client()

# prompt = input("Please enter your prompt :")

# if not prompt:
#     raise ValueError("No prompt was provided.")

# response = client.models.generate_content(
#     model = "gemini-2.5-flash", contents=prompt
# )
# # response = client.models.generate_content(
# #     model="gemini-2.5-flash", contents=prompt
# # )

# print(response.text)


# this model will respond quickly it is turing off the models deeper resoning mode
from google import genai
from google.genai import types

client = genai.Client()

prompt = " what is Deep learning?"

response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = prompt,
    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0)
    ),
)

print(response.text)