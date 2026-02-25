# 🧩 Skill Prompt — Backend Skill (FastAPI REST APIs)

This skill is focused on building and maintaining **FastAPI backend systems** for modern full-stack applications.

This skill should implement secure, scalable, and maintainable backend logic without breaking application features.

## Responsibilities
- Build REST APIs using FastAPI with clean routing structure
- Create request/response schemas using Pydantic
- Validate all inputs (body, query params, headers, path params)
- Implement authentication and authorization integration (JWT, Better Auth, sessions)
- Build protected endpoints and enforce access control rules
- Implement database interaction safely (CRUD, transactions, relationships)
- Ensure compatibility with Neon Serverless PostgreSQL
- Handle consistent error responses and HTTP status codes
- Apply backend security best practices (CORS, rate limiting, sanitization)
- Debug backend issues including validation errors and database failures

## Guidelines
- Keep clear separation of concerns (routers, services, database layer)
- Prefer dependency injection for auth and database access
- Use strict validation and never trust client input
- Avoid leaking sensitive data in logs and error messages
- Write backend code that is testable and easy to maintain
- Keep API responses consistent and predictable
- Prioritize correctness and security over shortcuts

## When to Use This Skill
Use this skill whenever:
- Building FastAPI endpoints
- Adding validation with Pydantic
- Integrating auth into API routes
- Connecting backend logic with Postgres
- Fixing backend bugs or improving API reliability
