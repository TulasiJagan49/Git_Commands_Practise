import os, datetime, logging, requests
from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from objects import User, Book, db
from book_details import getbookbyid, getbookbyisbn
from search import search_book

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
# db = SQLAlchemy(app)
db.init_app(app)
app.app_context().push()
db.create_all()
# migrate = Migrate(app, db)

@app.route("/")
def index():

    if session.get("name") != None:
        return render_template("index.html", flag=True, name=session.get("name"))
    return render_template("index.html", flag=False,
                           message=""" You have to login to continue...
                           Please access the link
                           provided below or navigate through the nav bar.""")

@app.route("/register", methods=["GET", "POST"])
def register():

    # If the user fills the form and submits it.
    if request.method == "POST":

        # Checking whether all the fields are filled.
        if not request.form.get("name"):
            return render_template("error.html", message="""Please provide
                                    User name.""", prev_page="register")
        if not request.form.get("password"):
            return render_template("error.html", message="""Please provide
                                    Password.""", prev_page="register")

        # Trying to see whether the user is already present or not. If present
        # will ask the user to login.
        try:
            User.query.filter_by(name=request.form.get("name")).one()
            return render_template("register.html", flag=True,
                                   name=request.form.get("name"),
                                   message="""It seems like you are already a
                                    registered user with us. Please use login
                                    button next time.""")

        # If the user is not added to our we will add that person to the
        # database.
        except:
            try:  
                # print(request.form.get("name"))
                # print(request.form.get("password"))
                db.session.add(User(request.form.get("name"),
                                    request.form.get("password")))
                db.session.commit() 

                return render_template("register.html", flag = True,
                                        name = request.form.get("name"),
                                        message = """Aww yeah, you successfully
                                        registered for this application.""")
            except:
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
    if request.method == "POST":
        try:
            session['name'] = request.form.get("name")
            
            if not session['name']:
                return render_template("error.html", message="Please provide User name.",
                prev_page = "register")
            if not request.form.get("password"):
                return render_template("error.html", message="Please provide Password.",
                prev_page = "register")
            data = User.query.filter_by(name=session['name']).one()
            
            if check_password_hash(data.password, request.form.get("password")):
                return redirect("/")
            else:
                return render_template("error.html",
                    message = """Invalid Username and(or) password""")
        except:
            session.clear()
            return render_template("error.html", 
                message = """You might not be registered user. Please register first""",
                prev_page = "register")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/book/<id>",methods=['GET'])
def book(id):
    book = getbookbyid(int(id))
    return render_template("book.html",book=book)

@app.route("/api/book/<isbn>",methods=['GET'])
def book_details_api(isbn):
    book = getbookbyisbn(isbn)
    if book is None:
        return jsonify({"error":"Incorrect ISBN!"}), 404
    elif book:
        return jsonify({"ISBN" : book.isbn, "Title": book.title, 
        "Author" : book.author, 
        "year" : int(book.year)}), 200


@app.route("/search")
def search():
    if not request.args.get("book"):
        return render_template("error.html", 
        message="Please provide details of a book.",
        prev_page = "index")

    books = search_book(request.args.get("book"))
    

    if len(books) == 0:
        return render_template("error.html", message="We can't find any books.",
         prev_page = "index")
    
    return render_template("search.html", books=books)

@app.route("/api/search/", methods=['POST'])
def api_search():

    if request.is_json:
        content = request.get_json()
        if 'query' in content:
            query = content['query'].strip()
            books = search_book(query)
            if books:
                l = []
                books_json = {}
                for book in books:
                    d = {}
                    d['isbn'] = book.isbn
                    d['title'] = book.title
                    d['author'] = book.author
                    d['year'] = int(book.year)
                    l.append(d)
                books_json['books'] = l
                return (jsonify(books_json), 200) 
            else:
                return (jsonify({'Error': "No book was found."}), 404) 
        else:
            return (jsonify({'Error': "Invalid JSON data"}), 400)
    else:
        return (jsonify({"Error": "Takes only json as input"}), 422)
        
# if __name__ == "__main__":
#     db.create_all()
#     db.session.commit()
    # os.system("flask db migrate")
    # os.system("flask db upgrade")