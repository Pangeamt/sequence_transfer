from sequence_transfer.sequence import CharSequence, TokenSequence
from sequence_transfer.plugin.biluo_plugin import BILUOPlugin, BILUOAnnotationSequence
from sequence_transfer.magic_transfer import MagicTransfer
from bert.tokenization import FullTokenizer


text = " Mary Poppins"
s1 = CharSequence.new(text)

# We create the token sequence and their annotations
tokenizer = FullTokenizer('vocab.txt')
tokens = tokenizer.tokenize(text)
print(tokens)
s2 = TokenSequence.new(tokens)


s3 = BILUOAnnotationSequence.new([
    ['O', 'O'],
    ['B-PER', 'B-FIRST'],
    ['I-PER', 'I-FIRST'],
    ['I-PER', 'I-FIRST'],
    ['I-PER', 'L-FIRST'],
    ['I-PER', 'O'],
    ['I-PER', 'B-LAST'],
    ['I-PER', 'L-LAST'],
    ['I-PER', 'B-XXXX'],
    ['I-PER', 'I-XXXX'],
    ['I-PER', 'I-XXXX'],
    ['I-PER', 'I-XXXX'],
    ['L-PER', 'L-XXXX'],


])

# We create a magic transfer
transfer = MagicTransfer(s1, s2)

# We use the created transfer function to transfer our annotations
s4 = transfer.apply(s3, plugin=BILUOPlugin())




