# Learning FastAPI

A small FastAPI project using SQLModel, PostgreSQL, and Alembic.

```text
app/
├── __init__.py
├── main.py       # FastAPI app and routes
├── db.py         # Database connection and session
├── models/
│   ├── song.py   # Song database table
│   └── user.py   # User database table
├── schemas/
│   ├── song.py   # Song request and response schemas
│   └── user.py   # User request and response schemas
├── routers/
│   ├── songs.py  # Song routes
│   └── users.py  # User routes
└── services/
    ├── songs.py  # Song business logic
    └── users.py  # User business logic
migrations/       # Database migration files
alembic.ini       # Alembic configuration
.env              # Local database URL (not committed)
```

## Run the project

Configure `.env` using `.env.sample`, then run:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to use the API.

The API provides `GET` and `POST` routes at `/songs` and `/users`.

Each feature has a model, schema, router, and service. Routers handle HTTP while
services contain database operations and business logic. The active features are
users and songs.

## Change the database

After changing a table in `app/models/`, run:

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

If Alembic says `Target database is not up to date`, run `alembic upgrade head` before creating another migration.
