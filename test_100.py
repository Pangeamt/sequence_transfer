from sequence_transfer.sequence import CharSequence, TokenSequence
from sequence_transfer.magic_transfer import MagicTransfer
from sequence_transfer.plugin.entity_annotation_transfer_plugin import EntityAnnotationTransferPlugin, \
    EntityAnnotationSequence

text = CharSequence.new("  J'adore  Zoé!  ")  # Sequence of chars
bert_tokens = TokenSequence.new(['j', "'", 'ado', '##re', 'zo', '##e', '!'])  # Sequence of tokens
moses_tokens = TokenSequence.new(['J&apos;', 'adore', 'Zoé', '!'])   # Sequence of tokens
moses_detokenized = CharSequence.new("J'adore Zoé !")  # Sequence of chars

s = bert_tokens[4:6]  # We select the 5th and 6th BERT tokens
transfer1 = MagicTransfer(bert_tokens, text)  # We create a transfer function
transferred = transfer1.apply(s)
print(f"Transfered text: {transferred.text}")
print(f"Offsets: {transferred.start}, {transferred.stop}")
transfer2 = MagicTransfer(bert_tokens, moses_tokens)
transferred = transfer2.apply(s)
print(f"Offsets: {transferred.start}, {transferred.stop}")

annotations = EntityAnnotationSequence.new([
    "O",
    "O",
    "O",
    "O",
    "B-PER",
    "L-PER",
    "O",
], "biluo")

transferred_annotations = transfer1.apply(annotations, plugin=EntityAnnotationTransferPlugin())
print("xxxxxxxxx", transferred_annotations.convert("biluo"))

