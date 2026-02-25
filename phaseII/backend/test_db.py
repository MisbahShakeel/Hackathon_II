from src.main import app
from src.database.session import create_db_and_tables
from sqlmodel import Session
from src.models.user import User, UserCreate
from src.core.security import get_password_hash

# Initialize database
print("Creating database tables...")
create_db_and_tables()
print("Tables created successfully!")

# Test database connection
from src.database.session import engine
with Session(engine) as session:
    print("Database connection successful!")
    
    # Test creating a user
    print("Testing user creation...")
    user_data = UserCreate(email="test@example.com", password="testpassword")
    hashed_password = get_password_hash(user_data.password)
    db_user = User(email=user_data.email, hashed_password=hashed_password)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    print(f"User created successfully with ID: {db_user.id}")
    
    # Clean up test user
    session.delete(db_user)
    session.commit()
    print("Test completed successfully!")