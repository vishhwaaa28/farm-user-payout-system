# API Design Documentation

# Faym User Payout Management System

**Author:** Vishwanath Mishra

---

# 1. Introduction

The Faym User Payout Management System exposes a set of RESTful APIs for managing the complete payout lifecycle.

The APIs are designed following REST principles and provide functionality for:

- Processing advance payouts
- Reconciling sales
- Calculating user balances
- Processing withdrawals
- Monitoring service health

All APIs exchange data using JSON.

---

# 2. API Design Principles

The API follows the following design principles.

## RESTful Endpoints

Resources are represented using nouns rather than verbs.

Examples

```
/users/{user_id}/balance

/users/{user_id}/withdraw

/sales/{sale_id}/reconcile
```

---

## JSON Communication

All requests and responses use JSON.

Example

```json
{
    "amount": 500.00
}
```

---

## Appropriate HTTP Status Codes

The API returns meaningful HTTP status codes.

Examples

| Status | Meaning |
|---------|----------|
| 200 | Successful request |
| 201 | Resource created |
| 400 | Business rule violation |
| 404 | Resource not found |
| 422 | Validation error |
| 500 | Internal server error |

---

## Input Validation

Request validation is handled using Pydantic models.

Invalid requests never reach the business logic.

---

## Consistent Error Responses

Business exceptions are handled centrally to ensure consistent API responses.

---

# 3. API Overview

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | `/health` | Service health check |
| POST | `/payouts/advance` | Process advance payouts |
| POST | `/sales/{sale_id}/reconcile` | Reconcile a sale |
| GET | `/users/{user_id}/balance` | Fetch available balance |
| POST | `/users/{user_id}/withdraw` | Create a withdrawal |

---

# 4. Health Check API

## Endpoint

```
GET /health
```

## Purpose

Checks whether the application is running.

---

### Success Response

```json
{
    "status": "healthy"
}
```

---

### Response Code

```
200 OK
```

---

# 5. Advance Payout API

## Endpoint

```
POST /payouts/advance
```

---

## Purpose

Processes advance payouts for all pending sales.

Each eligible sale receives an advance payout equal to **10%** of its earning.

The operation is **idempotent**, meaning repeated execution does not create duplicate advance payouts.

---

## Request

No request body is required.

---

## Success Response

```json
{
    "processed": 5,
    "skipped": 2
}
```

---

### Response Fields

| Field | Description |
|---------|-------------|
| processed | Number of advance payouts created |
| skipped | Number of sales skipped because an advance payout already existed |

---

### Response Code

```
200 OK
```

---

# 6. Sale Reconciliation API

## Endpoint

```
POST /sales/{sale_id}/reconcile
```

---

## Purpose

Reconciles a sale after verification.

Depending on the outcome, the service creates either:

- Final Payout
- Adjustment Payout

---

## Request

Example

```json
{
    "status": "APPROVED"
}
```

---

## Success Response

```json
{
    "message": "Sale reconciled successfully."
}
```

---

### Error Responses

| Status | Reason |
|----------|--------|
| 400 | Sale already reconciled |
| 404 | Sale not found |
| 422 | Invalid request |

---

# 7. User Balance API

## Endpoint

```
GET /users/{user_id}/balance
```

---

## Purpose

Returns the user's available balance.

Available Balance is calculated as

```
Successful Payouts

−

Successful Withdrawals
```

---

## Success Response

```json
{
    "user_id": 1,
    "balance": 400.00
}
```

---

### Response Code

```
200 OK
```

---

### Error Responses

| Status | Reason |
|----------|--------|
| 404 | User not found |

---

# 8. Withdrawal API

## Endpoint

```
POST /users/{user_id}/withdraw
```

---

## Purpose

Creates a withdrawal request for a user.

If sufficient balance exists, a withdrawal and corresponding payment transaction are created.

---

## Request

```json
{
    "amount": 200.00
}
```

---

## Success Response

```json
{
    "withdrawal_id": 12,
    "status": "SUCCESS",
    "amount": 200.00
}
```

---

### Error Responses

| Status | Reason |
|----------|--------|
| 400 | Insufficient balance |
| 404 | User not found |
| 422 | Invalid amount |

---

# 9. Validation Rules

The API validates all incoming requests before business logic is executed.

Examples include:

- Withdrawal amount must be greater than zero.
- Route parameters must be integers.
- Enum values must be valid.
- Required request bodies must be present.

Invalid requests return

```
HTTP 422 Unprocessable Entity
```

---

# 10. Error Response Format

Business exceptions return a consistent JSON structure.

Example

```json
{
    "detail": "Insufficient balance."
}
```

Validation errors are returned by FastAPI.

Example

```json
{
    "detail": [
        {
            "loc": [
                "body",
                "amount"
            ],
            "msg": "Input should be greater than 0",
            "type": "greater_than"
        }
    ]
}
```

---

# 11. API Workflow

## Advance Payout Workflow

```
Pending Sale

↓

Advance Payout Request

↓

Advance Already Exists?

      │

 ┌────┴────┐

 │         │

Yes        No

 │          │

Skip     Create Advance

 │          │

 └────┬─────┘

      ▼

Return Summary
```

---

## Withdrawal Workflow

```
Withdrawal Request

↓

Validate Request

↓

Calculate Balance

↓

Enough Balance?

│

├── No

│      ↓

│   HTTP 400

│

└── Yes

       ↓

Create Withdrawal

↓

Create Payment Transaction

↓

Return Success
```

---

# 12. Idempotency

The advance payout endpoint is intentionally idempotent.

Repeated execution produces the same result.

Example

```
First Request

↓

Advance Created

Second Request

↓

Skipped

Third Request

↓

Skipped
```

This prevents duplicate payouts while allowing the operation to be safely retried.

---

# 13. Security Considerations

The current implementation focuses on backend business logic.

For production deployment, the API should include:

- JWT Authentication
- Authorization
- HTTPS
- Rate Limiting
- API Keys (if required)
- Request Logging
- Audit Trails

---

# 14. Future API Enhancements

Possible future endpoints include:

```
GET /users

GET /sales

GET /payouts

GET /withdrawals

GET /transactions

DELETE /withdrawals/{id}

PATCH /sales/{id}

POST /users
```

Additional enhancements:

- Pagination
- Filtering
- Sorting
- Search
- Bulk operations
- Versioning (`/api/v1`)
- OpenTelemetry tracing

---

# 15. Conclusion

The Faym User Payout Management System exposes a clean and consistent REST API that follows modern backend development practices.

The API emphasizes:

- Clear resource-oriented endpoints
- Automatic request validation
- Consistent error handling
- Idempotent financial operations
- Proper HTTP status codes
- Separation of business logic from transport logic

Combined with the project's layered architecture and comprehensive documentation, these APIs provide a solid foundation for a scalable and maintainable payout management system.