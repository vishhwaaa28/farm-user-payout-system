# Edge Cases & Failure Scenarios

# Faym User Payout Management System

**Author:** Vishwanath Mishra

---

# 1. Introduction

A robust backend system must handle not only successful requests but also invalid inputs, unexpected situations, and business rule violations.

The Faym User Payout Management System has been designed to validate incoming requests, enforce business constraints, and maintain database consistency throughout the payout lifecycle.

This document describes the major edge cases, failure scenarios, and the strategies used to handle them.

---

# 2. Error Handling Strategy

The project follows a centralized exception handling approach.

Business-specific exceptions are raised from the Service Layer and are converted into consistent HTTP responses by global exception handlers.

```
Client Request
      │
      ▼
API Route
      │
      ▼
Service Layer
      │
      ▼
Business Validation
      │
      ▼
Custom Exception
      │
      ▼
Global Exception Handler
      │
      ▼
HTTP Response
```

### Benefits

- Consistent API responses
- Cleaner business logic
- Separation of concerns
- Easier debugging and maintenance

---

# 3. Input Validation

Input validation is performed using **Pydantic** before business logic is executed.

Example:

```python
amount: Decimal = Field(gt=0)
```

If a client submits

```json
{
    "amount": -100
}
```

FastAPI automatically returns

```
HTTP 422 Unprocessable Entity
```

without invoking the service layer.

This prevents invalid data from reaching the application logic.

---

# 4. Edge Cases

---

## 4.1 Negative Withdrawal Amount

### Scenario

A user attempts to withdraw a negative amount.

```json
{
    "amount": -100
}
```

### Expected Behaviour

The request is rejected during request validation.

### Response

```
HTTP 422 Unprocessable Entity
```

### Reason

Withdrawal amounts must always be greater than zero.

---

## 4.2 Zero Withdrawal Amount

### Scenario

```json
{
    "amount": 0
}
```

### Expected Behaviour

The request is rejected.

### Response

```
HTTP 422 Unprocessable Entity
```

### Reason

Zero-value financial transactions are not allowed.

---

## 4.3 Insufficient Balance

### Scenario

User Balance

```
₹400
```

Requested Withdrawal

```
₹700
```

### Expected Behaviour

The withdrawal request is rejected.

### Response

```
HTTP 400 Bad Request
```

### Exception

```
InsufficientBalanceException
```

### Reason

Users cannot withdraw more than their available balance.

Available Balance is calculated as:

```
Total Successful Payouts
-
Total Successful Withdrawals
```

---

## 4.4 Sale Not Found

### Scenario

```
POST /sales/999/reconcile
```

where Sale 999 does not exist.

### Expected Behaviour

The request is rejected.

### Response

```
HTTP 404 Not Found
```

### Exception

```
ResourceNotFoundException
```

---

## 4.5 User Not Found

### Scenario

```
GET /users/999/balance
```

### Expected Behaviour

The request is rejected.

### Response

```
HTTP 404 Not Found
```

### Reason

Balance cannot be calculated for a non-existent user.

---

## 4.6 Duplicate Sale Reconciliation

### Scenario

A sale that has already been reconciled is reconciled again.

### Expected Behaviour

The request is rejected.

### Response

```
HTTP 400 Bad Request
```

### Exception

```
SaleAlreadyReconciledException
```

### Reason

Each sale can only be reconciled once to prevent duplicate final payouts.

---

## 4.7 Duplicate Advance Payout

### Scenario

An advance payout process is triggered more than once for the same sale.

### Expected Behaviour

The system first checks whether an advance payout already exists.

If an advance payout has already been created, no additional payout is generated.

The service simply skips processing that sale.

### Current Implementation

```text
Advance Exists?

        Yes
         │
         ▼
Return None

No New Payout Created
```

### Reason

The service is intentionally **idempotent**.

Repeated execution of the advance payout process produces the same result without creating duplicate payments.

This prevents accidental double payouts while allowing the payout process to be safely retried.

---

## 4.8 Invalid Route Parameters

### Scenario

```
GET /users/abc/balance
```

### Expected Behaviour

FastAPI automatically rejects the request.

### Response

```
HTTP 422 Unprocessable Entity
```

### Reason

Route parameter validation fails before reaching the application logic.

---

## 4.9 Missing Request Body

### Scenario

A client sends

```
POST /users/1/withdraw
```

without a JSON body.

### Expected Behaviour

FastAPI rejects the request.

### Response

```
HTTP 422 Unprocessable Entity
```

---

## 4.10 Invalid Enum Values

### Scenario

A client provides an invalid enum value for sale or payout status.

Example

```json
{
    "status": "completed"
}
```

### Expected Behaviour

The request is rejected during validation.

### Response

```
HTTP 422 Unprocessable Entity
```

### Reason

Only predefined enum values are accepted by the application.

---

# 5. Failure Scenarios

---

## Database Connection Failure

### Scenario

The database becomes unavailable.

### Expected Behaviour

Database operations fail gracefully.

The request returns an internal server error.

No partial updates remain in the database.

---

## Transaction Failure

### Scenario

A payout or withdrawal operation fails while updating the database.

### Expected Behaviour

The database transaction is rolled back.

The application avoids partial or inconsistent data.

---

## Unexpected Exceptions

Unexpected runtime errors are handled by the global exception handler.

### Benefits

- Prevents internal stack traces from being exposed.
- Returns consistent API responses.
- Simplifies debugging.
- Improves application stability.

---

# 6. Data Consistency Rules

The following business rules are enforced to maintain financial consistency.

---

## Rule 1

Total Withdrawals

≤

Total Successful Payouts

---

## Rule 2

Every Withdrawal

↓

One Payment Transaction

---

## Rule 3

Every Sale

↓

At Most One Advance Payout

---

## Rule 4

Every Approved Sale

↓

One Final Payout

---

## Rule 5

A Sale Can Be Reconciled Only Once

---

# 7. HTTP Status Codes

| Status Code | Description | Example |
|-------------|-------------|----------|
| **200 OK** | Successful request | Balance fetched |
| **201 Created** | Resource created | Withdrawal created |
| **400 Bad Request** | Business rule violation | Insufficient balance |
| **404 Not Found** | Resource does not exist | Sale/User missing |
| **422 Unprocessable Entity** | Request validation failed | Invalid request body |
| **500 Internal Server Error** | Unexpected server failure | Database failure |

---

# 8. Concurrency Considerations

The current implementation uses SQLite, which is suitable for development and low-concurrency environments.

Potential issues in production include:

- Simultaneous withdrawal requests
- Concurrent payout processing
- Race conditions during balance calculation

Possible future improvements include:

- Database transactions
- Row-level locking
- Optimistic locking
- PostgreSQL migration
- Distributed locking for payment workflows

---

# 9. Security Considerations

Authentication and authorization are intentionally outside the scope of this assignment.

For production deployment, the following enhancements are recommended:

- JWT Authentication
- Role-Based Access Control (RBAC)
- HTTPS
- Rate Limiting
- Secure Secret Management
- Audit Logging
- API Request Logging
- Input Sanitization

---

# 10. Assumptions

The application assumes:

- Every sale belongs to exactly one user.
- Every user belongs to one brand.
- Advance payout is fixed at **10%** of the sale earning.
- Every sale can receive **only one advance payout**.
- A sale can only be reconciled once.
- Monetary values are represented using `Decimal`.
- Every successful withdrawal generates one payment transaction.
- SQLite is used for local development.

---

# 11. Testing Summary

The following scenarios have been verified during development.

| Scenario | Result |
|----------|--------|
| Advance payout creation | ✅ Passed |
| Duplicate advance payout prevention | ✅ Passed |
| Sale approval | ✅ Passed |
| Sale rejection | ✅ Passed |
| Balance calculation | ✅ Passed |
| Successful withdrawal | ✅ Passed |
| Negative withdrawal validation | ✅ Passed |
| Zero withdrawal validation | ✅ Passed |
| Insufficient balance | ✅ Passed |
| Sale not found | ✅ Passed |
| Duplicate reconciliation | ✅ Passed |
| Database consistency | ✅ Passed |

---

# 12. Conclusion

The Faym User Payout Management System has been designed to gracefully handle both expected and unexpected scenarios while maintaining financial consistency and database integrity.

The application validates requests at multiple layers:

- Request validation using Pydantic
- Business rule validation within the Service Layer
- Centralized exception handling for consistent API responses

Additionally, the advance payout process is implemented as an **idempotent operation**, ensuring that repeated executions cannot generate duplicate payouts.

This layered design results in a backend application that is reliable, maintainable, and scalable while providing a solid foundation for future enhancements such as authentication, payment gateway integration, and migration to production-grade databases.