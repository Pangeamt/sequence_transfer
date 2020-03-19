# Sequence Transfer

The sequence transfer library is part of the MAPA anonymisation project, funded by the European Commission.
The main goal of the library is to make easy, the transfer of annotations between different representations of a text produced by tokenization. 


## Sequences & transfers 
Transfering annotations between BERT and Moses tokens or between BERT tokens and the text source, requires a kind of "mapping". Thoses "mappings", in the Sequence Transfer library, are called transfers.

A transfer operate over sequences, sequences of chars or sequences of tokens. But let's start with an example:


First We create some sequences:

```python
from sequence_transfer.sequence import CharSequence, TokenSequence
from sequence_transfer.magic_transfer import MagicTransfer

text = CharSequence.new("  J'adore  Zoé!  ")  # Sequence of chars
bert_tokens = TokenSequence.new(['j', "'", 'ado', '##re', 'zo', '##e', '!'])  # Sequence of tokens
moses_tokens = TokenSequence.new(['J&apos;', 'adore', 'Zoé', '!'])   # Sequence of tokens
moses_detokenized = CharSequence.new("J'adore Zoé !")  # Sequence of chars

```

Now we can create a transfer function between any pair of sequences. For example, let's suppose we want to know what are the "images" of the  5th and 6th BERT tokens 'zo' and '##e' in the source text:

```python
s = bert_tokens[4:6]  # We select the 5th and 6th BERT tokens
transfer1 = MagicTransfer(bert_tokens, text)  # We create a transfer function
transferred = transfer1.apply(s)
print(f"text: {transferred.text}")
print(f"Offsets: {transferred.start}, {transferred.stop}")
```

What we did between BERT tokens and the source text can be achieved between any pair of sequences. For example between BERT tokens and Moses Tokens:

```python
transfer2 = MagicTransfer(bert_tokens, moses_tokens) 
transferred = transfer2.apply(s)
print(f"Offsets: {transferred.start}, {transferred.stop}")
```

It's possible to print the mapping:

```python
transfer2.debug()
```

```
|Src slice|Index src|Text src|    |Text tgt|Index tgt|Tgt slice|
|:-------:|:-------:|:------:|:--:|:------:|:-------:|:-------:|
|  [0:2]  |    0    |   j    |--->|J&apos; |    0    |  [0:1]  |
|         |    1    |   '    |    |        |         |         |
|         |         |        |    |        |         |         |
|  [2:4]  |    2    |  ado   |--->| adore  |    1    |  [1:2]  |
|         |    3    |  ##re  |    |        |         |         |
|         |         |        |    |        |         |         |
|  [4:6]  |    4    |   zo   |--->|  Zoé   |    2    |  [2:3]  |
|         |    5    |  ##e   |    |        |         |         |
|         |         |        |    |        |         |         |
|  [6:7]  |    6    |   !    |--->|   !    |    3    |  [3:4]  |
```


## The sequence transfer library

What we have done between tokens can be achieved between tokens and the text source itself and it is possible to find, in the source the offsets of the text corresponding to any sequence or subsequence of tokens.

We are working on a multilevel BILUO annotation transfer function that will be able to transfer BILUO codes from tokens to the appropriate letters of the source. That means that we will be able to annotate a text, letter by letter, without altering it at all (even a space).

The MagicTransfer is one of the multiple transfer functions available on the library. They are composable and reversible.
The "Magic" transfer is still in BETA and have to be tested. Nevertheless, because of his architecture we think that it should be quite strong very soon.

### The magic transfer architecture
The Magic transfer is based on a supervised renormalization of both texts, source and tokenized. Supervised means that each renormalization function return a transfer function that track the changes they made.

After the renormalization process, both texts tend to be very similar so we use what git use to detect changes in code: the LCS algorithm and detect the most longest common subsequence of these two texts and convert that result to another transfer function.

Then it is mathematics:
- if f1, f2, .., fn are the transfer functions for the normalization of the source
- if g1, g2, .., gn are  the transfer functions for the renormalization of the tokenized text
- if h is the LCS transfer
- Then MagicTransfer = Compose(Compose(f1, f2, ...fn), h , Inverse(Compose(g1, g2, ..., gn)))

At this moment, the MagicTransfer function use only 4 normalizers but we will add more in a near future.

Note for developers: The transfer functions are not letter to letter functions but slice to slice functions. Just observe, in the debug table, that the slice [3:4] is transferred to the slice [3:7]. Slices are sequences and "sequence" is the term used in the source code of the library. My preferred notation for a slice or a sequence is [n p[ reflecting the antisymmetry between the status of both numbers. [n n[ starts with n, but ends before n. It is empty, but positioned!

## Installation

### Requirements
python 3.7

### Test the library
Clone the repository from Github
```BASH
git clone https://github.com/Pangeamt/sequence_transfer.git test_sequence_transfer
cd test_sequence_transfer
```

Create a virtualenv

```BASH
virtualenv -p python3.7 venv
source venv/bin/activate
```

Install requirements
```BASH
pip install -r requirements.txt
```

Install sequence_transfer
```BASH
python setup.py install
```
