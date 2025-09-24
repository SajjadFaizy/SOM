# from flask import Flask
# from config.config import Config
# from .routes import api

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config.FLASK_CONFIG)
#     app.register_blueprint(api)
#     return app

from flask import Flask
from .routes import api
from config.config import Config

def create_app():
    app = Flask(__name__, 
                template_folder='../../templates',
                static_folder='../../static')
    app.config.from_object(Config.FLASK_CONFIG)
    app.register_blueprint(api)
    return app
