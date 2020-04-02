import unittest, sys, os, requests
sys.path.insert(0, 'E:/Redefined_WP/project1/')
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from search import search_book
from application import app

class TestApplicationRequests(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db = SQLAlchemy(app)
        app.app_context().push()
    
    def test_index_route(self):
        """ Test Case 1 for checking '/' route"""
        res = requests.get("http://127.0.0.1:5000/")
        self.assertEqual(res.status_code, 200)
    
    def test_register_route(self):
        """ Test Case 2 for checking '/register' route"""
        res = requests.get("http://127.0.0.1:5000/register")
        self.assertEqual(res.status_code, 200)
        res = requests.post("http://127.0.0.1:5000/register")
        self.assertEqual(res.status_code, 200)
    
    def test_admin_route(self):
        """ Test Case 3 for checking '/admin' route"""
        res = requests.get("http://127.0.0.1:5000/admin")
        self.assertEqual(res.status_code, 200)
    
    def test_auth_route(self):
        """ Test Case 4 for checking '/auth' route"""
        res = requests.post("http://127.0.0.1:5000/auth")
        self.assertEqual(res.status_code, 200)
    
    def test_logout_route(self):
        """ Test Case 5 for checking '/logout' route"""
        res = requests.get("http://127.0.0.1:5000/logout")
        self.assertEqual(res.status_code, 200)
    
    def test_search_route(self):
        """ Test Case 6 for checking '/search' route"""
        res = requests.get("http://127.0.0.1:5000/search")
        self.assertEqual(res.status_code, 200)
    
if __name__ == "__main__":
    unittest.main()

