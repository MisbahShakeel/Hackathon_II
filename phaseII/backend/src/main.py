from fastapi import FastAPI
from .api.todos import router as todos_router
from .api.auth import router as auth_router
from .core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from .database.session import create_db_and_tables

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(todos_router, prefix="/api/todos", tags=["todos"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Todo Web Application API"}