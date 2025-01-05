# Marina Sobrino Blanco
## Mejores Entregable 2
    
1. En mi código actual, me aseguro que el mensaje recibido de Kafka sea un array de objetos JSON (lista de diccionarios). Cada evento recibido se maneja correctamente como una lista de diccionarios.
2. Ya se está publicando directamente el array de respuestas (responses), sin envolverlo en un diccionario. En el código actual, en lugar de enviar un diccionario con la clave "responses", envío directamente el array responses.
3. Actualmente, el proxy al servicio remotetypes ya no está hardcoded en el código. En lugar de definirlo de forma rígida en la línea 109 de kafka_client.py, el proxy ahora se carga de forma configurable desde el archivo config.yaml
4. El código ya tiene una estructura que sigue parcialmente el principio, ya que he encapsulado las operaciones en clases específicas como RDictHandler, RListHandler, y RSetHandler. Además, la fábrica OperationHandlerFactory facilita la elección del manejador adecuado según el tipo de objeto.
5. El proyecto ya tiene el cliente kafka como una entrada en el pyproject.

## Cliente kafka como entrada en el pyproject

Para cumplir con esta tarea, realicé los siguientes pasos:

1. *Migración de Lógica a command_handlers.py:* Primero, trasladé toda la lógica de la clase PruebaKafka.py a la clase command_handlers.py. Este cambio permitió centralizar la gestión del cliente Kafka dentro del archivo command_handlers.py, facilitando su ejecución posterior dentro del flujo del proyecto.

2. *Modificación en el Archivo kafka_client.py:* En el archivo kafka_client.py, tuve que realizar un ajuste específico en la forma en que se carga el archivo remotetypes.ice. Originalmente, el código cargaba el archivo de la siguiente manera:
```
Ice.loadSlice("remotetypes.ice")
```
Sin embargo, debido a la necesidad de gestionar las rutas correctamente en el entorno de ejecución, modifiqué esa línea para utilizar una ruta absoluta.
```
import os
ICE_FILE = os.path.join(os.path.dirname(__file__), "remotetypes.ice")
Ice.loadSlice(ICE_FILE)
```
Esta modificación asegura que la ruta al archivo remotetypes.ice se maneje de manera más robusta, independientemente de dónde se ejecute el script.

3. *Actualización de Dependencias:* Tras realizar los cambios, volví a instalar las dependencias del proyecto para asegurar que todos los ajustes y modificaciones se reflejaran correctamente. Esto lo hice con el siguiente comando:
```
pip install -e .
```

4. *Ejecución del Cliente Kafka:* Finalmente, para ejecutar el cliente Kafka, desde el directorio remotetypes, que es donde se encuentra el archivo de configuración realizo el siguiente comando: 
```
remotetypes-kafka-client config.yaml
```

Con estos pasos, el cliente Kafka está correctamente integrado como entrada en el proyecto y puede ejecutarse directamente desde la ubicación configurada, asegurando la correcta carga de las dependencias y la ejecución del cliente con los parámetros adecuados.


## Entregable 2
### Introducción

Lo primero que he hecho ha sido solucionar el problema con la clase `iterable`, que anteriormente producía una violación de segmento. Para esto, he añadido comprobaciones específicas en el cliente que garantizan su correcto funcionamiento en todas las acciones. Después de verificar que todo funciona como se espera, puedo dar por finalizado el **Entregable 1** y empezar con el **Entregable 2**.

### Nuevos archivos
He creado los siguientes archivos para este entregable:

- **`config.yaml`**: Archivo de configuración en formato YAML donde describo las características del servidor Kafka.
- **`PruebaKafka.py`**: Este archivo Python estaba originalmente encargado de cargar la configuración del servidor Kafka y lanzar el cliente Kafka desarrollado para procesar las operaciones. Sin embargo, he trasladado esta lógica a la clase command_handlers. A pesar de este cambio, he mantenido PruebaKafka.py como una opción adicional para la inicialización del cliente Kafka, de modo que aún se pueda utilizar como una alternativa en caso de ser necesario.
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
    Tras realizar las modificaciones, ahora existe la posibilidad de ejecutar la inicialización del cliente de Kafka de dos maneras diferentes. Originalmente, la ejecución se realizaba mediante el archivo PruebaKafka.py, que carga la configuración del servidor Kafka e inicializa el cliente. Para ejecutarlo de esta forma, se utilizaba el siguiente comando:
    ```
        python3 PruebaKafka.py
    ```
    Sin embargo, con la última modificación que implementé, he adaptado el proceso para que pueda ejecutarse directamente como una entrada desde el pyproject, utilizando el siguiente comando:
    ```
        remotetypes-kafka-client config.yaml
    ```
    De esta forma, ya no es necesario ejecutar el archivo Python directamente. Ahora, la inicialización del cliente está integrada en el pyproject, lo que facilita su ejecución de manera más eficiente.

    Es importante mencionar que, independientemente de la forma de ejecución, en ambos casos, el cliente requiere que el servidor Kafka esté activo para funcionar correctamente. Si el servidor Kafka no está en funcionamiento, la inicialización no se llevará a cabo con éxito en ninguno de los dos métodos.

*Flujo de trabajo*

    En el topic operations, he añadido operaciones para que el cliente Kafka las procese.
    Los resultados generados se publican en el topic results, pero la salida final que considero válida es la que se muestra en la terminal del cliente Kafka, gracias al uso de consumer groups. Este mecanismo asegura que múltiples instancias del cliente no procesen el mismo mensaje simultáneamente.
    Tanto el servidor Ice como el cliente Kafka se ejecutan en terminales independientes.

### Ejemplos de operaciones probadas
He probado múltiples operaciones en los objetos RList, RSet y RDict, y funcionan correctamente. Todas las operaciones inválidas, como iter, generan errores apropiados, cumpliendo con los requisitos del enunciado.

#### OPERACIONES PARA LA RLIST:

```
[{"id": "1", "object_identifier": "my_list", "object_type": "RList", "operation": "append", "args": {"item": "apple"}}, {"id": "7", "object_identifier": "my_list", "object_type": "RList", "operation": "append", "args": {"item": "orange"}}, {"id": "2", "object_identifier": "my_list", "object_type": "RList", "operation": "append", "args": {"item": "banana"}}]
[{"id": "3", "object_identifier": "my_list", "object_type": "RList", "operation": "length"}, {"id": "4", "object_identifier": "my_list", "object_type": "RList", "operation": "contains", "args": {"item": "apple"}}, {"id": "5", "object_identifier": "my_list", "object_type": "RList", "operation": "contains", "args": {"item": "grape"}}]
[{"id": "6", "object_identifier": "my_list", "object_type": "RList", "operation": "remove", "args": {"item": "banana"}}, {"id": "7", "object_identifier": "my_list", "object_type": "RList", "operation": "remove", "args": {"item": "orange"}}, {"id": "8", "object_identifier": "my_list", "object_type": "RList", "operation": "hash"}]
[{"id": "9", "object_identifier": "my_list", "object_type": "RList", "operation": "hash"}, {"id": "10", "object_identifier": "my_list", "object_type": "RList", "operation": "pop", "args": {}}, {"id": "11", "object_identifier": "my_list", "object_type": "RList", "operation": "pop", "args": {"index": 0}}]
[{"id": "12", "object_identifier": "my_list", "object_type": "RList", "operation": "pop", "args": {"index": 5}}, {"id": "13", "object_identifier": "my_list", "object_type": "RList", "operation": "getItem", "args": {"index": 0}}, {"id": "14", "object_identifier": "my_list", "object_type": "RList", "operation": "getItem", "args": {"index": 10}}]
[{"id": "15", "object_identifier": "my_list", "object_type": "RList", "operation": "getItem", "args": {"index": 1}}, {"id": "16", "object_identifier": "my_list", "object_type": "RList", "operation": "pop", "args": {"index": -1}}, {"id": "1", "object_identifier": "prueba1", "object_type": "RList", "operation": "identifier"}]
[{"id": "1", "object_identifier": "my_list", "object_type": "RList", "operation": "iter"}]
```

#### OPERACIONES PARA LA RSET:

```
[{"id": "1", "object_identifier": "my_set", "object_type": "RSet", "operation": "add", "args": {"item": "apple"}}, {"id": "2", "object_identifier": "my_set", "object_type": "RSet", "operation": "add", "args": {"item": "banana"}}, {"id": "7", "object_identifier": "my_set", "object_type": "RSet", "operation": "add", "args": {"item": "orange"}}]
[{"id": "3", "object_identifier": "my_set", "object_type": "RSet", "operation": "length"}, {"id": "4", "object_identifier": "my_set", "object_type": "RSet", "operation": "contains", "args": {"item": "apple"}}, {"id": "5", "object_identifier": "my_set", "object_type": "RSet", "operation": "contains", "args": {"item": "grape"}}]
[{"id": "6", "object_identifier": "my_set", "object_type": "RSet", "operation": "remove", "args": {"item": "banana"}}, {"id": "7", "object_identifier": "my_set", "object_type": "RSet", "operation": "remove", "args": {"item": "orange"}}, {"id": "8", "object_identifier": "my_set", "object_type": "RSet", "operation": "hash"}]
[{"id": "9", "object_identifier": "my_set", "object_type": "RSet", "operation": "hash"}, {"id": "10", "object_identifier": "my_set", "object_type": "RSet", "operation": "pop", "args": {}}, {"id": "1", "object_identifier": "my_set", "object_type": "RSet", "operation": "identifier"}]
[{"id": "1", "object_identifier": "my_set", "object_type": "RSet", "operation": "iter"}] 
```

#### OPERACIONES PARA RDICT:

```
[{"id": "1", "object_identifier": "my_dict", "object_type": "RDict", "operation": "setItem", "args": {"item": "apple", "value": "10"}}, {"id": "2", "object_identifier": "my_dict", "object_type": "RDict", "operation": "setItem", "args": {"item": "banana", "value": "20"}}]
[{"id": "3", "object_identifier": "my_dict", "object_type": "RDict", "operation": "length"}, {"id": "4", "object_identifier": "my_dict", "object_type": "RDict", "operation": "contains", "args": {"item": "apple"}}, {"id": "5", "object_identifier": "my_dict", "object_type": "RDict", "operation": "contains", "args": {"item": "grape"}}]
[{"id": "6", "object_identifier": "my_dict", "object_type": "RDict", "operation": "remove", "args": {"item": "apple"}}, {"id": "7", "object_identifier": "my_dict", "object_type": "RDict", "operation": "remove", "args": {"item": "orange"}}, {"id": "8", "object_identifier": "my_dict", "object_type": "RDict", "operation": "hash"}]
[{"id": "9", "object_identifier": "my_dict", "object_type": "RDict", "operation": "hash"}, {"id": "10", "object_identifier": "my_dict", "object_type": "RDict", "operation": "getItem", "args": {"item": "apple"}}, {"id": "11", "object_identifier": "my_dict", "object_type": "RDict", "operation": "getItem", "args": {"item": "grape"}}]
[{"id": "12", "object_identifier": "my_dict", "object_type": "RDict", "operation": "pop", "args": {"item": "apple"}}, {"id": "13", "object_identifier": "my_dict", "object_type": "RDict", "operation": "pop", "args": {"item": "grape"}}, {"id": "14", "object_identifier": "my_dict", "object_type": "RDict", "operation": "getItem", "args": {"item": "banana"}}]
[{"id": "15", "object_identifier": "my_dict", "object_type": "RDict", "operation": "setItem", "args": {"item": "banana", "value": "25"}}, {"id": "16", "object_identifier": "my_dict", "object_type": "RDict", "operation": "setItem", "args": {"item": "apple", "value": "15"}}, {"id": "1", "object_identifier": "Dicc", "object_type": "RDict", "operation": "identifier"}]
[{"id": "1", "object_identifier": "Conjunto", "object_type": "RDict", "operation": "iter"}]
```

#### OPERACIONES FALTANDO ELEMENTOS CLAVES:
En este caso ha sido comprobado que no se llega a ejecutar la operación, es descartada.

```
[{"object_identifier": "Dicc", "object_type": "RDict", "operation": "identifier"}] 
[{"id": "1", "object_type": "RDict", "operation": "identifier"}]
[{"id": "1", "object_identifier": "Dicc", "operation": "identifier"}]
[{"id": "1", "object_identifier": "Dicc", "object_type": "RDict"}]
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
