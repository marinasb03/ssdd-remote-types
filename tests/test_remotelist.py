"""Pruebas remotelist."""
import pytest
from remotetypes.remotelist import RemoteList
import RemoteTypes as rt

@pytest.fixture
def remote_list():
    """Fixture to create a fresh RemoteList."""
    return RemoteList("test_list")


def test_append(remote_list):
    """Test appending items to the list."""
    remote_list.append("item1")
    assert remote_list.length() == 1
    assert remote_list.contains("item1")


def test_remove(remote_list):
    """Test removing an item from the list."""
    remote_list.append("item1")
    remote_list.remove("item1")
    assert remote_list.length() == 0
    assert not remote_list.contains("item1")


def test_pop(remote_list):
    """Test popping an item from the list."""
    remote_list.append("item1")
    remote_list.append("item2")
    item = remote_list.pop()
    assert item == "item2"
    assert remote_list.length() == 1
    assert remote_list.contains("item1")
    assert not remote_list.contains("item2")


def test_pop_at_index(remote_list):
    """Test popping an item at a specific index."""
    remote_list.append("item1")
    remote_list.append("item2")
    item = remote_list.pop(0)
    assert item == "item1"
    assert remote_list.length() == 1
    assert not remote_list.contains("item1")
    assert remote_list.contains("item2")


def test_pop_empty_list(remote_list):
    """Test popping an item from an empty list."""
    with pytest.raises(rt.IndexError):
        remote_list.pop()


def test_length(remote_list):
    """Test the length of the list."""
    remote_list.append("item1")
    remote_list.append("item2")
    assert remote_list.length() == 2


def test_contains(remote_list):
    """Test checking if an item is contained in the list."""
    remote_list.append("item1")
    assert remote_list.contains("item1")
    assert not remote_list.contains("item2")


def test_hash(remote_list):
    """Test the hash function of the list."""
    remote_list.append("item1")
    remote_list.append("item2")
    hash_value = remote_list.hash()
    assert isinstance(hash_value, int)

def test_get_item(remote_list):
    """Test getting an item from the list."""
    remote_list.append("item1")
    remote_list.append("item2")
    item = remote_list.getItem(0)
    assert item == "item1"

    item = remote_list.getItem(1)
    assert item == "item2"


def test_get_item_index_error(remote_list):
    """Test getting an item from the list with an invalid index."""
    remote_list.append("item1")
    with pytest.raises(rt.IndexError):
        remote_list.getItem(1)  # Index 1 is out of bounds, as only "item1" is in the list.


def test_iter(remote_list):
    """Test iterating over the list."""
    remote_list.append("item1")
    remote_list.append("item2")
    iterator = remote_list.iter()

    # Verificar que el primer item es "item1"
    assert next(iterator) == "item1"

    # Verificar que el siguiente item es "item2"
    assert next(iterator) == "item2"

    # Verificar que StopIteration es lanzado cuando no hay más elementos
    with pytest.raises(rt.StopIteration):
        next(iterator)


def test_invalidate_iterators(remote_list):
    """Test invalidating iterators when items are modified."""
    remote_list.append("item1")
    iterator = remote_list.iter()
    remote_list.append("item2")
    remote_list.invalidate_iterators()
    new_iterator = remote_list.iter()
    assert new_iterator != iterator  # Ensure new iterator is created
