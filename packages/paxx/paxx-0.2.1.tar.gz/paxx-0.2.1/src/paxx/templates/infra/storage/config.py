"""Object storage infrastructure configuration."""

from dataclasses import dataclass, field


@dataclass
class InfraConfig:
    """Configuration for object storage infrastructure."""

    name: str = "storage"
    docker_service: str = "minio"
    core_files: list[str] = field(default_factory=lambda: ["storage.py"])
    dependencies: list[str] = field(
        default_factory=lambda: ["aioboto3>=13.0", "aiofiles>=24.0"]
    )
    env_vars: dict[str, str] = field(
        default_factory=lambda: {
            "STORAGE_BACKEND": "local",
            "STORAGE_LOCAL_PATH": "./uploads",
            "STORAGE_S3_BUCKET": "",
            "STORAGE_S3_REGION": "us-east-1",
            "STORAGE_S3_ENDPOINT_URL": "",
            "STORAGE_S3_ACCESS_KEY": "",
            "STORAGE_S3_SECRET_KEY": "",
        }
    )
