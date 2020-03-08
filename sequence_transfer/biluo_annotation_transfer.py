from sequence_transfer.contextualized_sequence_transfer import ContextualizedTransfer
from sequence_transfer.sequence_transfer import SequenceTransfer
from sequence_transfer.sequence import BILUOAnnotationSequence
from sequence_transfer.sequence import BILUOAnnotation


B, I, L, I, O = BILUOAnnotation.CODES


class BILUOAnnotationTransfer:
    def __init__(self, transfer: ContextualizedTransfer):
        self._transfer = transfer

    def apply(self, sequence: BILUOAnnotationSequence, zip_target=False):

        for annotation in sequence:
            # Apply is passed to the base class that transfer simple sequence
            transferred = SequenceTransfer.apply(self._transfer, annotation)

            # Extract sequence
            a = self._transfer.source.context


class BILUOTransferException:
    def __init__(self):
        super().__init__("TransferException")


def transfer_biluo(x: str, nb_slot: int) -> str:
    if nb_slot == 0:
        raise BILUOTransferException()
    else:
        if x == I:
            return I*nb_slot
        if x == B:
            return B + I*(nb_slot - 1)
        elif x == L:
            return I*(nb_slot - 1) + L



