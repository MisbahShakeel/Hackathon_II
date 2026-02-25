# Quickstart Guide: Todo Web Application

**Date**: 2026-02-08
**Feature**: Todo Web Application

## Prerequisites

- Node.js 18+ (for Next.js frontend)
- Python 3.11+ (for FastAPI backend)
- PostgreSQL client tools
- Git
- A Neon Serverless PostgreSQL account

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Database Setup
1. Create a Neon Serverless PostgreSQL project
2. Copy the connection string
3. Create a `.env` file in the backend directory with:
```env
DATABASE_URL=your_neon_connection_string
SECRET_KEY=your_secret_key_for_jwt_tokens
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Better Auth Configuration
Add the following to your environment files:
```env
# Backend
AUTH_SECRET=your_better_auth_secret

# Frontend
NEXT_PUBLIC_AUTH_URL=http://localhost:3000/api/auth
```

## Running the Application

### 1. Start the Backend
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

### 2. Start the Frontend
```bash
cd frontend
npm run dev
```

### 3. Access the Application
Open your browser to `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/logout` - Logout user

### Todos
- `GET /api/todos` - Get all todos for the authenticated user
- `POST /api/todos` - Create a new todo
- `PUT /api/todos/{id}` - Update a todo
- `DELETE /api/todos/{id}` - Delete a todo

## Development Commands

### Backend
- Run tests: `pytest`
- Format code: `black .`
- Lint: `flake8`

### Frontend
- Run tests: `npm test`
- Build: `npm run build`
- Lint: `npm run lint`

## Troubleshooting

### Common Issues
1. **Database Connection**: Ensure your Neon Serverless PostgreSQL connection string is correct
2. **JWT Expiration**: Tokens expire after 30 minutes by default; increase if needed
3. **CORS Issues**: Make sure frontend and backend origins are properly configured
4. **Authentication**: Verify that JWT tokens are properly included in API requests