"""محولات مزودي LLM."""
from __future__ import annotations
import os
import httpx

class LLMClient:
    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model
        self.api_key = os.getenv("GEMINI_API_KEY")

    def chat(self, prompt: str) -> str:
        if not self.api_key:
            return "خطأ: مفتاح API غير موجود في ملف .env"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        try:
            with httpx.Client() as client:
                response = client.post(url, headers=headers, json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"حدث خطأ أثناء الاتصال بـ Gemini: {e}"
