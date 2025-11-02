import chromadb
from chromadb.config import Settings
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer


chroma_client1 = chromadb.PersistentClient(path="/workspaces/RAG-Powered-Multi-Agent-Q-A-Assistant/Chunks_storage/Chunks_storage")
collection1 = chroma_client1.get_or_create_collection(name = "chunks_storage_from")

chroma_client2 = chromadb.PersistentClient(path="/workspaces/RAG-Powered-Multi-Agent-Q-A-Assistant/intent_classifier/intent_classifier")
collection2 = chroma_client2.get_collection(name="intent_classifier")


model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_top_k(query, k=3):
    query_embedding = model.encode([query])[0].tolist()
    results = collection1.query(query_embeddings=[query_embedding], n_results=k)
    return results['documents'][0]


def classify_query_with_chroma(query, top_k=3):
    query_embedding = model.encode([query]).tolist()[0]
    
    results = collection2.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    intents = [meta['intent'] for meta in results['metadatas'][0]]
    print(f"Top {top_k} retrieved intents:", intents)

    # Majority vote
    from collections import Counter
    intent = Counter(intents).most_common(1)[0][0]
    return intent

