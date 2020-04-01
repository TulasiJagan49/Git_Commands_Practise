import unittest, sys, os
sys.path.insert(0, 'E:/Redefined_WP/project1/') 
from search import search_book


class TestSearchMethod(unittest.TestCase):

    def test_valid_isbn(self):
        """Test Case 1 checking the validity of search function
            using a valid ISBN."""
        self.assertEquals(search_book("0380795272")[0].title(),
                        "Krondor: The Betrayal")


    # def test_valid_title(self):
    #     """""Test Case 2 checking the validity of search function
    #         using a string."""
    #     self.assertTrue(search_book("the beTRAy")[0].title(),
    #                     "Krondor: The Betrayal")
    
    # def test_valid_author(self):
    #     """""Test Case 3 checking the validity of search function
    #         using a string."""
    #     self.assertTrue(search_book("beth")[0].isbn,
    #                     "0312364687")
    
    # def test_invalid_isbn(self):
    #     """Test Case 4 checking the validity of search function
    #        using a invalid ISBN."""
    #     self.assertTrue(search_book("99597333117"),[])
    
    # def test_invalid_string(self):
    #     """Test Case 5 checking the validity of search function
    #        using an empty string"""
    #     self.assertTrue(search_book(""), [])


if __name__ == "__main__":
    unittest.main()
        

