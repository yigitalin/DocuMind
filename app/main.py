from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
from app.rag import add_document, search, ask

app = FastAPI()

class AskRequest(BaseModel):
    question: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ask")
def ask_question(request: AskRequest):
    answer = ask(request.question)
    return {"answer": answer}

@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Sadece PDF dosyası yüklenebilir.")
    
    file_path = f"docs/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    doc_id = file.filename.replace(".pdf", "")
    add_document(file_path, doc_id)
    
    return {"message": f"{file.filename} başarıyla yüklendi."}