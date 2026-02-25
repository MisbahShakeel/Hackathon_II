# Data Model: Todo Web Application

**Date**: 2026-02-08
**Feature**: Todo Web Application

## Entity Relationship Diagram

```
┌─────────────────────────┐         ┌─────────────────────────┐
│        User             │         │         Todo            │
├─────────────────────────┤    ┌───▶├─────────────────────────┤
│ id: UUID (PK)           │    │    │ id: UUID (PK)           │
│ email: String (unique)  │    │    │ title: String (not null)│
│ created_at: DateTime    │    │    │ description: Text       │
│ updated_at: DateTime    │    │    │ completed: Boolean      │
│ is_active: Boolean      │    │    │ created_at: DateTime    │
└─────────────────────────┘    │    │ updated_at: DateTime    │
                               │    │ owner_id: UUID (FK)     │
                               └────┤ owner: User (relationship)│
                                    └─────────────────────────┘
```

## Detailed Entity Definitions

### User
- **id** (UUID, Primary Key)
  - Unique identifier for each user
  - Auto-generated using UUID4
- **email** (String, unique, not null)
  - User's email address for login
  - Used as username
- **hashed_password** (String, not null)
  - BCrypt hashed password
- **created_at** (DateTime, not null)
  - Timestamp when user was created
  - Auto-populated
- **updated_at** (DateTime, not null)
  - Timestamp when user was last updated
  - Auto-populated
- **is_active** (Boolean, default: true)
  - Whether the user account is active

### Todo
- **id** (UUID, Primary Key)
  - Unique identifier for each todo
  - Auto-generated using UUID4
- **title** (String, not null)
  - Title of the todo item
  - Maximum length: 255 characters
- **description** (Text, nullable)
  - Optional detailed description of the todo
- **completed** (Boolean, default: false)
  - Whether the todo is marked as completed
- **created_at** (DateTime, not null)
  - Timestamp when todo was created
  - Auto-populated
- **updated_at** (DateTime, not null)
  - Timestamp when todo was last updated
  - Auto-populated
- **owner_id** (UUID, Foreign Key)
  - References the User who owns this todo
  - Enforces referential integrity

## Relationships
- One User to Many Todos (one-to-many)
- Each Todo belongs to exactly one User
- When a User is deleted, their Todos are also deleted (cascade delete)

## Indexes
- User.email: Unique index for fast lookups
- Todo.owner_id: Index for efficient filtering by user
- Todo.created_at: Index for chronological sorting

## Constraints
- User.email must be unique
- Todo.title cannot be empty/null
- Todo.owner_id must reference an existing User
- Prevent deletion of User if they have associated Todos (to be reviewed for cascade policy)