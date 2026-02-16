from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import StaticPool
import pytest
from models import *
from crud import *
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

# CRUD testing modules

def test_get_books_logic(test_session, book_init):
    books = get_books_logic(test_session)
    assert type(books) == list
    assert books[0].id == book_init.id
    assert books[0].title == book_init.title
    assert books[0].author == book_init.author
    assert books[0].isbn == book_init.isbn
    assert books[0].publication_year == book_init.publication_year
    assert books[0].total_copies == book_init.total_copies
    assert books[0].available_copies == books[0].total_copies

def test_get_book_logic(test_session, book_init):
    book = get_book_logic(test_session, book_init.id)
    Book.model_validate(book)
    assert book.id == book_init.id
    assert book.title == book_init.title
    assert book.author == book_init.author
    assert book.isbn == book_init.isbn
    assert book.publication_year == book_init.publication_year
    assert book.total_copies == book_init.total_copies
    assert book.available_copies == book.total_copies

def test_create_book_logic(test_session):
    book_request = BookCreate(
        title="create_test",
        author="create_test_author",
        isbn="create_test_isbn",
        publication_year=2012,
        total_copies=4
    )
    book = create_book_logic(test_session, book_request)
    assert hasattr(book, "id")
    assert book.title == "create_test"
    assert book.author == "create_test_author"
    assert book.isbn == "create_test_isbn"
    assert book.publication_year == 2012
    assert book.total_copies == 4
    assert book.available_copies == book.total_copies

def test_update_book_logic(test_session, book_init):
    book_request = BookCreate(
        title="update_test",
        author="update_test_author",
        isbn="update_test_isbn",
        publication_year=2013,
        total_copies=5
    )
    book = update_book_logic(test_session, book_init.id, book_request)
    assert book.id == book_init.id
    assert book.title == "update_test"
    assert book.author == "update_test_author"
    assert book.isbn == "update_test_isbn"
    assert book.publication_year == 2013
    assert book.total_copies == 5
    assert book.available_copies == book.total_copies

def test_delete_book_logic(test_session, book_init):
    confirm = delete_book_logic(test_session, book_init.id)
    assert confirm["message"] == "Book deleted successfully."

def test_get_users_logic(test_session, user_init):
    users = get_users_logic(test_session)
    assert type(users) == list
    assert users[0].id is not None
    assert users[0].name == "test_name"
    assert users[0].email == "test_email"

def test_get_user_logic(test_session, user_init):
    user = get_user_logic(test_session, user_init.id)
    assert type(user) == User
    assert user.id is not None
    assert user.name == "test_name"
    assert user.email == "test_email"

def test_create_user_logic(test_session, user_init):
    user_request = UserCreate(
        name="create_test",
        email="create_test_email"
    )
    user_created = create_user_logic(test_session, user_request)
    assert type(user_created) == User
    assert user_created.id is not None
    assert user_created.name == "create_test"
    assert user_created.email == "create_test_email"

def test_get_loans_logic(test_session, loan_init):
    loans = get_loans_logic(test_session)
    assert type(loans) == list
    assert type(loans[0]) == Loan
    assert loans[0].id == 1
    assert loans[0].book_id == 1
    assert loans[0].user_id == 1
    assert loans[0].status == 'borrowed'

def test_get_loan_logic(test_session, loan_init):
    loan = get_loan_logic(test_session, loan_init.id)
    assert type(loan) == Loan
    assert loan.id == 1
    assert loan.book_id == 1
    assert loan.user_id == 1
    assert loan.status == 'borrowed'