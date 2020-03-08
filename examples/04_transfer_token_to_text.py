from sequence_transfer.sequence import CharSequence, TokenSequence
from sequence_transfer.magic_transfer import MagicTransfer
from bert.tokenization import FullTokenizer


text = "She lives in Lindström, Minnesota"
tokenizer = FullTokenizer('../vocab.txt')
tokens = tokenizer.tokenize(text)

# 01 - We create sequences
s1 = CharSequence.new(text)
s2 = TokenSequence.new(tokens)

# 02 - We create a magic transfer that will try to match "similar" subsequences between s1 and s2:
transfer = MagicTransfer(s1, s2)

# 03 - We will use the transfer object to find the tokens that correspond to the word `Lindström`
sub1 = s1[13, 22]  # `Lindström` in s1
sub2 = transfer.apply(sub1)
for token in sub2:
    print(token.text)

# 04 - We can debug the transfer
transfer.debug()