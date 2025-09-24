import board
import adafruit_dht
from config.logging_config import setup_logger

logger = setup_logger(__name__)

class TemperatureReader:
    def __init__(self, pin=board.D23):
        self.device = adafruit_dht.DHT11(pin)
        
    def read_temperature(self):
        try:
            temperature = self.device.temperature
            logger.info(f"Temperature read: {temperature}°C")
            return temperature
        except RuntimeError as error:
            logger.error(f"Error reading temperature: {error}")
            return None
        
    def cleanup(self):
        self.device.exit()