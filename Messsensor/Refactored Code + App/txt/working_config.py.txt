class Config:
    # MQTT Configuration
    MQTT_CONFIG = {
        "BROKER": "localhost",
        "PORT": 1883,
        "TOPIC": "Gruppe2",
        "QOS": 1,
        "KEEPALIVE": 60
    }

    # Temperature Configuration
    TEMP_CONFIG = {
        "MIN_TEMP": 20.0,
        "MAX_TEMP": 30.0,
        "SAMPLE_RATE": 1,  # seconds
        "WINDOW_SIZE": 60  # samples
    }

    # Flask Configuration
    FLASK_CONFIG = {
        "DEBUG": True,
        "HOST": "0.0.0.0",
        "PORT": 5000
    }

# config/logging_config.py
import logging

def setup_logger(name):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
