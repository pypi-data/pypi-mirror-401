"""Configuration for Redis infrastructure component."""

from dataclasses import dataclass, field


@dataclass
class InfraConfig:
    name: str = "redis"
    docker_service: str = "redis"
    core_files: list[str] = field(default_factory=lambda: ["cache.py"])
    dependencies: list[str] = field(default_factory=lambda: ["redis>=5.0"])
    env_vars: dict[str, str] = field(
        default_factory=lambda: {"REDIS_URL": "redis://localhost:6379/0"}
    )
