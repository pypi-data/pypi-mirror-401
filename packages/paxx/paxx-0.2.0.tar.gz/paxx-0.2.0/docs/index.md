# paxx

**Python Async API** - a domain-oriented FastAPI project scaffolding CLI.

paxx generates production-ready code using well-known libraries (FastAPI, SQLAlchemy async, Pydantic v2, Alembic) directly. No wrapper abstractions, no framework lock-in - just a solid starting point for domain-driven FastAPI applications.

## Philosophy

- **No magic** - Generated code uses FastAPI, SQLAlchemy, and Pydantic directly
- **No lock-in** - After bootstrapping, your project has zero dependency on paxx
- **Domain-driven** - Features organized by business capability, not technical layer
- **Production-ready** - Includes Docker, migrations, logging, and deployment configs

## Quick Start

```bash
# Install paxx
pip install paxx

# Create a new project
paxx bootstrap myproject

# Navigate and start
cd myproject
docker compose up
```

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to see your API documentation.

### Alternative: Local Development

```bash
cd myproject
docker compose up db -d    # Start only the database
uv sync --all-extras       # Install dependencies
uv run paxx start          # Start dev server with hot reload
```

## What's Generated?

When you run `paxx bootstrap`, you get a fully configured FastAPI project with:

- **Application factory pattern** with async lifespan management
- **Pydantic Settings** for type-safe configuration
- **SQLAlchemy async** with session management and BaseModel
- **Alembic** migrations pre-configured
- **Docker Compose** for local development (app + PostgreSQL)
- **Structured logging** with JSON and console output formats
- **CORS middleware** pre-configured
- **Health check endpoint** out of the box
- **Domain-driven structure** with a `features/` directory for business logic

## Core Concepts

### Features

Features are self-contained domain modules under `features/`. Each feature contains models, schemas, services, and routes for a specific business capability.

```bash
# Create a new feature
paxx feature create users

# Add a bundled feature
paxx feature add example_products
```

### Infrastructure

Infrastructure components add cross-cutting capabilities like caching, background tasks, and object storage.

```bash
# Add Redis caching
paxx infra add redis

# Add background tasks
paxx infra add arq
```

### Deployment

Generate deployment configurations for different environments.

```bash
# Add Linux server deployment (Traefik + systemd)
paxx deploy add linux-server
```

## Documentation

- [Getting Started](getting-started.md) - Installation and your first project
- [Project Structure](project-structure.md) - Understanding the generated code
- [CLI Reference](cli-reference.md) - All available commands
- [Infrastructure](infrastructure.md) - Adding Redis, background tasks, storage, and more
- [Tutorial](tutorial.md) - Build a complete feature step by step
- [Deployment](deployment.md) - Deploy to production

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager (recommended) or pip
- Docker (for local development)
