import unittest
from sequence_transfer.sequence import Sequence
from sequence_transfer.normalizer.remove_whitespace import remove_whitespace


class TestNormalizer(unittest.TestCase):
    #  TODO test all normalizers
    def test_remove_whitespace(self):
        t1 = " te \n\r\txt "
        t2, transfer = remove_whitespace(t1)

        assert ' ' not in t2
        assert '\n' not in t2
        assert '\r' not in t2
        assert '\t' not in t2

        assert transfer.apply(Sequence(0)) == Sequence(0, 0)
        assert transfer.apply(Sequence(1)) == Sequence(0)
        assert transfer.apply(Sequence(2)) == Sequence(1)
        assert transfer.apply(Sequence(3)) == Sequence(2, 2)
        assert transfer.apply(Sequence(4)) == Sequence(2, 2)
        assert transfer.apply(Sequence(5)) == Sequence(2, 2)
        assert transfer.apply(Sequence(6)) == Sequence(2, 2)
        assert transfer.apply(Sequence(7)) == Sequence(2, 3)
        assert transfer.apply(Sequence(8)) == Sequence(3, 4)
        assert transfer.apply(Sequence(9)) == Sequence(4, 4)

