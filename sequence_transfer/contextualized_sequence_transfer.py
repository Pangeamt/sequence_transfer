from typing import Union, List, Tuple
from sequence_transfer.sequence_transfer import SequenceTransfer
from sequence_transfer.sequence import TextualSequence
from prettytable import PrettyTable


class ContextualizedTransfer(SequenceTransfer):  # TODO: Think about a more appropriate name
    def __init__(self,
                 source: TextualSequence,
                 target: TextualSequence,
                 matches: List[Tuple[TextualSequence, TextualSequence]]):
        super().__init__(source, target, matches)

    def apply(self, sequence: TextualSequence) -> TextualSequence:
        sequence_type = type(sequence)
        transferred = super().apply(sequence)
        return sequence_type(transferred.start, transferred.stop, self._target.context)

    def invert(self):
        matches = self.get_inverted_matches()
        return ContextualizedTransfer(self._target, self._source, matches)

    def debug(self):
        table = PrettyTable(["SRC SLICE", "INDEX SRC", "TEXT SRC", "", "TEXT TGT", "INDEX TGT", "TGT SLICE"])
        parallel_matches = self._parallelize()

        for source_sequence, target_sequence in parallel_matches:
            source_sequence.context = self._source.context
            target_sequence.context = self._target.context
            col1 = source_sequence.slice_representation()
            col2 = "\n".join([str(i) for i in source_sequence.iter_index()])
            col3 = "\n".join([s.context.get_sequence_text(s) for s in source_sequence])
            col4 = '--->'
            col5 = "\n".join([s.context.get_sequence_text(s) for s in target_sequence])
            col6 = "\n".join([str(i) for i in target_sequence.iter_index()])
            col7 = target_sequence.slice_representation()
            table.add_row([
                col1, col2, col3, col4, col5, col6, col7
            ])
        print(table)
