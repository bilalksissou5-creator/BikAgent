"""سجل ديناميكي للأدوات."""
from __future__ import annotations
from typing import Any
from .base import BaseTool

class ToolRegistry:
    """يحتفظ بالأدوات المسجلة ويسمح بإضافتها ديناميكيًا."""
    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        if not tool.name or tool.name == "base":
            raise ValueError("يجب أن يكون للأداة اسم فريد.")
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def list(self) -> list[str]:
        return sorted(self._tools)

    def run(self, name: str, **kwargs: Any) -> Any:
        tool = self.get(name)
        if tool is None:
            raise KeyError(f"الأداة غير مسجلة: {name}")
        return tool.run(**kwargs)
