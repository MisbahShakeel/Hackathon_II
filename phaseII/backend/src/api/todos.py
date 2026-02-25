from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from typing import List
from uuid import UUID
import uuid
from ..database.session import get_db
from ..models.todo import Todo, TodoCreate, TodoRead, TodoUpdate
from ..models.user import User
from ..core.security import verify_token
from jose import JWTError

router = APIRouter()

def get_current_user_from_request(request: Request, db: Session = Depends(get_db)) -> User:
    """
    Extract user from the authorization header, assuming Better Auth JWT format
    """
    authorization = request.headers.get("authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = authorization.split(" ")[1]
    user_id = verify_token(token)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Convert string user_id to UUID for database lookup
    from uuid import UUID as UUID_TYPE
    user_uuid = UUID_TYPE(user_id)
    user = db.get(User, user_uuid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

@router.get("/", response_model=List[TodoRead])
def read_todos(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user_from_request),
    db: Session = Depends(get_db)
):
    """
    Retrieve todos for the current user.
    """
    statement = select(Todo).where(Todo.owner_id == current_user.id).offset(skip).limit(limit)
    result = db.execute(statement)
    todos = result.scalars().all()
    return todos

@router.post("/", response_model=TodoRead)
def create_todo(
    request: Request,
    todo: TodoCreate,
    current_user: User = Depends(get_current_user_from_request),
    db: Session = Depends(get_db)
):
    """
    Create a new todo for the current user.
    """
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        owner_id=current_user.id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/{todo_id}", response_model=TodoRead)
def read_todo(
    request: Request,
    todo_id: UUID,  # Using UUID type for proper validation
    current_user: User = Depends(get_current_user_from_request),
    db: Session = Depends(get_db)
):
    """
    Get a specific todo by ID.
    """
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if str(todo.owner_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this todo")
    return todo

@router.put("/{todo_id}", response_model=TodoRead)
def update_todo(
    request: Request,
    todo_id: UUID,  # Using UUID type for proper validation
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user_from_request),
    db: Session = Depends(get_db)
):
    """
    Update a specific todo.
    """
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if str(todo.owner_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this todo")

    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)

    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/{todo_id}")
def delete_todo(
    request: Request,
    todo_id: UUID,  # Using UUID type for proper validation
    current_user: User = Depends(get_current_user_from_request),
    db: Session = Depends(get_db)
):
    """
    Delete a specific todo.
    """
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if str(todo.owner_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this todo")

    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}