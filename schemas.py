from sqlmodel import Field, SQLModel
from pydantic import ConfigDict, model_validator
from datetime import datetime

class BookBase(SQLModel):
    title: str
    author: str
    isbn: str
    publication_year: int
    total_copies: int = Field(default=1, ge=0)

class BookCreate(BookBase):
    pass

class BookPublic(BookBase):
    id: int

    # @model_validator(mode="after")
    # def set_available_copies(self):
    #     if self.available_copies is None:
    #         self.available_copies = self.total_copies
    #     return self

    model_config = ConfigDict(from_attributes=True)

class UserBase(SQLModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserPublic(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class LoanBase(SQLModel):
    book_id: int
    user_id: int
    borrow_date: datetime
    due_date: datetime
    return_date: datetime
    status: str

class LoanCreate(SQLModel):
    book_id: int
    user_id: int

class LoanPublic(LoanBase):
    id: int
    book: BookPublic
    user: UserPublic

    model_config = ConfigDict(from_attributes=True)

class BookBorrowRequest(SQLModel):
    user_id: int

class BookReturnRequest(SQLModel):
    loan_id: int