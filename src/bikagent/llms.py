"""محولات مزودي LLM."""
from __future__ import annotations
import os
import httpx

class LLMClient:
    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model
        self.api_key = os.getenv("GEMINI_API_KEY")

    def chat(self, prompt: str, registry: any) -> str:
        if not self.api_key:
            return "خطأ: مفتاح API غير موجود في ملف .env"

        # تجهيز هيكل الأدوات لـ Gemini
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
                response = client.post(url, headers=headers, json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                parts = data["candidates"][0]["content"]["parts"]
                
                # إذا طلب النموذج استخدام أداة
                if "functionCall" in parts[0]:
                    func_call = parts[0]["functionCall"]
                    tool_name = func_call["name"]
                    args = func_call["args"]
                    
                    # تنفيذ الأداة
                    result = registry.run(tool_name, **args)
                    
                    # إرسال النتيجة مرة أخرى للنموذج للحصول على الرد النهائي
                    payload["contents"].append({"role": "model", "parts": [{"functionCall": func_call}]})
                    payload["contents"].append({"role": "user", "parts": [{"functionResponse": {"name": tool_name, "response": {"result": result}}}]})
                    
                    response2 = client.post(url, headers=headers, json=payload, timeout=30.0)
                    response2.raise_for_status()
                    data2 = response2.json()
                    return data2["candidates"][0]["content"]["parts"][0]["text"]

                return parts[0]["text"]
        except Exception as e:
            return f"حدث خطأ في الاتصال: {e}"
