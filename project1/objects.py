from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True,nullable = False)
    name = db.Column(db.String, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False)

    def __init__(self, name, password):
        self.name = name
        self.password = generate_password_hash(password)
        self.timestamp = datetime.datetime.now()

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    isbn = db.Column(db.String, nullable = False)
    title = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    year = db.Column(db.Integer, nullable = False)

    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year