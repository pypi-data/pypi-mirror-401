"""CLI subcommands for managing infrastructure components."""

import ast
import importlib.util
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from paxx.cli.utils import check_project_context
from paxx.templates.infra import get_infra_dir, list_infra

app = typer.Typer(
    name="infra",
    help="Manage infrastructure components",
    no_args_is_help=True,
)

console = Console()


def _load_infra_config(infra_dir: Path) -> dict:
    """Load the InfraConfig from an infra component.

    Args:
        infra_dir: Path to the infra component directory.

    Returns:
        Dict with infra configuration values.
    """
    config_path = infra_dir / "config.py"
    if not config_path.exists():
        return {}

    spec = importlib.util.spec_from_file_location("config", config_path)
    if spec is None or spec.loader is None:
        return {}

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, "InfraConfig"):
        config = module.InfraConfig()
        return {
            "name": config.name,
            "docker_service": config.docker_service,
            "core_files": config.core_files,
            "dependencies": config.dependencies,
            "env_vars": config.env_vars,
        }
    return {}


def _copy_templates(templates_dir: Path, dest: Path) -> None:
    """Copy and render templates to destination.

    Args:
        templates_dir: Path to the templates directory.
        dest: Destination directory for rendered files.
    """
    from jinja2 import Environment, FileSystemLoader

    if not templates_dir.exists():
        return

    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    dest.mkdir(exist_ok=True)

    for template_file in templates_dir.glob("*.jinja"):
        template = env.get_template(template_file.name)
        output_name = template_file.stem  # Remove .jinja extension
        output_path = dest / output_name
        output_path.write_text(template.render())
        console.print(f"  [green]Created[/green] {output_path}")


def _upgrade_postgres_to_postgis() -> None:
    """Upgrade postgres service in docker-compose.yml to use PostGIS image.

    Finds the postgres service (named db, postgres, or database) and updates
    its image from postgres:X to postgis/postgis:X-3.4.
    """
    import yaml

    compose_path = Path("docker-compose.yml")
    if not compose_path.exists():
        console.print("  [yellow]Warning:[/yellow] docker-compose.yml not found")
        return

    with open(compose_path) as f:
        compose = yaml.safe_load(f)

    services = compose.get("services", {})

    # Find postgres service (might be named db, postgres, database)
    pg_service = None
    pg_name = None
    for name in ["db", "postgres", "database"]:
        if name in services:
            pg_service = services[name]
            pg_name = name
            break

    if not pg_service:
        console.print("  [yellow]Warning:[/yellow] No postgres service found in docker-compose.yml")
        console.print("  [dim]Expected service named: db, postgres, or database[/dim]")
        return

    # Check if already using postgis
    current_image = pg_service.get("image", "")
    if "postgis" in current_image:
        console.print("  [yellow]Already using PostGIS image[/yellow]")
        return

    # Extract version from current image (e.g., postgres:16 -> 16)
    version = "16"
    if ":" in current_image:
        version = current_image.split(":")[1].split("-")[0]

    # Update to PostGIS image
    pg_service["image"] = f"postgis/postgis:{version}-3.4"

    with open(compose_path, "w") as f:
        yaml.dump(compose, f, default_flow_style=False, sort_keys=False)

    console.print(f"  [green]Updated[/green] {pg_name} service to postgis/postgis:{version}-3.4")


def _merge_docker_service(service_file: Path) -> None:
    """Add service definition to docker-compose.yml.

    Args:
        service_file: Path to the service YAML file to merge.
    """
    import yaml

    compose_path = Path("docker-compose.yml")
    if not compose_path.exists():
        console.print("  [yellow]Warning:[/yellow] docker-compose.yml not found")
        return

    if not service_file.exists():
        return

    with open(compose_path) as f:
        compose = yaml.safe_load(f)

    with open(service_file) as f:
        new_service = yaml.safe_load(f)

    # Skip if file is empty or has no content
    if not new_service:
        return

    service_name = list(new_service.keys())[0]

    # Check if already added
    if service_name in compose.get("services", {}):
        console.print(
            f"  [yellow]Service '{service_name}' already exists in docker-compose.yml[/yellow]"
        )
        return

    compose["services"][service_name] = new_service[service_name]

    # Add volume if service uses one
    service_config = new_service[service_name]
    if "volumes" in service_config:
        if "volumes" not in compose:
            compose["volumes"] = {}
        for vol in service_config["volumes"]:
            if ":" in vol:
                vol_name = vol.split(":")[0]
                if vol_name not in compose["volumes"]:
                    compose["volumes"][vol_name] = None

    with open(compose_path, "w") as f:
        yaml.dump(compose, f, default_flow_style=False, sort_keys=False)

    console.print("  [green]Updated[/green] docker-compose.yml")


def _add_dependencies(deps_file: Path) -> None:
    """Add dependencies to pyproject.toml.

    Args:
        deps_file: Path to the dependencies.txt file.
    """
    import tomllib

    import tomli_w

    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        console.print("  [yellow]Warning:[/yellow] pyproject.toml not found")
        return

    if not deps_file.exists():
        return

    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    deps = [d.strip() for d in deps_file.read_text().strip().split("\n") if d.strip()]
    current = pyproject.get("project", {}).get("dependencies", [])

    added = []
    for dep in deps:
        # Check if dependency already exists (by package name)
        dep_name = dep.split(">=")[0].split("==")[0].split("<")[0].strip()
        existing_names = [
            d.split(">=")[0].split("==")[0].split("<")[0].strip() for d in current
        ]
        if dep_name not in existing_names:
            current.append(dep)
            added.append(dep)

    if added:
        pyproject["project"]["dependencies"] = current
        with open(pyproject_path, "wb") as f:
            tomli_w.dump(pyproject, f)
        console.print("  [green]Updated[/green] pyproject.toml")
    else:
        console.print("  [yellow]Dependencies already in pyproject.toml[/yellow]")


def _add_env_vars(env_vars: dict[str, str]) -> None:
    """Add environment variables to settings.py and .env.example.

    Args:
        env_vars: Dict of env var names and default values.
    """
    if not env_vars:
        return

    _add_env_vars_to_settings(env_vars)
    _add_env_vars_to_env_example(env_vars)


def _add_env_vars_to_settings(env_vars: dict[str, str]) -> None:
    """Add environment variables to settings.py using AST.

    Args:
        env_vars: Dict of env var names and default values.
    """
    settings_path = Path("settings.py")
    if not settings_path.exists():
        console.print("  [yellow]Warning:[/yellow] settings.py not found")
        return

    content = settings_path.read_text()
    tree = ast.parse(content)

    # Find the Settings class
    settings_class = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "Settings":
            settings_class = node
            break

    if not settings_class:
        console.print("  [yellow]Warning:[/yellow] Settings class not found")
        return

    # Get existing field names
    existing_fields = set()
    for item in settings_class.body:
        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            existing_fields.add(item.target.id.lower())

    # Build new fields to add
    new_fields = []
    for var_name, default_value in env_vars.items():
        field_name = var_name.lower()
        if field_name not in existing_fields:
            new_fields.append(f'    {field_name}: str = "{default_value}"')

    if not new_fields:
        console.print("  [yellow]Settings already contain these env vars[/yellow]")
        return

    # Find the insertion point (before the first method or at end of class)
    lines = content.split("\n")
    insert_line = None

    # Find the class definition line
    class_start = None
    for i, line in enumerate(lines):
        if "class Settings" in line:
            class_start = i
            break

    if class_start is None:
        return

    # Find the first method (@property, @field_validator, def) or end of class fields
    for i in range(class_start + 1, len(lines)):
        line = lines[i].strip()
        if line.startswith("@") or line.startswith("def "):
            insert_line = i
            break
        # Check for end of class (next class definition or end of indented block)
        if line and not line.startswith("#") and not lines[i].startswith(" "):
            insert_line = i
            break

    if insert_line is None:
        insert_line = len(lines)

    # Insert new fields with a comment
    new_content = "\n".join(new_fields)
    comment = "\n    # Infrastructure"
    lines.insert(insert_line, "")
    lines.insert(insert_line, new_content)
    lines.insert(insert_line, comment)

    settings_path.write_text("\n".join(lines))
    console.print("  [green]Updated[/green] settings.py")


def _add_env_vars_to_env_example(env_vars: dict[str, str]) -> None:
    """Add environment variables to .env.example.

    Args:
        env_vars: Dict of env var names and default values.
    """
    env_example_path = Path(".env.example")
    if not env_example_path.exists():
        console.print("  [yellow]Warning:[/yellow] .env.example not found")
        return

    content = env_example_path.read_text()

    # Check which vars already exist
    new_vars = []
    for var_name, default_value in env_vars.items():
        if f"{var_name}=" not in content:
            new_vars.append(f"{var_name}={default_value}")

    if not new_vars:
        return

    # Append new vars with a section header
    if not content.endswith("\n"):
        content += "\n"

    content += "\n# Infrastructure\n"
    content += "\n".join(new_vars) + "\n"

    env_example_path.write_text(content)
    console.print("  [green]Updated[/green] .env.example")


@app.command("add")
def add(
    name: str = typer.Argument(..., help="Name of the infrastructure component"),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite existing files",
    ),
) -> None:
    """Add an infrastructure component (redis, tasks, storage, etc.).

    Infrastructure components modify core files, docker-compose, and dependencies.
    Unlike domain features, they integrate with your project's foundation.

    Examples:
        paxx infra add redis     # Add Redis caching
        paxx infra list          # List available components
    """
    # Validate we're in a project
    check_project_context()

    # Check if infra exists
    infra_dir = get_infra_dir(name)
    if not infra_dir:
        available = ", ".join(list_infra()) or "none"
        console.print(f"[red]Error: Unknown infra component '{name}'[/red]")
        console.print(f"Available: {available}")
        raise typer.Exit(1)

    console.print(f"Adding infrastructure: [bold cyan]{name}[/bold cyan]")

    # Load config
    config = _load_infra_config(infra_dir)

    # Check prerequisites
    if name == "arq":
        settings_path = Path("settings.py")
        if settings_path.exists():
            settings_content = settings_path.read_text()
            if "redis_url" not in settings_content.lower():
                console.print(
                    "[yellow]Note:[/yellow] ARQ requires Redis. "
                    "Run [bold]paxx infra add redis[/bold] or configure ARQ_REDIS_URL."
                )

    # Special handling for postgis - upgrade existing postgres service
    if name == "postgis":
        _upgrade_postgres_to_postgis()

    # 1. Copy templates to core/
    templates_dir = infra_dir / "templates"
    if templates_dir.exists():
        _copy_templates(templates_dir, Path("core"))

    # 2. Merge docker service into docker-compose.yml
    service_file = infra_dir / "docker_service.yml"
    if service_file.exists():
        _merge_docker_service(service_file)

    # 3. Add dependencies to pyproject.toml
    deps_file = infra_dir / "dependencies.txt"
    if deps_file.exists():
        _add_dependencies(deps_file)

    # 4. Add env vars to settings.py and .env.example
    if config.get("env_vars"):
        _add_env_vars(config["env_vars"])

    console.print()
    console.print(f"[bold green]Added {name} infrastructure[/bold green]")
    console.print()
    console.print("Next steps:")
    console.print("  1. Run: [bold]uv sync[/bold]")
    console.print("  2. Start services: [bold]docker compose up -d[/bold]")
    if name == "redis":
        console.print("  3. Import in your code:")
        console.print(
            "     [dim]from core.cache import cache_get, cache_set, get_redis[/dim]"
        )

    if name == "arq":
        console.print()
        console.print("[bold]Running the worker:[/bold]")
        console.print("  [dim]uv run arq core.tasks.WorkerSettings[/dim]")
        console.print()
        console.print("[bold]Enqueue tasks from your code:[/bold]")
        console.print("  [dim]from core.arq import enqueue[/dim]")
        console.print("  [dim]await enqueue('send_welcome_email', user_id=123)[/dim]")

    if name == "storage":
        console.print()
        console.print("[bold]Local development:[/bold]")
        console.print("  Files are stored in ./uploads by default")
        console.print()
        console.print("[bold]MinIO testing (S3-compatible):[/bold]")
        console.print("  1. Start MinIO: [dim]docker compose up -d minio[/dim]")
        console.print("  2. Open console: [dim]http://localhost:9001[/dim]")
        console.print("  3. Create a bucket in the console")
        console.print("  4. Set env vars:")
        console.print("     [dim]STORAGE_BACKEND=s3[/dim]")
        console.print("     [dim]STORAGE_S3_BUCKET=my-bucket[/dim]")
        console.print("     [dim]STORAGE_S3_ENDPOINT_URL=http://localhost:9000[/dim]")
        console.print("     [dim]STORAGE_S3_ACCESS_KEY=minioadmin[/dim]")
        console.print("     [dim]STORAGE_S3_SECRET_KEY=minioadmin[/dim]")
        console.print()
        console.print("[bold]Usage in code:[/bold]")
        console.print("  [dim]from core.storage import get_storage[/dim]")
        console.print("  [dim]storage = get_storage()[/dim]")
        console.print("  [dim]url = await storage.upload('path/file.jpg', data)[/dim]")

    if name == "websocket":
        console.print()
        console.print("[bold]Basic WebSocket endpoint:[/bold]")
        console.print("  [dim]from fastapi import WebSocket, WebSocketDisconnect[/dim]")
        console.print("  [dim]from core.ws import manager[/dim]")
        console.print()
        console.print("  [dim]@app.websocket('/ws/{client_id}')[/dim]")
        console.print("  [dim]async def websocket_endpoint(websocket: WebSocket, client_id: str):[/dim]")
        console.print("  [dim]    await manager.connect(websocket, client_id)[/dim]")
        console.print("  [dim]    try:[/dim]")
        console.print("  [dim]        while True:[/dim]")
        console.print("  [dim]            data = await websocket.receive_text()[/dim]")
        console.print("  [dim]            await manager.broadcast(data)[/dim]")
        console.print("  [dim]    except WebSocketDisconnect:[/dim]")
        console.print("  [dim]        manager.disconnect(client_id)[/dim]")
        console.print()
        console.print("[bold]Room support:[/bold]")
        console.print("  [dim]await manager.join_room(client_id, 'chat-room')[/dim]")
        console.print("  [dim]await manager.broadcast_to_room('chat-room', {'msg': 'Hello!'})[/dim]")
        console.print()
        console.print("[bold]Multi-instance mode:[/bold]")
        console.print("  Set [bold]WS_REDIS_URL[/bold] and call [dim]await manager.start_pubsub()[/dim] in lifespan")

    if name == "postgis":
        console.print()
        console.print("[bold]Important:[/bold] Restart your database to use the new PostGIS image:")
        console.print("  [dim]docker compose down && docker compose up -d[/dim]")
        console.print()
        console.print("[bold]Usage in models:[/bold]")
        console.print("  [dim]from core.geo import Geography[/dim]")
        console.print("  [dim]from sqlalchemy.orm import mapped_column[/dim]")
        console.print()
        console.print("  [dim]class Location(Base):[/dim]")
        console.print("  [dim]    __tablename__ = 'locations'[/dim]")
        console.print("  [dim]    location = mapped_column([/dim]")
        console.print("  [dim]        Geography(geometry_type='POINT', srid=4326),[/dim]")
        console.print("  [dim]        index=True,  # Creates GIST index[/dim]")
        console.print("  [dim]    )[/dim]")
        console.print()
        console.print("[bold]Query helpers:[/bold]")
        console.print("  [dim]from core.geo import distance_within, bbox_filter, distance_meters[/dim]")
        console.print()
        console.print("  [dim]# Filter by radius (100m)[/dim]")
        console.print("  [dim]stmt = select(Location).where([/dim]")
        console.print("  [dim]    distance_within(Location.location, lat=52.52, lng=13.4, radius_meters=100)[/dim]")
        console.print("  [dim])[/dim]")
        console.print()
        console.print("  [dim]# Viewport/bounding box query[/dim]")
        console.print("  [dim]stmt = select(Location).where([/dim]")
        console.print("  [dim]    bbox_filter(Location.location, west=13.0, south=52.0, east=14.0, north=53.0)[/dim]")
        console.print("  [dim])[/dim]")


@app.command("list")
def list_cmd() -> None:
    """List available infrastructure components."""
    infra = list_infra()

    if not infra:
        console.print("[yellow]No infrastructure components available yet.[/yellow]")
        return

    # Descriptions for known infra components
    descriptions = {
        "redis": "Redis caching with async support",
        "arq": "Background task queue with ARQ",
        "tasks": "Background task queue (Celery/ARQ)",
        "storage": "Object storage (S3/MinIO)",
        "websocket": "WebSocket connections with room support",
        "postgis": "PostGIS geospatial extension for Postgres",
        "metrics": "Prometheus metrics and OpenTelemetry tracing",
        "email": "Email sending service",
    }

    table = Table(title="Available Infrastructure")
    table.add_column("Component", style="cyan")
    table.add_column("Description", style="white")

    for name in infra:
        description = descriptions.get(name, "No description available")
        table.add_row(name, description)

    console.print(table)
    console.print("\nUsage: [bold]paxx infra add <component>[/bold]")
