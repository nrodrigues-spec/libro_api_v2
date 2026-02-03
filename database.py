import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session

load_dotenv()

db_url = os.getenv('SQLALCHEMY_DATABASE_URL')
engine = create_engine(db_url, echo=True)

def get_session():
    with Session(engine) as session_local:
        yield session_local