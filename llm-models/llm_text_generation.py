from transformers import GPT2Tokenizer,GPT2Model,GPT2LMHeadModel
import torch

# define prompt 

prompt = "Ai is replacing most of the Human jobs with ai."


# define prompt and head_mdoel
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

head_model = GPT2LMHeadModel.from_pretrained("gpt2")


# Genearate token IDs for your prompt

input_ids = tokenizer.encode(prompt,return_tensors = "pt")

output_model = head_model.generate(input_ids,max_length = 200 , do_sample = True)


generated_text = tokenizer.decode(output_model[0],skip_special_tokens = True)

print(f"\n Prompt : {prompt}")

print(f"\n Generated Text : {generated_text} ")

