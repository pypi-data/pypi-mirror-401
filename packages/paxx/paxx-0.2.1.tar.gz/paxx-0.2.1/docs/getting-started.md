# Getting Started

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager (recommended) or pip
- Docker and Docker Compose

## Installation

```bash
pip install paxx
```

Or with uv:

```bash
uv tool install paxx
```

## Create Your First Project

```bash
paxx bootstrap myproject
```

This creates a new directory `myproject/` with the complete project structure.

### Bootstrap Options

```bash
# With a description
paxx bootstrap myproject --description "My awesome API"

# With author name
paxx bootstrap myproject --author "Your Name"

# In a specific directory
paxx bootstrap myproject --output-dir /path/to/projects

# Bootstrap in current directory
paxx bootstrap .

# Skip confirmation prompts (CI-friendly)
paxx bootstrap myproject --force
```

## Start the Development Environment

### Option 1: Full Docker Setup (Recommended)

The easiest way to get started is with Docker Compose:

```bash
cd myproject
docker compose up
```

This starts both the application and PostgreSQL database. The app runs with hot-reload enabled.

### Option 2: Local Development with Dockerized Database

If you prefer running the app locally:

```bash
cd myproject

# Start only the database
docker compose up db -d

# Install dependencies
uv sync --all-extras

# Start the dev server
uv run paxx start
```

Your API is now running at [http://127.0.0.1:8000](http://127.0.0.1:8000).

- **API Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI)
- **Alternative docs**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) (ReDoc)
- **Health check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

## Create Your First Feature

Features are domain modules that contain your business logic. Create one with:

```bash
uv run paxx feature create users
```

This generates:

```
features/users/
├── __init__.py
├── config.py      # Router prefix and tags
├── models.py      # SQLAlchemy models
├── schemas.py     # Pydantic schemas
├── services.py    # Business logic
└── routes.py      # API endpoints
```

## Set Up the Database

After defining your models, create and apply migrations:

```bash
# Create a migration
uv run paxx db migrate "add users table"

# Apply the migration
uv run paxx db upgrade
```

## Add Infrastructure (Optional)

Add common infrastructure components as needed:

```bash
# Redis caching
uv run paxx infra add redis

# Background tasks
uv run paxx infra add arq

# Object storage (S3/local)
uv run paxx infra add storage

# List all available components
uv run paxx infra list
```

## Project Structure Overview

```
myproject/
├── main.py              # Application entry point
├── settings.py          # Configuration
├── docker-compose.yml   # Development environment
├── core/                # Shared utilities
├── db/                  # Database setup & migrations
├── features/            # Domain features
└── e2e/                 # End-to-end tests
```

See [Project Structure](project-structure.md) for detailed documentation.

## Next Steps

- Read the [CLI Reference](cli-reference.md) for all available commands
- Understand the [Project Structure](project-structure.md)
- Learn about [Infrastructure](infrastructure.md) components
- Follow the [Tutorial](tutorial.md) to build a complete feature
- Set up [Deployment](deployment.md) for production
