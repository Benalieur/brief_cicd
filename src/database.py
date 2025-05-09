import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer les valeurs depuis le .env
DATABASE_URL = os.getenv('DATABASE_URL')

# Create engine
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        print("Connexion à la base de données réussie !")
except Exception as e:
    print(f"Erreur de connexion à la base de données : {e}")


# Configuration de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Fonction pour récupérer une session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base pour les modèles SQLAlchemy
Base = declarative_base()


# Modèle SQLAlchemy pour la base de données
class TodoDB(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)


def create_tables(max_retries=10, delay=2):
    for attempt in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("Les tables ont été créées avec succès !")
            return
        except OperationalError as e:
            print(f"⏳ Tentative {attempt + 1}/{max_retries} : base non prête ({e})")
            time.sleep(delay)
    print("Échec de la création des tables après plusieurs tentatives.")
