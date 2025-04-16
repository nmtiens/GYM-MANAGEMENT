from flask import Flask
from flask_cors import CORS
from .database import init_db
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Initialize database
    init_db()

    


    # Register routes
    register_routes(app)

    return app
