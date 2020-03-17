from bert.tokenization import FullTokenizer
from sequence_transfer.sequence import CharSequence, TokenSequence
from sequence_transfer.entity_annotation_transfer import EntityAnnotationSequence, EntityAnnotationTransfer
from sequence_transfer.magic_transfer import MagicTransfer


# We create a char sequence sequence
text = " Mary Poppins"
char_sequence = CharSequence.new(text)

# We create the token sequence
tokenizer = FullTokenizer('../vocab.txt')
tokens = tokenizer.tokenize(text)
token_sequence = TokenSequence.new(tokens)

# We create a magic transfer
transfer = MagicTransfer(char_sequence, token_sequence)

# We create an annotation transfer
entity_annotation_transfer = EntityAnnotationTransfer(transfer)

annotations = EntityAnnotationSequence.new([
    "O",
    "B-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "L-PER",
], "biluo")

# We use the created transfer function to transfer our annotations

transferred_annotations = entity_annotation_transfer.apply(annotations).convert("biluo")

for token, transferred_annotation in zip(tokens, transferred_annotations):
    print(f"{token}, {transferred_annotation}")
