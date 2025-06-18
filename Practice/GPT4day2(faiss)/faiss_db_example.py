from openai import OpenAI
import pickle # Save and Load Dictionary (label to Index) - Heatmap
import numpy as np
import faiss
import os

#Configuration 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FAISS_INDEX = "text_index.faiss"
LABEL_MAP_FILE = "text_labels.pkl"

VECTOR_DIM = 1536  # - Embeddings - Mean, Full -> Mean -> 768 -d (GPT2) : GPT4 : 1536

#Init Open AI GPT4 - client

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# create or use existing index

if os.path.exists(FAISS_INDEX):
    index = faiss.read_index(FAISS_INDEX) # use existing index

else:
    index = faiss.IndexFlatL2(VECTOR_DIM) # create index


# create or Init pickle file
if os.path.exists(LABEL_MAP_FILE):
    with open(LABEL_MAP_FILE,"rb") as f:
        label_map = pickle.load(f)
else :
    label_map = {} #index,label

def get_mean_embeddings(text:str) -> list:
    response = client.embeddings.create(model = "text-embedding-3-small",input=text)
    return response.data[0].embedding # return final embeddings

def add_index():
    text = input("Enter text to add to faiss db(index): ").strip()
    label = input(f"Enter label for text {text}")

    text_embeddings = get_mean_embeddings(text)
    print(f"text_embeddings : {text_embeddings}")

    vector = np.array([text_embeddings]).astype('float32')
    print(f"vector : {vector}")

    index_id = index.ntotal # current size of total vectors
    print(f"index_id :{index_id}")

    index.add(vector) 
    label_map[index_id] = label
    save_index()

def save_index():
    faiss.write_index(index,FAISS_INDEX)
    with open(LABEL_MAP_FILE,"wb") as f:
        pickle.dump(label_map,f)


def list_labels():
    for idx,label in label_map.items():
        print(f"{idx} : {label}")

def main():
    add_index()
    list_labels()

if __name__ == "__main__":
    main()
