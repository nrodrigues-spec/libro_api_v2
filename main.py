from fastapi import FastAPI
from crud import *
from database import SessionLocal
from schemas import BookPublic, UserPublic, LoanPublic

app = FastAPI()

@app.get("/books", response_model=list[BookPublic])
def get_books(session:SessionLocal):
    return get_books_logic(session)

@app.get("/books/{book_id}", response_model=BookPublic)
def get_book(session:SessionLocal, book_id:int):
    return get_book_logic(session, book_id)

@app.post("/books", response_model=BookPublic)
def create_book(session:SessionLocal, book:BookCreate):
    return create_book_logic(session, book)

@app.put("/books/{book_id}", response_model=BookPublic)
def update_book(session:SessionLocal, book:BookCreate, book_id:int):
    return update_book_logic(session, book_id, book)

@app.delete("/books/{book_id}", response_model=dict)
def delete(session:SessionLocal, book_id:int):
    return delete_book_logic(session, book_id)

@app.post("/books/{book_id}/borrow", response_model=LoanPublic)
def borrow_book(session:SessionLocal, book_id:int, user_id:int):
    return borrow_book_logic(session, book_id, user_id)

@app.get("/users", response_model=list[UserPublic])
def get_users(session:SessionLocal):
    return get_users_logic(session)

@app.get("/users/{user_id}", response_model=UserPublic)
def get_user(session:SessionLocal, user_id:int):
    return get_user_logic(session, user_id)

@app.post("/users", response_model=UserPublic)
def create_user(session:SessionLocal, user:UserCreate):
    return create_book_logic(session, user)

@app.get("/loans", response_model=list[LoanPublic])
def get_loans(session:SessionLocal):
    return get_loans_logic(session)

@app.get("/loans/{loan_id}", response_model=LoanPublic)
def get_user(session:SessionLocal, loan_id:int):
    return get_loan_logic(session, loan_id)

@app.post("/loans/{loan_id}/return", response_model=LoanPublic)
def return_book(session:SessionLocal, loan_id:int):
    return_book_logic(session, loan_id)