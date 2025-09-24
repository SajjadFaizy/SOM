from src.data_collection.mqtt_publisher import MQTTPublisher
from config.config import Config
from config.logging_config import setup_logger
import random
import time

logger = setup_logger(__name__)

def main():
    publisher = MQTTPublisher()
    config = Config.TEMP_CONFIG
    
    logger.info("Starting temperature simulation...")
    try:
        while True:
            temperature = random.uniform(
                config["MIN_TEMP"],
                config["MAX_TEMP"]
            )
            publisher.publish_temperature(temperature)
            #time.sleep(config["SAMPLE_RATE"])
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Program stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
