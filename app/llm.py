import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_ollama(prompt: str) -> str:
    """
    Ollama'ya soru gönderir ve cevabı döndürür.

    Args:
        prompt: Ollama'ya gönderilecek metin

    Returns:
        Ollama'nın ürettiği cevap metni
    """
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False,
    }

    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()["response"]
