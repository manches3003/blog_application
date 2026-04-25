from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Load .env from project root
project_root = os.path.abspath(os.path.dirname(__file__) + '/..')
load_dotenv(os.path.join(project_root, '.env'))

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    # Get the absolute path to the project root
    project_root = os.path.abspath(os.path.dirname(__file__) + '/..')
    static_folder = os.path.join(project_root, 'static')
    
    print(f"DEBUG: Project root = {project_root}")
    print(f"DEBUG: Static folder = {static_folder}")
    print(f"DEBUG: Static folder exists? {os.path.exists(static_folder)}")
    
    app = Flask(__name__, static_folder=static_folder, static_url_path='/static')
    
    from app.config import config_by_name
    app.config.from_object(config_by_name[config_name])
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.routes.api import api_bp
    from app.routes.web import web_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)
    
    return app