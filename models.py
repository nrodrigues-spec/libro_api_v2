from sqlmodel import SQLModel, Field, Column, TIMESTAMP, DateTime, func, Relationship
from pydantic import model_validator
from datetime import datetime, timezone, timedelta
from typing import List

class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    author: str = Field(nullable=False)
    isbn: str = Field(unique=True, nullable=False)
    publication_year: int = Field(nullable=False)
    total_copies: int = Field(default=1, nullable=False, ge=0)
    available_copies: int = Field(default=1, nullable=False, ge=0)

    loans: List["Loan"] = Relationship(back_populates="loan")

    @model_validator(mode="after")
    def set_available_copies(self):
        if self.available_copies is None or self.available_copies == 1:
            self.available_copies = self.total_copies
        return self

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(unique=True, nullable=False)

    loans: List["Loan"] = Relationship(back_populates="loan")

class Loan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id", nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    borrow_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now()
        )
    )
    due_date: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        )
    )

    book: Book | None = Relationship(back_populates="loans")
    user: User | None = Relationship(back_populates="loans")

    @model_validator(mode="after")
    def check_dates(self):
        if self.due_date < self.borrow_date:
            raise ValueError
        return self
    
    @model_validator(mode="after")
    def add_due_date(self):
        if self.due_date is None:
            self.due_date = self.borrow_date + timedelta(days=14)
        return self