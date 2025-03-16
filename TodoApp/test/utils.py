from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from ..database import Base
from sqlalchemy.orm import sessionmaker
from ..main import app
import pytest
from ..models import Todos, Users
from fastapi.testclient import TestClient
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine (
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'Ulug', 'id': 5, 'user_role': 'admin'}

client = TestClient(app)

@pytest.fixture()
def test_todo():
    todo = Todos(
        title='limon',
        description='string',
        priority=5,
        complete=False,
        owner_id=5,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo) 
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

@pytest.fixture
def test_user():
    test_user = Users(
        username='Ulug',
        email='ulug@gmail.com',
        first_name='Ulugbek',
        last_name='Urakov',
        hashed_password=bcrypt_context.hash('test12345'),
        role='admin',
        phone_number='998974795636'
    )

    db = TestingSessionLocal()
    db.add(test_user)
    db.commit()
    db.refresh(test_user)  # ✅ Ensure test_user.id is set
    yield test_user

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
