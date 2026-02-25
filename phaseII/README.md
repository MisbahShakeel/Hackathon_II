# Todo Web Application

A modern multi-user todo application built with Next.js, FastAPI, and Neon Serverless PostgreSQL.

## Features

- User registration and authentication
- Secure todo management (Create, Read, Update, Delete)
- Multi-user isolation (users can only see their own todos)
- Responsive UI that works on all device sizes
- JWT-based authentication
- SQLModel ORM with PostgreSQL database

## Tech Stack

- **Frontend**: Next.js 16+ (App Router)
- **Backend**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Custom JWT implementation (compatible with Better Auth patterns)
- **Styling**: Tailwind CSS

## Project Structure

```
todo-web-app/
├── backend/
│   ├── src/
│   │   ├── models/          # Database models
│   │   ├── api/             # API routes
│   │   ├── core/            # Core utilities
│   │   ├── database/        # Database configuration
│   │   └── auth/            # Authentication utilities
│   ├── requirements.txt
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js app router pages
│   │   ├── components/      # React components
│   │   ├── lib/             # Utilities and API clients
│   │   ├── hooks/           # Custom React hooks
│   │   └── styles/          # Global styles
│   ├── package.json
│   └── next.config.js
└── specs/
    └── todo-web-app/        # Project specifications
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database connection and secret key
```

5. Start the backend server:
```bash
uvicorn src.main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Visit `http://localhost:3000` in your browser

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

### Todos
- `GET /api/todos` - Get all todos for the authenticated user
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a specific todo
- `DELETE /api/todos/{id}` - Delete a specific todo

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=your_neon_postgresql_connection_string
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
BACKEND_API_URL=http://localhost:8000
```

## Running Tests

To run backend tests:
```bash
cd backend
pytest
```

## Deployment

### Backend
The FastAPI application can be deployed to any Python hosting service. Make sure to configure the production database URL and secret key.

### Frontend
The Next.js application can be deployed to Vercel, Netlify, or any hosting service that supports Next.js applications.

## Security Features

- Passwords are hashed using bcrypt
- JWT tokens with expiration times
- User data isolation (users can only access their own todos)
- Input validation using Pydantic models
- CORS configured for secure cross-origin requests

## Development

This project was developed using the Spec-Driven Development approach with Claude Code and Spec-Kit Plus, following the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code.