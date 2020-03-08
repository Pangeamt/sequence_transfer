from sequence_transfer.sequence import Sequence
from sequence_transfer.sequence_transfer import SequenceTransfer


def lcs_transfer(x: str, y: str) -> SequenceTransfer:
    m = len(x)
    n = len(y)

    L = [[None] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif x[i - 1] == y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    transfers = []
    while m > 0 and n > 0:
        max_neighbor = max(L[m - 1][n - 1], L[m][n - 1], L[m - 1][n])
        match = None
        if L[m - 1][n - 1] == max_neighbor:
            match = (Sequence(m - 1, m), Sequence(n - 1, n))
            m = m - 1
            n = n - 1
        elif L[m][n - 1] == max_neighbor:
            # match = (Sequence(m, m), Sequence(n - 1, n))
            n = n - 1
        elif L[m - 1][n] == max_neighbor:
            match = (Sequence(m - 1, m), Sequence(n, n))
            m = m - 1
        if match is not None:
            transfers.append(match)

    while m > 0:
        match = (Sequence(m - 1, m), Sequence(n, n))
        transfers.append(match)
        m -= 1

    # while n > 0:
    #     match = (Sequence(m, m), Sequence(n - 1, n))
    #     transfers.append(match)
    #     n -= 1

    transfers.reverse()

    return SequenceTransfer(
        Sequence(0, len(x)),
        Sequence(0, len(y)),
        transfers
    )

