"""Module containing the handler functions for CLI commands."""

import logging
import os
import sys
import yaml
from remotetypes.kafka_client import KafkaClient

from remotetypes.server import Server


def remotetypes_server() -> None:
    """Handle for running the server for remote types."""
    logging.basicConfig(level=logging.DEBUG)

    cmd_name = os.path.basename(sys.argv[0])

    logger = logging.getLogger(cmd_name)
    logger.info("Running remotetypes server...")

    server = Server()
    sys.exit(server.main(sys.argv))

def kafka_client():
    """Función para inicializar y ejecutar el cliente Kafka."""
    def load_config(file_path: str = "config.yaml") -> dict:
        """Carga la configuración desde un archivo YAML."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No se encuentra el archivo de configuración: {file_path}")
        
        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    logging.basicConfig(level=logging.INFO)
    config = load_config()
    kafka_config = config['kafka']
    remotetypes_config = config['remotetypes']

    client = KafkaClient(
        server=kafka_config['server'],
        input_topic=kafka_config['input_topic'],
        output_topic=kafka_config['output_topic'],
        group_id=kafka_config['group_id'],
        remotetypes_proxy=remotetypes_config['proxy']
    )
    client.consume_messages()
