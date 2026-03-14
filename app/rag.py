import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection("documents")

def add_document(file_path: str, doc_id: str) -> None:
    reader = PdfReader(file_path)
    
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    chunks = [text[i:i+500] for i in range(0, len(text), 500)]

    embeddings = model.encode(chunks).tolist()

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"{doc_id}_{i}" for i in range(len(chunks))]
    )

def search(query: str, n_results: int = 3) -> list:
    query_embedding = model.encode([query]).tolist()[0]
    results = collection.query(
        query_embeddings = [query_embedding],
        n_results=n_results
    )
    return results["documents"][0]