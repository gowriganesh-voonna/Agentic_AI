from transformers import GPT2Tokenizer, GPT2Model
import torch
 
# Import your custom exception-handling decorator
from utiles.decoratores import handle_exceptions
 
 
@handle_exceptions
def get_gpt2_embeddings(text: str):
    """
    Tokenizes the input text using GPT2Tokenizer and retrieves token embeddings using GPT2Model.
 
    Args:
        text (str): The input sentence or phrase.
 
    Returns:
        torch.Tensor: The embeddings tensor of shape [1, sequence_length, 768]
    """
    # Load the pre-trained GPT2 tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
 
    # Load the pre-trained GPT2 model (without LM head)
    model = GPT2Model.from_pretrained("gpt2")
 
    # Tokenize the input and convert it to tensor format
    inputs = tokenizer(text, return_tensors="pt")
 
    # Run the model without computing gradients (inference mode)
    with torch.no_grad():
        outputs = model(**inputs)
 
    # Extract the last hidden state (token embeddings)
    embeddings = outputs.last_hidden_state
 
    # Print the shape of the embedding tensor
    print(f"Embeddings shape: {embeddings.shape}")
 
    print(embeddings)
 
 
# Example usage
if __name__ == "__main__":
    get_gpt2_embeddings("GPT-2 embeddings example")

# output :
# Embeddings shape: torch.Size([1, 8, 768])
# tensor([[[-0.2023, -0.1084, -0.1990,  ..., -0.1866,  0.0799, -0.0417],
#          [ 0.3028, -0.0956,  0.3298,  ...,  0.2122,  0.2060, -0.2252],
#          [-0.0335,  0.0473,  0.2137,  ..., -0.0744,  0.4494, -0.0472],
#          ...,
#          [-0.0941, -0.1020,  1.0095,  ..., -0.4113, -0.6200,  0.1524],
#          [ 0.1354, -0.1038, -0.5818,  ...,  0.3190,  0.1542,  0.4927],