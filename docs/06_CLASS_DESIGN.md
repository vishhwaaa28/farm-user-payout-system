# Class Design

# Faym User Payout Management System

**Author:** Vishwanath Mishra

---

# 1. Introduction

The Faym User Payout Management System follows an object-oriented design where each class has a clearly defined responsibility.

The project adopts the Repository-Service Pattern, separating business logic, data access, request validation, and persistence into independent components.

This separation improves readability, maintainability, and scalability while adhering to object-oriented design principles such as the Single Responsibility Principle (SRP) and Separation of Concerns (SoC).

---

# 2. Class Architecture

```
                        FastAPI Routes
                               │
                               ▼
                    ┌────────────────────┐
                    │      Services       │
                    └────────────────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
     AdvancePayout     Reconciliation     Withdrawal
         Service           Service           Service
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌────────────────────┐
                    │    Repositories     │
                    └────────────────────┘
                               │
             ┌─────────────────┼──────────────────┐
             ▼                 ▼                  ▼
      SaleRepository   PayoutRepository   WithdrawalRepository
                               │
                               ▼
                 PaymentTransactionRepository
                               │
                               ▼
                    SQLAlchemy ORM Models
                               │
                               ▼
                          SQLite Database
```

# 2.1 UML Class Diagram

The following UML Class Diagram illustrates the relationships between the major classes in the application.

```text
                                        +----------------------+
                                        |    FastAPI Routes    |
                                        +----------------------+
                                                   |
                                                   |
                              -----------------------------------------
                              |                   |                   |
                              |                   |                   |
                              ▼                   ▼                   ▼
               +----------------------+ +----------------------+ +----------------------+
               | AdvancePayoutService | | ReconciliationService| |  WithdrawalService  |
               +----------------------+ +----------------------+ +----------------------+
               | +calculateAdvance()  | | +reconcileSale()     | | +withdraw()         |
               | +processSale()       | |                      | | +getBalance()       |
               | +run()               | |                      | |                     |
               +----------+-----------+ +----------+-----------+ +----------+----------+
                          |                          |                          |
            --------------+--------------------------+--------------------------+
                          |                          |                          |
                          ▼                          ▼                          ▼
                +----------------+         +----------------+        +----------------------+
                | SaleRepository |         |PayoutRepository|        |WithdrawalRepository |
                +----------------+         +----------------+        +----------------------+
                | +getById()     |         | +create()      |        | +create()           |
                | +getPending()  |         | +advanceExists()|       | +getTotalWithdrawn()|
                | +updateStatus()|         | +getBySale()   |        +----------+----------+
                +--------+-------+         | +createPayout()|                   |
                         |                 | +getTotal()    |                   |
                         |                 +--------+-------+                   |
                         |                          |                           |
                         |                          |                           |
                         |                          ▼                           ▼
                         |              +--------------------------+   +--------------------------+
                         |              | PaymentTransactionRepo   |   |      SQLAlchemy ORM      |
                         |              +--------------------------+   +--------------------------+
                         |              | +createTransaction()     |              |
                         |              +------------+-------------+              |
                         |                           |                            |
                         ----------------------------+----------------------------
                                                     |
                                                     ▼
                                      +----------------------------------+
                                      |        Database Models           |
                                      +----------------------------------+
                                      | Brand                            |
                                      | User                             |
                                      | Sale                             |
                                      | Payout                           |
                                      | Withdrawal                       |
                                      | PaymentTransaction               |
                                      +----------------------------------+
                                                     |
                                                     ▼
                                            SQLite Database
```

# 2.2 Class Relationships

The project follows a layered dependency structure.

```
FastAPI Routes
        │
        ▼
Service Layer
        │
        ▼
Repository Layer
        │
        ▼
ORM Models
        │
        ▼
Database
```

The dependencies are one-directional.

- Routes depend on Services.
- Services depend on Repositories.
- Repositories depend on SQLAlchemy Models.
- Models represent the database tables.

No layer depends on a higher layer, reducing coupling and making the architecture easier to maintain.

---

# 3. Domain Model Classes

The domain model represents the business entities stored in the database.

---

## Brand

### Responsibility

Represents a company or organization to which users belong.

### Key Attributes

- id
- name

### Relationships

```
Brand

↓

Users
```

---

## User

### Responsibility

Represents a user eligible to receive payouts.

### Key Attributes

- id
- brand_id
- name
- email

### Relationships

```
Brand

↓

User

↓

Sales

↓

Withdrawals
```

---

## Sale

### Responsibility

Represents a completed sale made by a user.

### Key Attributes

- id
- user_id
- earning
- status

### Relationships

```
User

↓

Sale

↓

Payouts
```

---

## Payout

### Responsibility

Represents money credited against a sale.

### Key Attributes

- sale_id
- user_id
- amount
- type
- status

### Types

- ADVANCE
- FINAL
- ADJUSTMENT

---

## Withdrawal

### Responsibility

Represents money withdrawn by a user.

### Key Attributes

- user_id
- amount
- status

---

## PaymentTransaction

### Responsibility

Represents the financial transaction corresponding to a withdrawal.

### Key Attributes

- withdrawal_id
- transaction_id
- status

---

# 4. Repository Classes

Repositories are responsible for interacting with the database.

They contain **only persistence logic** and no business rules.

---

## SaleRepository

### Responsibilities

- Retrieve sales
- Fetch pending sales
- Update sale status

### Used By

- AdvancePayoutService
- ReconciliationService

---

## PayoutRepository

### Responsibilities

- Create payouts
- Retrieve payouts
- Check duplicate advance payouts
- Calculate payout totals

### Used By

- AdvancePayoutService
- ReconciliationService
- WithdrawalService

---

## WithdrawalRepository

### Responsibilities

- Create withdrawals
- Retrieve withdrawals
- Calculate withdrawn amount

### Used By

- WithdrawalService

---

## PaymentTransactionRepository

### Responsibilities

- Create payment transactions
- Store payment status

### Used By

- WithdrawalService

---

# 5. Service Classes

Services implement the application's business rules.

Unlike repositories, services coordinate multiple repositories to complete a business operation.

---

## AdvancePayoutService

### Responsibility

Processes advance payouts for pending sales.

### Business Rules

- Advance payout equals 10% of sale earnings.
- Only one advance payout is allowed per sale.
- Processing is idempotent.
- Duplicate payouts are skipped.

### Collaborating Classes

```
AdvancePayoutService

↓

SaleRepository

↓

PayoutRepository
```

---

## ReconciliationService

### Responsibility

Processes sale reconciliation.

### Business Rules

- Sale can only be reconciled once.
- Approved sales receive final payouts.
- Rejected sales may generate adjustment payouts.

### Collaborating Classes

```
ReconciliationService

↓

SaleRepository

↓

PayoutRepository
```

---

## WithdrawalService

### Responsibility

Processes user withdrawal requests.

### Business Rules

- Calculate available balance.
- Validate withdrawal amount.
- Prevent overdrawing.
- Create payment transaction.

### Collaborating Classes

```
WithdrawalService

↓

PayoutRepository

↓

WithdrawalRepository

↓

PaymentTransactionRepository
```

---

# 6. Schema Classes

Pydantic schema classes define request and response models.

These classes provide validation before requests reach the Service Layer.

Examples include:

- AdvancePayoutResponse
- ReconciliationRequest
- WithdrawalRequest
- WithdrawalResponse
- BalanceResponse

### Responsibilities

- Input validation
- Response serialization
- Type safety
- Automatic API documentation

---

# 7. Exception Classes

Custom exception classes represent business rule violations.

Examples include:

- AppException
- ValidationException
- ResourceNotFoundException
- InsufficientBalanceException
- SaleAlreadyReconciledException

### Responsibilities

- Standardize error handling
- Improve readability
- Map business failures to HTTP responses

---

# 8. Class Relationships

```
FastAPI Routes

↓

Service Classes

↓

Repository Classes

↓

SQLAlchemy Models

↓

Database
```

Dependencies:

```
AdvancePayoutService

├── SaleRepository

└── PayoutRepository
```

```
ReconciliationService

├── SaleRepository

└── PayoutRepository
```

```
WithdrawalService

├── WithdrawalRepository

├── PaymentTransactionRepository

└── PayoutRepository
```

---

# 9. Design Principles

The class design follows several object-oriented design principles.

## Single Responsibility Principle (SRP)

Each class has one clearly defined responsibility.

Examples

- Repository → Database access
- Service → Business logic
- Schema → Validation
- Model → Persistence

---

## Separation of Concerns

Different layers perform different tasks.

This reduces coupling between components.

---

## Reusability

Repositories and services can be reused by multiple API endpoints.

---

## Maintainability

Changes to business rules are isolated to service classes.

Database changes remain confined to repositories and models.

---

## Extensibility

New services, repositories, or models can be added without affecting existing functionality.

---

# 10. Summary

The class design follows a clean layered architecture with well-defined responsibilities for each component.

Business logic is encapsulated within service classes, persistence logic is isolated in repositories, and validation is handled through Pydantic schemas.

This design results in a modular, maintainable, and scalable backend system that aligns with object-oriented programming principles and industry best practices.