from flask import Flask
from .mon_blueprint import routes_fonction

def create_app():
    server=Flask(__name__)
    mon_blueprint=routes_fonction()

    #On enregistre/importe le blueprint
    server.register_blueprint(mon_blueprint)
    
    return server