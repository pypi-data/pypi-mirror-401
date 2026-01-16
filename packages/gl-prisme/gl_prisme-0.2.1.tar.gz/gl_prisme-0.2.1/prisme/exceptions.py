from typing import Any


class PrismeException(Exception):
    def __init__(self, code: int | str, text: str, context: Any):
        super().__init__()
        self.code = int(code)
        self.text = text
        self.context = context

    def __str__(self) -> str:
        return f"Error in response from Prisme. Code: {self.code}, Text: {self.text}"
