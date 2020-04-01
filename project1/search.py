import os

from sqlalchemy import or_
from objects import Book, db

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

def search_book(book_query):

    # Take input and add a wildcard
    book_query = "%" + book_query + "%"

    # Capitalize all words of input for search

    book_query = book_query.title()

    books = Book.query.filter(
        or_(Book.isbn.like(book_query),
        Book.title.like(book_query),
        Book.author.like(book_query),
        Book.year.like(book_query))).all()

    return books

def main():
    print(search_book("0380795272")[0].title)

if __name__ == "__main__":
    main()