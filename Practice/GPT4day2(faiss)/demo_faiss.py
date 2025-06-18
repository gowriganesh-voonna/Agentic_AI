import numpy as np
import faiss

# define dimenisonis and data size 

d= 128   # dimenisions : each vector has 128 dimenisions

nb = 1000 # number of base vector in your database

query_vector =1  # number of vectors you want to search /query

# step2 : create ramdom vectors 

data = np.random.random((nb,d)).astype('float32')  # why float32 : FAISS Requires 32-bit 
                                                   # floats for performance and compatibility.
query = np.random.random((query_vector,d)).astype('float32')

# Step 3: Create a FAISS Index
index = faiss.IndexFlatL2(d)   # L2 = Euclidean distance

# IndexFlatL2: A type of index that uses flat (brute-force) search with L2 (Euclidean) distance.

# This index doesn't compress or optimize — it simply compares every vector in the dataset.


# add data to index

index.add(data)  # add 1000 vectores to index
#Now, index holds your 1000 vectors and is ready to perform similarity searches.


# Step 5: Perform Similarity Search
Distance , Index = index.search(query,5)

print("Nearest indices:", Index)   #  Nearest indices: [[491 780 639 128  71]]
print("Distances:", Distance)      # Distances: [[16.216928 16.435602 16.534378 16.66146  16.890089]]

