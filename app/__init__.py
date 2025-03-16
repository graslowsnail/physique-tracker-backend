import os
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv

from app.routes.user_routes import user_routes
from app.routes.main_routes import main_routes
from app.routes.pdf_routes import pdf_routes

# Load env variables from .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Get from .env
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Import db after app is created
    from app.models.db import db
    db.init_app(app)
    
    # Initialize migrate
    migrate = Migrate(app, db)
    
    # Import models
    from app.models.user import User
    from app.models.project import Project, PDFPage
    
    # Register Blueprints
    app.register_blueprint(main_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(pdf_routes)
    
    return app

