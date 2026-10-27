"""الفئة الأساسية لأدوات BikAgent."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class BaseTool(ABC):
    """كل أداة يجب أن ترث من هذا الصنف وتنفذ `run`."""
    name: str = "base"
    description: str = ""

    @abstractmethod
    def run(self, **kwargs: Any) -> Any:
        raise NotImplementedError
