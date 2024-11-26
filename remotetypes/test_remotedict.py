import pytest # type : ignore
from remotetypes.remotedict import RemoteDict
import RemoteTypes as rt

@pytest.fixture
def remote_dict():
    """Fixture to create a fresh RemoteDict."""
    return RemoteDict("test_dict")


def test_set_item(remote_dict):
    """Test setting an item in the dictionary."""
    remote_dict.setItem("key1", "value1")
    assert remote_dict.length() == 1
    assert remote_dict.contains("key1")
    assert remote_dict.getItem("key1") == "value1"


def test_remove_item(remote_dict):
    """Test removing an item from the dictionary."""
    remote_dict.setItem("key1", "value1")
    remote_dict.remove("key1")
    assert remote_dict.length() == 0
    assert not remote_dict.contains("key1")


def test_pop_item(remote_dict):
    """Test popping an item from the dictionary."""
    remote_dict.setItem("key1", "value1")
    remote_dict.setItem("key2", "value2")
    value = remote_dict.pop("key1")
    assert value == "value1"
    assert remote_dict.length() == 1
    assert remote_dict.contains("key2")
    assert not remote_dict.contains("key1")


def test_pop_non_existent_item(remote_dict):
    """Test popping an item that does not exist in the dictionary."""
    with pytest.raises(rt.KeyError):
        remote_dict.pop("non_existent_key")


def test_get_item(remote_dict):
    """Test getting an item from the dictionary."""
    remote_dict.setItem("key1", "value1")
    value = remote_dict.getItem("key1")
    assert value == "value1"


def test_get_non_existent_item(remote_dict):
    """Test getting a non-existent item from the dictionary."""
    with pytest.raises(rt.KeyError):
        remote_dict.getItem("non_existent_key")


def test_length(remote_dict):
    """Test the length of the dictionary."""
    remote_dict.setItem("key1", "value1")
    remote_dict.setItem("key2", "value2")
    assert remote_dict.length() == 2


def test_contains(remote_dict):
    """Test checking if an item is contained in the dictionary."""
    remote_dict.setItem("key1", "value1")
    assert remote_dict.contains("key1")
    assert not remote_dict.contains("key2")


def test_hash(remote_dict):
    """Test the hash function of the dictionary."""
    remote_dict.setItem("key1", "value1")
    remote_dict.setItem("key2", "value2")
    hash_value = remote_dict.hash()
    assert isinstance(hash_value, int)


def test_iter(remote_dict):
    """Test iterating over the dictionary."""
    remote_dict.setItem("key1", "value1")
    remote_dict.setItem("key2", "value2")
    iterator = remote_dict.iter()

    # Verificar que el primer item es "key1"
    assert next(iterator) == "key1"

    # Verificar que el siguiente item es "key2"
    assert next(iterator) == "key2"

    # Verificar que StopIteration es lanzado cuando no hay más elementos
    with pytest.raises(rt.StopIteration):
        next(iterator)


def test_invalidate_iterators(remote_dict):
    """Test invalidating iterators when items are modified."""
    remote_dict.setItem("key1", "value1")
    iterator = remote_dict.iter()
    remote_dict.setItem("key2", "value2")
    remote_dict.invalidate_iterators()
    new_iterator = remote_dict.iter()
    assert new_iterator != iterator  # Ensure new iterator is created
