# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from src.database import Base, get_db
from src.main import app

# 1. Créer un engine SQLite in-memory
@pytest.fixture(scope="session")
def engine():
    return create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}  # nécessaire pour SQLite multithread pytest
    )

# 2. Créer les tables avant les tests, puis les supprimer après
@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# 3. Fournir une session SQLAlchemy liée à l'engine de test
@pytest.fixture
def db_session(engine, tables):
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# 4. Override de la dépendance FastAPI pour qu'elle utilise db_session
@pytest.fixture
def client(db_session, monkeypatch):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # On remplace get_db par le override
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
