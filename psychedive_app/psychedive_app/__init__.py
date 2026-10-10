"""PsycheDive application factory."""
from pathlib import Path

from flask import Flask, request

from config import Config

STATIC_DIR = Path(__file__).resolve().parent.parent / 'static'


def create_app(config_object=Config) -> Flask:
    app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path='/static')
    app.config['PDA'] = config_object
    app.config['JSON_SORT_KEYS'] = False

    from .routes import bp as api_bp
    app.register_blueprint(api_bp)

    @app.get('/')
    def index():
        # the whole app is the single HTML file
        return app.send_static_file('psychedive.html')

    @app.get('/healthz')
    def healthz():
        return {'ok': True, 'version': config_object.APP_VERSION}

    if getattr(config_object, 'CORS', True):
        @app.after_request
        def _cors(response):
            origin = request.headers.get('Origin', '')
            allowed = getattr(config_object, 'ALLOWED_ORIGINS', [])
            if getattr(config_object, 'PUBLIC_MODE', False):
                if origin and origin in allowed:
                    response.headers.setdefault('Access-Control-Allow-Origin', origin)
            else:
                response.headers.setdefault('Access-Control-Allow-Origin', '*')
            response.headers.setdefault(
                'Access-Control-Allow-Headers', 'Content-Type, Authorization')
            response.headers.setdefault(
                'Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            return response

    return app
