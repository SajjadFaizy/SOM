import paho.mqtt.client as mqtt
import re
from datetime import datetime
from collections import deque
from config.config import Config
from config.logging_config import setup_logger

logger = setup_logger(__name__)

class TemperatureSubscriber:
    def __init__(self):
        self.config = Config.MQTT_CONFIG
        self.temperature_data = deque(
            maxlen=Config.TEMP_CONFIG["WINDOW_SIZE"]
        )
        self.client = mqtt.Client()
        self._setup_client()
        self.last_connection_code = 0
        
    def _setup_client(self):
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
    def _on_connect(self, client, userdata, flags, rc):
        self.last_connection_code = rc
        logger.info(f"Connected with result code {rc}")
        self.client.subscribe(self.config["TOPIC"])
        
    def _on_message(self, client, userdata, msg):
        try:
            match = re.search(r"Temp:(\d+\.\d+)°C", msg.payload.decode())
            if match:
                temperature = float(match.group(1))
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.temperature_data.append({
                    "time": timestamp,
                    "temp": temperature
                })
                logger.info(f"Received temperature: {temperature}°C")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            
    def start(self):
        try:
            self.client.connect(
                self.config["BROKER"],
                self.config["PORT"],
                self.config["KEEPALIVE"]
            )
            self.client.loop_start()
        except Exception as e:
            logger.error(f"Error starting subscriber: {e}")
            
    def get_temperature_data(self):
        return list(self.temperature_data)
