import unittest 
from book_details import getbookbyisbn, getbookbyid

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from objects import Book, User


def setupAppTest():
    app = Flask(__name__)
    db = SQLAlchemy()
    
    # Check for environment variable
    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL is not set")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.app_context().push()

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        setupAppTest()
    
    def test(self):
        self.assertTrue(True)

    # tests to check if the details of book are correct after a query

    def testISBNbyId(self):
        book = getbookbyid("1")
        self.assertEqual(book.isbn, "0380795272")

    def testTitlebyId(self):
        book = getbookbyid("1")
        self.assertEqual(book.title, "Krondor: The Betrayal")

    def testAuthorbyId(self):
        book = getbookbyid("1")
        self.assertEqual(book.author, "Raymond E. Feist")

    def testYearbyID(self):
        book = getbookbyid("1")
        self.assertEqual(book.year, 1998)

    def testTitlebyISBN(self):
        book = getbookbyisbn("0380795272")
        self.assertEqual(book.title, "Krondor: The Betrayal")

    def testAuthorbyISBN(self):
        book = getbookbyisbn("0380795272")
        self.assertEqual(book.author, "Raymond E. Feist")

    def testYearbyISBN(self):
        book = getbookbyisbn("0380795272")
        self.assertEqual(book.year, 1998)

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()