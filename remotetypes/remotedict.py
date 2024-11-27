"""Clase remotedict."""
from typing import Dict, List
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.iterable import DictIterable


class RemoteDict(rt.RDict):
    """Implementation of the RDict interface."""

    def __init__(self, identifier: str) -> None:
        """Inicialización."""
        self._storage_: Dict[str, str] = {}
        self._iterators: List[DictIterable] = []
        self.id_: str = identifier

    def identifier(self) -> str:
        """Return the identifier of the object."""
        return self.id_

    def remove(self, item: str) -> None:
        """Remove an item by key."""
        if item not in self._storage_:
            raise rt.KeyError(key=item)
        del self._storage_[item]

    def length(self) -> int:
        """Return the number of elements in the dictionary."""
        return len(self._storage_)

    def contains(self, item: str) -> bool:
        """Check if a key exists in the dictionary."""
        return item in self._storage_

    def hash(self) -> int:
        """Calculate a hash based on the dictionary content."""
        items = sorted(self._storage_.items())
        return hash(repr(items))

    def iter(self) -> rt.IterablePrx:
        """Iterador."""
        iterable = DictIterable(self._storage_)
        self._iterators.append(iterable)
        return iterable

    def setItem(self, key: str, item: str) -> None:
        """Set iterador."""
        self.invalidate_iterators()
        self._storage_[key] = item

    def getItem(self, key: str) -> str:
        """Retrieve a value by key."""
        if key not in self._storage_:
            raise rt.KeyError(key=key)
        return self._storage_[key]

    def pop(self, key: str) -> str:
        """Retrieve and remove a key-value pair."""
        if key not in self._storage_:
            raise rt.KeyError(key=key)
        return self._storage_.pop(key)

    def invalidate_iterators(self) -> None:
        """Invalidar iterador."""
        for it in self._iterators:
            it.invalidate()
        self._iterators.clear()
