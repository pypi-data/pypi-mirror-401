"""ARQ background tasks infrastructure configuration."""

from dataclasses import dataclass, field


@dataclass
class InfraConfig:
    """Configuration for ARQ task queue infrastructure."""

    name: str = "arq"
    docker_service: str = ""  # Reuses existing Redis service
    core_files: list[str] = field(default_factory=lambda: ["arq.py", "tasks.py"])
    dependencies: list[str] = field(default_factory=lambda: ["arq>=0.26"])
    env_vars: dict[str, str] = field(
        default_factory=lambda: {
            "ARQ_REDIS_URL": "redis://localhost:6379/1",
            "ARQ_MAX_JOBS": "10",
            "ARQ_JOB_TIMEOUT": "300",
        }
    )
