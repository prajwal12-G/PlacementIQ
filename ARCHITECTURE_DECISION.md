# PlacementIQ Architecture Decisions

Version: 1.0
Status: Active

---

# Purpose

This document explains *why* the backend architecture is designed the way it is.

It is not a progress log.

It explains the reasoning behind every important design decision so future contributors (human or AI) do not accidentally break the architecture.

---

# Overall Architecture

PlacementIQ follows a layered architecture.

```
Client
    │
    ▼
FastAPI Router (HTTP Layer)
    │
    ▼
Service Layer (Business Logic)
    │
    ▼
Repository Layer (Database Access)
    │
    ▼
MySQL Database
```

Each layer has exactly one responsibility.

---

# Why Layered Architecture?

The project is expected to become large.

Future modules include

- Resume Parser
- ATS Engine
- AI Resume Feedback
- Interview Engine
- Job Recommendation
- Student Dashboard
- Analytics
- Admin Panel

Putting everything inside routes would quickly become impossible to maintain.

The layered approach keeps every responsibility isolated.

---

# Router Responsibilities

Routers only handle HTTP.

A router should

- receive requests
- validate input
- call a service
- return responses

A router must NEVER

- execute SQL
- hash passwords
- verify passwords
- generate JWT logic
- contain business rules

Example:

Good

```
POST /auth/login

↓

AuthService.login_user()
```

Bad

```
POST /auth/login

↓

query database

↓

verify password

↓

generate token

↓

return response
```

---

# Service Responsibilities

Services contain business logic.

Services answer questions like

"What should happen when a user registers?"

"What should happen when a user logs in?"

"What should happen when a resume is uploaded?"

Services may

- validate business rules
- hash passwords
- compare passwords
- call repositories
- generate tokens
- combine multiple repositories

Services must NEVER write SQL.

---

# Repository Responsibilities

Repositories only communicate with the database.

Repositories know

- SQLAlchemy
- queries
- inserts
- updates
- deletes

Repositories DO NOT know

- JWT
- Password hashing
- Business rules
- FastAPI

Repositories should remain thin.

---

# Dependency Injection

Everything is injected using FastAPI dependencies.

Instead of

```
AuthService()
```

the application uses

```
Depends(get_auth_service)
```

This provides

- easier testing
- loose coupling
- cleaner architecture

---

# Database Session Ownership

The database session is created once per request.

```
get_db()

↓

yield Session

↓

close session
```

Services never create sessions.

Repositories never create sessions.

Only FastAPI dependencies manage session lifecycle.

---

# Authentication Design

Authentication currently supports

- Registration
- Login
- JWT generation

JWT verification has not yet been completed.

Future endpoints will use

```
Depends(get_current_user)
```

instead of manually reading Authorization headers.

---

# Password Strategy

Passwords are never stored.

Only bcrypt hashes are stored.

Flow

```
password

↓

hash_password()

↓

database
```

Login

```
password

↓

verify_password()

↓

True / False
```

---

# JWT Strategy

JWT contains only minimal identity.

Current payload

```
{
    "sub": email
}
```

Later this may include

```
id
role
permissions
token version
```

The token should never contain sensitive user information.

---

# Why Email in JWT?

Email is currently unique.

It allows retrieving the user quickly.

Later the project may migrate to

```
sub = user_id
```

without changing service architecture.

---

# Response Models

ORM models never leave the service directly.

Every API returns Pydantic schemas.

Example

```
User ORM

↓

UserResponse

↓

JSON
```

Benefits

- hides password
- hides internal fields
- stable API contract

---

# Error Handling

Business errors are raised inside services.

Example

```
email already exists

↓

HTTPException(400)
```

Authentication failure

```
invalid password

↓

HTTPException(401)
```

Repositories should not raise HTTP exceptions.

---

# Configuration

Secrets belong only inside

```
.env
```

Configuration is loaded through

```
Settings
```

inside

```
core/config.py
```

No secrets should appear inside source code.

---

# Why Not Generic Repository?

The project intentionally avoids generic repositories.

Example

```
BaseRepository
```

was rejected.

Reason

Every aggregate eventually gains unique queries.

UserRepository

ResumeRepository

JobRepository

InterviewRepository

would all diverge anyway.

Keeping repositories explicit improves readability.

---

# Why Not CRUD Classes?

Generic CRUD classes hide logic and become difficult to debug.

Explicit repositories are preferred.

Future contributors should immediately understand every query.

---

# Why SQLAlchemy ORM?

Reasons

- mature
- type hints
- relationships
- migrations
- integrates well with FastAPI

---

# Migration Strategy

Development currently uses

```
Base.metadata.create_all()
```

Production will use

```
Alembic
```

No production deployment should rely on create_all().

---

# Testing Strategy

Future tests should target layers independently.

Repository tests

↓

database only

Service tests

↓

fake repositories

Router tests

↓

HTTP requests

This separation allows faster and more reliable testing.

---

# Scalability

Future services

```
ResumeService

InterviewService

ATSService

RecommendationService

AnalyticsService

JobService

AdminService
```

should follow the exact same architecture.

No shortcuts should be introduced.

---

# Architecture Principle

Every new feature should answer three questions.

1.

Where does HTTP belong?

Router

2.

Where does business logic belong?

Service

3.

Where does SQL belong?

Repository

If those answers remain true, the architecture remains healthy.