
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class students(db.Model):
    id = db.Column(db.Integer, primary_key=True, AUTO_INCREMENT=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    Class = db.Column(db.String(100), nullable=False)
    adm_no = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    blood = db.Column(db.String(100), nullable=False)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True, AUTO_INCREMENT=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)