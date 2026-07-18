# Low-Level Design (LLD)

# Faym User Payout Management System

**Author:** Vishwanath Mishra

---

# 1. Introduction

## 1.1 Purpose

The Faym User Payout Management System is a backend application developed to automate the payout lifecycle for users earning through sales.

The system manages:

- Advance payouts
- Sale reconciliation
- Final payouts
- User withdrawals
- Payment transaction tracking

The application is implemented using **FastAPI**, **SQLAlchemy**, and **SQLite**, following a layered architecture that separates API handling, business logic, and database operations.

---

## 1.2 Objectives

The primary objectives of the project are:

- Design a scalable backend architecture.
- Separate business logic from database operations.
- Provide clean REST APIs.
- Ensure proper validation and exception handling.
- Maintain data consistency during payout processing.
- Build an easily maintainable and extensible codebase.

---

# 2. System Architecture

The project follows a **Layered Architecture** using the **Repository-Service Pattern**.

```
                    Client
                       │
                       ▼
              FastAPI Route Layer
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
                 SQLite Database
```

Each layer has a dedicated responsibility, ensuring low coupling and high cohesion.

---

# 3. Layer Description

## 3.1 API Layer

Location:

```
app/api/
```

Responsibilities:

- Define REST endpoints
- Validate request payloads
- Return HTTP responses
- Inject dependencies
- Call service layer methods
- Convert exceptions into API responses

The API layer contains **no business logic**.

Example:

```
POST /users/{user_id}/withdraw
```

↓

Calls

```
WithdrawalService.withdraw()
```

---

## 3.2 Service Layer

Location

```
app/services/
```

Responsibilities:

- Implement business rules
- Coordinate multiple repositories
- Validate business constraints
- Maintain transactional integrity

Services implemented:

### AdvancePayoutService

Responsible for:

- Creating advance payouts
- Validating sale existence
- Calculating advance amount (10%)

---

### ReconciliationService

Responsible for:

- Approving sales
- Rejecting sales
- Creating final payouts
- Creating adjustment payouts
- Preventing duplicate reconciliation

---

### WithdrawalService

Responsible for:

- Balance calculation
- Withdrawal validation
- Payment transaction creation
- Withdrawal processing

---

## 3.3 Repository Layer

Location

```
app/repositories/
```

Responsibilities:

- Perform CRUD operations
- Execute SQLAlchemy queries
- Hide database implementation from services

Repositories implemented:

### SaleRepository

Operations

- Find sale
- Update status

---

### PayoutRepository

Operations

- Create payout
- Fetch payouts

---

### WithdrawalRepository

Operations

- Create withdrawal
- Calculate withdrawn amount

---

### PaymentTransactionRepository

Operations

- Create payment transaction
- Track payment status

---

## 3.4 Database Layer

The database layer is implemented using SQLAlchemy ORM.

SQLite is used as the persistence layer.

Benefits:

- ORM abstraction
- Database independence
- Object-oriented querying
- Easy migration to PostgreSQL

---

# 4. Request Flow

## 4.1 Advance Payout Flow

```
Client
   │
   │ POST /payouts/advance
   ▼
Advance Router
   │
   ▼
AdvancePayoutService
   │
   ▼
SaleRepository
   │
   ▼
Database
   │
   ▼
PayoutRepository
   │
   ▼
Database
   │
   ▼
Response
```

---

## 4.2 Sale Reconciliation Flow

```
Client
   │
   │ POST /sales/{id}/reconcile
   ▼
Reconciliation Router
   │
   ▼
ReconciliationService
   │
   ▼
SaleRepository
   │
   ▼
Update Sale Status
   │
   ▼
PayoutRepository
   │
   ▼
Create Final / Adjustment Payout
   │
   ▼
Database
   │
   ▼
Response
```

---

## 4.3 Withdrawal Flow

```
Client
   │
   │ POST /users/{id}/withdraw
   ▼
Withdrawal Router
   │
   ▼
WithdrawalService
   │
   ▼
WithdrawalRepository
   │
   ▼
Calculate Balance
   │
   ▼
Validate Funds
   │
   ▼
Create Withdrawal
   │
   ▼
PaymentTransactionRepository
   │
   ▼
Create Payment Transaction
   │
   ▼
Database
   │
   ▼
Response
```

---

# 5. Dependency Injection

FastAPI's dependency injection mechanism is used to inject database sessions.

```
Client Request

↓

FastAPI

↓

Depends(get_db)

↓

Database Session

↓

Repositories

↓

Services

↓

Response
```

Benefits:

- Loose coupling
- Easier testing
- Better scalability
- Centralized resource management

---

# 6. Project Structure

```
app
│
├── api
│   ├── deps.py
│   ├── router.py
│   └── routes/
│
├── core
│   ├── config.py
│   ├── database.py
│   ├── exceptions.py
│   └── exception_handlers.py
│
├── models
│
├── repositories
│
├── schemas
│
├── services
│
├── enums.py
│
└── main.py
```

---

# 7. Component Responsibilities

## Models

Represent database entities.

Examples

- User
- Sale
- Payout
- Withdrawal
- PaymentTransaction
- Brand

---

## Schemas

Responsible for request and response validation.

Implemented using Pydantic.

Examples

- WithdrawalRequest
- BalanceResponse
- AdvancePayoutRequest
- ReconciliationRequest

---

## Repositories

Responsible only for data access.

No business logic.

---

## Services

Responsible only for business logic.

No HTTP handling.

---

## Routes

Responsible only for API endpoints.

No database queries.

---

# 8. Design Principles

The project follows the following software engineering principles.

## Single Responsibility Principle

Each layer performs only one responsibility.

Example

Repository

↓

Database operations only

---

Service

↓

Business logic only

---

API

↓

Request handling only

---

## Separation of Concerns

Each module has an independent responsibility.

This improves readability and maintainability.

---

## Dependency Inversion

Services depend on repository abstractions instead of direct database access.

---

## Reusability

Repositories can be reused across multiple services.

---

## Scalability

The architecture supports future migration to:

- PostgreSQL
- MySQL
- Async SQLAlchemy
- Redis
- Docker
- Microservices

without significant architectural changes.

---

# 9. Advantages of the Chosen Architecture

The selected architecture provides several benefits:

- Clear separation between layers.
- Easy debugging and maintenance.
- High code readability.
- Better scalability.
- Easier unit testing.
- Reusable repositories.
- Independent business logic.
- Reduced code duplication.
- Improved extensibility.

---

# 10. Summary

The Faym User Payout Management System follows a clean layered architecture using FastAPI, SQLAlchemy, and the Repository-Service Pattern.

The design ensures that API handling, business logic, and database access remain independent, making the system maintainable, scalable, and suitable for production-level backend development.

This architecture also enables future enhancements such as authentication, asynchronous processing, PostgreSQL migration, Docker deployment, and cloud-native scalability with minimal code changes.