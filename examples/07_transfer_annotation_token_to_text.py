from bert.tokenization import FullTokenizer
from sequence_transfer.sequence import CharSequence, TokenSequence
from sequence_transfer.entity_annotation_transfer import EntityAnnotationSequence, EntityAnnotationTransfer
from sequence_transfer.magic_transfer import MagicTransfer


# We create a char sequence sequence
text = "She lives in Lindström, Minnesota"
char_sequence = CharSequence.new(text)

# We create the token sequence
tokenizer = FullTokenizer('../vocab.txt')
tokens = tokenizer.tokenize(text)
token_sequence = TokenSequence.new(tokens)

# We create a magic transfer
transfer = MagicTransfer(token_sequence, char_sequence)

# We create an annotation transfer
entity_annotation_transfer = EntityAnnotationTransfer(transfer)

annotations = EntityAnnotationSequence.new([
    'O',
    'O',
    'O',
    'B-LOC',
    'I-LOC',
    'I-LOC',
    'L-LOC',
    'O',
    'B-LOC',
    'I-LOC',
    'L-LOC',
], "biluo")

# We use the created transfer function to transfer our annotations
transferred_annotations = entity_annotation_transfer.apply(annotations).convert("biluo")

for char, transferred_annotation in zip(text, transferred_annotations):
    print(f"{char} --> {transferred_annotation}")
