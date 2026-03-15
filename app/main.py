from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from app.rag import add_document, search, ask

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str

@app.get("/health")
def health_check():
    """
    Servisin çalışıp çalışmadığını kontrol eder.

    Returns:
        Servis durumunu gösteren JSON
    """
    return {"status": "ok"}

@app.post("/ask")
def ask_question(request: AskRequest):
    """
    Kullanıcının sorusunu alır ve cevap döndürür.

    Args:
        request: Kullanıcının sorusunu içeren istek

    Returns:
        Ollama'nın ürettiği cevap
    """
    if not request.question.strip():
        raise HTTPException(status_code=422, detail="Soru boş olamaz.")
    answer = ask(request.question)
    return {"answer": answer}

@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    """
    PDF dosyasını yükler ve ChromaDB'ye kaydeder.

    Args:
        file: Yüklenen PDF dosyası

    Returns:
        Yükleme başarı mesajı
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Sadece PDF dosyası yüklenebilir.")
    
    file_path = f"docs/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    doc_id = file.filename.replace(".pdf", "")
    add_document(file_path, doc_id)
    
    return {"message": f"{file.filename} başarıyla yüklendi."}

@app.get("/documents")
def list_documents():
    """
    Yüklenen dokümanları listeler.

    Returns:
        Yüklü PDF dosyalarının listesi
    """
    files = os.listdir("docs")
    pdfs = [f for f in files if f.endswith(".pdf")]
    return {"documents": pdfs}

@app.delete("/documents/{filename}")
def delete_document(filename: str):
    """
    Belirtilen dokümanı siler.

    Args:
        filename: Silinecek dosyanın adı

    Returns:
        Silme başarı mesajı
    """
    file_path = f"docs/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Dosya bulunamadı.")
    os.remove(file_path)
    return {"message": f"{filename} silindi."}