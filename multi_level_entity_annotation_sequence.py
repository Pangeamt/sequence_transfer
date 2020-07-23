from sequence_transfer.plugin.entity_annotation_transfer_plugin import EntityAnnotationSequence


from itertools import zip_longest, groupby

# class MultiEntityAnnotationSequence:
#     def __init__(self, nb_levels: int):
#         self._nb_levels = nb_levels
#         self._levels = [None]*self._nb_levels
#         print(self._levels)
#
#     @staticmethod
#     def add(self, level: int, entity_annotation_sequence):
#         self
#
#
#
# def merge_annotations(*args: EntityAnnotationSequence) \
#         -> EntityAnnotationSequence:
#     annotation_sequences = list(args)
#     entities = []
#     for i, s in enumerate(annotation_sequences):
#         j = 0
#         for signature, group in groupby(s, key=lambda a: a.signature):
#             group = list(group)
#             if signature == NOT_ANNOTATED:
#                j += len(group)
#             else:
#                 start = j + 1
#                 end = start + len(list(group)) - 1
#                 entities.append(
#                     (start, i, end, group[0])
#                 )
#     for start, priority, end, entity_id in  entities.sort():
#         pass
#
# b = MultiEntityAnnotationSequence(2)


class EntityAnnotationAlchemistSchema:
    def __init__(self, schema: dict):
        self._schema = schema

    def merge(self):
        pass


class EntityAnnotationSequenceAlchemist:
    def __init__(self, schema: EntityAnnotationAlchemistSchema):
        self._schema = schema

    def merge(self, *args: EntityAnnotationSequence):
        """
        Strategy:
        1. Get all subsequences with entities
        2. separate by level following schema.
        3. Order by sequence start
        4. Resolve conflicts:
            previous.end <= current start --> Raise error
            options: position adjustment
        5 resolve nesting conflicts:

        :param args:
        :return:
        """
        pass

    def _extract_levels(self, *args: EntityAnnotationSequence):
        """

        :param args:
        :return:
        """
        pass

    def _resolve_in_level_conflicts(self, levels):
        pass

    def _resolve_nesting_conflicts(self):
        pass


s = {
    'person': {
        'priority': 1
    },
    'lastname': {
        'priority': 1,
        'parents': 'person'
    },
    'firstname': {
        'priority': 2,
        'parents': 'person'
    },
    'M': {
        'priority': 1,
        'parents': ['firstname', 'lastname']
    },
    'F': {
        'priority': 1,
        'parents': ['firstname', 'lastname']
    },
    'location': {
        'priority': 2
    }
}
