"""Pruebas clase factory."""
import pytest
from remotetypes.factory import Factory
from remotetypes.remotedict import RemoteDict
from remotetypes.remotelist import RemoteList
from remotetypes.remoteset import RemoteSet
import RemoteTypes as rt

@pytest.fixture
def factory():
    """Fixture to create a fresh Factory instance."""
    return Factory(persistence_file="test_data.json")

def test_create_rdict(factory):
    """Test the creation of a new RDict."""
    rdict = factory.get(rt.TypeName.RDict)
    assert isinstance(rdict, RemoteDict)
    assert rdict.identifier() is not None

def test_create_rlist(factory):
    """Test the creation of a new RList."""
    rlist = factory.get(rt.TypeName.RList)
    assert isinstance(rlist, RemoteList)
    assert rlist.identifier() is not None

def test_create_rset(factory):
    """Test the creation of a new RSet."""
    rset = factory.get(rt.TypeName.RSet)
    assert isinstance(rset, RemoteSet)
    assert rset.identifier() is not None

def test_create_rdict_with_identifier(factory):
    """Test creating an RDict with a specific identifier."""
    rdict = factory.get(rt.TypeName.RDict, "customDict")
    assert isinstance(rdict, RemoteDict)
    assert rdict.identifier() == "customDict"

def test_create_rlist_with_identifier(factory):
    """Test creating an RList with a specific identifier."""
    rlist = factory.get(rt.TypeName.RList, "customList")
    assert isinstance(rlist, RemoteList)
    assert rlist.identifier() == "customList"

def test_create_rset_with_identifier(factory):
    """Test creating an RSet with a specific identifier."""
    rset = factory.get(rt.TypeName.RSet, "customSet")
    assert isinstance(rset, RemoteSet)
    assert rset.identifier() == "customSet"

def test_get_existing_rdict(factory):
    """Test getting an existing RDict."""
    rdict = factory.get(rt.TypeName.RDict, "existingDict")
    rdict.setItem("key1", "value1")

    same_rdict = factory.get(rt.TypeName.RDict, "existingDict")
    assert same_rdict is rdict
    assert same_rdict.getItem("key1") == "value1"


def test_get_existing_rlist(factory):
    """Test getting an existing RList."""
    rlist = factory.get(rt.TypeName.RList, "existingList")
    rlist.append("item1")

    same_rlist = factory.get(rt.TypeName.RList, "existingList")
    assert same_rlist is rlist
    assert same_rlist.pop(0) == "item1"


def test_get_existing_rset(factory):
    """Test getting an existing RSet."""
    rset = factory.get(rt.TypeName.RSet, "existingSet")
    rset.add("item1")

    same_rset = factory.get(rt.TypeName.RSet, "existingSet")
    assert same_rset is rset
    assert same_rset.contains("item1")


def test_persistence(factory):
    """Test if objects are persisted correctly."""
    rdict = factory.get(rt.TypeName.RDict, "mydict")
    rdict.setItem("key1", "value1")
    factory._save_persistent_data()

    new_factory = Factory(persistence_file="test_data.json")
    rdict_restored = new_factory.get(rt.TypeName.RDict, "mydict")
    assert rdict_restored.getItem("key1") == "value1"
