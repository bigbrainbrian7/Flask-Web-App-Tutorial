from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os

db = SQLAlchemy()
DB_NAME = "database.db"

DATABASE_FULL_PATH=os.getenv('DATABASE_PATH')+'/'+DB_NAME

def create_app():
    app =Flask(__name__)
    app.config['SECRET_KEY'] = 'vdlkzszSVKDJbwejhf'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_FULL_PATH
    db.init_app(app)

    from .auth import auth
    from .views import views

    from .models import User, Note

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')