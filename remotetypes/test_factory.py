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
    assert rdict.identifier() is not None  # Verificar que el identificador no sea None

def test_create_rlist(factory):
    """Test the creation of a new RList."""
    rlist = factory.get(rt.TypeName.RList)
    assert isinstance(rlist, RemoteList)
    assert rlist.identifier() is not None  # Verificar que el identificador no sea None

def test_create_rset(factory):
    """Test the creation of a new RSet."""
    rset = factory.get(rt.TypeName.RSet)
    assert isinstance(rset, RemoteSet)
    assert rset.identifier() is not None  # Verificar que el identificador no sea None

def test_create_rdict_with_identifier(factory):
    """Test creating an RDict with a specific identifier."""
    rdict = factory.get(rt.TypeName.RDict, "customDict")
    assert isinstance(rdict, RemoteDict)
    assert rdict.identifier() == "customDict"  # Verificar que el identificador sea el esperado

def test_create_rlist_with_identifier(factory):
    """Test creating an RList with a specific identifier."""
    rlist = factory.get(rt.TypeName.RList, "customList")
    assert isinstance(rlist, RemoteList)
    assert rlist.identifier() == "customList"  # Verificar que el identificador sea el esperado

def test_create_rset_with_identifier(factory):
    """Test creating an RSet with a specific identifier."""
    rset = factory.get(rt.TypeName.RSet, "customSet")
    assert isinstance(rset, RemoteSet)
    assert rset.identifier() == "customSet"  # Verificar que el identificador sea el esperado

def test_get_existing_rdict(factory):
    """Test getting an existing RDict."""
    rdict = factory.get(rt.TypeName.RDict, "existingDict")
    rdict.setItem("key1", "value1")
    
    # Obtener el mismo RDict con el mismo identificador
    same_rdict = factory.get(rt.TypeName.RDict, "existingDict")
    assert same_rdict is rdict  # Debe devolver el mismo objeto
    
    # Verificar que el valor persistió
    assert same_rdict.getItem("key1") == "value1"


def test_get_existing_rlist(factory):
    """Test getting an existing RList."""
    rlist = factory.get(rt.TypeName.RList, "existingList")
    rlist.append("item1")
    
    # Obtener el mismo RList con el mismo identificador
    same_rlist = factory.get(rt.TypeName.RList, "existingList")
    assert same_rlist is rlist  # Debe devolver el mismo objeto
    
    # Verificar que el valor persistió (usando un método adecuado para obtener el primer elemento)
    # Suponiendo que el método 'get(0)' existe:
    assert same_rlist.pop(0) == "item1"  # Método de acceso adecuado para RemoteList


def test_get_existing_rset(factory):
    """Test getting an existing RSet."""
    rset = factory.get(rt.TypeName.RSet, "existingSet")
    rset.add("item1")
    
    # Obtener el mismo RSet con el mismo identificador
    same_rset = factory.get(rt.TypeName.RSet, "existingSet")
    assert same_rset is rset  # Debe devolver el mismo objeto
    
    # Verificar que el valor persistió (usando un método adecuado para verificar si el item existe)
    # Suponiendo que el método 'contains()' existe:
    assert same_rset.contains("item1")  # Método de comprobación adecuado para RemoteSet


def test_persistence(factory):
    """Test if objects are persisted correctly."""
    rdict = factory.get(rt.TypeName.RDict, "mydict")
    rdict.setItem("key1", "value1")
    factory._save_persistent_data()  # Guardar datos persistentes

    # Crear un nuevo factory y cargar el objeto
    new_factory = Factory(persistence_file="test_data.json")
    rdict_restored = new_factory.get(rt.TypeName.RDict, "mydict")
    assert rdict_restored.getItem("key1") == "value1"  # Verificar que el objeto restaurado contiene los datos guardados

