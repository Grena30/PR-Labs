from flask import Flask
from raft import *
from models.database import db
from flask_swagger_ui import get_swaggerui_blueprint
from models.electro_scooter import ElectroScooter

import threading
import random
import time

service_info = {
    "host": "127.0.0.1",
    "port": 8001,
}


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    SWAGGER_URL = "/swagger"
    API_URL = "/static/swagger.json"

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Access API'
        }
    )

    print("Starting service...")
    time.sleep(random.randint(1, 3))

    crud = Raft(service_info).get_crud_object()

    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    import routes

    app.run(host=service_info["host"],
            port=service_info["port"])
