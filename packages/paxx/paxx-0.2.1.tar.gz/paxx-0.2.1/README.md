# paxx

[![PyPI version](https://img.shields.io/pypi/v/paxx.svg)](https://pypi.org/project/paxx/)
[![Python](https://img.shields.io/pypi/pyversions/paxx.svg)](https://pypi.org/project/paxx/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Domain-oriented FastAPI scaffolding with zero lock-in.**

paxx generates production-ready Python code using FastAPI, SQLAlchemy async, Pydantic v2, and Alembic. No wrapper abstractions—just clean, readable code you own and can modify freely.

## Features

- **Zero lock-in** — Generated projects have no dependency on paxx after scaffolding
- **Domain-driven** — Features organized by business capability, not technical layer
- **Async-first** — Built on SQLAlchemy async and FastAPI's async capabilities
- **Production-ready** — Includes Docker, migrations, structured logging, and deployment configs
- **Batteries included** — Add Redis caching, background tasks, object storage, WebSockets, and more

## Installation

```bash
pip install paxx
# or with uv
uv add paxx
```

## Quick Start

```bash
# Create a new project
paxx bootstrap myproject
cd myproject

# Start Docker services (PostgreSQL)
paxx docker up -d

# Install dependencies and run migrations
uv sync --all-extras
paxx db upgrade

# Start the development server
paxx start
```

Visit http://127.0.0.1:8000/docs to see your API documentation.

## CLI Reference

### Project Scaffolding

#### `paxx bootstrap <name>`

Create a new project with the complete directory structure.

```bash
paxx bootstrap myproject
paxx bootstrap my-api --description "My awesome API" --author "Jane Doe"
paxx bootstrap . --force  # Bootstrap in current directory
```

#### `paxx start`

Start the development server (uvicorn).

```bash
paxx start                         # localhost:8000 with hot reload
paxx start --port 3000             # Custom port
paxx start --host 0.0.0.0          # Bind to all interfaces
paxx start --no-reload --workers 4 # Production-like mode
```

### Feature Management

Features are self-contained domain modules with models, schemas, services, and routes.

#### `paxx feature create <name>`

Create a new feature from the blank template.

```bash
paxx feature create users
paxx feature create orders --description "Order management"
```

Creates:
```
features/<name>/
├── config.py      # Router prefix and tags
├── models.py      # SQLAlchemy models
├── schemas.py     # Pydantic schemas
├── services.py    # Business logic
└── routes.py      # API endpoints
```

#### `paxx feature add <feature>`

Add a bundled feature with auto-registration in `main.py`.

```bash
paxx feature add health           # Health check endpoint
paxx feature add example_products # Complete CRUD example with tests
```

#### `paxx feature list`

List available bundled features.

### Infrastructure Components

Add production infrastructure with a single command.

#### `paxx infra add <component>`

```bash
paxx infra add redis      # Async Redis caching
paxx infra add arq        # Background task queue
paxx infra add storage    # S3/MinIO object storage
paxx infra add websocket  # WebSocket with room support
paxx infra add postgis    # PostGIS geospatial extensions
paxx infra add metrics    # Prometheus + OpenTelemetry tracing
```

Each component adds:
- Python modules in `core/`
- Docker services in `docker-compose.yml`
- Dependencies in `pyproject.toml`
- Environment variables in `settings.py` and `.env.example`

#### `paxx infra list`

List available infrastructure components with descriptions.

### Database Migrations

Alembic wrappers for database migrations.

```bash
paxx db migrate "add users table"  # Create migration (auto-detects changes)
paxx db upgrade                    # Apply all pending migrations
paxx db upgrade +1                 # Apply next migration only
paxx db downgrade                  # Revert last migration
paxx db downgrade -2               # Revert last 2 migrations
paxx db status                     # Show current revision
paxx db history                    # Show migration history
paxx db heads                      # Show branch heads
```

### Docker Commands

Docker Compose wrappers for local development.

```bash
paxx docker up              # Start containers
paxx docker up -d -b        # Detached mode, rebuild images
paxx docker down            # Stop containers
paxx docker down -v         # Stop and remove volumes
paxx docker logs -f         # Follow logs
paxx docker ps              # Container status
paxx docker exec app        # Shell into app container
paxx docker exec db psql    # Run psql in db container
```

### Deployment

#### `paxx deploy add <type>`

Add deployment configuration.

```bash
paxx deploy add linux-server  # Traefik + systemd + SSL + GitHub Actions
```

## Project Structure

Generated projects follow this structure:

```
myproject/
├── main.py                  # FastAPI app factory with lifespan
├── settings.py              # Pydantic Settings (env-aware)
├── alembic.ini              # Migration config
├── pyproject.toml           # Dependencies
├── docker-compose.yml       # Local dev environment
├── Dockerfile               # Production image
├── Dockerfile.dev           # Development image
├── .env / .env.example      # Environment variables
│
├── core/                    # Core utilities
│   ├── exceptions.py        # Custom exceptions + handlers
│   ├── middleware.py        # Request/response middleware
│   ├── logging.py           # JSON/console logging config
│   ├── dependencies.py      # FastAPI dependencies (pagination)
│   └── schemas.py           # Shared schemas (ListResponse)
│
├── db/                      # Database
│   ├── database.py          # Async SQLAlchemy, Base, get_db
│   └── migrations/          # Alembic migrations
│
├── features/                # Domain features
│   └── <name>/
│       ├── config.py        # Router prefix, tags
│       ├── models.py        # SQLAlchemy models
│       ├── schemas.py       # Pydantic schemas
│       ├── services.py      # Async business logic
│       └── routes.py        # FastAPI endpoints
│
├── e2e/                     # End-to-end tests
│   ├── conftest.py          # Test fixtures
│   └── test_*.py            # API tests
│
└── deploy/                  # Deployment configs (via paxx deploy)
```

## Philosophy

paxx is a **scaffolding tool**, not a framework:

- **No magic** — Generated code uses FastAPI, SQLAlchemy, and Pydantic directly
- **No lock-in** — After scaffolding, your project has zero dependency on paxx
- **Readable code** — Everything is plain Python you can understand and modify
- **Convention over configuration** — Sensible defaults, fully customizable
- **Domain-driven** — Features organized by business capability

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## License

MIT
