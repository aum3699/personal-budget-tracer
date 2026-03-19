# app/__init__.py - Flask app factory and initialization
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    
    # Use absolute path to avoid permission issues
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'budget.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['CURRENCY_SYMBOL'] = '₹'  # Indian Rupee

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    from .routes import main
    from .auth import auth
    from .admin import admin
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin)

    return app 