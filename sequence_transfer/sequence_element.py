from collections import namedtuple


class Token:
    def __init__(self, text):
        self._text = text
        if " " in text:
            raise ValueError(f"The token with whitespace")

    def get_text(self):
        return self._text
    text = property(get_text)

    def __len__(self):
        return len(self._text)


class Char:
    def __init__(self, text):
        self._text = text

    def get_text(self):
        return self._text
    text = property(get_text)

    def __len__(self):
        return len(self._text)


class InvalidBILUOCodeException(Exception):
    def __init__(self, code):
        super().__init__(f"Invalid BILUO code {code}")


BILUOAnnotationAtom = namedtuple("BILUOAnnotationAtom", ["code", "tag"])


class BILUOAnnotation:
    B = "B"
    I = "I"
    L = "L"
    U = "U"
    O = "O"
    CODES = {B, I, L, U, O}

    def __init__(self, annotation: str, *args: str):
        self._annotations = []

        for annotation in (annotation, *args):
            if annotation == self.O:
                self._annotations.append(
                    BILUOAnnotationAtom(code=self.O, tag=""))
            else:
                code, tag = annotation.split('-')
                if code not in self.CODES:
                    raise InvalidBILUOCodeException(code)
                self._annotations.append(
                    BILUOAnnotationAtom(code=code, tag=tag))
