from sequence_transfer.sequence import CharSequence, TokenSequence
from sequence_transfer.plugin.biluo_plugin import BILUOPlugin, BILUOAnnotationSequence
from sequence_transfer.magic_transfer import MagicTransfer
from bert.tokenization import FullTokenizer


text = "  She lives in Lindström, Minnesota  "
s1 = CharSequence.new(text)

# We create the token sequence and their annotations
tokenizer = FullTokenizer('vocab.txt')
tokens = tokenizer.tokenize(text)
s2 = TokenSequence.new(tokens)


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
transfer = MagicTransfer(s2, s1)

# We use the created transfer function to transfer our annotations
s4 = transfer.apply(s3, plugin=BILUOPlugin())




