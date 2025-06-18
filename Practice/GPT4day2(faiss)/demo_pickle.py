import pickle

# In Python, pickle is a module used for serializing and deserializing Python objects.
# Serialization (also called "pickling") means converting a Python object into a byte stream, 
# and deserialization ("unpickling") is converting that byte stream back into a Python object

# sample data
data = {"Name" :"Voonna Gowri Ganesh",
        "Gender":"Male"}


# serializiing pickle data
with open("data.pkl","wb") as f:
    pickle.dump(data,f)


# deserilaizing pickle data
with open("data.pkl","rb") as f:
    loaded_data = pickle.load(f)

print(loaded_data)

