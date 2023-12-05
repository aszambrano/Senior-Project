#This file sets up the database used to allow users to create an account
from . import db
from flask_login import UserMixin
from sqlalchemy .sql import func

class Note(db.Model): #this defining the class note so that users will be able to create entries and add them to the database
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin): #this creates the user class defining their relationship with the Note class 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    first_name = db.Column(db.String(120))
    notes = db.relationship('Note')
