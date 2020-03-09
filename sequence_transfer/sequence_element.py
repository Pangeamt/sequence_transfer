from collections import namedtuple
from typing import List

class Token:
    def __init__(self, text: str):
        self._text = text
        if " " in text:
            raise ValueError(f"The token with whitespace")

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

    @staticmethod
    def new(annotation: str, *args: str):
        atoms = []
        for annotation in (annotation, *args):
            if annotation == BILUOAnnotation.O:
                atoms.append(
                    BILUOAnnotationAtom(code=BILUOAnnotation.O, tag=""))
            else:
                code, tag = annotation.split('-')
                if code not in BILUOAnnotation.CODES:
                    raise InvalidBILUOCodeException(code)
                atoms.append(
                    BILUOAnnotationAtom(code=code, tag=tag))
        return BILUOAnnotation(*atoms)

    # def __init__(self, annotation: str, *args: str):
    #     self._atoms = []
    #
    #     for annotation in (annotation, *args):
    #         if annotation == self.O:
    #             self._atoms.append(
    #                 BILUOAnnotationAtom(code=self.O, tag=""))
    #         else:
    #             code, tag = annotation.split('-')
    #             if code not in self.CODES:
    #                 raise InvalidBILUOCodeException(code)
    #             self._atoms.append(
    #                 BILUOAnnotationAtom(code=code, tag=tag))

    def __init__(self, atom: BILUOAnnotationAtom, *args: BILUOAnnotationAtom):
        self._atoms = [atom, *args]

        # for annotation in (annotation, *args):
        #     if annotation == self.O:
        #         self._atoms.append(
        #             BILUOAnnotationAtom(code=self.O, tag=""))
        #     else:
        #         code, tag = annotation.split('-')
        #         if code not in self.CODES:
        #             raise InvalidBILUOCodeException(code)
        #         self._atoms.append(
        #             BILUOAnnotationAtom(code=code, tag=tag))


    def get_atoms(self) -> List[BILUOAnnotationAtom]:
        return self._atoms
    atoms = property(get_atoms)

