from remotetypes.iterable import ListIterable, DictIterable, SetIterable
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error


def test_list_iterable():
    """Test iterating through a list."""
    data = ["a", "b", "c"]
    iterator = ListIterable(data)

    assert iter(iterator) is iterator  # Verificar que iter devuelve el propio objeto
    assert iterator.next() == "a"
    assert iterator.next() == "b"
    assert iterator.next() == "c"

    try:
        iterator.next()
    except rt.StopIteration:
        pass


def test_dict_iterable():
    """Test iterating through a dictionary."""
    data = {"key1": "value1", "key2": "value2"}
    iterator = DictIterable(data)

    assert iter(iterator) is iterator  # Verificar que iter devuelve el propio objeto
    assert iterator.next() == "key1"
    assert iterator.next() == "key2"

    try:
        iterator.next()
    except rt.StopIteration:
        pass


def test_set_iterable():
    """Test iterating through a set."""
    data = {"a", "b", "c"}
    iterator = SetIterable(data)

    assert iter(iterator) is iterator  # Verificar que iter devuelve el propio objeto

    seen = set()
    for _ in range(3):
        seen.add(iterator.next())
    
    assert seen == {"a", "b", "c"}

    try:
        iterator.next()
    except rt.StopIteration:
        pass


def test_invalidate_iterator():
    """Test that calling invalidate() causes CancelIteration."""
    data = ["x", "y", "z"]
    iterator = ListIterable(data)

    iterator.invalidate()  # Invalidar el iterador

    try:
        iterator.next()
    except rt.CancelIteration:
        pass
