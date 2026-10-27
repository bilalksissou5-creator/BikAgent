"""واجهات الذاكرة للوكيل."""
from __future__ import annotations
from typing import Any

class DictMemory:
    """ذاكرة مؤقتة داخل الجلسة."""
    def __init__(self) -> None:
        self._items: list[dict[str, Any]] = []
    def add(self, item: dict[str, Any]) -> None:
        self._items.append(item)
    def all(self) -> list[dict[str, Any]]:
        return list(self._items)
