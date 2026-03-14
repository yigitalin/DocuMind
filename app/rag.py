import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from app.llm import ask_ollama

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection("documents")

def add_document(file_path: str, doc_id: str) -> None:
    """
    PDF dosyasını okur ve ChromaDB'ye kaydeder.

    Args:
        file_path: PDF dosyasının yolu
        doc_id: Dokümanın benzersiz kimliği

    Returns:
        None
    """
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
    """
    Soruya en benzer doküman parçalarını ChromaDB'den bulur.

    Args:
        query: Arama sorgusu
        n_results: Döndürülecek sonuç sayısı

    Returns:
        En benzer doküman parçalarının listesi
    """
    query_embedding = model.encode([query]).tolist()[0]
    results = collection.query(
        query_embeddings = [query_embedding],
        n_results=n_results
    )
    return results["documents"][0]

def ask(question: str) -> str:
    """
    Kullanıcının sorusunu cevaplar.

    Args:
        question: Kullanıcının sorusu

    Returns:
        Ollama'nın ürettiği cevap metni
    """
    context = search(question)
    prompt = f"Bağlam: {context}\n\nSoru: {question}\n\nCevap:"
    return ask_ollama(prompt)