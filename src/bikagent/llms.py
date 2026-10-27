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

    def _send_request(self, client, url, headers, payload, retries=3):
        for attempt in range(retries):
            try:
                response = client.post(url, headers=headers, json=payload, timeout=30.0)
                if response.status_code in [503, 429]:
                    time.sleep(2)
                    continue
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                time.sleep(2)
        raise Exception("فشل الاتصال بعد عدة محاولات")

    def chat(self, prompt: str, registry: any) -> str:
        if not self.api_key:
            return "خطأ: مفتاح API غير موجود في ملف .env"

        tools_schema = []
        for name in registry.list():
            tool = registry.get(name)
            tools_schema.append({
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "expression": {"type": "STRING", "description": "التعبير الرياضي"}
                    },
                    "required": ["expression"]
                }
            })

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        headers = {"Content-Type": "application/json", "x-goog-api-key": self.api_key}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "tools": [{"function_declarations": tools_schema}]
        }

        try:
            with httpx.Client() as client:
                data = self._send_request(client, url, headers, payload)
                parts = data["candidates"][0]["content"]["parts"]

                if "functionCall" in parts[0]:
                    func_call = parts[0]["functionCall"]
                    tool_name = func_call["name"]
                    args = func_call["args"]
                    
                    result = registry.run(tool_name, **args)
                    
                    payload["contents"].append({"role": "model", "parts": [{"functionCall": func_call}]})
                    payload["contents"].append({"role": "user", "parts": [{"functionResponse": {"name": tool_name, "response": {"result": result}}}]})
                    
                    data2 = self._send_request(client, url, headers, payload)
                    return data2["candidates"][0]["content"]["parts"][0]["text"]

                return parts[0]["text"]
        except Exception as e:
            return f"عذراً، خوادم Gemini مزدحمة حالياً أو حدث خطأ: {e}"
