import html
from typing import Tuple
from sequence_transfer.sequence import Sequence
from sequence_transfer.sequence_transfer import SequenceTransfer


def is_entity(text: str, index: int) -> bool:
    for i in range(index, index + 10):
        if i < len(text):
            if text[i] == ";":
                return True, i + 1
            if text[i] == " ":
                break
    return False, -1


def remove_html_entities(text: str) -> Tuple[str, SequenceTransfer]:
    output = html.unescape(text)

    i = 0
    j = 0
    transfers = []
    while i < len(text):
        char = text[i]
        if char == "&":
            is_html, fin = is_entity(text, i)
            if is_html:
                transfers.append((Sequence(i, fin), Sequence(j)))
                i = fin
                j += 1
        else:
            transfers.append((Sequence(i), Sequence(j)))
            i += 1
            j += 1

    transfer = SequenceTransfer(
        Sequence(0, len(text)),
        Sequence(0, len(output)),
        transfers
    )
    # print(transfer.debug_in_text(text, output))
    return output, transfer
