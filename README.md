# Marina Sobrino Blanco
## Entregable 2
### Introducción

Lo primero que he hecho ha sido solucionar el problema con la clase `iterable`, que anteriormente producía una violación de segmento. Para esto, he añadido comprobaciones específicas en el cliente que garantizan su correcto funcionamiento en todas las acciones. Después de verificar que todo funciona como se espera, puedo dar por finalizado el **Entregable 1** y empezar con el **Entregable 2**.

### Nuevos archivos
He creado los siguientes archivos para este entregable:

- **`config.yaml`**: Archivo de configuración en formato YAML donde describo las características del servidor Kafka.
- **`PruebaKafka.py`**: Archivo Python que carga la configuración del servidor Kafka y lanza el cliente Kafka que he desarrollado para procesar las operaciones.
- **`kafka_client.py`**: Archivo Python donde he implementado todas las operaciones necesarias para recibir, procesar, ejecutar y devolver las respuestas a las operaciones introducidas.

### Configuración del servidor Kafka
Como Kafka no está instalado como un programa del sistema, lo primero que he hecho ha sido moverme manualmente a la ubicación donde se encuentran los scripts y binarios necesarios para ejecutar Kafka:
```
    cd kafka_2.13-3.9.0/bin
```
Todas las terminales que he utilizado parten de este directorio, ya que aquí se encuentran los scripts para iniciar los servidores, crear topics y gestionar consumidores y productores.

*Inicio de servicios*

    En la primera terminal, he iniciado Zookeeper, que es un servicio necesario para que Kafka coordine internamente:
    ```
        ./zookeeper-server-start.sh ../config/zookeeper.properties
    ```
    En una segunda terminal, he iniciado el servidor Kafka, que es el componente encargado de almacenar y gestionar los mensajes que los productores envían y los consumidores leen:
    ```
        ./kafka-server-start.sh ../config/server.properties
    ```

*Creación de topics*

Después de iniciar los servicios, he creado los topics necesarios en Kafka, según las indicaciones del enunciado:

    operations: Topic donde envío las operaciones a procesar.
    results: Topic donde Kafka publica las respuestas procesadas.

Esto lo he hecho desde una misma terminal utilizando los siguientes comandos:
```
    ./kafka-topics.sh --create --topic operations --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
    ./kafka-topics.sh --create --topic results --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
    ./kafka-topics.sh --list --bootstrap-server localhost:9092
```
He utilizado --list para verificar que los topics se han creado correctamente. Una vez creados, no he necesitado volver a hacerlo.

*Uso de productor y consumidor*

He configurado el flujo de mensajes de la siguiente manera:

Productor Kafka:
    En una terminal, he lanzado un productor que publica mensajes en el topic operations. He utilizado este comando:
    ```
        ./kafka-console-producer.sh --topic operations --bootstrap-server localhost:9092
    ```
    En esta terminal, voy escribiendo mensajes en formato JSON, como el siguiente ejemplo:

    {"operations": [{"id": "1", "object_identifier": "my_list", "object_type": "RList", "operation": "append", "args": {"item": "apple"}}]}

    He tenido en cuenta que algunas operaciones no necesitan la clave opcional args, como length, hash e identifier.

Consumidor Kafka:
    En otra terminal, he lanzado un consumidor que lee los mensajes procesados del topic results:
    ```
        ./kafka-console-consumer.sh --topic results --from-beginning --bootstrap-server localhost:9092
    ```
    En esta terminal, voy obteniendo las respuestas generadas por el cliente Kafka.

### Manual usuario
*Lanzar servicios*

    Primero, he lanzado el servidor Ice, el servidor Kafka ya lo debo tener operativo, como lo hacía en el primer entregable. Esto lo he hecho desde una terminal independiente con el comando:
    ```
        remotetypes --Ice.Config=config/remotetypes.config
    ```
    Luego, he lanzado el archivo PruebaKafka.py, que carga la configuración del servidor Kafka e inicializa el cliente:
    ```
        python3 PruebaKafka.py
    ```
    El cual si no se encuentra el servidor kafka en activo, no se ejecutará correctamente.

*Flujo de trabajo*

    En el topic operations, he añadido operaciones para que el cliente Kafka las procese.
    Los resultados generados se publican en el topic results, pero la salida final que considero válida es la que se muestra en la terminal del cliente Kafka, gracias al uso de consumer groups. Este mecanismo asegura que múltiples instancias del cliente no procesen el mismo mensaje simultáneamente.
    Tanto el servidor Ice como el cliente Kafka se ejecutan en terminales independientes.

### Ejemplos de operaciones probadas
He probado múltiples operaciones en los objetos RList, RSet y RDict, y funcionan correctamente. Todas las operaciones inválidas, como iter, generan errores apropiados, cumpliendo con los requisitos del enunciado.

#### OPERACIONES PARA LA RLIST:
```
{"operations": [{"id": "1", "object_identifier": "my_list", "object_type": "RList", "operation": "append", "args": {"item": "apple"}}]}
{"operations": [{"id": "7", "object_identifier": "my_list", "object_type": "RList", "operation": "append", "args": {"item": "orange"}}]}
{"operations": [{"id": "2", "object_identifier": "my_list", "object_type": "RList", "operation": "append", "args": {"item": "banana"}}]}
{"operations": [{"id": "3", "object_identifier": "my_list", "object_type": "RList", "operation": "length"}]}
{"operations": [{"id": "4", "object_identifier": "my_list", "object_type": "RList", "operation": "contains", "args": {"item": "apple"}}]}
{"operations": [{"id": "5", "object_identifier": "my_list", "object_type": "RList", "operation": "contains", "args": {"item": "grape"}}]}
{"operations": [{"id": "6", "object_identifier": "my_list", "object_type": "RList", "operation": "remove", "args": {"item": "banana"}}]} 
{"operations": [{"id": "7", "object_identifier": "my_list", "object_type": "RList", "operation": "remove", "args": {"item": "orange"}}]}
{"operations": [{"id": "8", "object_identifier": "my_list", "object_type": "RList", "operation": "hash"}]}
{"operations": [{"id": "9", "object_identifier": "my_list", "object_type": "RList", "operation": "hash"}]}
{"operations": [{"id": "10", "object_identifier": "my_list", "object_type": "RList", "operation": "pop", "args": {}}]}
{"operations": [{"id": "11", "object_identifier": "my_list", "object_type": "RList", "operation": "pop", "args": {"index": 0}}]}
{"operations": [{"id": "12", "object_identifier": "my_list", "object_type": "RList", "operation": "pop", "args": {"index": 5}}]}
{"operations": [{"id": "13", "object_identifier": "my_list", "object_type": "RList", "operation": "getItem", "args": {"index": 0}}]}
{"operations": [{"id": "14", "object_identifier": "my_list", "object_type": "RList", "operation": "getItem", "args": {"index": 10}}]}
{"operations": [{"id": "15", "object_identifier": "my_list", "object_type": "RList", "operation": "getItem", "args": {"index": 1}}]}
{"operations": [{"id": "16", "object_identifier": "my_list", "object_type": "RList", "operation": "pop", "args": {"index": -1}}]}
{"operations": [{"id": "1", "object_identifier": "prueba1", "object_type": "RList", "operation": "identifier"}]}
{"operations": [{"id": "1", "object_identifier": "my_list", "object_type": "RList", "operation": "iter"}]}
```

#### OPERACIONES PARA LA RSET:
```
{"operations": [{"id": "1", "object_identifier": "my_set", "object_type": "RSet", "operation": "add", "args": {"item": "apple"}}]}
{"operations": [{"id": "2", "object_identifier": "my_set", "object_type": "RSet", "operation": "add", "args": {"item": "banana"}}]}
{"operations": [{"id": "7", "object_identifier": "my_set", "object_type": "RSet", "operation": "add", "args": {"item": "orange"}}]}
{"operations": [{"id": "3", "object_identifier": "my_set", "object_type": "RSet", "operation": "length"}]}
{"operations": [{"id": "4", "object_identifier": "my_set", "object_type": "RSet", "operation": "contains", "args": {"item": "apple"}}]}
{"operations": [{"id": "5", "object_identifier": "my_set", "object_type": "RSet", "operation": "contains", "args": {"item": "grape"}}]}
{"operations": [{"id": "6", "object_identifier": "my_set", "object_type": "RSet", "operation": "remove", "args": {"item": "banana"}}]}
{"operations": [{"id": "7", "object_identifier": "my_set", "object_type": "RSet", "operation": "remove", "args": {"item": "orange"}}]}
{"operations": [{"id": "8", "object_identifier": "my_set", "object_type": "RSet", "operation": "hash"}]}
{"operations": [{"id": "9", "object_identifier": "my_set", "object_type": "RSet", "operation": "hash"}]}
{"operations": [{"id": "10", "object_identifier": "my_set", "object_type": "RSet", "operation": "pop", "args": {}}]}
{"operations": [{"id": "1", "object_identifier": "my_set", "object_type": "RSet", "operation": "identifier"}]}
{"operations": [{"id": "1", "object_identifier": "my_set", "object_type": "RSet", "operation": "iter"}]}
```
#### OPERACIONES PARA RDICT:
```
{"operations": [{"id": "1", "object_identifier": "my_dict", "object_type": "RDict", "operation": "setItem", "args": {"item": "apple", "value": "10"}}]}
{"operations": [{"id": "2", "object_identifier": "my_dict", "object_type": "RDict", "operation": "setItem", "args": {"item": "banana", "value": "20"}}]}
{"operations": [{"id": "3", "object_identifier": "my_dict", "object_type": "RDict", "operation": "length"}]}
{"operations": [{"id": "4", "object_identifier": "my_dict", "object_type": "RDict", "operation": "contains", "args": {"item": "apple"}}]}
{"operations": [{"id": "5", "object_identifier": "my_dict", "object_type": "RDict", "operation": "contains", "args": {"item": "grape"}}]}
{"operations": [{"id": "6", "object_identifier": "my_dict", "object_type": "RDict", "operation": "remove", "args": {"item": "apple"}}]}
{"operations": [{"id": "7", "object_identifier": "my_dict", "object_type": "RDict", "operation": "remove", "args": {"item": "orange"}}]}
{"operations": [{"id": "8", "object_identifier": "my_dict", "object_type": "RDict", "operation": "hash"}]}
{"operations": [{"id": "9", "object_identifier": "my_dict", "object_type": "RDict", "operation": "hash"}]}
{"operations": [{"id": "10", "object_identifier": "my_dict", "object_type": "RDict", "operation": "getItem", "args": {"item": "apple"}}]}
{"operations": [{"id": "11", "object_identifier": "my_dict", "object_type": "RDict", "operation": "getItem", "args": {"item": "grape"}}]}
{"operations": [{"id": "12", "object_identifier": "my_dict", "object_type": "RDict", "operation": "pop", "args": {"item": "apple"}}]}
{"operations": [{"id": "13", "object_identifier": "my_dict", "object_type": "RDict", "operation": "pop", "args": {"item": "grape"}}]}
{"operations": [{"id": "14", "object_identifier": "my_dict", "object_type": "RDict", "operation": "getItem", "args": {"item": "banana"}}]}
{"operations": [{"id": "15", "object_identifier": "my_dict", "object_type": "RDict", "operation": "setItem", "args": {"item": "banana", "value": "25"}}]}
{"operations": [{"id": "16", "object_identifier": "my_dict", "object_type": "RDict", "operation": "setItem", "args": {"item": "apple", "value": "15"}}]}
{"operations": [{"id": "1", "object_identifier": "Dicc", "object_type": "RDict", "operation": "identifier"}]}
{"operations": [{"id": "1", "object_identifier": "Conjunto", "object_type": "RDict", "operation": "iter"}]}
```

#### OPERACIONES FALTANDO ELEMENTOS CLAVES:
En este caso ha sido comprobado que no se llega a ejecutar la operación, es descartada.

```
{"operations": [{"object_identifier": "Dicc", "object_type": "RDict", "operation": "identifier"}]}
{"operations": [{"id": "1", "object_type": "RDict", "operation": "identifier"}]}
{"operations": [{"id": "1", "object_identifier": "Dicc", "operation": "identifier"}]}
{"operations": [{"id": "1", "object_identifier": "Dicc", "object_type": "RDict"}]}
```

## Mejoras

Tras verlo detenidamente me he dado cuenta que de la forma que yo comprobaba sus funcionalidades era local, lo cual no era lo que se me pedía. Por lo que he eliminado las pruebas locales que había creado para el servidor, y a su vez he creado un cliente que pudiera comunicarse con el servidor y realizar acciones. 

Lo cual al inicio, bien como me esperaba me saltaba todo el rato error, pero tras las modificaciones pertinentes de convertir objetos de un tipo que la clase factory no pedía. Tras arreglarlo y vlver a ejecutar mi cliente, ahora si me funcionaba correctamente el servidor.

Su funcionamiento es simplemente:
```
slice2py -I. remotetypes.ice
```
Tras ello lanzamos el servidor: 
```
remotetypes --Ice.Config=config/remotetypes.config
```
Y con ello el cliente, sabiendo que si el servidor no esta activo nuestro cliente no ejecutará:
```
python3 Cliente.py
```
La simplicidad de la ejecución del cliente se debe a que ya dentro del propio código he facilitado la configuración de mi servidor, para que sepa donde se debe conectar: 
```

    proxy_string = "factory:default -p 10000"
    print(f"Usando el proxy: {proxy_string}")

    try:
        proxy = self.communicator().stringToProxy(proxy_string)
    except Exception as e:
        print(f"Error al crear el proxy: {e}")
        return -1

    factory = rt.FactoryPrx.checkedCast(proxy)
    if not factory:
        print("No se pudo conectar con el servidor.")
        return -1
```
Sabiendo que mi archivo de configuración sigue siendo el mismo del principio:
```
remotetypes.Endpoints=tcp -p 10000
```
Añadir que he eliminado las pruebas que se hacía de forma local, dejando solo este cliente como prueba del funcionamiento del servidor.

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

Dado que el servidor (activo) no se incluye en el repositorio, esta prueba no se añadió directamente al directorio /tests. Esto evita errores en sistemas donde el servidor no está configurado o en ejecución. Sin embargo, la prueba ha sido validada localmente y funciona correctamente bajo las condiciones especificadas en el archivo requisitos.md.

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
