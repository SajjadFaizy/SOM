import paho.mqtt.client as mqtt
from config.config import Config
from config.logging_config import setup_logger

logger = setup_logger(__name__)

class MQTTPublisher:
    def __init__(self):
        self.client = mqtt.Client()
        self.config = Config.MQTT_CONFIG
        self._connect()
    
    def _connect(self):
        try:
            self.client.connect(
                self.config["BROKER"],
                self.config["PORT"],
                self.config["KEEPALIVE"]
            )
            logger.info("Connected to MQTT broker")
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            
    def publish_temperature(self, temperature):
        if temperature is not None:
            message = f"Temp:{temperature:.1f}°C"
            self.client.publish(self.config["TOPIC"], message)
            logger.info(f"Published: {message}")