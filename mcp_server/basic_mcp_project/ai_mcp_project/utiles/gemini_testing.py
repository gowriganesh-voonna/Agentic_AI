from config import GEMINI_API_KEY
import google.generativeai as genai


api_key = GEMINI_API_KEY

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

# congigure the Gemini API client
genai.configure(api_key=api_key)

print("API key configured successfully.")

models = genai.list_models()

for model in models:

    if "generateContent" in model.supported_generation_methods:
        print(f"Model Name : {model.name}")
        print(f"Model Description : {model.description}")

    # context window size limit
    input_limit = getattr(model, "input_token_limit", "N/A")
    print(f"Input Token Limit : {input_limit}")

    output_limit = getattr(model, "output_token_limit", "N/A")
    print(f"Output Token Limit : {output_limit}")
    print("-" * 40)


# simple test to generate content using a specific model

print("Simple Text generation")

model = genai.GenerativeModel("gemini-2.5-flash")

response = model.generate_content(" Explain what is Gemini API ")


print("Generated Content :", response.text)
