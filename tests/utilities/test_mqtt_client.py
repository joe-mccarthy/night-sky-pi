from unittest.mock import patch
from src.app.utilities.mqtt_client import publish_message
from src.app.configuration.core_configuration import MQTTConfig


@patch("paho.mqtt.client.Client")
def test_publish_message(mock_client):

    mock_client_instance = mock_client.return_value
    config = MQTTConfig(host="test_host", enabled=True)
    topic = "test/topic"
    message = "test_message"

    publish_message(config, topic, message)

    mock_client_instance.connect.assert_called_once_with("test_host", 1883, 60)
    mock_client_instance.publish.assert_called_once_with(topic, message)
    mock_client_instance.disconnect.assert_called_once()
