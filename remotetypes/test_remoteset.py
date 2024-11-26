"""Pruebas remoteset"""
import pytest
from remotetypes.remoteset import RemoteSet
import RemoteTypes as rt


@pytest.fixture
def remote_set():
    """Fixture to create a fresh RemoteSet."""
    return RemoteSet("test_set")


def test_add(remote_set):
    """Test adding an item to the set."""
    remote_set.add("item1")
    assert remote_set.length() == 1
    assert remote_set.contains("item1")


def test_remove(remote_set):
    """Test removing an item from the set."""
    remote_set.add("item1")
    remote_set.remove("item1")
    assert remote_set.length() == 0
    assert not remote_set.contains("item1")


def test_remove_non_existent(remote_set):
    """Test attempting to remove an item that does not exist."""
    with pytest.raises(rt.KeyError):
        remote_set.remove("non_existent_item")


def test_pop(remote_set):
    """Test popping an item from the set."""
    remote_set.add("item1")
    remote_set.add("item2")
    item = remote_set.pop()
    assert item in ["item1", "item2"]
    assert remote_set.length() == 1


def test_pop_empty_set(remote_set):
    """Test popping an item from an empty set."""
    with pytest.raises(rt.KeyError):
        remote_set.pop()


def test_length(remote_set):
    """Test the length of the set."""
    remote_set.add("item1")
    remote_set.add("item2")
    assert remote_set.length() == 2


def test_contains(remote_set):
    """Test checking if an item is contained in the set."""
    remote_set.add("item1")
    assert remote_set.contains("item1")
    assert not remote_set.contains("item2")


def test_hash(remote_set):
    """Test the hash function of the set."""
    remote_set.add("item1")
    remote_set.add("item2")
    hash_value = remote_set.hash()
    assert isinstance(hash_value, int)


def test_iter(remote_set):
    """Test iterating over the set."""
    remote_set.add("item1")
    remote_set.add("item2")
    iterator = remote_set.iter()

    # Verify that the first item is "item1"
    assert next(iterator) == "item1"

    # Verify that the next item is "item2"
    assert next(iterator) == "item2"

    # Verify that StopIteration is raised when there are no more elements
    with pytest.raises(rt.StopIteration):
        next(iterator)


def test_invalidate_iterators(remote_set):
    """Test invalidating iterators when items are modified."""
    remote_set.add("item1")
    iterator = remote_set.iter()
    remote_set.add("item2")
    remote_set.invalidate_iterators()
    new_iterator = remote_set.iter()
    assert new_iterator != iterator  # Ensure a new iterator is created
