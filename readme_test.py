from bert.tokenization import FullTokenizer
from sacremoses import MosesTokenizer, MosesDetokenizer
from sequence_transfer.sequence import CharSequence, TokenSequence
from sequence_transfer.plugin.entity_annotation_transfer_plugin import EntityAnnotationTransferPlugin, \
    EntityAnnotationSequence
from sequence_transfer.magic_transfer import MagicTransfer


# We create a char sequence sequence
text = "  J'adore  Zoé!  "
char_sequence = CharSequence.new(text)

# We create the token sequence
tokenizer = FullTokenizer('vocab.txt')
tokens = tokenizer.tokenize(text)
print(tokens)

tokenizer = MosesTokenizer('fr')
tokens = tokenizer.tokenize(text)
print(tokens)

detokenizer = MosesDetokenizer('fr')
y = detokenizer.detokenize(tokens)

print(y)

exit()
token_sequence = TokenSequence.new(tokens)

# We create a magic transfer
transfer = MagicTransfer(char_sequence, token_sequence)

# We annotate our text
annotations = EntityAnnotationSequence.new([
    "O",
    "B-PER",
    "I-PER",
    "I-PER",
    "L-PER",
    "B-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "L-PER",
], "biluo")

# We use the created transfer function to transfer our annotations
transferred_annotations = transfer.apply(
    annotations,
    plugin=EntityAnnotationTransferPlugin()).convert("biluo")


for token, transferred_annotation in zip(tokens, transferred_annotations):
    print(f"{token}, {transferred_annotation}")
