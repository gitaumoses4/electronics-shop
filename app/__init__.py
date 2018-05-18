from flask import Flask
from routes import api, web
from config import app_config

app = Flask(__name__, instance_relative_config=True)


def create_app(config_name="DEVELOPMENT"):
    app.config.from_object(app_config[config_name])

    api.create_api(app)
    web.create_routes(app)

    return app
