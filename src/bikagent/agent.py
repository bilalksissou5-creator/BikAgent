"""الحلقة الأساسية للوكيل."""
from __future__ import annotations
from typing import Any
from .config import load_config
from .llms import LLMClient
from .tools.registry import ToolRegistry
from .tools.calculator import CalculatorTool

class BikAgent:
    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or load_config()
        self.memory: list[dict[str, Any]] = []
        
        # تسجيل الأدوات
        self.registry = ToolRegistry()
        self.registry.register(CalculatorTool())

        llm_config = self.config.get("llm", {})
        self.llm = LLMClient(
            provider=llm_config.get("provider", "gemini"),
            model=llm_config.get("model", "gemini-3.5-flash")
        )

    def run(self, prompt: str) -> str:
        self.memory.append({"role": "user", "content": prompt})
        response = self.llm.chat(prompt, self.registry)
        self.memory.append({"role": "assistant", "content": response})
        return response

if __name__ == "__main__":
    agent = BikAgent()
    print("🤖 تم تشغيل BikAgent بنجاح (اكتب 'خروج' للإنهاء)")
    while True:
        try:
            user_input = input("\nأنت: ")
            if user_input.lower() in ["exit", "quit", "خروج"]:
                break
            print(f"BikAgent: {agent.run(user_input)}")
        except KeyboardInterrupt:
            break
