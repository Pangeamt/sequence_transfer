from sequence_transfer.sequence import CharSequence
from sequence_transfer.magic_transfer import MagicTransfer
from bert.tokenization import FullTokenizer


text = "She lives in Lindström, Minnesota"

tokenizer = FullTokenizer('../vocab.txt')
tokens = tokenizer.tokenize(text)
tokenized = " ".join(tokens)

# 01 - We create sequences
s1 = CharSequence.new(text)
s2 = CharSequence.new(tokenized)

# 02 - We create a magic transfer that will try to match "similar" subsequences between s1 and s2:
transfer = MagicTransfer(s1, s2)

# 03 - We will use the transfer object to find the chars in s2 that corresponds to the word `Lindström` in s1
sub1 = s1[13, 22]  # `Lindström` in s1
sub2 = transfer.apply(sub1)
print(sub2.text)  # `li ##nds ##tro ##m` in s2

# 04 - We can debug the transfer
transfer.debug()
