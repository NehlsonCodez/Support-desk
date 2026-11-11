# Support Desk API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A role-based Support Desk and Ticketing REST API built with **FastAPI**, **SQLAlchemy (async)** and **PostgreSQL**. Customers raise support tickets, agents work on them, and admins manage users, priorities, and ticket assignments — with JWT authentication and per-role data isolation throughout.

## Features

- **JWT authentication** — register, login (form or JSON), token-protected endpoints
- **Three user roles** — `admin`, `agent`, `customer` — with role-based access control on every route
- **Ticket lifecycle** — create, update, change status/priority, assign to agents, delete
- **Ticket replies** — threaded responses with ownership rules (edit/delete your own)
- **Activity log** — every ticket change (status, priority, assignment) is recorded with old/new values
- **Customer data isolation** — customers can only see and act on their own tickets, replies, and activity
- **Auto-generated interactive docs** — Swagger UI and ReDoc out of the box

## Tech Stack

| Tool | Purpose |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework |
| [SQLAlchemy 2.0](https://docs.sqlalchemy.org/) (async) + [asyncpg](https://github.com/MagicStack/asyncpg) | ORM and PostgreSQL driver |
| [Alembic](https://alembic.sqlalchemy.org/) | Database migrations |
| [python-jose](https://github.com/mpdavis/python-jose) + [passlib/bcrypt](https://passlib.readthedocs.io/) | JWT tokens and password hashing |
| [Pydantic v2](https://docs.pydantic.dev/) + pydantic-settings | Validation and configuration |
| [Docker Compose](https://docs.docker.com/compose/) | Local PostgreSQL database |

## Project Structure

```
backend/app/
├── main.py              # FastAPI app, router registration, CORS, health check
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Local PostgreSQL container
├── .env.example         # Template for environment variables
├── alembic/             # Database migrations
├── core/                # Settings (configs.py) and JWT/password security
├── database/            # Engine and session setup
├── models/              # SQLAlchemy models (users, tickets, replies, activities)
├── schemas/             # Pydantic request/response schemas and enums
├── crud/                # Direct database access functions
├── services/            # Business logic layer
├── routers/             # API route handlers
├── dependencies/        # Auth, DB session, and role guards
└── scripts/             # Utilities (promote_admin.py)
```

## Getting Started

### Prerequisites

- Python 3.10+
- Docker (for the database)

### 1. Clone and set up the environment

```bash
git clone https://github.com/NehlsonCodez/Support-desk.git
cd Support-desk

python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/app/requirements.txt
```

### 2. Start the database

```bash
docker compose -f backend/app/docker-compose.yml up -d
```

This starts PostgreSQL on host port **5438** (user `postgres`, password `postgres`, database `support_desk`).

### 3. Configure environment variables

```bash
cp backend/app/.env.example backend/app/.env
```

Then edit `backend/app/.env` and set a strong `SECRET_KEY`. All variables:

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Secret used to sign JWT tokens | any long random string |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `DATABASE_URL` | Async SQLAlchemy connection string | `postgresql+asyncpg://postgres:postgres@localhost:5438/support_desk` |
| `ACCESS_TOKEN_EXPIRE_MIN` | Access token lifetime in minutes | `60` |
| `BACKEND_URL` | Base URL of the API | `http://localhost:8000` |

### 4. Run migrations

```bash
cd backend/app
alembic upgrade head
```

### 5. Start the API

```bash
uvicorn main:app --reload
```

The API is now running at `http://127.0.0.1:8000`, with interactive docs at:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

### 6. Create your first admin

New registrations are customers by default. To promote a user to admin (run from `backend/app` with the venv active):

```bash
python scripts/promote_admin.py you@example.com
```

## Roles and Permissions

| Ability | Customer | Agent | Admin |
|---|:---:|:---:|:---:|
| Register / login | ✅ | ✅ | ✅ |
| Create tickets | ✅ | ❌ | ❌ |
| View tickets | Own only | All | All |
| Edit ticket details | Own (if not resolved/closed) | ❌ | All |
| Change ticket status | ❌ | ✅ | ✅ |
| Change ticket priority | ❌ | ❌ | ✅ |
| Assign tickets to agents | ❌ | ❌ | ✅ |
| Delete tickets | Own, only while `open` | ❌ | All |
| Reply to tickets | Own tickets | ✅ | ✅ |
| Edit/delete replies | Own only | Own only | All |
| View activity log | Own tickets | ✅ | ✅ |
| List / manage users | ❌ | Filter by role | ✅ |

Ticket statuses flow `open → in_progress → resolved → closed`; priorities are `low`, `medium`, `high`, `urgent`.

## API Endpoints

All endpoints except auth require an `Authorization: Bearer <token>` header.

### Auth

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/auth/register` | Public | Create an account (customer role) |
| POST | `/auth/login` | Public | Login (OAuth2 form: `username` = email) |
| POST | `/auth/login-json` | Public | Login with JSON body |

### Users

| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/users/me` | Authenticated | View own profile |
| PATCH | `/users/me` | Authenticated | Update own profile |
| POST | `/users/change-password` | Authenticated | Change own password |
| GET | `/users` | Admin | List all users |
| GET | `/users/role/{role}` | Admin, Agent | List users by role |
| GET | `/users/{user_id}` | Admin, or self | View a user |
| PATCH | `/users/{user_id}/role` | Admin | Change a user's role |

### Tickets

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/ticket/create-ticket` | Customer | Create a ticket |
| GET | `/ticket/get-tickets` | Authenticated | List tickets (customers see own) |
| GET | `/ticket/get-ticket/{ticket_id}` | Authenticated | Get one ticket |
| GET | `/ticket/get-customer-tickets/{customer_id}` | Admin, Agent, or self | List a customer's tickets |
| GET | `/ticket/get-assigned-tickets/{agent_id}` | Admin, or own agent ID | List tickets assigned to an agent |
| PATCH | `/ticket/update-ticket/{ticket_id}` | Customer (own, open), Admin | Update ticket details |
| PATCH | `/ticket/update-ticket-status/{ticket_id}` | Admin, Agent | Change ticket status |
| PATCH | `/ticket/update-ticket-priority/{ticket_id}` | Admin | Change ticket priority |
| PATCH | `/ticket/assign-ticket/{ticket_id}` | Admin | Assign a ticket to an agent |
| DELETE | `/ticket/delete-ticket/{ticket_id}` | Admin, or Customer (own, open) | Delete a ticket |

### Ticket Replies

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/ticket-reply/create-ticket-reply/{ticket_id}` | Customer (own), Agent, Admin | Reply to a ticket |
| GET | `/ticket-reply/get-ticket-replies/{ticket_id}` | Authenticated | List replies (customers: own tickets) |
| GET | `/ticket-reply/get-ticket-reply/{reply_id}` | Authenticated | Get one reply |
| PATCH | `/ticket-reply/update-ticket-reply/{reply_id}` | Author, Admin | Edit a reply |
| DELETE | `/ticket-reply/delete-ticket-reply/{reply_id}` | Author, Admin | Delete a reply |

### Ticket Activities

| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/ticket-activity/ticket/{ticket_id}` | Authenticated | Activity log for a ticket |
| GET | `/ticket-activity/{activity_id}` | Authenticated | Single activity entry |

### Health

| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/` | Public | Service health check |

## Quick Example

```bash
# 1. Register a customer
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Jane Doe", "email": "jane@example.com", "password": "supersecret123"}'

# 2. Login (returns {"access_token": "...", "token_type": "bearer"})
curl -X POST http://127.0.0.1:8000/auth/login-json \
  -H "Content-Type: application/json" \
  -d '{"email": "jane@example.com", "password": "supersecret123"}'

# 3. Create a ticket
curl -X POST http://127.0.0.1:8000/ticket/create-ticket \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Cannot log in", "description": "I get an error on the login page"}'

# 4. View your tickets
curl http://127.0.0.1:8000/ticket/get-tickets -H "Authorization: Bearer <token>"
```

## License

This project is open source and licensed under the [MIT License](LICENSE) — you're free to use, modify, and distribute it, including commercially, as long as you include the original copyright notice.

