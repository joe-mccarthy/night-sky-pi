import paho.mqtt.client as mqtt
from ..configuration.core_configuration import MQTTConfig

def publish_message(config:MQTTConfig, topic:str, message:str) -> None:
    """
    Publishes a message to an MQTT broker.

    Args:
        config (MQTTConfig): The MQTT configuration object.
        topic (str): The topic to publish the message to.
        message (str): The message to be published.

    Returns:
        None
    """
    client = mqtt.Client()
    client.connect(config.host, 1883, 60)
    client.publish(topic, message)
    client.disconnect()