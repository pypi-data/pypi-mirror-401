"""Configuration for PostGIS infrastructure component."""

from dataclasses import dataclass, field


@dataclass
class InfraConfig:
    name: str = "postgis"
    docker_service: str = ""  # Special case - modifies existing postgres
    core_files: list[str] = field(default_factory=lambda: ["geo.py"])
    dependencies: list[str] = field(
        default_factory=lambda: [
            "geoalchemy2>=0.14",
        ]
    )
    env_vars: dict[str, str] = field(default_factory=dict)  # No new env vars
