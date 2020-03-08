from bert.tokenization import FullTokenizer
from sacremoses import MosesTokenizer
from sequence_transfer.sequence import TokenSequence
from sequence_transfer.magic_transfer import MagicTransfer

# 01 - Create tokenizer
moses_tokenizer = MosesTokenizer('en')
bert_tokenizer = FullTokenizer('../vocab.txt')


# 02 - Create tokens
text = "She lives in Lindström, Minnesota"
moses_tokens = moses_tokenizer.tokenize(text)
bert_tokens = bert_tokenizer.tokenize(text)


# 03 - Create sequences
s1 = TokenSequence.new(moses_tokens)
s2 = TokenSequence.new(bert_tokens)

# 04 - Create transfer
transfer = MagicTransfer(s1, s2)


# 05 - We will use the transfer object to find the bert tokens that correspond to the third moses token (`Lindström`)
sub1 = s1[3]  # `Lindström`
sub2 = transfer.apply(sub1)
for token in sub2:
    print(token.text)

# 04 - We can debug the transfer
transfer.debug()