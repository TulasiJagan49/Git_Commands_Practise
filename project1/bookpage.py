import os

from objects import Book, db


if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")



def getbook(id):
    book = Book.query.filter_by(id=id).one()
    return book