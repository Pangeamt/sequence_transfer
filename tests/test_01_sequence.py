import unittest
from sequence_transfer.sequence import Sequence, CharSequence, TokenSequence
from sequence_transfer.sequence import InvalidSequenceException


class TestSequence(unittest.TestCase):
    def test_creation(self):
        s = Sequence(1, 2)
        assert s.start == 1
        assert s.stop == 2

        with self.assertRaises(InvalidSequenceException):
            s = Sequence(2, 1)

        s = Sequence(1, 1)
        assert s.start == 1
        assert s.stop == 1

    def test_basics(self):
        s1 = Sequence(5, 10)
        assert s1.size == 5
        assert len(s1) == 5

        s1 = Sequence(1, 1)
        assert s1.size == 0

        s1 = Sequence(1, 4)
        for i, s2 in enumerate(s1):
            assert s2.start == s1.start + i
            assert s2.stop == s2.start + 1

        s1 = Sequence(1, 4)
        s2 = Sequence(1, 4)
        assert s1 == s2

    def test_iter(self):
        s1 = Sequence(5, 8)
        for s in s1:
            assert s == Sequence(s.start, s.start + 1)

    def test_subsequence(self):
        s1 = Sequence(1, 4)

        s2 = s1[0]
        assert s2.start == 1
        assert s2.stop == 2

        s2 = s1[1]
        assert s2.start == 2
        assert s2.stop == 3

        s2 = s1[2]
        assert s2.start == 3
        assert s2.stop == 4

        with self.assertRaises(KeyError):
            s2 = s1[-1]

        with self.assertRaises(KeyError):
            s2 = s1[3]

        s2 = s1[0:1]
        assert s2.start == 1
        assert s2.stop == 2

        s2 = s1[1:2]
        assert s2.start == 2
        assert s2.stop == 3

        s2 = s1[2:3]
        assert s2.start == 3
        assert s2.stop == 4

        s2 = s1[0:3]
        assert s2.start == 1
        assert s2.stop == 4

        s2 = s1[-1:3]
        assert s2.start == 3
        assert s2.stop == 4

        s2 = s1[:-1]
        assert s2.start == 1
        assert s2.stop == 3



