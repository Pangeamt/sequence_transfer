# Sequence transfer

The sequence transfer library is part of the MAPA anonymisation project funded by the European Commission.

```python
# A simple sentence
text = '  I live in  Lindström ! '  

# We create TokenSeqence from tokens produced by Moses and BERT
moses_tokens = TokenSeqence.new(['I', 'live', 'in', 'Lindström', '!']) 
bert_tokens = TokenSeqence.new((['i', 'live', 'in', 'li', '##nds', '##tro', '##m', '!'])

# We create a transfer function and we can find the BERT tokens that correspond to the 4th Moses token 'Lindström' 
transfer = MagicTransfer(moses_tokens, bert_tokens)
print(transfer.apply(moses_tokens[3]))
# -->  ['li', '##nds', '##tro', '##m']
```

if we want to see all the transfers together:
```python
transfer.debug()
```
+-----------+-----------+-----------+------+----------+-----------+-----------+
| SRC SLICE | INDEX SRC |  TEXT SRC |      | TEXT TGT | INDEX TGT | TGT SLICE |
+-----------+-----------+-----------+------+----------+-----------+-----------+
|   [0:1]   |     0     |     I     | ---> |    i     |     0     |   [0:1]   |
|   [1:2]   |     1     |    live   | ---> |   live   |     1     |   [1:2]   |
|   [2:3]   |     2     |     in    | ---> |    in    |     2     |   [2:3]   |
|   [3:4]   |     3     | Lindström | ---> |    li    |     3     |   [3:7]   |
|           |           |           |      |  ##nds   |     4     |           |
|           |           |           |      |  ##tro   |     5     |           |
|           |           |           |      |   ##m    |     6     |           |
|   [4:5]   |     4     |     !     | ---> |    !     |     7     |   [7:8]   |
+-----------+-----------+-----------+------+----------+-----------+-----------+
``` 
 
## Requirements
python 3.7

## Test the library
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
