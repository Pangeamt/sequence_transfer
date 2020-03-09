from sequence_transfer.sequence import CharSequence, TokenSequence, BILUOAnnotationSequence
from sequence_transfer.sequence_element import BILUOAnnotation
from sequence_transfer.magic_transfer import MagicTransfer
from sequence_transfer.biluo_annotation_transfer import BILUOAnnotationTransfer
from bert.tokenization import FullTokenizer


text = "She lives in Lindström, Minnesota"
tokenizer = FullTokenizer('vocab.txt')
tokens = tokenizer.tokenize(text)

# We create sequences
s1 = TokenSequence.new(tokens)
s2 = CharSequence.new(text)

# We create a sequence of annotations
annotation_sequence = BILUOAnnotationSequence.new([
    ('O', 'O'),
    ('O', 'O'),
    ('O', 'O'),
    ('O', 'O'),
    ('B-LOC', 'B-CITY'),
    ('I-LOC', 'I-CITY'),
    ('I-LOC', 'L-CITY'),
    ('I-LOC', 'O'),
    ('I-LOC', 'B-REGION'),
    ('I-LOC', 'I-REGION'),
    ('I-LOC', 'L-REGION')
])

# We create a magic transfer
transfer = MagicTransfer(s1, s2)

# And create an BILUOAnnotationTransfer
biluo_annotation_transfer = BILUOAnnotationTransfer(transfer)
transferred = biluo_annotation_transfer.apply(annotation_sequence)




