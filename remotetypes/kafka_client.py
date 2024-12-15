import json
from confluent_kafka import Consumer, Producer, KafkaException, KafkaError
import logging
import sys
import Ice
from typing import List
Ice.loadSlice("remotetypes.ice")
import RemoteTypes as rt  # type: ignore

class KafkaClient:
    def __init__(self, server: str, input_topic: str, output_topic: str, group_id: str):
        self.server = server
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.group_id = group_id

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
                    event = json.loads(raw_message)
                    self.logger.info("Evento recibido: %s", event)
                    self.process_event(event)
                except json.JSONDecodeError as e:
                    self.logger.error(f"Error al procesar el JSON: {e}")
                    continue
                self.consumer.commit()
            except Exception as e:
                self.logger.error(f"Error al consumir mensajes: {e}")

    def process_event(self, event: dict):
        responses = []
        operations = event.get("operations", [])
        if not operations:
            self.logger.error("No se encontraron operaciones en el evento")
            return

        for operation in operations:
            

            try:
                if not self.validate_operation_format(operation):
                    self.logger.info(f"Operación descartada: {operation}")
                    continue 
                    
                self.validate_operation_format(operation)
                response = self.execute_operation(operation)
                responses.append(response)  

                
            except Exception as e:
                responses.append({
                    "id": operation.get("id", "unknown"),
                    "status": "error",
                    "error": str(type(e).__name__)
                })

        self.publish_responses(responses)

    def validate_operation_format(self, operation: dict):
        if "id" not in operation:
            self.logger.warning(f"Operación descartada por falta de 'id': {operation}")
            return False
        
        required_fields = ["object_identifier", "object_type", "operation"] 
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
                proxy = communicator.stringToProxy("factory:default -p 10000")
                factory = rt.FactoryPrx.checkedCast(proxy)
                if not factory:
                    raise RuntimeError("No se pudo conectar con el servidor remoto.")

                obj_type_enum = getattr(rt.TypeName, object_type)
                obj_proxy = factory.get(obj_type_enum, object_identifier)

                obj = getattr(rt, f"{object_type}Prx").checkedCast(obj_proxy)
                if not obj:
                    raise ValueError(f"No se pudo obtener el proxy del objeto {object_identifier} de tipo {object_type}.")

                self.logger.info(f"Ejecutando operación '{op_name}' en '{object_identifier}' con argumentos: {args}")

                if object_type == "RDict":
                    result = self.execute_rdict_operation(obj, op_name, args)
                    
                elif object_type == "RList":
                    result = self.execute_rlist_operation(obj, op_name, args)
             
                elif object_type == "RSet":
                    result = self.execute_rset_operation(obj, op_name, args)    
                  
                else:
                    raise ValueError(f"Operación no soportada para el tipo de objeto {object_type}")

                return {
                    "id": operation["id"],
                    "status": "ok",
                    "result": result
                }
        except Exception as e:
            self.logger.error(f"Error al ejecutar la operación: {e}")
            return {
                "id": operation["id"],
                "status": "error",
                "error": str(e)
            }

    def execute_rdict_operation(self, obj, op_name, args):
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


    def execute_rlist_operation(self, obj, op_name, args):
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

    def execute_rset_operation(self, obj, op_name, args):
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

    def publish_responses(self, responses: List[dict]):
        try:
            message = json.dumps({"responses": responses}).encode("utf-8")
            self.producer.produce(self.output_topic, value=message)
            self.producer.flush()
            self.logger.info(f"Respuestas publicadas: {responses}")
        except KafkaException as e:
            self.logger.error(f"Error al publicar la respuesta: {e}")
