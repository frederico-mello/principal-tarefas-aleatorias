from flask import Flask
from .database import db  

def create_app():
    app = Flask(__name__)
    
    # Configurações do app
    app.config['SECRET_KEY'] = 'orgbira2'  
    
    # Registrar blueprints
    from . import routes
    app.register_blueprint(routes.bp)
    
    return app