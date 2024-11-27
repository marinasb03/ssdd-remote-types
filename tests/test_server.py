"""Pruebas de conexión con el servidor."""
import pytest
import Ice
from remotetypes.factory import Factory
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error

SERVER_ENDPOINT = "factory:default -p 10000"

@pytest.fixture(scope="module")
def ice_communicator():
    """Fixture para crear un comunicador de Ice."""
    communicator = Ice.initialize()
    yield communicator
    communicator.destroy()


def test_server_connection_success(ice_communicator):
    """Prueba de conexión exitosa al servidor."""
    try:
        proxy = ice_communicator.stringToProxy(SERVER_ENDPOINT)
        factory = rt.FactoryPrx.checkedCast(proxy)
        assert factory is not None, "No se pudo conectar al servidor o no es del tipo esperado."
    except Ice.ConnectionRefusedException:
        pytest.fail("Conexión rechazada: el servidor no está disponible.")
    except Exception as e:
        pytest.fail(f"Excepción inesperada: {e}")
