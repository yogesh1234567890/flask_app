from flask import Flask
from app.utils.config import Config
from flask_marshmallow import Marshmallow
from app.errors.handlers import register_error_handlers
from app.routes.app_routes import app_routes


ma = Marshmallow()

def create_app(config_class=Config):
    app = Flask(__name__)
    ma.init_app(app)
    app.register_blueprint(app_routes, url_prefix='/api/v1')
    register_error_handlers(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    