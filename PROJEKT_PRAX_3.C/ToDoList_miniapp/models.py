from extensions import db
from datetime import datetime



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    photo = db.Column(db.String(80), default= 'default.jpg')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class SavedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_author = db.Column(db.String(80))
    rating = db.Column(db.Integer, nullable = True)
    notes = db.Column(db.Text, nullable= True)
    reading_status = db.Column(db.String(80), nullable=True)