"""الحلقة الأساسية للوكيل."""
from __future__ import annotations
from typing import Any
from .config import load_config

class BikAgent:
    """وكيل قابل للتوسع."""
    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or load_config()
        self.tools: dict[str, Any] = {}
        self.memory: list[dict[str, Any]] = []

    def register_tool(self, name: str, func: Any) -> None:
        self.tools[name] = func

    def run(self, prompt: str) -> str:
        self.memory.append({"role": "user", "content": prompt})
        response = f"[BikAgent] تم استلام طلبك: {prompt}"
        self.memory.append({"role": "assistant", "content": response})
        return response

if __name__ == "__main__":
    agent = BikAgent()
    print(agent.run("مرحبًا، هذا اختبار أولي."))
