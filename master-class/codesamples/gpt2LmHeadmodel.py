# Import required libraries
from transformers import GPT2Tokenizer, GPT2LMHeadModel  # For loading GPT2 tokenizer and language model
import torch  # For tensor computations
from utiles.decoratores import handle_exceptions
 
# Function to load the GPT-2 tokenizer and language model
@handle_exceptions
def load_model():
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")  # Load pre-trained tokenizer
    model = GPT2LMHeadModel.from_pretrained("gpt2")    # Load pre-trained GPT-2 language model head
    return tokenizer, model
 
# Function to generate text based on a given prompt
@handle_exceptions
def generate_text(prompt, max_len=100):
    tokenizer, model = load_model()  # Load tokenizer and model
 
    # Encode the input prompt into tensor of input IDs
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
 
    # Generate text using the model with sampling
    output_ids = model.generate(
        input_ids,
        max_length=max_len,  # Maximum number of tokens in generated text
        do_sample=True       # Enable sampling for more randomness
    )
 
    # Decode output IDs into readable text
    generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
 
    return generated_text
 
# --- Main Execution ---
if __name__ == "__main__":
    prompt = "Python is used for programming the AI models"
 
    # Print original prompt
    print(f"\nPrompt:\n{prompt}\n")
 
    # Generate and print output text
    generated = generate_text(prompt, max_len=100)
    print(f"Generated Text:\n{generated}")


Prompt:
Python is used for programming the AI models

Generated Text:
Python is used for programming the AI models using the R programming language. So when we get a data set from Python and use R, it will be in R, using some basic programming language to control the AI model. But there is a bigger problem at play here. We can't make a data set with Python. I can't.

A Data Set with Python: The Problem

To get around this, we need to create an R data set which can manipulate values. By doing