"""أداة الآلة الحاسبة."""
from typing import Any
from .base import BaseTool

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "أداة لإجراء العمليات الحسابية البسيطة (جمع، طرح، ضرب، قسمة)."

    def run(self, expression: str) -> Any:
        try:
            # تقييم آمن للتعبير الرياضي
            allowed_chars = set("0123456789+-*/(). ")
            if not set(expression).issubset(allowed_chars):
                return "خطأ: تعبير غير مسموح به."
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"خطأ في الحساب: {e}"
