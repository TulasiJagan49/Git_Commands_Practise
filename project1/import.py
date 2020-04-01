import os, csv

from objects import Book

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

def main():

    db.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, isbn VARCHAR NOT NULL,title VARCHAR NOT NULL,author VARCHAR NOT NULL,year INTEGER NOT NULL)")
    f=open("books.csv")
    reader =csv.reader(f)
    headers = reader.next()
    for isbn,title,author,year in reader:
        db.session.add(Book(isbn,title,author,year))        
    print("done")            
    db.commit()

if __name__ == "__main__":
    main()
