from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
    app.config['UPLOAD_FOLDER'] = './uploads'
    app.config['ZIP_FOLDER'] = './zips'
    
    # Importando as rotas
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
