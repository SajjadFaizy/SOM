from src.web_interface.app import create_app
from config.logging_config import setup_logger

logger = setup_logger(__name__)

if __name__ == "__main__":
    try:
        app = create_app()
        logger.info("Starting web application...")
        app.run(
            host=app.config.get('HOST', '0.0.0.0'),
            port=app.config.get('PORT', 5000),
            debug=app.config.get('DEBUG', True)
        )
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
