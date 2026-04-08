import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from db.database import get_db
from models.models import Base

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def sample_owner_data():
    return {
        "name": "Test Owner",
        "address": "123 Stable Lane",
        "phone": "+1234567890"
    }

@pytest.fixture
def sample_horse_data():
    return {
        "name": "Test Horse",
        "gender": "female",
        "age": 5
    }

@pytest.fixture
def sample_jockey_data():
    return {
        "name": "Test Jockey",
        "address": "456 Track Road",
        "age": 28,
        "rating": 8.5
    }

@pytest.fixture
def sample_race_data():
    return {
        "date": "2026-05-01",
        "time": "15:30:00",
        "hippodrome": "Central Racetrack",
        "name": "Spring Cup"
    }

@pytest.fixture
def sample_race_result_data():
    return {
        "horse_id": 1,
        "jockey_id": 1,
        "place": 1,
        "finish_time": 72.35
    }
