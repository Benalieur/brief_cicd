import streamlit as st
import requests

# Base URL de l'API FastAPI
BASE_URL = "http://fastapi_app:8000"

# Fonction pour récupérer toutes les tâches
def get_todos():
    response = requests.get(f"{BASE_URL}/todos")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Impossible de récupérer les tâches depuis l'API.")
        return []

# Fonction pour créer une tâche
def create_todo():
    st.header("Créer une tâche")
    title = st.text_input("Titre")
    description = st.text_area("Description")
    completed = st.checkbox("Complétée")
    
    if st.button("Ajouter la tâche"):
        if title.strip():
            todo_data = {"id": 0, "title": title, "description": description, "completed": completed}
            response = requests.post(f"{BASE_URL}/todos", json=todo_data)
            if response.status_code == 200:
                st.success("Tâche ajoutée avec succès!")
                st.rerun()
            else:
                st.error("Erreur lors de l'ajout de la tâche.")
        else:
            st.error("Le titre est obligatoire.")

# Fonction pour modifier une tâche
def update_todo(todo_id, title, description, completed):
    todo_data = {"title": title, "description": description, "completed": completed}
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=todo_data)
    if response.status_code == 200:
        st.success("Tâche mise à jour avec succès!")
        st.rerun()
    else:
        st.error("Erreur lors de la mise à jour de la tâche.")

# Fonction pour supprimer une tâche
def delete_todo(todo_id):
    response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
    if response.status_code == 200:
        st.success("Tâche supprimée avec succès!")
        st.rerun()
    else:
        st.error("Erreur lors de la suppression de la tâche.")

# Interface Streamlit
st.title("Application To-Do avec FastAPI")

create_todo()

st.header("Liste des tâches")
todos = get_todos()

for todo in todos:
    with st.expander(f"{todo['title']} - {'Complétée' if todo['completed'] else 'Non complétée'}"):
        new_title = st.text_input("Modifier le titre", todo["title"], key=f"title_{todo['id']}")
        new_description = st.text_area("Modifier la description", todo["description"] or "", key=f"desc_{todo['id']}")
        new_completed = st.checkbox("Complétée", todo["completed"], key=f"comp_{todo['id']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Mettre à jour", key=f"update_{todo['id']}"):
                update_todo(todo["id"], new_title, new_description, new_completed)
        with col2:
            if st.button("Supprimer", key=f"delete_{todo['id']}"):
                delete_todo(todo["id"])
