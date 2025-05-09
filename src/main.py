from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy import inspect

from database import Base, engine, get_db, TodoDB, create_tables
from models import Todo, TodoUpdate


# Initialiser l'application FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Vérifie si la table "todos" existe
    inspector = inspect(engine)
    if "todos" not in inspector.get_table_names():
        print("Table 'todos' absente, création en cours...")
        create_tables()
    else:
        print("Table 'todos' déjà présente")
    yield


app = FastAPI(lifespan=lifespan)


# Route racine de l'API
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API To-Do avec Docker"}


# Lire toutes les tâches
@app.get("/todos", response_model=list[Todo])
def get_todos(db: Session = Depends(get_db)):
    return db.query(TodoDB).all()


# Lire une tâche par ID
@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return todo


# Créer une nouvelle tâche
@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo, db: Session = Depends(get_db)):
    # Crée une nouvelle tâche sans fournir d'ID (SQLite s'en charge)
    new_todo = TodoDB(
        title=todo.title, description=todo.description, completed=todo.completed
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


# Supprimer une tâche
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    db.delete(todo)
    db.commit()
    return {"message": "Tâche supprimée"}


# Mettre à jour une tâche
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    # Mise à jour uniquement des champs fournis
    if updated_todo.title is not None:
        todo.title = updated_todo.title
    if updated_todo.description is not None:
        todo.description = updated_todo.description
    if updated_todo.completed is not None:
        todo.completed = updated_todo.completed

    db.commit()
    db.refresh(todo)
    return todo
