import html
from typing import Tuple
from sequence_transfer.sequence import Sequence
from sequence_transfer.sequence_transfer import SequenceTransfer


def is_entity(text: str, index: int) -> bool:
    for i in range(index, index + 10):
        if i < len(text):
            if text[i] == ";":
                return True, i
            if text[i] == " ":
                break
    return False, -1


def remove_html_entities(text: str) -> Tuple[str, SequenceTransfer]:
    output = html.unescape(text)
    j = 0
    counter = 0
    transfers = []

    for i, char in enumerate(text):
        if counter:
            counter -= 1
        elif char == "&":
            is_html, fin = is_entity(text, i)
            if is_html:
                transfers.append((Sequence(i, fin + 1), Sequence(j)))
                j += 1
                counter = fin - i
        else:
            transfers.append((Sequence(i), Sequence(j)))
            j += 1

    transfer = SequenceTransfer(
        Sequence(0, len(text)),
        Sequence(0, len(output)),
        transfers
    )
    return output, transfer
