from typing import Union
from sequence_transfer.sequence_transfer import SequenceTransfer
from sequence_transfer.normalizer.remove_whitespace import remove_whitespace
from sequence_transfer.normalizer.to_lower import to_lower
from sequence_transfer.normalizer.remove_accents import remove_accents
from sequence_transfer.lcs_transfer import lcs_transfer
from sequence_transfer.token_to_text_transfer import token_to_text_transfer
from sequence_transfer.sequence import CharSequence, TokenSequence, TokenSequenceContext
from sequence_transfer.contextualized_sequence_transfer import ContextualizedTransfer


class MagicTransfer(ContextualizedTransfer):
    def __init__(self,
                 source: Union[CharSequence, TokenSequence],
                 target: Union[CharSequence, TokenSequence]):

        normalized_source, t1 = _normalize(source)
        normalized_target, t2 = _normalize(target)
        t2_inv = t2.invert()

        t3 = lcs_transfer(normalized_source, normalized_target)
        t4 = SequenceTransfer.compose(t1, t3, t2_inv)

        if isinstance(source.context, TokenSequenceContext) or \
                isinstance(target.context, TokenSequenceContext):
            compose = []
            if isinstance(source.context, TokenSequenceContext):
                compose.append(
                    token_to_text_transfer(source.context.context)
                )
            compose.append(t4)
            if isinstance(target.context, TokenSequenceContext):
                compose.append(
                    token_to_text_transfer(target.context.context).invert()
                )
            t4 = SequenceTransfer.compose(*compose)

        super().__init__(source, target, t4.matches)


def _normalize(sequence:  Union[CharSequence, TokenSequence]):
    text1 = sequence.text
    text2, t1 = remove_whitespace(text1)
    text3, t2 = to_lower(text2)
    text4, t3 = remove_accents(text3)
    t = SequenceTransfer.compose(t1, t2, t3)
    return text4, t





