"""Clase remotelist."""
from typing import List, Optional
import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.iterable import ListIterable


class RemoteList(rt.RList):
    """Implementation of the RList interface."""

    def __init__(self, identifier: str) -> None:
        """Init."""
        self._storage_: List[str] = []
        self._iterators: List[ListIterable] = []
        self.id_: str = identifier

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.id_

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item from the list."""
        try:
            self._storage_.remove(item)
        except ValueError:
            raise rt.KeyError(key=item)

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the list."""
        return len(self._storage_)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if an item exists in the list."""
        return item in self._storage_

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash based on the list content."""
        return hash(repr(self._storage_))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Crear y devolver un iterador remoto."""
        try:
            iterable = ListIterable(self._storage_)

            if current and current.adapter:
                identity = current.adapter.getCommunicator().stringToIdentity(f"iter-{self.id_}-{len(self._iterators)}")
                proxy = rt.IterablePrx.uncheckedCast(current.adapter.add(iterable, identity))
                self._iterators.append(iterable)
                return proxy
            else:
                raise RuntimeError("No se puede registrar el iterador porque no hay adaptador disponible.")
        except Exception as e:
            print(f"Error en el iterador: {e}")
            raise


    def append(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Append."""
        self.invalidate_iterators()
        self._storage_.append(item)

    def pop(self, index: Optional[int] = None, current: Optional[Ice.Current] = None) -> str:
        """Remove and return an item from the list."""
        try:
            return self._storage_.pop(index if index is not None else -1)
        except IndexError:
            raise rt.IndexError(message=f"Index {index} is out of bounds.")

    def getItem(self, index: int, current: Optional[Ice.Current] = None) -> str:
        """Devuelve el elemento en la posición indicada."""
        try:
            item = self._storage_[index]
            return item
        except IndexError:
            raise rt.IndexError(message=f"Index {index} is out of bounds.")

    def invalidate_iterators(self, current: Optional[Ice.Current] = None) -> None:
        """Invalidar."""
        for it in self._iterators:
            it.invalidate()
        self._iterators.clear()
