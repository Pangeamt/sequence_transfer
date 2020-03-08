# Sequence transfer

The sequence transfer library is part of the MAPA anonymisation project funded by the European Commission.

Right to the code:
```python
# a simple sentence
text = '  I live in  Lindström ! '  

# Tokens produced by Moses and BERT
moses_tokens = ['I', 'live', 'in', 'Lindström', '!'] # Tokenized with Moses
bert_tokens = ['i', 'live', 'in', 'li', '##nds', '##tro', '##m', '!']  # Tokenized with BERT

# Now, if we want to map Moses and BERT tokens 
transfer = MagicTransfer(moses_tokens, bert_tokens)
transfer.debug()

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
