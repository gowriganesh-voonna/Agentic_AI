from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
input_string = input("Please Enter the text").strip()
tokens = tokenizer.tokenize(input_string)

print(tokens)