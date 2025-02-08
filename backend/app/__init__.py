from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
    
    JWTManager(app)
    mongo = PyMongo(app)
    app.mongo = mongo
    
    # Importando as rotas
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app
