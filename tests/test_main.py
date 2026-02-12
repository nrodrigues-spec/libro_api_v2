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
def book_init(client):
    client.post("/books",
                json={
                    "title": "test1",
                    "author": "test1",
                    "isbn": "test1",
                    "publication_year": 2001,
                    "total_copies": 3
                    })

# Database setup and teardown

# @pytest.fixture
# def population(test_session):
#     new_book = Book(
#         title="initiated_book_test",
#         author="initiated_book_test",
#         isbn="initiated_book_test",
#         publication_year=1900,
#         total_copies=2
#     )
#     new_book_2 = Book(
#         title="initiated_book_test_2",
#         author="initiated_book_test_2",
#         isbn="initiated_book_test_2",
#         publication_year=1900,
#         total_copies=2
#     )
#     new_user = User(
#         name="test_user",
#         email="test_user"
#     )
#     test_session.add(new_book)
#     test_session.add(new_book_2)
#     test_session.add(new_user)
#     test_session.commit()
#     test_session.close()
#     yield test_session
#     test

# Test cases

def test_get_books(client):
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert type(data) == list

@pytest.mark.parametrize("num, avail_copies",
                         [(1, 3),
                          (2, 5)])
def test_get_book(client, book_init, num, avail_copies):
    new_book = client.post("/books",
                        json={
                        "title": "test2",
                        "author": "test2",
                        "isbn": "test2",
                        "publication_year": 2002,
                        "total_copies": 5
                        })
    response = client.get(f"/books/{num}")
    assert response.status_code == 200
    assert 'id' in response.json()
    assert response.json()["available_copies"] == avail_copies

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
    assert data["available_copies"] == 4

def test_create_book_duplicate_isbns(client, book_init):
    with pytest.raises(exc.IntegrityError):
        client.post("/books",
                    json={
                        "title": "test2",
                        "author": "test2",
                        "isbn": "test1",
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