import os

from objects import Book, db


if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")



# return the book object by id

def getbookbyid(id):
    book = Book.query.filter_by(id=id).one()
    return book

# return the book object by isbn

def getbookbyisbn(isbn):
    book = Book.query.filter_by(isbn=isbn).one()
    return book