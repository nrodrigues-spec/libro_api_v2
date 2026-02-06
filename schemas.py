from sqlmodel import Field, SQLModel
from pydantic import ConfigDict, model_validator
from datetime import datetime

class BookBase(SQLModel):
    title: str
    author: str
    isbn: str
    publication_year: int
    total_copies: int = Field(default=1, ge=0)
    available_copies: int | None = None

class BookCreate(BookBase):
    pass

class BookPublic(BookBase):
    id: int

    @model_validator(mode="after")
    def set_available_copies(self):
        if self.available_copies is None:
            self.available_copies = self.total_copies
        return self

class UserBase(SQLModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserPublic(UserBase):
    id: int

class LoanBase(SQLModel):
    book_id: int
    user_id: int

class LoanCreate(LoanBase):
    pass

class LoanPublic(LoanBase):
    id: int
    book: BookPublic
    user: UserPublic
    borrow_date: datetime
    due_date: datetime
    return_date: datetime | None
    status: str

class BookBorrowRequest(SQLModel):
    user_id: int

class BookReturnRequest(SQLModel):
    loan_id: int