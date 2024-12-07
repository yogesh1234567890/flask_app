from flask import Flask
from app.utils.config import Config
from app.errors.handlers import register_error_handlers
from app.routes.app_routes import app_routes
from app.utils.swagger import swagger_ui_blueprint, SWAGGER_URL
from celery import Celery  


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(app_routes, url_prefix='/api/v1')
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    register_error_handlers(app)
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
    celery.conf.update(app.config)
    return app, celery


app, celery_app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)
