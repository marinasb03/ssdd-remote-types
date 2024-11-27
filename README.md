# Marina Sobrino Blanco
## Configuración del Servidor y Pruebas
### Configuración inicial del servidor

El servidor utiliza la siguiente configuración en el archivo remotetypes.config para establecer el endpoint de comunicación:
```
remotetypes.Endpoints=tcp -p 10000
```
Este endpoint define que el servidor escucha en el puerto 10000 utilizando el protocolo TCP.

Antes de interactuar con el servidor, es necesario generar las interfaces requeridas a partir del archivo remotetypes.ice. Esto se realiza mediante el siguiente comando:
```
slice2py -I. remotetypes.ice
```
Este comando genera el código necesario para que el servidor y las pruebas puedan utilizar las definiciones de tipos y métodos especificados en el archivo .ice. En este caso, se genera el módulo RemoteTypes, que será utilizado tanto por el servidor como por las pruebas.

### Inicio del servidor

Para iniciar el servidor, ejecuto el siguiente comando:
```
remotetypes --Ice.Config=config/remotetypes.config
```
Este comando lanza el servidor utilizando la configuración definida en remotetypes.config. Una vez en marcha, el servidor estará listo para procesar peticiones en el endpoint especificado.

### Pruebas de funcionalidad

El servidor implementa soporte para diferentes tipos de datos remotos, como listas, conjuntos y diccionarios. Para garantizar su correcto funcionamiento, he desarrollado pruebas unitarias que validan las funcionalidades de cada tipo de dato.

Estas pruebas están ubicadas en el directorio /tests y se ejecutan utilizando pytest. Por ejemplo, para probar la funcionalidad de la clase Factory, ejecuto el siguiente comando:
```
pytest -v test_factory.py
```
El parámetro -v permite obtener un detalle más completo de los resultados de las pruebas. Este esquema de pruebas asegura que cada componente del servidor se comporte según lo esperado.

### Prueba de conectividad al servidor

Adicionalmente, he implementado una prueba para verificar si el servidor está activo y accesible. Dicha prueba intenta conectarse al servidor en el endpoint configurado (tcp -p 10000) y valida que el proxy obtenido sea del tipo esperado (FactoryPrx).

El código de la prueba es el siguiente:
```
"""Pruebas de conexión con el servidor."""
import pytest  # type: ignore
import Ice
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
```
Esta prueba verifica los siguientes escenarios:

    Si el servidor está activo, se obtiene un proxy válido, y el test confirma que el proxy corresponde al tipo esperado (FactoryPrx).
    Si el servidor no está en ejecución, se captura la excepción ConnectionRefusedException y el test falla con un mensaje descriptivo.

### Exclusión de la prueba del repositorio

Dado que el servidor (activo) no se incluye en el repositorio (por motivos como la infraestructura o configuración específica), esta prueba no se añadió directamente al directorio /tests. Esto evita errores en sistemas donde el servidor no está configurado o en ejecución. Sin embargo, la prueba ha sido validada localmente y funciona correctamente bajo las condiciones especificadas en el archivo requisitos.md.

### Validación del proyecto

Todo lo mencionado en el archivo requisitos.md y el enunciado ha sido implementado y probado exhaustivamente para garantizar el correcto funcionamiento del servidor y sus funcionalidades.

# remote-types repository template

[![Tests](https://github.com/UCLM-ESI/remote-types/actions/workflows/tests.yml/badge.svg)](https://github.com/UCLM-ESI/remote-types/actions/workflows/tests.yml)
[![Linters](https://github.com/UCLM-ESI/remote-types/actions/workflows/linters.yml/badge.svg)](https://github.com/UCLM-ESI/remote-types/actions/workflows/linters.yml)
[![Type checking](https://github.com/UCLM-ESI/remote-types/actions/workflows/typechecking.yml/badge.svg)](https://github.com/UCLM-ESI/remote-types/actions/workflows/typechecking.yml)

Template for the SSDD laboratory 2024-2025

## Installation

To locally install the package, just run

```
pip install .
```

Or, if you want to modify it during your development,

```
pip install -e .
```

## Execution

To run the template server, just install the package and run

```
remotetypes --Ice.Config=config/remotetypes.config
```

## Configuration

This template only allows to configure the server endpoint. To do so, you need to modify
the file `config/remotetypes.config` and change the existing line.

For example, if you want to make your server to listen always in the same TCP port, your file
should look like

```
remotetypes.Endpoints=tcp -p 10000
```

## Running tests and linters locally

If you want to run the tests and/or linters, you need to install the dependencies for them:

- To install test dependencies: `pip install .[tests]`
- To install linters dependencies: `pip install .[linters]`

All the tests runners and linters are configured in the `pyproject.toml`.

## Continuous integration

This repository is already configured to run the following workflows:

- Ruff: checks the format, code style and docs style of the source code.
- Pylint: same as Ruff, but it evaluates the code. If the code is rated under a given threshold, it fails.
- MyPy: checks the types definitions and the usages, showing possible errors.
- Unit tests: uses `pytest` to run unit tests. The code coverage is quite low. Fixing the tests, checking the
    test coverage and improving it will make a difference.

If you create your repository from this template, you will get all those CI for free.

## Slice usage

The Slice file is provided inside the `remotetypes` directory. It is only loaded once when the `remotetypes`
package is loaded by Python. It makes your life much easier, as you don't need to load the Slice in every module
or submodule that you define.

The code loading the Slice is inside the `__init__.py` file.
