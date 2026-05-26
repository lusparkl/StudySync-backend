import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_session
from app import models

TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False
)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=test_engine)

    session = TestingSessionLocal()

    try: 
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def client(db_session):
    def override_get_session():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(client):
    register_responce = client.post(
        "/users",
        json={
            "username": "test_user",
            "email": "test@gmail.com",
            "password": "test_password"
        }
    )

    assert register_responce.status_code == 200

    register_data = register_responce.json()
    assert register_data["access_token"] is not None
    
    login_responce = client.post(
        "/users/login",
        data={
            "username": "test@gmail.com",
            "password": "test_password"
        }
    )

    assert login_responce.status_code == 200

    login_data = login_responce.json()
    token = login_data["access_token"]

    assert token 

    return {
        "Authorization": f"Bearer {token}"
    }