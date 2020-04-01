import os
import csv

from flask_sqlalchemy import SQLAlchemy

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine= create_engine(os.getenv("DATABASE_URL"))
db =scoped_session(sessionmaker(bind=engine))

def main():
    db.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, isbn VARCHAR NOT NULL,title VARCHAR NOT NULL,author VARCHAR NOT NULL,year INTEGER NOT NULL)")
    f=open("books.csv")
    reader =csv.reader(f)
    headers = reader.next()
    for isbn,title,author,year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:a,:b,:c,:d)",{"a":isbn,"b":title,"c":author,"d":year})
        
    print("done")            
    db.commit()

if __name__ == "__main__":
    main()
