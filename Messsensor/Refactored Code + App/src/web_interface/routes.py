from flask import Blueprint, jsonify, render_template
from src.data_processing.mqtt_subscriber import TemperatureSubscriber
from config.logging_config import setup_logger

logger = setup_logger(__name__)
api = Blueprint('api', __name__)
temperature_subscriber = TemperatureSubscriber()
temperature_subscriber.start()

@api.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index page: {e}")
        return jsonify({"error": "Failed to load page"}), 500

@api.route('/data')
def get_temperature_data():
    try:
        data = temperature_subscriber.get_temperature_data()
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error fetching temperature data: {e}")
        return jsonify({"error": "Failed to fetch temperature data"}), 500
