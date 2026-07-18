# Faym User Payout Management System

A backend service built using **FastAPI**, **SQLAlchemy**, and **SQLite** to manage user payouts, sale reconciliation, and withdrawals. The application follows a clean **Repository-Service Architecture**, ensuring maintainability, scalability, and separation of concerns.

> **GitHub Repository:**  
> https://github.com/vishhwaaa28/faym-user-payout-system

## 📚 Documentation

Detailed project documentation is available in the `docs/` directory.

| Document | Description |
|----------|-------------|
| [01_LLD.md](docs/01_LLD.md) | Low-Level Design |
| [02_DATABASE_SCHEMA.md](docs/02_DATABASE_SCHEMA.md) | Database Schema & Relationships |
| [03_DESIGN_DECISIONS.md](docs/03_DESIGN_DECISIONS.md) | Design Decisions & Trade-offs |
| [04_EDGE_CASES.md](docs/04_EDGE_CASES.md) | Edge Cases & Failure Scenarios |
| [05_API_DESIGN.md](docs/05_API_DESIGN.md) | REST API Documentation |
| [06_CLASS_DESIGN.md](docs/06_CLASS_DESIGN.md) | Class Design |
| [07_ARCHITECTURE_DECISIONS.md](docs/07_ARCHITECTURE_DECISIONS.md) | Architecture Decision Records |

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Business Rules](#business-rules)
- [Error Handling](#error-handling)
- [Example Requests](#example-requests)
- [Testing](#testing)
- [Design Principles](#design-principles)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

# Project Overview

The **Faym User Payout Management System** is a backend application that simulates a payout workflow for users earning through sales.

The system provides APIs for:

- Advance payout generation
- Sale reconciliation
- User balance management
- Withdrawal processing
- Payment transaction tracking

The application is built using modern backend development practices with a clean layered architecture.

---

# Features

- Advance payout generation (10% of sale amount)
- Sale approval and rejection workflow
- Automatic final payout generation
- Automatic payout adjustment on rejected sales
- User balance calculation
- Withdrawal processing with balance validation
- Payment transaction recording
- RESTful APIs
- Centralized exception handling
- Request validation using Pydantic
- Interactive Swagger API documentation

---

# Architecture

The application follows a layered architecture using the **Repository-Service Pattern**.

```
                Client
                   │
                   ▼
            FastAPI Routes
                   │
                   ▼
             Service Layer
                   │
                   ▼
          Repository Layer
                   │
                   ▼
          SQLAlchemy Models
                   │
                   ▼
             SQLite Database
```

## Repository Layer

Responsible for all database operations.

- Sale Repository
- Payout Repository
- Withdrawal Repository
- Payment Transaction Repository

## Service Layer

Contains all business logic.

- Advance Payout Service
- Reconciliation Service
- Withdrawal Service

## API Layer

Responsible for:

- Request validation
- Dependency Injection
- HTTP responses
- Exception propagation

---

# Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.13 | Programming Language |
| FastAPI | Backend Framework |
| SQLAlchemy 2.x | ORM |
| SQLite | Database |
| Pydantic v2 | Validation |
| Uvicorn | ASGI Server |
| Python Dotenv | Configuration Management |

---

# Project Structure

```
.
├── app
│   ├── api
│   ├── core
│   ├── models
│   ├── repositories
│   ├── schemas
│   ├── services
│   ├── enums.py
│   └── main.py
│
├── scripts
├── requirements.txt
├── README.md
└── app.db
```

---

# Installation & Setup

## 1. Clone the repository

```bash
git clone https://github.com/vishhwaaa28/faym-user-payout-system.git

cd faym-user-payout-system
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=sqlite:///./app.db
```

---

# Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The server will start at

```
http://127.0.0.1:8000
```

---

# API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# API Endpoints

## Health Check

| Method | Endpoint |
|---------|----------|
| GET | `/health` |

Checks whether the application is running.

---

## Advance Payout

| Method | Endpoint |
|---------|----------|
| POST | `/payouts/advance` |

Creates a 10% advance payout for a sale.

---

## Sale Reconciliation

| Method | Endpoint |
|---------|----------|
| POST | `/sales/{sale_id}/reconcile` |

Approves or rejects a sale and processes the remaining payout.

---

## User Balance

| Method | Endpoint |
|---------|----------|
| GET | `/users/{user_id}/balance` |

Returns the user's available withdrawal balance.

---

## Withdraw Funds

| Method | Endpoint |
|---------|----------|
| POST | `/users/{user_id}/withdraw` |

Creates a withdrawal after validating the user's available balance.

---

# Business Rules

## 1. Advance Payout

Every eligible sale receives an advance payout equal to **10% of the sale amount**.

Example

Sale Amount

```
1000
```

Advance Payout

```
100
```

---

## 2. Sale Approval

When a sale is approved:

- Sale status becomes **APPROVED**
- Remaining **90% payout** is generated

Example

Sale Amount

```
1000
```

Advance Payout

```
100
```

Final Payout

```
900
```

---

## 3. Sale Rejection

When a sale is rejected:

- Sale status becomes **REJECTED**
- Adjustment payout is generated (if applicable)

---

## 4. Withdrawals

A withdrawal is allowed only when:

- Requested amount > 0
- User has sufficient available balance

Otherwise an appropriate error response is returned.

---

## 5. Payment Transactions

Every successful withdrawal automatically creates a payment transaction record.

---

# Error Handling

The project uses centralized exception handling.

Custom exceptions include:

- ValidationException
- ResourceNotFoundException
- InsufficientBalanceException
- SaleAlreadyReconciledException

The API returns meaningful HTTP status codes and error messages.

---

# Example Requests

## Create Advance Payout

```http
POST /payouts/advance
```

```json
{
    "sale_id": 1
}
```

---

## Reconcile Sale

```http
POST /sales/1/reconcile
```

```json
{
    "approved": true
}
```

---

## Withdraw Money

```http
POST /users/1/withdraw
```

```json
{
    "amount": 100
}
```

---

## Get User Balance

```http
GET /users/1/balance
```

---

# Testing

The project has been tested using:

- Swagger UI
- SQLite Database Verification
- Business Logic Test Scripts

Scenarios tested include:

- Advance payout creation
- Sale approval
- Sale rejection
- Balance calculation
- Successful withdrawals
- Insufficient balance validation
- Sale not found
- Already reconciled sale
- Database consistency

---

# Design Principles

The project follows modern backend development practices:

- Repository Pattern
- Service Layer Pattern
- Dependency Injection
- Layered Architecture
- Separation of Concerns
- Single Responsibility Principle
- RESTful API Design

---

# Future Improvements

- JWT Authentication
- Role-Based Authorization
- PostgreSQL Support
- Docker Containerization
- Unit Testing with Pytest
- CI/CD Pipeline
- Logging & Monitoring
- Async SQLAlchemy
- Background Task Processing

---

# Repository

GitHub Repository:

**https://github.com/vishhwaaa28/faym-user-payout-system**

---

# Author

## Vishwanath Mishra

GitHub: https://github.com/vishhwaaa28

---

## License

This project was developed as part of a backend engineering assignment for educational and evaluation purposes.