import os, datetime, logging
from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from objects import User, Book
from bookpage import getbook

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/")
def index():

    if(session.get("name") != None):
        return render_template("index.html", flag = True, name = session.get("name"))
    return render_template("/index.html", flag = False,
     message = """ You have to login to continue...Please access the link provided below or navigate through the nav bar.""")

@app.route("/register", methods = ["GET", "POST"])
def register():  

    # If the user fills the form and submits it.
    if request.method == "POST":

        # Checking whether all the fields are filled.
        if not request.form.get("name"):
            return render_template("error.html", message="Please provide User name.",prev_page="register")
        if not request.form.get("password"):
            return render_template("error.html", message="Please provide Password.",prev_page="register")

        # Trying to see whether the user is already present or not. If present
        # will ask the user to login.
        try:
            existing = User.query.filter_by(name=request.form.get("name")).one()
            return render_template("register.html", flag = True,
                name = request.form.get("name"),
                message = """It seems like you are already a
                 registered user with us. Please use login button next time.""")

        # If the user is not added to our we will add that person to the
        # database.
        except:
            try:  
                # print(request.form.get("name"))
                # print(request.form.get("password"))
                db.session.add(User(request.form.get("name"),
                 request.form.get("password")))
                db.session.commit()

                os.system("flask db migrate")
                os.system("flask db upgrade")

                return render_template("register.html", flag = True,
                        name = request.form.get("name"),
                        message = """Aww yeah, you successfully registered
                         for this application.""")
            except Exception as ex:
                db.session.rollback()
                return render_template("error.html", flag = False,
                    message = """There was some error on our side. 
                    Please try registering again.""", prev_page = "register") 
                       # This is the for get request to present the register page.
    return render_template("register.html", flag = False, message = "")

@app.route("/admin")
def admin():
    # This method shows all the users in a table format.
    users = User.query.order_by(User.timestamp.desc()).all()
    return render_template("admin.html", users = users)

@app.route("/auth", methods = ["POST"])
def auth():

    # Tries to see whether the user provided the details correct or not.
    # Otherwise will redirect to login page.
    if request.method == "POST":
        try:
            session['name'] = request.form.get("name")
            
            if not session['name']:
                return render_template("error.html", message="Please provide User name.")
            if not request.form.get("password"):
                return render_template("error.html", message="Please provide Password.")
            data = User.query.filter_by(name=session['name']).one()
            
            if check_password_hash(data.password, request.form.get("password")):
                return redirect("/")
            else:
                return render_template("error.html",
                    message = """Invalid Username and(or) password""")
        except:
            session.clear()
            return render_template("error.html", 
                message = """You might not be registered user. Please register first""")

# For this task-2 already session is created and 
# now in this route is cleared.
@app.route("/logout")
def logout():
    """ Log user out """

    # Forget any user ID
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/book/<id>",methods=['GET'])
def book(id):
    book = getbook(id)
    return render_template("book.html",book=book)
