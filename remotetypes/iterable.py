"""Clase iterable."""
from typing import Optional
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
import Ice

class ListIterable(rt.Iterable):
    """Iterable implementation for RemoteList."""

    def __init__(self, data: list[str]) -> None:
        """Init."""
        self._data = data
        self._index = 0
        self._valid = True

    def __iter__(self):
        """Iter."""
        return self

    def __next__(self) -> str:
        """Next iterador."""
        if not self._valid:
            raise rt.CancelIteration()

        if self._index >= len(self._data):
            raise rt.StopIteration()

        value = self._data[self._index]
        self._index += 1
        return value

    def next(self) -> str:
        """Next."""
        return self.__next__()

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
        """Iter."""
        return self

    def __next__(self) -> str:
        """Next iterador."""
        if not self._valid:
            raise rt.CancelIteration()

        if self._index >= len(self._keys):
            raise rt.StopIteration()

        key = self._keys[self._index]
        self._index += 1
        return key

    def next(self) -> str:
        """Next."""
        return self.__next__()

    def invalidate(self) -> None:
        """Invalidate."""
        self._valid = False

class SetIterable(rt.Iterable):
    """Iterable implementation for RemoteSet."""

    def __init__(self, data: set[str]) -> None:
        """Init conjuntos."""
        self._items = iter(data)
        self._valid = True

    def __iter__(self):
        """Iter."""
        return self

    def __next__(self) -> str:
        """Next iterador."""
        if not self._valid:
            raise rt.CancelIteration()

        try:
            return next(self._items)
        except StopIteration:
            raise rt.StopIteration()

    def next(self) -> str:
        """Next."""
        return self.__next__()

    def invalidate(self) -> None:
        """Invalidate."""
        self._valid = False
