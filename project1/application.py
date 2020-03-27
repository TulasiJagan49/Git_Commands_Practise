import os
import datetime
from passlib.hash import bcrypt
from flask import Flask, session, render_template, request
from flask_session import Session
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_migrate import Migrate

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True,nullable = False)
    name = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False)

    def __init__(self, name, password):
    
        self.name = name
        self.password = bcrypt.encrypt(password)
        self.timestamp = datetime.datetime.now()


@app.route("/")
def index():
    return render_template("index.html", flag = False)

@app.route("/register", methods = ["GET", "POST"])
def register():  
    if request.method == "POST":       
        db.session.add(User(request.form.get("name"), request.form.get("password")))
        return render_template("register.html", flag = True, name = request.form.get("name"))
    return render_template("register.html", flag = False)

@app.route("/admin")
def admin():
    users = User.query.order_by(User.timestamp.desc()).all()
    return render_template("admin.html", users = users)
