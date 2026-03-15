# DocuMind — Yerel LLM ile Doküman Soru-Cevap Servisi

DocuMind, internet bağlantısı gerektirmeden kendi bilgisayarında çalışan bir yapay zeka destekli doküman soru-cevap servisidir. PDF yükle, soru sor, cevabı al.

---

## Özellikler

- PDF doküman yükleme ve işleme
- RAG (Retrieval-Augmented Generation) mimarisi
- Yerel LLM ile cevap üretme (Ollama + Mistral)
- FastAPI ile REST API
- Modern web arayüzü
- Tamamen yerel — veriler dışarı çıkmaz

---

## Mimari
```
Kullanıcı → Arayüz (HTML/CSS/JS)
         → FastAPI (main.py)
         → RAG Katmanı (rag.py) → ChromaDB
         → LLM Katmanı (llm.py) → Ollama (Mistral)
```

---

## Klasör Yapısı
```
DocuMind/
├── app/
│   ├── main.py        → FastAPI endpointleri
│   ├── rag.py         → RAG mantığı (PDF okuma, ChromaDB)
│   └── llm.py         → Ollama bağlantısı
├── docs/              → Yüklenen PDF dosyaları
├── frontend/
│   └── index.html     → Web arayüzü
├── tests/
│   └── test_api.py    → 13 birim testi
├── requirements.txt   → Python bağımlılıkları
├── start.bat          → Projeyi başlatma scripti
└── README.md
```

---

## Kurulum

### 1. Gereksinimler

- Python 3.11+
- Ollama kurulu olmalı (https://ollama.com)

### 2. Ollama Kurulumu
```bash
# Mistral modelini indir:
ollama pull mistral

# Modelin çalıştığını kontrol et:
ollama list
```

### 3. Projeyi Klonla
```bash
git clone https://github.com/yigitalin/DocuMind.git
cd DocuMind
```

### 4. Sanal Ortam Oluştur
```bash
python -m venv venv
venv\Scripts\activate.bat
```

### 5. Bağımlılıkları Kur
```bash
venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## Çalıştırma

### Yöntem 1: start.bat (Windows)

`start.bat` dosyasına çift tıkla.

### Yöntem 2: Terminal
```bash
venv\Scripts\activate.bat
venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Tarayıcıda aç: `frontend/index.html`

---

## API Endpointleri

| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/health` | GET | Servis durumu |
| `/ask` | POST | Soru sor |
| `/upload` | POST | PDF yükle |
| `/documents` | GET | Yüklü dokümanlar |

---

## Kullanılan Teknolojiler

| Teknoloji | Neden Seçildi |
|-----------|---------------|
| **FastAPI** | Hızlı, modern Python API framework. Otomatik dokümantasyon sağlar. |
| **Ollama** | Yerel LLM çalıştırmak için en kolay araç. İnternet gerektirmez. |
| **Mistral** | Türkçe/İngilizce karışık dokümanlarda iyi performans. Küçük boyutu (4.4GB) ile hızlı. |
| **ChromaDB** | Vektör veritabanı. Anlam benzerliğine göre arama yapar. Kurulumu kolay. |
| **sentence-transformers** | Metni vektöre çevirmek için. `all-MiniLM-L6-v2` modeli hızlı ve yeterince iyi. |
| **pypdf** | PDF dosyalarından metin çıkarmak için. |

---

## Testler
```bash
venv\Scripts\python.exe -m pytest tests/test_api.py -v
```

13 birim testi — tamamı başarılı.

---

## Geliştirici

**Mustafa Yiğit Alın**
Bilgisayar Mühendisliği, 2. Sınıf
GitHub: https://github.com/yigitalin