"""محولات مزودي LLM."""
from __future__ import annotations
import os
import time
import httpx

class LLMClient:
    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model
        self.api_key = os.getenv("GEMINI_API_KEY")

    def chat(self, prompt: str, retries: int = 3) -> str:
        if not self.api_key:
            return "خطأ: مفتاح API غير موجود في ملف .env"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        for attempt in range(retries):
            try:
                with httpx.Client() as client:
                    response = client.post(url, headers=headers, json=payload, timeout=30.0)
                    if response.status_code in [503, 429]:
                        time.sleep(2) # الانتظار ثانيتين والمحاولة مجدداً
                        continue
                    response.raise_for_status()
                    data = response.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                if attempt == retries - 1:
                    return f"عذراً، خوادم Gemini مزدحمة حالياً. يرجى المحاولة بعد قليل."
                time.sleep(2)
        
        return "عذراً، فشل الاتصال بعد عدة محاولات."
