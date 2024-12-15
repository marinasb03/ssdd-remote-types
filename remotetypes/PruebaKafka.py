import yaml
import os
from remotetypes.kafka_client import KafkaClient

def load_config(file_path: str = "config.yaml") -> dict:
    """Carga la configuración desde un archivo YAML."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encuentra el archivo de configuración: {file_path}")
    
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


if __name__ == "__main__":

    config = load_config()
    kafka_config = config['kafka']

    client = KafkaClient(
        server=kafka_config['server'],
        input_topic=kafka_config['input_topic'],
        output_topic=kafka_config['output_topic'],
        group_id=kafka_config['group_id']
    )
    client.consume_messages()
