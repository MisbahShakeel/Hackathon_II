# 🧩 Skill Prompt — Database Skill (Neon Serverless PostgreSQL)

This skill is focused on managing **Neon Serverless PostgreSQL** operations for modern full-stack applications.

This skill should implement reliable, scalable, and secure database logic without breaking application features.

## Responsibilities
- Configure and manage Neon Serverless PostgreSQL connections
- Design and maintain database schemas (tables, relations, constraints)
- Write safe and efficient SQL queries
- Implement CRUD operations with clean database logic
- Handle migrations and schema evolution safely
- Optimize query performance using indexes and query analysis
- Manage transactions properly for multi-step operations
- Prevent SQL injection using parameterized queries
- Support integration with Next.js, FastAPI, and serverless runtimes

## Guidelines
- Use environment variables for all credentials and connection strings
- Prefer connection pooling or Neon-recommended serverless connection handling
- Use constraints and foreign keys for data integrity
- Keep schemas consistent and normalized where appropriate
- Write queries that are readable, maintainable, and testable
- Avoid unnecessary joins, heavy queries, and unbounded selects
- Ensure error handling does not leak sensitive database details

## When to Use This Skill
Use this skill whenever:
- Creating or updating database schemas
- Writing SQL queries or database logic
- Debugging database connection issues
- Improving database performance
- Implementing Postgres operations for APIs and web apps
