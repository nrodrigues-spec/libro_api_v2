from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import StaticPool
from fastapi import Depends
import pytest
from typing import Annotated
from models import *
from main import app
from database import get_session
from fastapi.testclient import TestClient
from schemas import *
import sqlalchemy.exc as exc

# Fixtures and config

SQLITE_MEM_URL='sqlite:///:memory:'

@pytest.fixture(scope="session")
def make_test_engine():
    test_engine = create_engine(
        SQLITE_MEM_URL,
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
        )
    
    SQLModel.metadata.create_all(test_engine)
    yield test_engine
    test_engine.dispose()

@pytest.fixture
def test_session(make_test_engine):
    connection = make_test_engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection)
    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(test_session):
    def get_test_session():
        yield test_session

    app.dependency_overrides[get_session] = get_test_session
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def book_init(test_session):
    book = Book(
        title="test_title",
        author="test_author",
        isbn="test_isbn",
        publication_year=2000,
        total_copies=10,
        available_copies=10
        )
    test_session.add(book)
    test_session.commit()
    return book

@pytest.fixture
def user_init(test_session):
    user = User(
        name="test_name",
        email="test_email"
    )
    test_session.add(user)
    test_session.commit()
    return user

@pytest.fixture
def loan_init(test_session, book_init, user_init):
    loan = Loan(
            book_id=book_init.id,
            user_id=user_init.id,
            borrow_date=datetime.now(timezone.utc),
            due_date=datetime.now(timezone.utc)+timedelta(days=14),
            return_date=None
            )
    test_session.add(loan)
    test_session.commit()
    return loan


# Test cases

def test_get_books(client):
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert type(data) == list

def test_get_book(client, book_init):
    response = client.get("/books/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["available_copies"] == data["total_copies"]

def test_create_book(client):
    response = client.post("/books",
                           json={
                               "title": "test",
                               "author": "test",
                               "isbn": "test",
                               "publication_year": 2000,
                               "total_copies": 4
                               })
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["available_copies"] == data["total_copies"]

def test_create_book_duplicate_isbns(client, book_init):
    with pytest.raises(exc.IntegrityError):
        client.post("/books",
                    json={
                        "title": "test2",
                        "author": "test2",
                        "isbn": "test_isbn",
                        "publication_year": 2002,
                        "total_copies": 5
                        })

def test_update_book(client, book_init):
    response = client.put("/books/1",
                          json={
                              "title": "new_test1",
                              "author": "test1",
                              "isbn": "test1",
                              "publication_year": 2003,
                              "total_copies": 10
                              })
    assert response.status_code == 200

def test_delete_book(client, book_init):
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully."

def test_get_users(client, user_init):
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert type(data) == list
    assert "name" in data[0]
    assert "email" in data[0]

def test_get_user(client, user_init):
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "email" in data

def test_create_user(client):
    response = client.post("/users",
                           json={
                               "name": "test_user",
                               "email": "test_email"
                           })
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "email" in data

def test_get_loans(client, loan_init):
    response = client.get("/loans")
    assert response.status_code == 200
    data = response.json()
    assert type(data) == list
    assert "id" in data[0]
    assert "book" in data[0]
    assert "user" in data[0]
    assert data[0]["book"]["id"] == data[0]["book_id"]
    assert data[0]["user"]["id"] == data[0]["user_id"]
    assert "borrow_date" in data[0]
    assert "due_date" in data[0]
    assert data[0]["return_date"] == None

# def test_borrow_book(test_session, book_init, user_init):
#     initial_copies = book_init.available_copies
#     with test_session.begin_nested():
#         response = client.post(f"/books/{book_init.id}/borrow?user_id={user_init.id}")
#         assert response.status_code == 200