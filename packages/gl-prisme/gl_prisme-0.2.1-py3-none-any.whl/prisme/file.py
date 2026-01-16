from typing import Dict


class File:
    def __init__(
        self, name: str, content: bytes | None = None, path: str | None = None
    ):
        self.name = name
        if content is not None:
            self.content = content
        elif path is not None:
            with open(path, "rb") as f:
                self.content = f.read()

    @property
    def dict(self) -> Dict[str, str | bytes]:
        return {"Name": self.name, "Content": self.content}
