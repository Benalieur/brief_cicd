def test_get_todo_by_id(client):
    # Simulate a response from the API
    mock_todo = {
        "id": 1,
        "title": "Task 1",
        "description": "Description 1",
        "completed": False,
    }

    # Mock the API response
    client.get = lambda url: (
        type("Response", (object,), {"status_code": 200, "json": lambda: mock_todo})
        if url == "/todos/1"
        else None
    )

    # Call the function
    response = client.get("/todos/1")

    # Assertions
    assert response.status_code == 200
    assert response.json() == mock_todo


def test_create_todo(client):
    # Simulate a request and response from the API
    new_todo = {
        "title": "New Task",
        "description": "New Description",
        "completed": False,
    }
    created_todo = {"id": 1, **new_todo}

    # Mock the API response
    client.post = lambda url, json: (
        type("Response", (object,), {"status_code": 201, "json": lambda: created_todo})
        if url == "/todos"
        else None
    )

    # Call the function
    response = client.post("/todos", json=new_todo)

    # Assertions
    assert response.status_code == 201
    assert response.json() == created_todo


def test_delete_todo(client):
    # Mock the API response
    client.delete = lambda url: (
        type(
            "Response",
            (object,),
            {"status_code": 200, "json": lambda: {"message": "Tâche supprimée"}},
        )
        if url == "/todos/1"
        else None
    )

    # Call the function
    response = client.delete("/todos/1")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Tâche supprimée"}


def test_update_todo(client):
    # Simulate a request and response from the API
    updated_todo = {
        "title": "Updated Task",
        "description": "Updated Description",
        "completed": True,
    }
    returned_todo = {"id": 1, **updated_todo}

    # Mock the API response
    client.put = lambda url, json: (
        type("Response", (object,), {"status_code": 200, "json": lambda: returned_todo})
        if url == "/todos/1"
        else None
    )

    # Call the function
    response = client.put("/todos/1", json=updated_todo)

    # Assertions
    assert response.status_code == 200
    assert response.json() == returned_todo
