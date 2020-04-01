import unittest, sys, os
sys.path.insert(0, 'E:/Redefined_WP/project1/')
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from search import search_book
from application import app

class TestSearchMethod(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db = SQLAlchemy(app)
        app.app_context().push() 

    def test_valid_isbn(self):
        """Test Case 1 checking the validity of search function
            using a valid ISBN."""
        book_data = search_book("0380795272")
        self.assertEqual(book_data[0].title, "Krondor: The Betrayal")


    def test_valid_title(self):
        """""Test Case 2 checking the validity of search function
            using a string."""
        book_data = search_book("the beTRAy")
        self.assertEqual(book_data[0].title, "Krondor: The Betrayal")
    
    def test_valid_author(self):
        """""Test Case 3 checking the validity of search function
            using a string."""
        book_data = search_book("beth")
        self.assertEqual(book_data[0].isbn, "0312364687")
    
    def test_invalid_isbn(self):
        """Test Case 4 checking the validity of search function
           using a invalid ISBN."""
        self.assertEqual(search_book("99597333117"),[])
    
    def test_invalid_string(self):
        """Test Case 5 checking the validity of search function
           using an empty string"""
        self.assertEqual(search_book("tulasi"), [])

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
        

