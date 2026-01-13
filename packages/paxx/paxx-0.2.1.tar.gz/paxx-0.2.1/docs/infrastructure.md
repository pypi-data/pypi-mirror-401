# Infrastructure

Infrastructure components add cross-cutting capabilities like caching, background tasks, object storage, and observability to your paxx project.

## Overview

```bash
# List available components
paxx infra list

# Add a component
paxx infra add <component>
```

When you add an infrastructure component, paxx:

1. Renders templates to `core/` (e.g., `core/cache.py`)
2. Merges Docker services into `docker-compose.yml`
3. Adds dependencies to `pyproject.toml`
4. Adds environment variables to `settings.py` and `.env.example`

---

## Redis

Async Redis client for caching and pub/sub.

```bash
paxx infra add redis
```

### Generated Files

- `core/cache.py` - Redis client and caching utilities

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection URL |

### Docker Service

Adds Redis 7 Alpine to `docker-compose.yml`.

### Usage

```python
from core.cache import cache_get, cache_set, cache_delete, get_redis

# Simple caching
await cache_set("user:123", {"name": "John"}, expire=3600)
user = await cache_get("user:123")
await cache_delete("user:123")

# Direct Redis access
redis = await get_redis()
await redis.incr("page_views")
```

### Dependency

- `redis>=5.0`

---

## ARQ (Background Tasks)

Background task queue using ARQ (async Redis queue).

```bash
paxx infra add arq
```

### Prerequisites

ARQ requires Redis. Run `paxx infra add redis` first or configure `ARQ_REDIS_URL` separately.

### Generated Files

- `core/arq.py` - ARQ client and task enqueueing
- `core/tasks.py` - Worker settings and task definitions

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ARQ_REDIS_URL` | `redis://localhost:6379/1` | Redis URL for task queue |
| `ARQ_MAX_JOBS` | `10` | Maximum concurrent jobs |
| `ARQ_JOB_TIMEOUT` | `300` | Job timeout in seconds |

### Usage

Define tasks in `core/tasks.py`:

```python
async def send_welcome_email(ctx, user_id: int):
    """Send welcome email to a new user."""
    # Your email sending logic here
    print(f"Sending welcome email to user {user_id}")

class WorkerSettings:
    functions = [send_welcome_email]
    redis_settings = RedisSettings.from_dsn(settings.arq_redis_url)
```

Enqueue tasks from your code:

```python
from core.arq import enqueue

# Enqueue a task
await enqueue("send_welcome_email", user_id=123)

# With delay
await enqueue("send_reminder", user_id=123, _defer_by=timedelta(hours=24))
```

### Running the Worker

```bash
uv run arq core.tasks.WorkerSettings
```

### Dependency

- `arq>=0.26`

---

## Storage

Object storage supporting local filesystem and S3-compatible backends (AWS S3, MinIO).

```bash
paxx infra add storage
```

### Generated Files

- `core/storage.py` - Storage abstraction and backends

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STORAGE_BACKEND` | `local` | Storage backend (`local` or `s3`) |
| `STORAGE_LOCAL_PATH` | `./uploads` | Local storage path |
| `STORAGE_S3_BUCKET` | - | S3 bucket name |
| `STORAGE_S3_REGION` | `us-east-1` | S3 region |
| `STORAGE_S3_ENDPOINT_URL` | - | Custom S3 endpoint (for MinIO) |
| `STORAGE_S3_ACCESS_KEY` | - | S3 access key |
| `STORAGE_S3_SECRET_KEY` | - | S3 secret key |

### Docker Service

Adds MinIO service for local S3-compatible testing.

### Usage

```python
from core.storage import get_storage

storage = get_storage()

# Upload a file
url = await storage.upload("images/photo.jpg", file_data)

# Download a file
data = await storage.download("images/photo.jpg")

# Delete a file
await storage.delete("images/photo.jpg")

# Check if file exists
exists = await storage.exists("images/photo.jpg")
```

### Local Development

By default, files are stored in `./uploads`.

### MinIO Testing

1. Start MinIO:
   ```bash
   docker compose up -d minio
   ```

2. Open console at http://localhost:9001
   - Username: `minioadmin`
   - Password: `minioadmin`

3. Create a bucket

4. Configure environment:
   ```bash
   STORAGE_BACKEND=s3
   STORAGE_S3_BUCKET=my-bucket
   STORAGE_S3_ENDPOINT_URL=http://localhost:9000
   STORAGE_S3_ACCESS_KEY=minioadmin
   STORAGE_S3_SECRET_KEY=minioadmin
   ```

### Dependencies

- `aioboto3>=13.0`
- `aiofiles>=24.0`

---

## WebSocket

WebSocket connection manager with room support and optional Redis pub/sub for multi-instance scaling.

```bash
paxx infra add websocket
```

### Generated Files

- `core/ws.py` - WebSocket manager with room support

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WS_REDIS_URL` | - | Redis URL for multi-instance pub/sub |
| `WS_HEARTBEAT_INTERVAL` | `30` | Heartbeat interval in seconds |

### Usage

Basic WebSocket endpoint:

```python
from fastapi import WebSocket, WebSocketDisconnect
from core.ws import manager

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
```

Room support:

```python
# Join a room
await manager.join_room(client_id, "chat-room")

# Send to room
await manager.broadcast_to_room("chat-room", {"message": "Hello!"})

# Leave room
await manager.leave_room(client_id, "chat-room")
```

### Multi-Instance Mode

For running multiple app instances behind a load balancer:

1. Set `WS_REDIS_URL` environment variable
2. Start pub/sub in your app lifespan:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    await manager.start_pubsub()
    yield
    await manager.stop_pubsub()
```

### Dependencies

No additional dependencies (uses existing FastAPI WebSocket support).

---

## PostGIS

PostGIS geospatial extension for PostgreSQL, enabling location-based queries.

```bash
paxx infra add postgis
```

### What It Does

- Upgrades your PostgreSQL image to `postgis/postgis`
- Adds GeoAlchemy2 for SQLAlchemy integration
- Provides helper functions for common geospatial queries

### Generated Files

- `core/geo.py` - Geography types and query helpers

### Usage

Define location fields in models:

```python
from core.geo import Geography
from sqlalchemy.orm import Mapped, mapped_column

class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[Geography] = mapped_column(
        Geography(geometry_type="POINT", srid=4326),
        index=True,  # Creates GIST index
    )
```

Query helpers:

```python
from core.geo import distance_within, bbox_filter, distance_meters

# Find locations within 100 meters of a point
stmt = select(Location).where(
    distance_within(Location.location, lat=52.52, lng=13.4, radius_meters=100)
)

# Viewport/bounding box query
stmt = select(Location).where(
    bbox_filter(Location.location, west=13.0, south=52.0, east=14.0, north=53.0)
)

# Calculate distance between points
stmt = select(
    Location,
    distance_meters(Location.location, lat=52.52, lng=13.4).label("distance")
).order_by("distance")
```

### Important

After adding PostGIS, restart your database:

```bash
docker compose down && docker compose up -d
```

### Dependencies

- `geoalchemy2>=0.14`

---

## Metrics

Prometheus metrics and OpenTelemetry distributed tracing.

```bash
paxx infra add metrics
```

### Generated Files

- `core/metrics.py` - Prometheus metrics setup
- `core/tracing.py` - OpenTelemetry tracing setup

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OTEL_SERVICE_NAME` | `myapp` | Service name for tracing |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4317` | OTLP endpoint |
| `METRICS_ENABLED` | `true` | Enable/disable metrics |

### Docker Service

Adds Jaeger for local trace visualization.

### Prometheus Metrics

```python
from core.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    ACTIVE_REQUESTS,
)

# Metrics are automatically collected via middleware
# Access at /metrics endpoint
```

Built-in metrics:
- `http_requests_total` - Total HTTP requests (labels: method, path, status)
- `http_request_duration_seconds` - Request latency histogram
- `http_requests_in_progress` - Currently processing requests

### OpenTelemetry Tracing

Automatic instrumentation for:
- FastAPI requests
- SQLAlchemy queries
- HTTP client requests

View traces in Jaeger:

```bash
docker compose up -d jaeger
# Open http://localhost:16686
```

### Custom Spans

```python
from core.tracing import get_tracer

tracer = get_tracer(__name__)

async def process_order(order_id: int):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        # Your logic here
```

### Dependencies

- `opentelemetry-api>=1.20`
- `opentelemetry-sdk>=1.20`
- `opentelemetry-instrumentation-fastapi>=0.41b0`
- `opentelemetry-instrumentation-sqlalchemy>=0.41b0`
- `opentelemetry-exporter-otlp>=1.20`
- `prometheus-client>=0.19`

---

## Summary

| Component | Purpose | Docker Service | Key Files |
|-----------|---------|----------------|-----------|
| **redis** | Caching, pub/sub | Redis | `core/cache.py` |
| **arq** | Background tasks | (uses Redis) | `core/arq.py`, `core/tasks.py` |
| **storage** | Object storage | MinIO | `core/storage.py` |
| **websocket** | Real-time connections | (optional Redis) | `core/ws.py` |
| **postgis** | Geospatial queries | (upgrades postgres) | `core/geo.py` |
| **metrics** | Observability | Jaeger | `core/metrics.py`, `core/tracing.py` |

## Best Practices

1. **Start with what you need** - Add components as requirements emerge
2. **Development vs Production** - Docker services are for local development; configure production services separately
3. **Environment variables** - Always configure production values via environment variables, not in code
4. **Dependencies** - Run `uv sync` after adding infrastructure to install new dependencies
