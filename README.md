# Sequence transfer

The sequence transfer library is part of the MAPA anonymisation project funded by the European Commission.

## Introduction

```python
# A simple sentence
text = '  I live in  Lindström ! '  

# We create TokenSeqence from tokens produced by Moses and BERT
moses_tokens = TokenSeqence.new(['I', 'live', 'in', 'Lindström', '!']) 
bert_tokens = TokenSeqence.new((['i', 'live', 'in', 'li', '##nds', '##tro', '##m', '!'])

# We create a transfer function
transfer = MagicTransfer(moses_tokens, bert_tokens)

# Now we can find the BERT tokens that correspond to the 4th Moses token 'Lindström' 
transfered = transfer.apply(moses_tokens[3])
print(transfered)
# --->  ['li', '##nds', '##tro', '##m']

# We can print the offsets of the transfered sequence
print(f"Starts at: {transfered.start} and stops before: {transferred.stop}"
# --->  "Starts at: 3 and stops before: 7
```
To see the full mapping:

```python
# Print the table below
transfer.debug()
```

| src slice | src index |  src text |      | tgt text | tgt index | tgt slice |
| ----------| --------- | --------- | ---- | -------- | ----------| ----------|
|   [0:1]   |     0     |     I     | ---> |    i     |     0     |   [0:1]   |
|   [1:2]   |     1     |    live   | ---> |   live   |     1     |   [1:2]   |
|   [2:3]   |     2     |     in    | ---> |    in    |     2     |   [2:3]   |
|   [3:4]   |     3     | Lindström | ---> |    li    |     3     |   [3:7]   |
|           |           |           |      |  ##nds   |     4     |           |
|           |           |           |      |  ##tro   |     5     |           |
|           |           |           |      |   ##m    |     6     |           |
|   [4:5]   |     4     |     !     | ---> |    !     |     7     |   [7:8]   |



## The sequence transfer library

What we have done between tokens can be achieved between tokens and the text source itself and it is possible to find, in the source the offsets of the text corresponding to any sequence or subsequence of tokens.

We are working on a multilevel BILUO annotation transfer function that will be able to transfer BILUO codes from tokens to the appropriate letters of the source. That means that we will be able to annotate a text, letter by letter, without altering it at all (even a space).

The MagicTransfer is one of the multiple transfer functions available on the library. They are composable and reversible.
The "Magic" transfer is still in BETA and have to be tested. Nevertheless, because of his architecture we think that it should be quite strong very soon.

### The magic transfer architecture
The Magic transfer is based on a supervised renormalization of both text, source and tokenized. Supervised means that each renormalization function return a transfer function that track the changes they made.

After the renormalization process, both texts tend to be very similar so we use what git use to detect changes in code: the LCS algorithm and detect the most longest common subsequence of these two texts and convert that result to another transfer function.

Then it is mathematics:
- if f1, f2, .., fn are the transfer functions for the normalization of the source
- if g1, g2, .., gn are  the transfer functions for the renormalization of the tokenized text
- if h is the LSC transfer
- Then MagicTransfer = Compose(Compose(f1, f2, ...fn), h , Inverse(Compose(g1, g2, ..., gn)))

At this moment, the MagicTransfer function use only 4 normalizers but we will add more in a near future.



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
