from database import SessionLocal
from models import Book, User, Loan, LoanStatus
from schemas import BookPublic, BookCreate, UserPublic, UserCreate, LoanPublic, LoanCreate
from fastapi import HTTPException, Query
from sqlmodel import select
from typing import Annotated
from datetime import datetime, timezone


def create_book_logic(
        session:SessionLocal, 
        book_req:BookCreate
        ):
    book = Book.model_validate(book_req)
    print(f"after validation: {type(book)}")
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
    book_updated = Book.model_validate(book_pre)
    session.add(book_updated)
    session.commit()
    session.refresh(book_updated)
    return book_updated

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
    user = session.get(user_id)
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
    loan = session.get(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="User does not exist.")
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
        book = session.exec(select(Book).where(Book.id == book_id).with_for_update()).one()
        if not book:
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
        
        loan = Loan.model_validate(loan_creating)
        session.add(book)
        session.add(loan)
    
    session.refresh(book)
    session.refresh(loan)
        
def return_book_logic(
        session:SessionLocal,
        loan_id:int,
        ):
    with session.begin():
        loan = session.exec(select(Loan).where(Loan.id == loan_id).with_for_update()).one()
        if not loan:
            raise HTTPException(status_code=404, detail="No loan with this ID.")
        book = session.exec(select(Book).where(Book.id == loan.book_id).with_for_update()).one()
        if not book:
            raise HTTPException(status_code=404, detail="This loan has no valid book associated with it. Please check the database.")
        book.available_copies += 1
        loan.status = LoanStatus.RETURNED
        loan.return_date = datetime.now(timezone.utc)

        session.add(book)
        session.add(loan)
    
    session.refresh(book)
    session.refresh(loan)