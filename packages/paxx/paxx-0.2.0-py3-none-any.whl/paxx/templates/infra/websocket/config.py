"""WebSocket infrastructure configuration."""

from dataclasses import dataclass, field


@dataclass
class InfraConfig:
    """Configuration for WebSocket infrastructure."""

    name: str = "websocket"
    docker_service: str = ""  # Reuses existing Redis service for pub/sub
    core_files: list[str] = field(default_factory=lambda: ["ws.py"])
    dependencies: list[str] = field(default_factory=list)  # No extra deps needed
    env_vars: dict[str, str] = field(
        default_factory=lambda: {
            "WS_REDIS_URL": "",
            "WS_HEARTBEAT_INTERVAL": "30",
        }
    )
