import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_health_status():
    response = client.get("/health")
    assert response.json() == {"status": "ok"}

def test_health_response_time():
    import time
    start = time.time()
    client.get("/health")
    end = time.time()
    assert (end - start) < 1.0

def test_ask():
    response = client.post("/ask", json={"question": "Python nedir?"})
    assert response.status_code == 200

def test_ask_returns_string():
    response = client.post("/ask", json={"question": "Python nedir?"})
    assert isinstance(response.json()["answer"], str)

def test_ask_empty():
    response = client.post("/ask", json={"question": ""})
    assert response.status_code == 422

def test_upload():
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Test PDF", ln=True)
    pdf.output("docs/test.pdf")

    with open("docs/test.pdf", "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("test.pdf", f, "application/pdf")}
        )
    assert response.status_code == 200

def test_upload_invalid():
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"test content", "text/plain")}
    )
    assert response.status_code == 400

def test_upload_txt():
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"test content", "text/plain")}
    )
    assert response.json()["detail"] == "Sadece PDF dosyası yüklenebilir."

def test_upload_saves_to_docs():
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Test PDF", ln=True)
    pdf.output("docs/test.pdf")

    with open("docs/test.pdf", "rb") as f:
        client.post(
            "/upload",
            files={"file": ("test.pdf", f, "application/pdf")}
        )
    
    assert os.path.exists("docs/test.pdf")

def test_documents():
    response = client.get("/documents")
    assert response.status_code == 200

def test_documents_returns_list():
    response = client.get("/documents")
    assert isinstance(response.json()["documents"], list)

def test_ask_with_context():
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Python programlama dili hakkinda bilgi.", ln=True)
    pdf.output("docs/test.pdf")

    with open("docs/test.pdf", "rb") as f:
        client.post(
            "/upload",
            files={"file": ("test.pdf", f, "application/pdf")}
        )
    
    response = client.post("/ask", json={"question": "Python nedir?"})
    assert response.status_code == 200
    assert isinstance(response.json()["answer"], str)
