from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Pridaj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazov = db.Column(db.String(100), nullable=False)
    ohodnot = db.Column(db.String(50), nullable=False)
    teren = db.Column(db.String(50), nullable=False)
    pocasie = db.Column(db.String(50), nullable=False)
    popis = db.Column(db.Text, nullable=False)
    datum_pridania = db.Column(db.DateTime, default=datetime.utcnow)
