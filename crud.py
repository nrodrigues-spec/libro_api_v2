from database import SessionLocal
from models import Book, User, Loan
from schemas import BookCreate, UserCreate, LoanCreate
from fastapi import HTTPException, Query
from sqlmodel import select
from typing import Annotated
from datetime import datetime, timezone, timedelta
from sqlalchemy.exc import NoResultFound

def create_book_logic(
        session:SessionLocal, 
        book_req:BookCreate
        ):
    book = Book(
        title=book_req.title,
        author=book_req.author,
        isbn=book_req.isbn,
        publication_year=book_req.publication_year,
        total_copies=book_req.total_copies,
        available_copies=book_req.total_copies
        )
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

def get_book_logic(
        session:SessionLocal,
        book_id:int
        ):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    return book

def get_books_logic(
        session:SessionLocal,
        offset:Annotated[int, Query(ge=0)]=0,
        limit:Annotated[int, Query(le=100)]=100,
        ):
    books = session.exec(select(Book).offset(offset).limit(limit)).all()
    return books

def update_book_logic(
        session:SessionLocal,
        book_id:int,
        book_req:BookCreate
        ):
    book_pre = session.get(Book, book_id)
    if not book_pre:
        raise HTTPException(status_code=404, detail="Book not found.")
    book_data = book_req.model_dump(exclude_unset=True)
    book_pre.sqlmodel_update(book_data)
    session.commit()
    session.refresh(book_pre)
    return book_pre

def delete_book_logic(
        session:SessionLocal,
        book_id:int
        ):
    book_del = session.get(Book, book_id)
    if not book_del:
        raise HTTPException(status_code=404, detail="Book not found.")
    session.delete(book_del)
    session.commit()
    return {"message": "Book deleted successfully."}

def create_user_logic(
        session:SessionLocal,
        user_req:UserCreate
        ):
    user = User.model_validate(user_req)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_logic(
        session:SessionLocal,
        user_id:int
        ):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist.")
    return user

def get_users_logic(
        session:SessionLocal,
        offset:Annotated[int, Query(ge=0)]=0,
        limit:Annotated[int, Query(le=100)]=100,
        ):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

def get_loan_logic(
        session:SessionLocal,
        loan_id:int
        ):
    loan = session.get(Loan, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan does not exist.")
    return loan

def get_loans_logic(
        session:SessionLocal,
        offset:Annotated[int, Query(ge=0)]=0,
        limit:Annotated[int, Query(le=100)]=100,
        ):
    loans = session.exec(select(Loan).offset(offset).limit(limit)).all()
    return loans

def borrow_book_logic(
        session:SessionLocal,
        book_id:int,
        user_id:int
        ):
    with session.begin():
        try:
            book = session.exec(select(Book).where(Book.id == book_id).with_for_update()).one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Book not found.")
        if book.available_copies == 0:
            raise HTTPException(status_code=412, detail="This book has no available copies.")
        user = session.exec(select(User).where(User.id == user_id)).one()
        if not user:
            raise HTTPException(status_code=404, detail="User does not exist.")
        book.available_copies -= 1
        
        loan_creating = LoanCreate(
            user_id=user_id,
            book_id=book_id
            )
        
        loan = Loan(
            book_id=loan_creating.book_id,
            user_id=loan_creating.user_id,
            borrow_date=datetime.now(timezone.utc),
            due_date=datetime.now(timezone.utc)+timedelta(days=14),
            return_date=None
            )
        session.add(book)
        session.add(loan)
    
    session.refresh(book)
    session.refresh(loan)
    return loan
        
def return_book_logic(
        session:SessionLocal,
        loan_id:int,
        ):
    with session.begin():
        try:
            loan = session.exec(select(Loan).where(Loan.id == loan_id).with_for_update()).one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="No loan with this ID.")
        if loan.status == "returned":
            raise HTTPException(status_code=412, detail="This loan has already been cleared.")
        try:
            book = session.exec(select(Book).where(Book.id == loan.book_id).with_for_update()).one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="This loan has no valid book associated with it. Please check the database.")
        if book.available_copies == book.total_copies:
            raise HTTPException(status_code=412, detail="Invalid return as all copies of this book are in the library.")
        book.available_copies += 1
        loan.status = "returned"
        loan.return_date = datetime.now(timezone.utc)

        session.add(book)
        session.add(loan)
    
    session.refresh(book)
    session.refresh(loan)
    return loan