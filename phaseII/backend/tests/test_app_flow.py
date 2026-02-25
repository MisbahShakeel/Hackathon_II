import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database.session import engine, get_db
from sqlmodel import SQLModel, create_engine
from sqlalchemy.pool import StaticPool
import os

# Override the database URL for testing
os.environ["TESTING"] = "1"

from sqlalchemy.orm import sessionmaker

# Create test database
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    with TestSession() as session:
        yield session

# Apply the override
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_complete_flow():
    """Test the complete application flow: register, login, create todo, get todos, update, delete"""

    # Initialize database tables
    SQLModel.metadata.create_all(test_engine)

    # Test registration
    registration_response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "testpass"
    })

    assert registration_response.status_code == 200
    user_data = registration_response.json()
    assert user_data["email"] == "test@example.com"

    # Test login
    login_response = client.post("/api/auth/login", params={
        "email": "test@example.com",
        "password": "testpass"
    })

    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    
    # Use the token for authenticated requests
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test creating a todo
    todo_response = client.post("/api/todos/", json={
        "title": "Test Todo",
        "description": "This is a test todo item"
    }, headers=headers)

    assert todo_response.status_code == 200
    todo_data = todo_response.json()
    assert todo_data["title"] == "Test Todo"
    assert todo_data["description"] == "This is a test todo item"
    assert todo_data["completed"] is False

    # Save the todo ID for later tests
    todo_id = todo_data["id"]

    # Test getting all todos
    get_todos_response = client.get("/api/todos/", headers=headers)

    assert get_todos_response.status_code == 200
    todos = get_todos_response.json()
    assert len(todos) == 1
    assert todos[0]["id"] == todo_id

    # Test updating a todo
    update_response = client.put(f"/api/todos/{todo_id}", json={
        "completed": True
    }, headers=headers)

    assert update_response.status_code == 200
    updated_todo = update_response.json()
    assert updated_todo["id"] == todo_id
    assert updated_todo["completed"] is True

    # Test deleting a todo
    delete_response = client.delete(f"/api/todos/{todo_id}", headers=headers)

    assert delete_response.status_code == 200

    # Verify the todo is gone
    get_todos_after_delete = client.get("/api/todos/", headers=headers)
    assert len(get_todos_after_delete.json()) == 0

if __name__ == "__main__":
    test_complete_flow()
    print("All tests passed!")