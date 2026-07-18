# Design Decisions & Trade-offs

# Faym User Payout Management System

**Author:** Vishwanath Mishra

---

# 1. Introduction

Building a backend application involves making several architectural and technological decisions. Every decision affects the maintainability, scalability, performance, and complexity of the system.

This document explains the major design choices made during the implementation of the Faym User Payout Management System and discusses the trade-offs associated with each decision.

---

# 2. Overall Architecture

The project follows a **Layered Architecture** combined with the **Repository-Service Pattern**.

```
                Client
                   │
                   ▼
             API Layer (Routes)
                   │
                   ▼
             Service Layer
                   │
                   ▼
          Repository Layer
                   │
                   ▼
          SQLAlchemy ORM Models
                   │
                   ▼
                SQLite
```

Each layer has a single responsibility, ensuring high cohesion and low coupling.

---

# 3. Why Repository-Service Pattern Instead of MVC?

Traditional MVC (Model-View-Controller) applications often place business logic directly inside controllers or models.

For a backend REST API, the Repository-Service Pattern provides a cleaner separation of responsibilities.

```
Request

↓

API Route

↓

Service

↓

Repository

↓

Database
```

### Benefits

- Business logic remains independent of HTTP handling.
- Database operations are centralized.
- Services are easier to test.
- Repository methods can be reused across multiple services.
- Future migration to another database requires minimal changes.

### Trade-off

The architecture introduces additional classes and folders compared to a simple MVC application. However, this improves maintainability and scalability as the application grows.

---

# 4. Why FastAPI?

FastAPI was selected as the backend framework because it provides modern Python features while requiring minimal boilerplate.

## Advantages

- High performance
- Automatic OpenAPI documentation
- Built-in request validation
- Dependency Injection
- Type-safe programming
- Excellent developer experience

Example

```python
@app.post("/users/{user_id}/withdraw")
```

automatically generates interactive Swagger documentation.

### Trade-off

FastAPI has a smaller ecosystem compared to older frameworks like Django. However, for REST API development, its simplicity and performance make it an excellent choice.

---

# 5. Why SQLAlchemy ORM?

Instead of writing raw SQL queries, SQLAlchemy ORM was used.

## Advantages

- Database abstraction
- Object-oriented querying
- Relationship management
- Better readability
- Easier maintenance

Example

Instead of

```sql
SELECT * FROM sales;
```

the application uses

```python
db.query(Sale).all()
```

### Trade-off

ORM introduces a slight performance overhead compared to handwritten SQL, but the productivity and maintainability benefits outweigh this cost for this project.

---

# 6. Why SQLite?

SQLite was chosen because this project is intended as a backend assignment and development prototype.

## Advantages

- Zero configuration
- Lightweight
- Portable
- Easy setup
- Ideal for development

### Trade-off

SQLite is not suitable for highly concurrent production systems.

The project architecture allows migration to PostgreSQL or MySQL with minimal changes.

---

# 7. Why Repository Layer?

Repositories encapsulate all database operations.

Instead of

```
Service

↓

Database
```

the project follows

```
Service

↓

Repository

↓

Database
```

### Advantages

- Clean separation of concerns
- Reusable database logic
- Easier testing
- Reduced code duplication

### Trade-off

Additional abstraction increases the number of files, but significantly improves long-term maintainability.

---

# 8. Why Service Layer?

The Service Layer contains all business rules.

Examples include:

- Advance payout calculation
- Sale reconciliation
- Balance computation
- Withdrawal validation

Services coordinate multiple repositories while keeping API routes simple.

### Advantages

- Centralized business logic
- Better readability
- Easier unit testing
- Reusable logic

### Trade-off

Adds another architectural layer but greatly improves code organization.

---

# 9. Why Dependency Injection?

FastAPI's dependency injection system is used to provide database sessions and other dependencies.

Example

```python
db: Session = Depends(get_db)
```

### Advantages

- Loose coupling
- Cleaner code
- Easier testing
- Automatic resource management

Without dependency injection, every route would need to manually create database sessions.

---

# 10. Why Pydantic?

Pydantic performs automatic request validation.

Example

```python
amount: Decimal = Field(gt=0)
```

Invalid requests are rejected before reaching business logic.

Example

```json
{
    "amount": -100
}
```

returns

```
HTTP 422 Unprocessable Entity
```

### Advantages

- Automatic validation
- Type safety
- Less boilerplate
- Better API reliability

---

# 11. Why Decimal Instead of Float?

Financial applications require precise arithmetic.

Floating-point numbers can produce rounding errors.

Example

```
0.1 + 0.2

=

0.30000000000000004
```

Using `Decimal` guarantees exact monetary calculations.

Therefore, all monetary values in the project use `Decimal`.

---

# 12. Why Enumerations?

Status fields use Enumerations instead of plain strings.

Example

```
SaleStatus

- Pending
- Approved
- Rejected
```

instead of

```
"pending"

"approved"

"rejected"
```

### Advantages

- Prevent invalid values
- Improved readability
- Type safety
- Consistent business rules

---

# 13. Why Custom Exceptions?

Instead of generic exceptions, business-specific exceptions are used.

Examples

- ValidationException
- ResourceNotFoundException
- InsufficientBalanceException
- SaleAlreadyReconciledException

### Advantages

- Consistent API responses
- Better debugging
- Cleaner service logic
- Centralized error handling

Each exception maps to an appropriate HTTP status code.

---

# 14. Why Idempotent Advance Payout Processing?

One important design decision is that the advance payout process is **idempotent**.

Before creating an advance payout, the service checks whether one already exists for the sale.

```
Advance Exists?

↓

Yes

↓

Skip Processing

↓

No Duplicate Payout
```

### Why?

In financial systems, duplicate payments can lead to serious inconsistencies.

Making the operation idempotent ensures that retrying the same request multiple times produces the same outcome.

### Benefits

- Prevents duplicate advance payouts
- Safe retry mechanism
- Improved reliability
- Better fault tolerance

This behaviour is implemented using the repository method:

```python
advance_exists(sale_id)
```

If an advance payout already exists, the service skips processing rather than creating another payout.

---

# 15. Business Rule Decisions

The application enforces several business rules.

## Advance Payout

Advance payout is fixed at **10%** of the sale earning.

Example

```
Sale = ₹1000

Advance = ₹100

Final = ₹900
```

---

## Sale Reconciliation

Each sale can only be reconciled once.

Repeated reconciliation requests are rejected.

---

## Withdrawal Validation

Users cannot withdraw more than their available balance.

```
Available Balance

=

Successful Payouts

-

Successful Withdrawals
```

---

# 16. Scalability Considerations

Although SQLite is currently used, the architecture supports future enhancements.

Potential improvements include:

- PostgreSQL
- Redis caching
- JWT Authentication
- Docker deployment
- Async SQLAlchemy
- Celery background jobs
- Payment gateway integration
- Multi-currency support

The layered architecture allows these enhancements without major structural changes.

---

# 17. Trade-offs Summary

| Decision | Benefits | Trade-offs |
|----------|----------|------------|
| FastAPI | High performance, automatic docs | Smaller ecosystem than Django |
| SQLAlchemy ORM | Cleaner data access | Slight ORM overhead |
| SQLite | Lightweight and portable | Limited concurrency |
| Repository Pattern | Better separation of concerns | More files |
| Service Layer | Centralized business logic | Additional abstraction |
| Dependency Injection | Loose coupling | Initial learning curve |
| Pydantic | Automatic validation | Strict typing |
| Decimal | Accurate financial calculations | Slightly slower than float |
| Idempotent Processing | Prevents duplicate payouts | Requires additional existence checks |

---

# 18. Future Enhancements

Possible future improvements include:

- User Authentication
- Role-Based Authorization
- Audit Logging
- Notification Service
- Refund Workflow
- Background Workers
- Scheduled Payout Processing
- Docker Deployment
- Kubernetes Support
- CI/CD Pipeline
- Cloud Database Migration

---

# 19. Conclusion

The design decisions made in this project prioritize maintainability, readability, correctness, and scalability.

The Repository-Service architecture separates concerns effectively, while FastAPI, SQLAlchemy, and Pydantic provide a modern and reliable backend foundation.

A key design decision is the use of **idempotent advance payout processing**, which ensures duplicate requests cannot generate duplicate payments. Combined with centralized exception handling, request validation, and precise financial calculations using `Decimal`, the system provides a solid foundation for a production-ready payout management service.