from typing import Optional
import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.iterable import DictIterable

class RemoteDict(rt.RDict):
    """Implementation of the RDict interface."""

    def __init__(self, identifier: str) -> None:
        self._storage_ = {}
        self._iterators = []
        self.id_ = identifier

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.id_

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item by key."""
        if item not in self._storage_:
            raise rt.KeyError(key=item)
        del self._storage_[item]

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the dictionary."""
        return len(self._storage_)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if a key exists in the dictionary."""
        return item in self._storage_

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash based on the dictionary content."""
        items = sorted(self._storage_.items())
        return hash(repr(items))
    
    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        iterable = DictIterable(self._storage_)
        self._iterators.append(iterable)
        return iterable

    def setItem(self, key: str, item: str, current: Optional[Ice.Current] = None) -> None:
        self.invalidate_iterators()
        self._storage_[key] = item

    def getItem(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Retrieve a value by key."""
        if key not in self._storage_:
            raise rt.KeyError(key=key)
        return self._storage_[key]

    def pop(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Retrieve and remove a key-value pair."""
        if key not in self._storage_:
            raise rt.KeyError(key=key)
        return self._storage_.pop(key)

    def invalidate_iterators(self) -> None:
        for it in self._iterators:
            it.invalidate()
        self._iterators.clear()