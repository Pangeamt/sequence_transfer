from sequence_transfer.sequence import ContextualizedSequence
from itertools import zip_longest, groupby

class MultiEntityAnnotationSequence:
    def __init__(self, nb_levels: int):
        self._nb_levels = nb_levels
        self._levels = [None]*self._nb_levels
        print(self._levels)

    @staticmethod
    def add(self, level: int, entity_annotation_sequence):
        self



def merge_annotations(*args: EntityAnnotationSequence) \
        -> EntityAnnotationSequence:
    annotation_sequences = list(args)
    entities = []
    for i, s in enumerate(annotation_sequences):
        j = 0
        for signature, group in groupby(s, key=lambda a: a.signature):
            group = list(group)
            if signature == NOT_ANNOTATED:
               j += len(group)
            else:
                start = j + 1
                end = start + len(list(group)) - 1
                entities.append(
                    (start, i, end, group[0])
                )
    for start, priority, end, entity_id in  entities.sort():
        pass

b = MultiEntityAnnotationSequence(2)


class MultiLevelAnnotationSchema:
    def __init__(self, schema):
        self._schema = schema

    def merge(self):
# noinspection PyPep8
schema = {
    'person': {
        'priority': 1

    },
    'lastname': {
        'priority': 1,
        'parent': 'person'
    },
    'firstname': {
        'priority': 2,
        'parent': 'person'
    },
    'M': {
        'priority': 1,
        'parent': ['firstname', 'lastname']
    },
    'F': {
        'priority': 1,
        'parent': ['firstname', 'lastname']
    }
}
