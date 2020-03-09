from itertools import product
from sequence_transfer.contextualized_sequence_transfer import ContextualizedTransfer
from sequence_transfer.sequence_transfer import SequenceTransfer
from sequence_transfer.sequence import BILUOAnnotationSequence
from sequence_transfer.sequence import BILUOAnnotation
from sequence_transfer.sequence_element import BILUOAnnotationAtom

B = BILUOAnnotation.B
I = BILUOAnnotation.I
L = BILUOAnnotation.L
U = BILUOAnnotation.U
O = BILUOAnnotation.O




class BILUOAnnotationTransfer:
    def __init__(self, transfer: ContextualizedTransfer):
        self._transfer = transfer

    def apply(self, biluo_annotation_sequence: BILUOAnnotationSequence, zip_target=False):
        transferred_annotations = []
        for annotation in biluo_annotation_sequence:

            transferred = SequenceTransfer.apply(self._transfer, annotation)
            print(f"\n num letter {transferred.size}--------------")
            atoms = annotation.materialize()[0].atoms
            z = zip(*map(
                lambda atom: list(map(
                    lambda x: BILUOAnnotationAtom(x[0], x[1]),
                    product(transfer_biluo(atom.code, transferred.size), [atom.tag])))
                ,atoms))

            z2 =  map(lambda atom_list:BILUOAnnotation(*atom_list), z)
            for x in z2:
                transferred_annotations.append(x)

        print(transferred_annotations)
        # return BILUOAnnotationSequence(0,
        #
        # )

            # for i, y in enumerate(x):
            #     print(f"-->level {i}:", y)

            #print(*zip(*x))




            # for atom in atoms:
            #     code = atom.code
            #     tag = atom.tag
            #     t = map(
            #         lambda x: BILUOAnnotationAtom(x[0], x[1]),
            #         product(transfer_biluo(code, transferred.size), [tag]))
            #     for x in t:
            #         print(x.code, x.tag)
            #     print("----------------")
            # Apply is passed to the base class that transfer simple sequence


            # # Extract sequence
            # a = self._transfer.source.context




class BILUOTransferException:
    def __init__(self):
        super().__init__("TransferException")


def transfer_biluo(x: str, nb_slots: int) -> str:
    if nb_slots == 0:
        raise BILUOTransferException()
    else:
        if x == I or x == O:
            return x * nb_slots
        if x == B:
            return B + I*(nb_slots - 1)
        elif x == L:
            return I * (nb_slots - 1) + L
        elif x == U:
            if nb_slots == 1:
                return U
            else:
                return B + I * (nb_slots - 2) + L




