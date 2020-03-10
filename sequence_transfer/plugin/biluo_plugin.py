from collections import namedtuple
from typing import List, Tuple
from sequence_transfer.sequence import Sequence, SequenceContext, ContextualizedSequence
from sequence_transfer.sequence_transfer import SequenceTransferPlugin
from itertools import product, zip_longest
import uuid
from pprint import pprint


class InvalidBILUOAtomException(Exception):
    def __init__(self, atom: str):
        super().__init__(f"Invalid BILUO {atom}")


class InvalidBILUOCodeException(Exception):
    def __init__(self, code: str):
        super().__init__(f"Invalid BILUO code {code}")


class InvalidBILUOSequenceException(Exception):
    def __init__(self, index: int, level: int):
        super().__init__(f"Invalid BILUO sequence: index: {index}, level:{level}")


class BILUOSequenceSizeMismatchException(Exception):
    def __init__(self):
        super().__init__(f"BILUO Sequence size mismatch")


BILUOAnnotationAtom = namedtuple("BILUOAnnotationAtom", ["level", "code", "tag", "entity_id"])


class BILUOAnnotation:
    B = "B"
    I = "I"
    L = "L"
    U = "U"
    O = "O"
    CODES = {B, I, L, U, O}

    @staticmethod
    def new(annotation: str, *args: str):
        atoms = []
        for annotation in (annotation, *args):
            if annotation == BILUOAnnotation.O:
                atoms.append(
                    BILUOAnnotationAtom(code=BILUOAnnotation.O, tag=""))
            else:
                code, tag = annotation.split('-')
                if code not in BILUOAnnotation.CODES:
                    raise InvalidBILUOCodeException(code)
                atoms.append(
                    BILUOAnnotationAtom(code=code, tag=tag))
        return BILUOAnnotation(*atoms)

    def __init__(self, atom: BILUOAnnotationAtom, *args: BILUOAnnotationAtom):
        self._atoms = [atom, *args]

    def get_atoms(self) -> List[BILUOAnnotationAtom]:
        return self._atoms
    atoms = property(get_atoms)


B = BILUOAnnotation.B
I = BILUOAnnotation.I
L = BILUOAnnotation.L
U = BILUOAnnotation.U
O = BILUOAnnotation.O


def extract_code_tag(atom):
    if atom == O:
        return O, ''
    else:
        try:
            code, tag = atom.split('-')
        except Exception:
            raise InvalidBILUOAtomException(atom)

        if code not in BILUOAnnotation.CODES:
            raise InvalidBILUOCodeException(code)
        return code, tag


class BILUOAnnotationSequenceContext(SequenceContext):
    def __init__(self, context: List[Tuple[BILUOAnnotationAtom, ...]]):
        super().__init__(context)


class BILUOAnnotationSequence(ContextualizedSequence):
    @staticmethod
    def new(annotations: List[List[str]]) -> "BILUOAnnotationSequence":
        if type(annotations) is not list:
            raise ValueError(f"BILUOAnnotationSequence expect to be list of list of string")
        if len(annotations) == 0:
            raise ValueError(f"BILUOAnnotationSequence expect to be a non empty list of list of string")
        for annotation in annotations:
            if type(annotation) is not list:
                raise ValueError(f"BILUOAnnotationSequence expect to be a list of list of string")

        # Build the context
        atoms_by_level = list(zip_longest(*annotations))
        atoms_by_level_processed = []
        for level, atoms in enumerate(atoms_by_level):
            atoms_by_level_processed.append([])
            tmp = None
            for i, atom in enumerate(atoms):
                if atom is None:  # zip longest returns None if iterators have different sizes
                    raise BILUOSequenceSizeMismatchException()
                code, tag = extract_code_tag(atom)
                if code == B or code == U:
                    if tmp is not None:
                        raise InvalidBILUOSequenceException(i)
                    tmp = str(uuid.uuid4())
                atom = BILUOAnnotationAtom(
                    level=level,
                    code=code,
                    tag=tag,
                    entity_id=tmp
                )
                atoms_by_level_processed[level].append(atom)
                if code == L:
                    tmp = None

                # TODO raise error for an eventual missing L at the end.
                # TODO More checks... THINK

        annotations = list(zip(*atoms_by_level_processed))
        return BILUOAnnotationSequence(0, len(annotations), BILUOAnnotationSequenceContext(annotations))

    def __init__(self, start: int, stop: int, context: BILUOAnnotationSequenceContext):
        super().__init__(start, stop, context)


class BILUOPlugin(SequenceTransferPlugin):
    def apply(self, transfer, annotation_sequence: BILUOAnnotationSequence) -> BILUOAnnotationSequence:
        if annotation_sequence.size != transfer.source.size:
            raise ValueError("Annotation sequence size != transfer source size")  # TODO custom exception

        inverse_transfer = transfer.invert()
        for target_sequence in transfer.target:
            matching_source_sequence = inverse_transfer.apply(target_sequence)
            s = annotation_sequence.context.materialize_sequence(matching_source_sequence)
            print(target_sequence, matching_source_sequence, s)

        # atoms_by_level = list(zip(
        #     *[annotation.materialize()[0].atoms for annotation in annotation_sequence]))
        #
        # id_by_level = {}
        # for level, atoms in atoms_by_level:
        #     tmp = None
        #     id_by_level[level] = []
        #     for atom in atoms:
        #         if atom.code = 'B'

        # transferred_sequences = [
        #     transfer.apply(annotation) for annotation in annotation_sequence
        # ]
        # print(transferred_sequences)
        # for match in matches:
        #     source_annotation_seqence = annotation_sequence(match[0])
        #     transferred_annotations = []
        #     transferred = transfer.apply(annotation)
        #     print(f"\n num letter {transferred.size}--------------")
        #     atoms = annotation.materialize()[0].atoms
        #     z = zip(*map(
        #         lambda atom: list(map(
        #             lambda x: BILUOAnnotationAtom(x[0], x[1]),
        #             product(transfer_biluo(atom.code, transferred.size), [atom.tag])))
        #         , atoms))
        #
        #     z2 = map(lambda atom_list: BILUOAnnotation(*atom_list), z)
        #     for x in z2:
        #         transferred_annotations.append(x)
        #
        # print(transferred_annotations)











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

