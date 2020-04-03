import os, csv

from objects import Book
from application import db

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

def main():
    # db.create_all()
    f=open("books.csv")
    reader =csv.reader(f)
    headers = next(reader)
    for isbn,title,author,year in reader:
        db.session.add(Book(isbn,title,author,year))        
    print("done")            
    db.session.commit()

if __name__ == "__main__":
    main()
