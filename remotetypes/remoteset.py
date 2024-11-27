"""Needed classes to implement and serve the RSet type."""
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error

from remotetypes.customset import StringSet
from remotetypes.iterable import SetIterable


class RemoteSet(rt.RSet):
    """Implementation of the remote interface RSet."""

    def __init__(self, identifier) -> None:
        """Inicialización."""
        self._storage_ = StringSet()
        self._iterators = []
        self.id_ = identifier

    def identifier(self) -> str:
        """Return the identifier of the object."""
        return self.id_

    def remove(self, item: str) -> None:
        """Remove an item from the StringSet if added. Else, raise a remote exception."""
        try:
            self._storage_.remove(item)
        except KeyError as error:
            raise rt.KeyError(item) from error

    def length(self) -> int:
        """Return the number of elements in the StringSet."""
        return len(self._storage_)

    def contains(self, item: str) -> bool:
        """Check the pertenence of an item to the StringSet."""
        return item in self._storage_

    def hash(self) -> int:
        """Calculate a hash from the content of the internal StringSet."""
        contents = list(self._storage_)
        contents.sort()
        return hash(repr(contents))

    def iter(self) -> rt.IterablePrx:
        """Iterador."""
        iterable = SetIterable(sorted(self._storage_))
        self._iterators.append(iterable)
        return iterable

    def add(self, item: str) -> None:
        """Añadir."""
        self.invalidate_iterators()
        self._storage_.add(item)

    def pop(self) -> str:
        """Remove and return an element from the storage."""
        try:
            return self._storage_.pop()

        except KeyError as exc:
            raise rt.KeyError() from exc

    def invalidate_iterators(self) -> None:
        """Invalidar."""
        for it in self._iterators:
            it.invalidate()
        self._iterators.clear()
