"""Clase remoteset."""
from typing import List, Optional
import Ice
import threading
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.customset import StringSet
from remotetypes.iterable import SetIterable


class RemoteSet(rt.RSet):
    """Implementation of the remote interface RSet."""

    def __init__(self, identifier: str) -> None:
        """Inicialización."""
        self._storage_: StringSet = StringSet()
        self._iterators: List[SetIterable] = []
        self.id_: str = identifier

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.id_

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item from the StringSet if added. Else, raise a remote exception."""
        try:
            self._storage_.remove(item)
        except KeyError as error:
            raise rt.KeyError(item) from error

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the StringSet."""
        return len(self._storage_)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check the pertenence of an item to the StringSet."""
        return item in self._storage_

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash from the content of the internal StringSet."""
        contents = list(self._storage_)
        contents.sort()
        return hash(repr(contents))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Iterador."""
        try:
            if not self._storage_:
                raise ValueError("El almacenamiento está vacío o no es un conjunto válido.")

            iterable = SetIterable(sorted(self._storage_))

            self._iterators.append(iterable)

            return iterable
        except Exception as e:
            print(f"Error en el iterador: {e}")
            raise  

    def add(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Añadir."""
        self.invalidate_iterators()
        self._storage_.add(item)

    def pop(self, current: Optional[Ice.Current] = None) -> str:
        """Remove and return an element from the storage."""
        try:
            return self._storage_.pop()
        except KeyError as exc:
            raise rt.KeyError() from exc

    def invalidate_iterators(self, current: Optional[Ice.Current] = None) -> None:
        """Invalidar."""
        for it in self._iterators:
            it.invalidate()
        self._iterators.clear()
