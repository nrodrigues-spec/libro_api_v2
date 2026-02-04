from fastapi import FastAPI
from crud import *
from database import SessionLocal

app = FastAPI()

@app.get("/books")
def get_books(session:SessionLocal):
    return get_books_logic(session)

@app.get("/books/{book_id}")
def get_book(session:SessionLocal, book_id:int):
    return get_book_logic(session, book_id)

@app.post("/books/")
def create_book(session:SessionLocal, book:BookCreate):
    print(type(book))
    return create_book_logic(session, book)

@app.put("/books/{book_id}")
def update_book(session:SessionLocal, book:BookCreate, book_id:int):
    return update_book_logic(session, book_id, book)

@app.delete("/books/{book_id}")
def delete(session:SessionLocal, book_id:int):
    return delete_book_logic(session, book_id)