#this is the function that initializes the application and sets up a lot of the necessary functions that are used throughout the application.

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

#this is the function that sets up and initializes the app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1234567890'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
     
    from .views import views #importing the views function from the views folder
    from .auth import auth #importing the auth function from the auth
  
    app.register_blueprint(views, url_prefix= '/')
    app.register_blueprint(auth, url_prefix= '/')
        
    from .models import User, Note

    create_database(app) 

#setting up the login manager so that users can login to the application
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
            print('Created database')