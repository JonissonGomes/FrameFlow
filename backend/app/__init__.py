from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = './uploads'
    app.config['ZIP_FOLDER'] = './zips'
    
    # Importando as rotas
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
