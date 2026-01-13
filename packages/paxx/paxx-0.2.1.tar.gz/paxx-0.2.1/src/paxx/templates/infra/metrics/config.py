"""Configuration for metrics and tracing infrastructure component."""

from dataclasses import dataclass, field


@dataclass
class InfraConfig:
    name: str = "metrics"
    docker_service: str = "jaeger"
    core_files: list[str] = field(default_factory=lambda: ["tracing.py", "metrics.py"])
    dependencies: list[str] = field(
        default_factory=lambda: [
            "opentelemetry-api>=1.20",
            "opentelemetry-sdk>=1.20",
            "opentelemetry-instrumentation-fastapi>=0.41b0",
            "opentelemetry-instrumentation-sqlalchemy>=0.41b0",
            "opentelemetry-exporter-otlp>=1.20",
            "prometheus-client>=0.19",
        ]
    )
    env_vars: dict[str, str] = field(
        default_factory=lambda: {
            "OTEL_SERVICE_NAME": "myapp",
            "OTEL_EXPORTER_OTLP_ENDPOINT": "http://localhost:4317",
            "METRICS_ENABLED": "true",
        }
    )
