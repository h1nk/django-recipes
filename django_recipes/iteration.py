"""Collection of convenience functions for working with iterable objects like QuerySets."""

from itertools import islice

from typing import Iterable, Iterator

__all__ = (
    'group',
)


def group(iterable: Iterable, n: int = 2) -> Iterator[slice]:
    """
    Slice an iterable object into fixed maximum ``n`` length chunks and return each chunk of the original iterable on
    each generator iteration.

    :param n: Slice chunk size
    :param iterable: Object sequence to slice

    :return: Generator iterator of each chunk slice of the original sequence object.
    :rtype: Iterator[slice]
    """

    it = iter(iterable)

    while True:
        chunk = tuple(islice(it, n))

        if not chunk:
            return

        yield chunk
