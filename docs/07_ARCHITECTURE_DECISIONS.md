# Architecture Decisions

# Faym User Payout Management System

**Author:** Vishwanath Mishra

---

# 1. Introduction

Architectural decisions significantly influence the maintainability, scalability, and long-term evolution of a software system.

This document records the key architectural decisions made during the development of the Faym User Payout Management System, along with the rationale, alternatives considered, and associated trade-offs.

The goal of these decisions was to create a backend application that is modular, maintainable, testable, and easily extensible while keeping the implementation appropriate for the project's scope.

---

# 2. Decision Summary

| Decision | Selected Option |
|-----------|-----------------|
| Backend Framework | FastAPI |
| Programming Language | Python 3.13 |
| Database | SQLite |
| ORM | SQLAlchemy |
| Architecture | Layered Architecture |
| Design Pattern | Repository-Service Pattern |
| Validation | Pydantic |
| Financial Calculations | Decimal |
| API Documentation | OpenAPI / Swagger |
| Error Handling | Global Exception Handler |
| Dependency Management | FastAPI Dependency Injection |

---

# ADR-001: Layered Architecture

## Decision

Adopt a layered architecture consisting of:

- API Layer
- Service Layer
- Repository Layer
- Database Layer

```
Client

↓

API Layer

↓

Service Layer

↓

Repository Layer

↓

Database
```

---

## Context

Business logic, HTTP request handling, and database operations have different responsibilities.

Combining them in the same class increases coupling and makes maintenance difficult.

---

## Alternatives Considered

### Option 1

Everything inside API routes.

Example

```
Route

↓

Business Logic

↓

Database
```

Advantages

- Less code
- Faster initial development

Disadvantages

- Difficult to maintain
- Poor scalability
- Hard to test

---

### Option 2 (Selected)

Layered Architecture

Advantages

- Separation of concerns
- Easier testing
- Better maintainability
- Improved scalability

---

## Consequences

Positive

- Cleaner codebase
- Modular design
- Easier debugging

Negative

- More files
- Additional abstraction

---

# ADR-002: Repository-Service Pattern

## Decision

Separate database operations from business logic.

```
Service

↓

Repository

↓

Database
```

---

## Context

Business rules should not depend directly on database implementation.

Repositories encapsulate persistence while services coordinate business workflows.

---

## Alternatives Considered

Direct database queries inside services.

```
Service

↓

Database
```

Advantages

- Less code

Disadvantages

- Tight coupling
- Difficult testing
- Code duplication

---

## Decision Rationale

Repositories centralize database operations.

Services remain focused on business rules.

---

## Consequences

Positive

- Reusable queries
- Cleaner services
- Better unit testing

Negative

- Additional abstraction layer

---

# ADR-003: FastAPI as Backend Framework

## Decision

Use FastAPI.

---

## Context

The project requires

- REST APIs
- Validation
- Swagger documentation
- High performance

---

## Alternatives Considered

### Flask

Pros

- Lightweight
- Large ecosystem

Cons

- Manual validation
- Manual API documentation

---

### Django

Pros

- Batteries included

Cons

- Heavy framework
- More suitable for full-stack applications

---

### FastAPI (Selected)

Pros

- Automatic validation
- Automatic documentation
- High performance
- Dependency Injection
- Excellent type support

---

## Consequences

Positive

- Less boilerplate
- Cleaner APIs
- Better developer experience

Negative

- Smaller ecosystem compared to Django

---

# ADR-004: SQLAlchemy ORM

## Decision

Use SQLAlchemy ORM.

---

## Context

Database access should remain independent of SQL syntax.

---

## Alternatives Considered

### Raw SQL

Advantages

- Maximum performance

Disadvantages

- Difficult maintenance
- Vendor-specific queries
- More repetitive code

---

### SQLAlchemy (Selected)

Advantages

- ORM abstraction
- Relationship mapping
- Cleaner code
- Database portability

---

## Consequences

Positive

- Easier maintenance
- Better readability

Negative

- Slight ORM overhead

---

# ADR-005: SQLite Database

## Decision

Use SQLite.

---

## Context

The project is intended as a backend assignment and prototype.

A lightweight database is sufficient.

---

## Alternatives Considered

### PostgreSQL

Advantages

- Production-ready
- Better concurrency

Disadvantages

- Additional setup
- More operational complexity

---

### SQLite (Selected)

Advantages

- Lightweight
- Zero configuration
- Easy setup
- Portable

---

## Consequences

Positive

- Simple development
- Easy evaluation

Negative

- Limited concurrent write capability

Future production deployments should migrate to PostgreSQL.

---

# ADR-006: Pydantic Validation

## Decision

Use Pydantic for request validation.

---

## Context

Incoming requests should be validated before reaching business logic.

---

## Alternatives Considered

Manual validation.

Example

```python
if amount <= 0:
    ...
```

Advantages

- Flexible

Disadvantages

- Repetitive
- Error-prone

---

### Pydantic (Selected)

Advantages

- Automatic validation
- Type safety
- Better documentation
- Less boilerplate

---

## Consequences

Positive

- Cleaner services
- Automatic HTTP 422 responses

Negative

- Strict typing requires careful schema design

---

# ADR-007: Global Exception Handling

## Decision

Use centralized exception handling.

---

## Context

Business errors should return consistent API responses.

---

## Alternatives Considered

try/except blocks inside every route.

Advantages

- Simple

Disadvantages

- Repeated code
- Inconsistent responses

---

### Global Exception Handler (Selected)

Advantages

- Cleaner routes
- Standardized responses
- Easier maintenance

---

## Consequences

Positive

- Better API consistency
- Centralized error management

Negative

- Initial setup required

---

# ADR-008: Decimal for Monetary Values

## Decision

Use Decimal instead of float.

---

## Context

Financial applications require precise calculations.

---

## Alternatives Considered

float

Advantages

- Faster

Disadvantages

- Precision loss

Example

```
0.1 + 0.2

=

0.30000000000000004
```

---

### Decimal (Selected)

Advantages

- Exact arithmetic
- Suitable for financial systems

---

## Consequences

Positive

- Accurate payouts
- Consistent balance calculations

Negative

- Slight performance overhead

---

# ADR-009: Idempotent Advance Payout Processing

## Decision

Make advance payout processing idempotent.

---

## Context

The advance payout job may be executed multiple times due to retries or scheduling.

Duplicate payments must never occur.

---

## Implementation

Before creating an advance payout, the service checks whether one already exists.

```
Advance Exists?

↓

Yes

↓

Skip Processing

↓

No Duplicate Payment
```

---

## Alternatives Considered

Always create a payout.

Advantages

- Simpler implementation

Disadvantages

- Duplicate financial transactions
- Incorrect balances

---

## Consequences

Positive

- Safe retries
- Prevents duplicate payouts
- Reliable financial workflow

Negative

- Additional database lookup before payout creation

---

# ADR-010: OpenAPI Documentation

## Decision

Use FastAPI's automatic Swagger documentation.

---

## Context

Developers should be able to explore and test APIs without additional tools.

---

## Benefits

- Interactive API documentation
- Automatic schema generation
- Easier integration testing
- Improved developer experience

---

# 3. Architectural Principles

The system follows several software engineering principles.

## Separation of Concerns

Each layer performs a single responsibility.

---

## Single Responsibility Principle

Each class has one reason to change.

---

## Dependency Inversion

Services depend on repositories rather than direct database access.

---

## Modularity

Components are independently maintainable.

---

## Extensibility

Future features can be added without major restructuring.

---

# 4. Future Architectural Evolution

The current architecture can be extended to support:

- PostgreSQL
- Docker
- Redis
- JWT Authentication
- Role-Based Access Control
- Background Workers (Celery)
- Message Queues
- Distributed Caching
- API Versioning
- Cloud Deployment
- CI/CD Pipelines

The layered architecture ensures these enhancements require minimal changes to the existing codebase.

---

# 5. Conclusion

The architectural decisions made in this project prioritize maintainability, scalability, correctness, and clean software design.

Rather than optimizing for the smallest amount of code, the project emphasizes clear separation of responsibilities, reusable components, and robust business logic.

The combination of Layered Architecture, the Repository-Service Pattern, FastAPI, SQLAlchemy, centralized exception handling, and idempotent payout processing provides a solid foundation for a production-ready backend system while remaining appropriate for the scope of the assignment.