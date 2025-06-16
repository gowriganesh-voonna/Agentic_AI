from transformers import GPT2Tokenizer, GPT2Model
import torch


with open("input_text.txt","r",encoding="utf-8") as f:
    file_text = f.read().strip()  

print(f"File Contnent : {file_text}")

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")

tokens_list = tokenizer.encode(file_text)   # token ids in the format of list


print(f"length of the tokens_list : {len(tokens_list)}")
print(f"Encoded tokens : {tokens_list}")

chunk_size = 50

#spliting the tokens 171 into 171/50 chunks

for i in range(0,len(tokens_list),chunk_size):

    chunked_token = tokens_list[i:i+chunk_size]

    model_input = torch.tensor([chunked_token])

    #print(f"Chunk Obtained : {model_input}")


    with torch.no_grad():
        model_output = model(model_input)

        embeddings = model_output.last_hidden_state 

        #print(f"Last Hidden state : {embeddings}")


        mean_embeddings = embeddings.mean(dim=1) #[i,] 

        #print(f"Average of the embeddings : {mean_embeddings}")
    
    chunked_text = tokenizer.decode(chunked_token)

    print(f"Decode chunk text : {chunked_text}")