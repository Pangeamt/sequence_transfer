class Token:
    def __init__(self, text: str):
        self._text = text
        if " " in text:
            raise ValueError(f"token with whitespace `{text}`")

    def get_text(self) -> str:
        return self._text
    text = property(get_text)

    def __len__(self) -> int:
        return len(self._text)


class Char:
    def __init__(self, text: str):
        self._text = text

    def get_text(self) -> str:
        return self._text
    text = property(get_text)

    def __len__(self) -> int:
        return len(self._text)

