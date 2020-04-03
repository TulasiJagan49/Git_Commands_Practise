import os, csv

from objects import Book, db

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

def main():
    f=open("books.csv")
    reader =csv.reader(f)
    headers = reader.next()
    for isbn,title,author,year in reader:
        db.session.add(Book(isbn,title,author,year))        
    print("done")            
    db.commit()

if __name__ == "__main__":
    main()
