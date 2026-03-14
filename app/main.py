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