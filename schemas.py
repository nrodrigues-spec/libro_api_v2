from sqlmodel import Field, SQLModel
from pydantic import ConfigDict, model_validator
from datetime import datetime

class BookBase(SQLModel):
    title: str
    author: str
    isbn: str
    publication_year: int
    total_copies: int

class BookCreate(BookBase):
    pass

class BookPublic(BookBase):
    id: int
    available_copies: int
    loans: list[LoanPublicShort]

class BookPublicShort(BookBase):
    id: int
    available_copies: int

class UserBase(SQLModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserPublic(UserBase):
    id: int
    loans: list[LoanPublicShort]

class UserPublicShort(UserBase):
    id: int

class LoanBase(SQLModel):
    book_id: int
    user_id: int

class LoanCreate(LoanBase):
    pass

class LoanPublic(LoanBase):
    id: int
    book: BookPublicShort
    user: UserPublicShort
    borrow_date: datetime
    due_date: datetime
    return_date: datetime | None
    status: str

class LoanPublicShort(LoanBase):
    id: int
    due_date: datetime
    return_date: datetime | None
    status: str

class BookBorrowRequest(SQLModel):
    user_id: int

class BookReturnRequest(SQLModel):
    loan_id: int