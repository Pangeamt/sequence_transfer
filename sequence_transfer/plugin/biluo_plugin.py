from collections import namedtuple
from typing import List, Tuple
from sequence_transfer.sequence import Sequence, SequenceContext, ContextualizedSequence
from sequence_transfer.sequence_transfer import SequenceTransferPlugin
from itertools import product, zip_longest, groupby
import uuid
from pprint import pprint
from collections import Counter


# Codes


B = "B"
I = "I"
L = "L"
U = "U"
O = "O"
CODES = {B, I, L, U, O}


# Exceptions


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


BILUOAnnotationAtom = namedtuple("BILUOAnnotationAtom", ["code", "tag", "entity_id"])


def hack_repr(x):
    return f"{x.code}-{x.tag}"


# BILUOAnnotationAtom.__repr__ = hack_repr


def extract_code_tag(atom):
    if atom == O:
        return O, ''
    else:
        try:
            code, tag = atom.split('-')
        except Exception:
            raise InvalidBILUOAtomException(atom)
        if code not in CODES:
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
        materialize = annotation_sequence.context.materialize_sequence

        # print(list(map(inverse_transfer.apply, transfer.target)))


        x = list(map(handle_conflicts,
                list(map(materialize,
                     map(inverse_transfer.apply, transfer.target)))))

        pprint(x)
        exit()
        y = handle_not_annotated(x)
        z = recode_atoms (y)




def handle_conflicts(atoms_list: List[Tuple[BILUOAnnotationAtom]]):
    """
    TODO THINK about a better policy:  Handle U priority?
    :param atoms_list: [
                   (atom1_level1, atom2_level2, atom3_level3),
                   (atom4_level1, atom5_level2, atom6_level3),
                   etc...
                    ]s
    :return:
    """

    out = []
    for level, atoms_by_level in enumerate(zip(*list(map(list, atoms_list)))):
        best_entity_id = None
        best_tag = None
        best_num_occurence = 0
        grouped = list(groupby(atoms_by_level, key=lambda atom: (atom.entity_id, atom.tag)))
        for (entity_id, tag), atoms in grouped:
            num_atoms = len(list(atoms))
            if num_atoms >= best_num_occurence:
                best_entity_id = entity_id
                best_tag = tag
                best_num_occurence = num_atoms
        best_atom = BILUOAnnotationAtom(code=I, tag=best_tag, entity_id=best_entity_id)
        out.append(best_atom)
    return out



def handle_not_annotated(atoms: List[BILUOAnnotationAtom]) -> List[BILUOAnnotationAtom]:
    new_atoms = []
    for i, atom in enumerate(atoms):
        if atom is None:
            if i == 0 or i == len(atoms) - 1:
                new_atoms.append(
                    BILUOAnnotationAtom(
                        code=O,
                        tag='',
                        entity_id=None))
            else:
                previous_atom = atoms[i - 1]
                next_atom = atoms[i + 1]
                if previous_atom.entity_id == next_atom.entity_id:
                    new_atoms.append(
                        BILUOAnnotationAtom(
                            code=I,
                            tag=previous_atom.tag,
                            entity_id=previous_atom.entity_id
                        )
                    )
                else:
                    new_atoms.append(
                        BILUOAnnotationAtom(
                            code=O,
                            tag='',
                            entity_id=None))
        else:
            new_atoms.append(atom)
    print("xxxxx")
    print(new_atoms)

    return new_atoms


def recode_atoms(atoms: List[BILUOAnnotationAtom]) -> List[BILUOAnnotationAtom]:

    print("XXXXXXXXXXXXxx", atoms)

    new_atoms = []
    for entity_id, atoms in groupby(atoms, key=id):
        atoms = list(atoms)
        if entity_id is None:
            new_atoms.extend(atoms)
        else:
            for i, atom in enumerate(atoms):
                if i == 0:
                    if len(atoms) == 1:
                        code = U
                    else:
                        code = B
                elif i == len(atoms) - 1:
                    code = L
                else:
                    code = I

                new_atoms.append(
                    BILUOAnnotationAtom(
                        code=code,
                        tag=atom.tag,
                        entity_id=atom.entity_id
                    ))
    return new_atoms
