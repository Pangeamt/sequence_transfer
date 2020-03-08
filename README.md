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
If we want to see the full mapping:

```python
transfer.debug()
```

will print a table like this:

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

What we have done between tokens can be achieved between tokens and the text source. So it's possible to find the offsets of any text (in the source) corresonding to any sequence or subseqeunce of tokens. 


The MagicTransfer is one of the multiple transfers function available on the library. They are composable and reversible


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
