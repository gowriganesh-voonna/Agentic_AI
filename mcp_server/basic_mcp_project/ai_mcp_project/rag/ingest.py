from sentence_transformers import SentenceTransformer
import chromadb


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.get_or_create_collection(name="docs")


def ingest_documents(texts):

    embeddings = model.encode(texts).tolist()

    for i, text in enumerate(texts):

        collection.add(documents=[text], embeddings=[embeddings[i]], ids=[str(i)])


if __name__ == "__main__":
    texts = [
        "The cat is on the roof.",
        "The dog is in the garden.",
        "The bird is flying in the sky.",
    ]

    ingest_documents(texts)
    print("Documents ingested successfully.")
