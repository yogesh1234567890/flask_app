from flask import Flask
from app.utils.config import Config
from app.errors.handlers import register_error_handlers
from app.routes.app_routes import app_routes
from celery import Celery  


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(app_routes, url_prefix='/api/v1')
    register_error_handlers(app)
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
    celery.conf.update(app.config)
    return app, celery

if __name__ == '__main__':
    app, celery = create_app()
    app.run(debug=True, host="0.0.0.0", port=5002)
