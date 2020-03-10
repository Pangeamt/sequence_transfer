from sequence_transfer.sequence import CharSequence, TokenSequence
from sequence_transfer.plugin.biluo_plugin import BILUOPlugin, BILUOAnnotationSequence
from sequence_transfer.magic_transfer import MagicTransfer
from bert.tokenization import FullTokenizer


text = "  She lives in Lindström, Minnesota  "
tokenizer = FullTokenizer('vocab.txt')
tokens = tokenizer.tokenize(text)

# We create sequences
s1 = TokenSequence.new(tokens)
s2 = CharSequence.new(text)

# We create a sequence of annotations
s3 = BILUOAnnotationSequence.new([
    ['O', 'O'],
    ['O', 'O'],
    ['O', 'O'],
    ['O', 'O'],
    ['B-LOC', 'B-CITY'],
    ['I-LOC', 'I-CITY'],
    ['I-LOC', 'L-CITY'],
    ['I-LOC', 'O'],
    ['I-LOC', 'B-REGION'],
    ['I-LOC', 'I-REGION'],
    ['L-LOC', 'L-REGION']
])

# We create a magic transfer
transfer = MagicTransfer(s1, s2)
s4 = transfer.apply(s3, plugin=BILUOPlugin())




