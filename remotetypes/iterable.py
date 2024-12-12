"""Clase iterable."""
from typing import Optional
import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error

class ListIterable(rt.Iterable):
    """Iterable implementation for RemoteList."""

    def __init__(self, data: list[str]) -> None:
        """Init."""
        self._data = data
        self._index = 0
        self._valid = True

    def __iter__(self):
        """Itera sobre los elementos de la colección."""
        return self

    def next(self, current: Optional[Ice.Current] = None) -> str:
        """Next iterador."""
        if not self._valid:
            raise rt.CancelIteration()

        if self._index >= len(self._data):
            raise rt.StopIteration()

        value = self._data[self._index]
        self._index += 1
        return value

    def invalidate(self) -> None:
        """Invalidate."""
        self._valid = False

class DictIterable(rt.Iterable):
    """Iterable implementation for RemoteDict."""

    def __init__(self, data: dict[str, str]) -> None:
        """Init diccionarios."""
        self._keys = list(data.keys())
        self._index = 0
        self._valid = True

    def __iter__(self):
        """Itera sobre los elementos de la colección."""
        return self

    def next(self, current: Optional[Ice.Current] = None) -> str:
        """Next iterador."""
        if not self._valid:
            raise rt.CancelIteration()

        if self._index >= len(self._data):
            raise rt.StopIteration()

        value = self._data[self._index]
        self._index += 1
        return value

    def invalidate(self) -> None:
        """Invalidate."""
        self._valid = False

class SetIterable(rt.Iterable):
    """Implementación del iterador para RemoteSet."""
    
    def __init__(self, items):
        """Inicializa el iterador."""
        self._items = iter(items)
        self._invalidated = False 
        self._index = 0 

    def next(self, current: Optional[Ice.Current] = None):
        """Devuelve el siguiente elemento del iterador."""
        if self._invalidated:
            raise Ice.ObjectNotExistException("El iterador ha sido invalidado.")
        try:
            return next(self._items)
        except StopIteration:
            raise rt.StopIteration()

    def invalidate(self):
        """Invalidar el iterador."""
        self._invalidated = True
        self._items = iter([])
        self._index = 0
