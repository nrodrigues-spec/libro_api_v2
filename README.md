# Library API Project

## Project Purpose

This project was started with the intention of gaining an understanding into API design and testing in Python. Modules like FastAPI, Alembic, SQLModel and Pydantic have been implemented, which are all state-of-the-art technologies used in API design.

## Project Scope

This project is a simple library API that allows adding, updating, reading and deleting of Books. It also allows for creating and viewing of the different library Users. There are also endpoints that allow for borrowing and returning books, thus creating Loans connecting the User and the Book that has been borrowed.

This project does not, however, check if a loan is overdue. It also does not handle authentication of Users.

## Setup Instructions

### PostgreSQL through Docker

This API connects to a PostgreSQL server and saves all the information in a database. The easiest way to set it up is by using an official PostgreSQL image from Docker and running it on a container.

- Download and install Docker on your system. [Click here to find the package download and installation instructions.](https://www.docker.com/get-started/)
- Open a new terminal window and run the following command: (make sure to replace [container name], [new username] and [new password] with your values)

```bash
docker run --name [container name] -e POSTGRES_USER=[new username] POSTGRES_PASSWORD=[new password]> -p 5432:5432 -d postgres
```

This will create and run a new container with the latest PostgreSQL image.

Note: This container should be running after it has been made. If it has stopped for some reason, go to **Docker Desktop** > **Containers** and then find the container with your container name. Click the **play button** under **Actions** and the container will start up.

### Project Structure and Dependency Installation

- Navigate to the project root.
- Create and activate a new virtual environment and install the packages in the requirements.txt file by running the following commands:

```bash
python3 -m venv <virtual env name>
<virtual env name>/bin/activate
pip install -r requirements.txt
```

Note: If you have Visual Studio Code, you can do these steps by going to the **Command Palette** (ctrl-shift-P or Command-Shift-P) > **Python: Select Interpreter** > **Create Virtual Environment...** > either **Venv** or **Conda** > **Install requirements.txt**

- Set up the environmental variables for this application by making a `.env` file. The main variables needed are as follows:

```bash
SQLALCHEMY_DATABASE_URL='postgresql+psycopg2://[POSTGRES_USER]:[POSTGRES_PASSWORD]@localhost:5432/postgres'
SQLITE_MEM_URL='sqlite:///:memory:' # if performing testing
```

Make sure to replace [POSTGRES_USER] and [POSTGRES_PASSWORD] with the values defined when creating the Docker container. This will allow the application to connect to the PostgreSQL database.

## Running the Application

- In a terminal window with the virtual environment active, run `alembic upgrade head` to create all the tables in the database.
- Now that the database is created, run `fastapi run main.py` to run the application. The app should by default run on `http://0.0.0.0:8000`, while you can view the interactive Swagger API documentation on `http://0.0.0.0:8000/docs` and see and run the endpoints.

## Testing

For testing, simply run `pytest tests` from the root folder. The test files are already present in the tests folder and will run when this command is run.

## Endpoints

### GET /books

Endpoint to get a list of all the books in the database.
*Response model*: List[BookPublic]

```json
[
  {
    "title": "string",
    "author": "string",
    "isbn": "string",
    "publication_year": 0,
    "total_copies": 0,
    "id": 0,
    "available_copies": 0,
    "loans": [
      {
        "book_id": 0,
        "user_id": 0,
        "id": 0,
        "due_date": "2026-02-16T11:17:03.037Z",
        "return_date": "2026-02-16T11:17:03.037Z",
        "status": "string"
      }
    ]
  }
]
```

cURL command:

```curl
curl -X 'GET' \
  'http://127.0.0.1:8000/books' \
  -H 'accept: application/json'
```

### GET /books/{id}

Endpoint to get a singular book given the id number.
*Response model*: BookPublic

```json
{
  "title": "string",
  "author": "string",
  "isbn": "string",
  "publication_year": 0,
  "total_copies": 0,
  "id": 0,
  "available_copies": 0,
  "loans": [
    {
      "book_id": 0,
      "user_id": 0,
      "id": 0,
      "due_date": "2026-02-16T11:26:58.232Z",
      "return_date": "2026-02-16T11:26:58.232Z",
      "status": "string"
    }
  ]
}
```

cURL command:

```curl
curl -X 'GET' \
  'http://127.0.0.1:8000/books/20' \
  -H 'accept: application/json'
```

### POST /books

Endpoint to create a book given an input structure.
Input model: BookCreate

```json
{
  "title": "string",
  "author": "string",
  "isbn": "string",
  "publication_year": 0,
  "total_copies": 0
}
```

Response model: BookPublic

```json
{
  "title": "string",
  "author": "string",
  "isbn": "string",
  "publication_year": 0,
  "total_copies": 0,
  "id": 0,
  "available_copies": 0,
  "loans": [
    {
      "book_id": 0,
      "user_id": 0,
      "id": 0,
      "due_date": "2026-02-16T11:39:26.081Z",
      "return_date": "2026-02-16T11:39:26.081Z",
      "status": "string"
    }
  ]
}
```

cURL command:

```curl
curl -X 'POST' \
  'http://127.0.0.1:8000/books' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Percy Jackson and the Olympians: The Lightning Thief",
  "author": "Rick Riordan",
  "isbn": "0-7868-5629-7",
  "publication_year": 2023,
  "total_copies": 6
}'
```

### PUT /books/{id}

Endpoint to update the details of a book.

Input model BookCreate:

```json
{
  "title": "string",
  "author": "string",
  "isbn": "string",
  "publication_year": 0,
  "total_copies": 0
}
```

Response model: BookPublic

```json
{
  "title": "string",
  "author": "string",
  "isbn": "string",
  "publication_year": 0,
  "total_copies": 0,
  "id": 0,
  "available_copies": 0,
  "loans": [
    {
      "book_id": 0,
      "user_id": 0,
      "id": 0,
      "due_date": "2026-02-16T11:39:26.081Z",
      "return_date": "2026-02-16T11:39:26.081Z",
      "status": "string"
    }
  ]
}
```

cURL command:

```curl
curl -X 'PUT' \
  'http://127.0.0.1:8000/books/29' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Percy Jackson and the Olympians: The Lightning Thief",
  "author": "Rick Riordan",
  "isbn": "0-7868-5629-7",
  "publication_year": 2023,
  "total_copies": 5
}'
```

### DELETE /books/{id}

Endpoint to delete a book from the database.

Response:

```json
{
  "message": "Book deleted successfully."
}
```

cURL command:

```curl
curl -X 'DELETE' \
  'http://127.0.0.1:8000/books/29' \
  -H 'accept: application/json'
```

### POST /books/{id}/borrow

Endpoint to borrow one of the books from the library. This also decreases the available_copies by 1 (unless "available_copies" is already equal to 0, in which case it raises a 412 error.)

Response model: LoanPublic

```json
{
  "book_id": 0,
  "user_id": 0,
  "id": 0,
  "book": {
    "title": "string",
    "author": "string",
    "isbn": "string",
    "publication_year": 0,
    "total_copies": 0,
    "id": 0,
    "available_copies": 0
  },
  "user": {
    "name": "string",
    "email": "string",
    "id": 0
  },
  "borrow_date": "2026-02-16T13:40:28.589Z",
  "due_date": "2026-02-16T13:40:28.589Z",
  "return_date": "2026-02-16T13:40:28.589Z",
  "status": "string"
}
```

cURL command:

```curl
curl -X 'POST' \
  'http://127.0.0.1:8000/books/26/borrow?user_id=1' \
  -H 'accept: application/json' \
  -d ''
```

### GET /users

Retrieves a list of the registered users.

Response model: List[UserPublic]

```json
[
  {
    "name": "string",
    "email": "string",
    "id": 0,
    "loans": [
      {
        "book_id": 0,
        "user_id": 0,
        "id": 0,
        "due_date": "2026-02-16T12:48:52.186Z",
        "return_date": "2026-02-16T12:48:52.186Z",
        "status": "string"
      }
    ]
  }
]
```

cURL command:

```curl
curl -X 'GET' \
  'http://127.0.0.1:8000/users' \
  -H 'accept: application/json'
```

### GET /users/{id}

Endpoint to get a specific user with a given id number.

Response model: UserPublic

```json
{
  "name": "string",
  "email": "string",
  "id": 0,
  "loans": [
    {
      "book_id": 0,
      "user_id": 0,
      "id": 0,
      "due_date": "2026-02-16T13:03:04.830Z",
      "return_date": "2026-02-16T13:03:04.830Z",
      "status": "string"
    }
  ]
}
```

cURL command:

```curl
curl -X 'GET' \
  'http://127.0.0.1:8000/users/1' \
  -H 'accept: application/json'
```

### POST /users

Endpoint to create a new user.

Input model: UserCreate

```json
{
  "name": "string",
  "email": "string"
}
```

Response model: UserPublic

```json
{
  "name": "string",
  "email": "string",
  "id": 0,
  "loans": [
    {
      "book_id": 0,
      "user_id": 0,
      "id": 0,
      "due_date": "2026-02-16T13:04:03.432Z",
      "return_date": "2026-02-16T13:04:03.432Z",
      "status": "string"
    }
  ]
}
```

cURL command:

```curl
curl -X 'POST' \
  'http://127.0.0.1:8000/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Jane Doe",
  "email": "jandoe123@example.com"
}'
```

### GET /loans

Retrieves a list of the book loans.

Response model: List[LoanPublic]

```json
[
  {
    "book_id": 0,
    "user_id": 0,
    "id": 0,
    "book": {
      "title": "string",
      "author": "string",
      "isbn": "string",
      "publication_year": 0,
      "total_copies": 0,
      "id": 0,
      "available_copies": 0
    },
    "user": {
      "name": "string",
      "email": "string",
      "id": 0
    },
    "borrow_date": "2026-02-16T13:14:15.991Z",
    "due_date": "2026-02-16T13:14:15.991Z",
    "return_date": "2026-02-16T13:14:15.991Z",
    "status": "string"
  }
]
```

cURL command:

```curl
curl -X 'GET' \
  'http://127.0.0.1:8000/loans' \
  -H 'accept: application/json'
```

### GET /loans/{id}

Endpoint to get a specific loan given the id number.

Response model: LoanPublic

```json
{
  "book_id": 0,
  "user_id": 0,
  "id": 0,
  "book": {
    "title": "string",
    "author": "string",
    "isbn": "string",
    "publication_year": 0,
    "total_copies": 0,
    "id": 0,
    "available_copies": 0
  },
  "user": {
    "name": "string",
    "email": "string",
    "id": 0
  },
  "borrow_date": "2026-02-16T13:17:51.590Z",
  "due_date": "2026-02-16T13:17:51.590Z",
  "return_date": "2026-02-16T13:17:51.590Z",
  "status": "string"
}
```

cURL command:

```curl
curl -X 'GET' \
  'http://127.0.0.1:8000/loans/1' \
  -H 'accept: application/json'
```

### POST /loans/{id}/return

Endpoint to return a book and clear a loan. Note that "available_copies" in the loan increases by 1 on returning (unless "available_copies" is already equal to "total_copies", in which case it raises a 412 error.)

Response model: LoanPublic

```json
{
  "book_id": 0,
  "user_id": 0,
  "id": 0,
  "book": {
    "title": "string",
    "author": "string",
    "isbn": "string",
    "publication_year": 0,
    "total_copies": 0,
    "id": 0,
    "available_copies": 0
  },
  "user": {
    "name": "string",
    "email": "string",
    "id": 0
  },
  "borrow_date": "2026-02-16T13:57:50.519Z",
  "due_date": "2026-02-16T13:57:50.519Z",
  "return_date": "2026-02-16T13:57:50.519Z",
  "status": "string"
}
```

cURL command:

```curl
curl -X 'POST' \
  'http://127.0.0.1:8000/loans/7/return' \
  -H 'accept: application/json' \
  -d ''
```

## Summary

This project provided some keen insight to why a lot of the functionalities are used as they are and why they end up being used in production models, to the extent of being industry standards. As some one that has had to work with poorly written SQL injection code and has spent countless hours of work deleting and recreating schemas and table, the introduction of Alembic makes so much sense and is a sea change in backend database management. It was also great to exercise some web application design muscles and get the application to as much of a foolproof state as possible.
