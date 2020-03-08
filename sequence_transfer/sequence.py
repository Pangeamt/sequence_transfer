from typing import List, Optional, Union, Any
from colorama import Fore, Style
from sequence_transfer.sequence_element import Token, Char, BILUOAnnotation


#  Exceptions


class InvalidSequenceException(Exception):
    def __init__(self, start, stop):
        super().__init__(f"Invalid sequence_transfer Stop < start: [{start} {stop}[")


class SequenceNotInException(Exception):
    def __init__(self, sequence1: "Sequence", sequence2: "Sequence"):
        super().__init__(f"Sequence {sequence1} not in {sequence2}")


class EmptySequenceException(Exception):
    def __init__(self, sequence: "Sequence"):
        super().__init__(f"Sequence {sequence} is empty")


class NotContextualizedSequenceException(Exception):
    def __init__(self, sequence: "Sequence"):
        super().__init__(f"Sequence {sequence} has no context")


# Sequence. The queen...


class Sequence:
    def __init__(self, start: int, stop: Optional[int] = None, context: "SequenceContext" = None):
        """
        A  sequence is a discrete interval, with the particularity of being closed on the left and open on the right.

        Let 's suppose a sequence of consecutive numbers: 3 4 5 6 7 8 9 10 11
        Sequence(4,7) =  4 5 6 = [4 7[ ... An sequence_transfer is open on the right so 7 is excluded!
        Sequence(9) = 9 = [9 10[  ... It's a shortcut for Sequence(9,10)
        Sequence(4,4) = nothing = [4 4[ ... it's empty but positioned!

        :param start: Where the sequence start
        :param stop: Where the sequence stop (not included)
        :param context: The materialization of the sequence: A sequence of concrete things like chars, tokens
                Important: A subsequence of a sequence share his context
        """
        if stop is None:
            stop = start + 1
        if stop < start:
            raise InvalidSequenceException(start, stop)
        self._start = start
        self._stop = stop
        self._size = stop - start
        self._context = context

    def get_start(self):
        return self._start
    start = property(get_start)

    def get_stop(self):
        return self._stop
    stop = property(get_stop)

    def get_size(self):
        return self._size
    size = property(get_size)

    def is_subsequence(self, sequence):
        return sequence.start <= self._start and self._stop <= sequence.stop

    def raise_if_not_in(self, sequence):
        if not self.is_subsequence(sequence):
            raise SequenceNotInException(self, sequence)

    def is_empty(self):
        return self._size == 0

    def raise_if_empty(self):
        if self.is_empty():
            raise EmptySequenceException(self)

    def raise_if_not_contextualized(self):
        if self._context is None:
            raise NotContextualizedSequenceException(self)

    def split(self, n: Optional[int] = None) -> List["Sequence"]:
        """
        split the sequence in n sequences of "similar" size. If n == None -> n = self.size
        :param n:
        :return:
        """
        if n is None:
            n = self._size

        sizes = [self._size // n]*n
        for i in range(self._size % n):
            sizes[i] += 1

        sequences = []
        for i, size in enumerate(sizes):
            if i == 0:
                start = self._start
            else:
                start = sequences[-1].stop
            stop = start + size
            sequences.append(Sequence(start, stop))
        return sequences

    @staticmethod
    def expand(sequence1: "Sequence", sequence2: "Sequence") -> "Sequence":
        """
        [2 5[ 5 6 [7 9[  ->  0 1 [2 9[ 9
        :param sequence1:
        :param sequence2:
        :return:
        """
        if sequence1.start <= sequence2.stop:
            return Sequence(sequence1.start, sequence2.stop)
        else:
            return Sequence(sequence2.stop, sequence1.start)

    @staticmethod
    def between(sequence1: "Sequence", sequence2: "Sequence") -> "Sequence":
        return Sequence(sequence1.stop, sequence2.start)

    def iter_index(self):
        return iter(range(self.start, self.stop))

    def __iter__(self):
        sequence_type = type(self)
        return iter([sequence_type(i, context=self._context) for i in self.iter_index()])

    def __len__(self):
        return self._size

    def __getitem__(self, key):
        sequence_type = type(self)
        if type(key) is int:
            new_start = self._start + key
            sequence = sequence_type(new_start, context=self._context)
            if not sequence.is_subsequence(self):
                raise KeyError()
            return sequence

        elif type(key) is tuple:
            return self._get_item(key[0], key[1])
        elif type(key) is slice:
            return self._get_item(key.start, key.stop)

    def _get_item(self, start, stop):
        if start is None:
            start = self._start
        elif start < 0:
            start = self._stop + start
        else:
            start = self._start + start

        if stop is None:
            stop = self._stop
        elif stop < 0:
            stop = self._stop + stop
        else:
            stop = self._start + stop

        sequence_type = type(self)
        sequence = sequence_type(start, stop, context=self._context)
        if not sequence.is_subsequence(self):
            raise KeyError()
        return sequence

    def __setitem__(self, key, value):
        raise ValueError("sequence item changes are not allowed")

    def __eq__(self, other):
        if self._start != other.start or self._stop != other.stop:
            return False
        return True

    def __repr__(self):
        return self.slice_representation()

    def slice_representation(self):
        return f"[{self.start}:{self.stop}]"

    def get_context(self):
        return self._context

    def set_context(self, context: Union[str, List["Token"]]):
        self._context = context

    context = property(get_context, set_context)


#  Base contexts


class SequenceContext:
    def __init__(self, context: List[Any]):
        self._context = context

    def get_context(self):
        return self._context
    context = property(get_context)


class TextualSequenceContext(SequenceContext):
    def get_sequence_text(self, sequence) -> str:
        return ''


# Others  contexts


class CharSequenceContext(TextualSequenceContext):
    def __init__(self, context: List[Char]):
        super().__init__(context)

    def get_sequence_text(self, sequence: Sequence):
        elements_as_text = map(lambda x: x.text, self._context[sequence.start: sequence.stop])
        return "".join(elements_as_text)

    def represent_sequence(self, sequence: Sequence) -> str:
        return self.get_sequence_text(sequence)

    def represent_sequence_in_context(self, sequence: Sequence) -> str:
        print(f"representing {sequence} in {self}")
        return "".join([
                self.represent_sequence(Sequence(0, sequence.start)),
                Fore.CYAN + self.represent_sequence(sequence) + Style.RESET_ALL,
                self.represent_sequence(Sequence(sequence.stop, len(self._context))),
            ])


class TokenSequenceContext(TextualSequenceContext):
    def __init__(self, context: List[Token]):
        super().__init__(context)

    def get_sequence_text(self, sequence):
        elements_as_text = map(lambda x: x.text, self._context[sequence.start: sequence.stop])
        return " ".join(elements_as_text)

    def represent_sequence(self, sequence: Sequence) -> str:
        return self.get_sequence_text(sequence)

    def represent_sequence_in_context(self, sequence: Sequence) -> str:
        return " ".join([
                self.represent_sequence(Sequence(0, sequence.start)),
                Fore.CYAN + self.represent_sequence(sequence) + Style.RESET_ALL,
                self.represent_sequence(Sequence(sequence.stop, len(self._context))),
            ])


class BILUOAnnotationSequenceContext(SequenceContext):
    def __init__(self, context: List[BILUOAnnotation]):
        super().__init__(context)


# Special Sequences


class TextualSequence(Sequence):
    def in_context(self):
        return self._context.represent_sequence_in_context(self)

    def get_text(self):
        return self._context.get_sequence_text(self)
    text = property(get_text)


class TokenSequence(TextualSequence):
    @staticmethod
    def new(tokens: List[str]):
        if type(tokens) is not list:
            raise ValueError(f"TokenSequence expect a list of string")
        return TokenSequence(0, len(tokens), TokenSequenceContext(list(map(lambda token: Token(token), tokens))))


class CharSequence(TextualSequence):
    @staticmethod
    def new(text: str):
        if type(text) is not str:
            raise ValueError(f"CharSequence expect a string")
        return CharSequence(0, len(text), CharSequenceContext(list(map(lambda char: Char(char), text))))


class BILUOAnnotationSequence(Sequence):
    @staticmethod
    def new(annotations: List[BILUOAnnotation]) -> Sequence:
        if type(annotations) is not list:
            raise ValueError(f"BILUOAnnotationSequence expect a list")
        return BILUOAnnotationSequence(0, len(annotations), BILUOAnnotationSequenceContext(annotations))

