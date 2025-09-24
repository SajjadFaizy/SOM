from src.data_collection.temperature_reader import TemperatureReader
from src.data_collection.mqtt_publisher import MQTTPublisher
from config.logging_config import setup_logger
import time

logger = setup_logger(__name__)

def main():
    reader = TemperatureReader()
    publisher = MQTTPublisher()
    
    logger.info("Starting temperature reading from sensor...")
    try:
        while True:
            temperature = reader.read_temperature()
            if temperature is not None:
                publisher.publish_temperature(temperature)
            time.sleep(1)
    except KeyboardInterrupt:
        reader.cleanup()
        logger.info("Program stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        reader.cleanup()

if __name__ == "__main__":
    main()
