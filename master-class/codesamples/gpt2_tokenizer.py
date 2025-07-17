from transformers import GPT2Tokenizer
from utiles.decoratores import handle_exceptions

 
# 2. Load the pre-trained GPT-2 tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
 
@handle_exceptions
def gpt2_tokenizer(text):
        # 3. Tokenize the text and return as PyTorch tensors
    # return_tensors="pt" ensures the output is in PyTorch tensor format (used during model inference)
    inputs = tokenizer(text, return_tensors="pt")
    
    # 4. Get token IDs (numerical representations of tokens)
    token_ids = tokenizer.encode(text)
    
    # 5. Get tokens (readable subword units)
    tokens = tokenizer.tokenize(text)
    
    # 6. Print Outputs
    print("Tokens (Subword Units):")
    print(tokens)
    
    print("\nToken IDs (Numerical):")
    print(token_ids)
    
    print(f"\n Number of Tokens: {len(token_ids)}")
    
    print("\nPyTorch Tensor Output:")
    print(inputs)

def main():
    # 1. Input Text
    text = "Learning Python is very interesting."
    gpt2_tokenizer(text)

if __name__ == "__main__":
    main()

#Output :
# Tokens (Subword Units):
# ['Learning', 'ĠPython', 'Ġis', 'Ġvery', 'Ġinteresting', '.']

# Token IDs (Numerical):
# [41730, 11361, 318, 845, 3499, 13]

#  Number of Tokens: 6

# PyTorch Tensor Output:
# {'input_ids': tensor([[41730, 11361,   318,   845,  3499,    13]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1]])}