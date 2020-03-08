import unittest
from sequence_transfer.sequence import CharSequence


class TestSequence(unittest.TestCase):
    def test_creation(self):
        s = CharSequence.new("Hello")
        assert s.start == 0
        assert s.stop == 5

    def test_iter(self):
        text = "Hi!"
        s1 = CharSequence.new(text)
        for i, s in enumerate(s1):
            assert type(s) == CharSequence
            assert s.text == text[i]

