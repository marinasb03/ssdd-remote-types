"""Cliente kafka."""
import json
from confluent_kafka import Consumer, Producer, KafkaException, KafkaError
import logging
import sys
import Ice
from typing import List, Dict
import os
ICE_FILE = os.path.join(os.path.dirname(__file__), "remotetypes.ice")
Ice.loadSlice(ICE_FILE)
import RemoteTypes as rt  # type: ignore


class KafkaClient:
    """Clase Cliente Kafka."""
    def __init__(self, server: str, input_topic: str, output_topic: str, group_id: str, remotetypes_proxy: str):
        """Inicialización."""
        self.server = server
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.group_id = group_id
        self.remotetypes_proxy = remotetypes_proxy

        self.consumer = Consumer({
            'bootstrap.servers': self.server,
            'group.id': self.group_id,
            'enable.auto.commit': False,
            'auto.offset.reset': 'earliest',
        })

        self.producer = Producer({'bootstrap.servers': self.server})
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def consume_messages(self):
        """Consume y procesa mensajes del topic de entrada."""
        self.consumer.subscribe([self.input_topic])
        while True:
            try:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        raise KafkaException(msg.error())

                raw_message = msg.value().decode('utf-8')
                self.logger.info(f"Mensaje recibido (raw): {raw_message}")

                try:
                    events = json.loads(raw_message)
                    if not isinstance(events, list):
                        raise ValueError("El mensaje recibido no es un array.")
                    self.process_events(events)
                except json.JSONDecodeError as e:
                    self.logger.error(f"Error al procesar el JSON: {e}")
                    continue
                except ValueError as e:
                    self.logger.error(f"Formato incorrecto: {e}")
                    continue

                self.consumer.commit()
            except Exception as e:
                self.logger.error(f"Error al consumir mensajes: {e}")

    def process_events(self, events: List[dict]):
        """Procesa."""
        responses = []
        for operation in events:
            try:
                if not self.validate_operation_format(operation):
                    self.logger.info(f"Operación descartada: {operation}")
                    continue
                response = self.execute_operation(operation)
                responses.append(response)
            except Exception as e:
                responses.append({
                    "id": operation.get("id", "unknown"),
                    "status": "error",
                    "error": str(e)
                })

        self.publish_responses(responses)

    def validate_operation_format(self, operation: dict) -> bool:
        """Valida Operaciones."""
        required_fields = ["id", "object_identifier", "object_type", "operation"]
        for field in required_fields:
            if field not in operation:
                raise ValueError(f"Campo requerido '{field}' faltante en la operación.")

        if operation["operation"] in ["add", "remove", "setItem", "getItem", "pop", "contains", "append"]:
            if "args" not in operation:
                raise ValueError(f"La operación '{operation['operation']}' requiere argumentos.")

        return True

    def execute_operation(self, operation: dict):
        """Ejecuta una operación invocando al servidor remoto."""
        object_type = operation["object_type"]
        object_identifier = operation["object_identifier"]
        op_name = operation["operation"]
        args = operation.get("args", {})

        try:
            with Ice.initialize(sys.argv) as communicator:
                proxy = communicator.stringToProxy(self.remotetypes_proxy)
                factory = rt.FactoryPrx.checkedCast(proxy)
                if not factory:
                    raise RuntimeError("No se pudo conectar con el servidor remoto.")

                obj_type_enum = getattr(rt.TypeName, object_type)
                obj_proxy = factory.get(obj_type_enum, object_identifier)

                obj = getattr(rt, f"{object_type}Prx").checkedCast(obj_proxy)
                if not obj:
                    raise ValueError(f"No se obtuvo el proxy del objeto {object_identifier} de tipo {object_type}.")

                self.logger.info(f"Ejecutando operación '{op_name}' en '{object_identifier}' con argumentos: {args}")

                handler_class = OperationHandlerFactory.get_handler(object_type)
                result = handler_class.execute(obj, op_name, args)

                # Retorno en caso de éxito
                return {
                    "id": operation["id"],
                    "status": "ok",
                    "result": result if result is not None else None
                }

        except Exception as e:
            # Retorno en caso de error
            self.logger.error(f"Error al ejecutar la operación: {e}")
            return {
                "id": operation["id"],
                "status": "error",
                "error": str(e)
            }


    def publish_responses(self, responses: List[dict]):
        """Publica las respuestas."""
        try:
            message = json.dumps(responses).encode("utf-8")
            self.producer.produce(self.output_topic, value=message)
            self.producer.flush()
            self.logger.info(f"Respuestas publicadas: {responses}")
        except KafkaException as e:
            self.logger.error(f"Error al publicar la respuesta: {e}")


class OperationHandlerFactory:
    """Fábrica para obtener el manejador de operaciones adecuado según el tipo."""

    @staticmethod
    def get_handler(object_type: str):
        """Get handler."""
        if object_type == "RDict":
            return RDictHandler()
        elif object_type == "RList":
            return RListHandler()
        elif object_type == "RSet":
            return RSetHandler()
        else:
            raise ValueError(f"Tipo de objeto no soportado: {object_type}")


class RDictHandler:
    """Clase RDict."""

    def execute(self, obj, op_name, args):
        """Ejecución operaciones de Dict."""
        if op_name == "remove":
            try:
                obj.remove(args["item"])
                return args["item"]
            except KeyError:
                raise KeyError("Elemento no encontrado en el RDict")
        elif op_name == "length":
            return obj.length()
        elif op_name == "contains":
            return obj.contains(args["item"])
        elif op_name == "hash":
            return obj.hash()
        elif op_name == "identifier":
            return obj.identifier()
        elif op_name == "setItem":
            obj.setItem(args["item"], args["value"])
            return (args["item"],args["value"])
        elif op_name == "getItem":
            return obj.getItem(args["item"])
        elif op_name == "pop":
            return obj.pop(args["item"])

        else:
            raise ValueError(f"OperationNotSupported: {op_name}")
        pass

class RListHandler:
    """Clase RList."""

    def execute(self, obj, op_name, args):
        """Ejecución operaciones de List."""
        if op_name == "remove":
            try:
                obj.remove(args["item"])
                return args["item"]
            except KeyError:
                raise KeyError("Elemento no encontrado en el RList")
        elif op_name == "length":
            return obj.length()
        elif op_name == "contains":
            return obj.contains(args["item"])
        elif op_name == "hash":
            return obj.hash()
        elif op_name == "identifier":
            return obj.identifier()
        elif op_name == "append":
            obj.append(args["item"])
            return args["item"]
        elif op_name == "pop":
            if "index" in args:
                return obj.pop(args["index"])
            else:
                return obj.pop()
        elif op_name == "getItem":
            return obj.getItem(args["index"])
        else:
            raise ValueError(f"OperationNotSupported: {op_name}")
        pass

class RSetHandler:
    """Clase RSet."""

    def execute(self, obj, op_name, args):
        """Ejecución operaciones Set."""
        if op_name == "remove":
            try:
                obj.remove(args["item"])
                return args["item"]
            except KeyError:
                raise KeyError("Elemento no encontrado en el RSet")
        elif op_name == "length":
            return obj.length()
        elif op_name == "contains":
            return obj.contains(args["item"])
        elif op_name == "hash":
            return obj.hash()
        elif op_name == "identifier":
            return obj.identifier()
        elif op_name == "add":
            obj.add(args["item"])
            return args["item"]
        elif op_name == "pop":
            return obj.pop()
        else:
            raise ValueError(f"OperationNotSupported: {op_name}")
        pass
