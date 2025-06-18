import faiss
import os
import numpy as np
import json

d = 128

index_file = " username_index.faiss"
label_file = "id_to_label.json"

# check if file exists if not creates new file

if os.path.exists(index_file) and os.path.exists(label_file):

    # load the index file
    index = faiss.read_index(index_file)
    print(f"Index file :")
    print(index_file)
    print("-------------------------------------------")
    # Load label mapping from JSON file
    with open(label_file, "r") as f:
        id_to_label = json.load(f)
    print("Loaded label mapping from file.")

else :
    usernames = []
    num_users = int(input("Enter how many users you want to enter : "))

    for _ in range(num_users):
        username = input("Enter the username :").strip()
        usernames.append(username)
    
    # convert usernames to vector demo
    vectors = np.random.random((len(usernames),d)).astype('float32')

    # Build index and add vectors
    index = faiss.IndexFlatL2(d)
    index.add(vectors)


    # save index to file
    faiss.write_index(index,index_file)
    print(f"Index saved to file {index_file}")


    # save label mapping to .json file
    id_to_label = {i:name for i,name in enumerate(usernames)}  # keys as strings for JSON

    with open(label_file,"w") as f:
        json.dump(id_to_label,f)

    print(f"Saved label mapping to {label_file}.")


# now perform a query
query = input("Enter name to search")


#For demo: convert query username to random vector
query_vector = np.random.random((1,d)).astype('float32')

# index search
D,I = index.search(query_vector,2)

print("Nearest usernames found:")
for idx, dist in zip(I[0], D[0]):
    # idx is an int, but keys in JSON are strings, so convert
    label = id_to_label.get(str(idx), "Unknown")
    print(f"- {label} (distance: {dist})")
