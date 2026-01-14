"""Configuration management for iseq-flow CLI."""

import json
from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings


# Environment presets - service URLs for each environment
ENVIRONMENTS = {
    "prod": {
        "name": "Production",
        "domain": "iflow.intelliseq.com",
        "file_url": "https://files.iflow.intelliseq.com",
        "compute_url": "https://compute.iflow.intelliseq.com",
        "admin_url": "https://admin.iflow.intelliseq.com",
        "miner_url": "https://miner.iflow.intelliseq.com",
        "zitadel_issuer": "https://zitadel.iflow.intelliseq.com",
        "zitadel_client_id": "354511658992861447",
    },
    "stg": {
        "name": "Staging",
        "domain": "stg.iflow.intelliseq.com",
        "file_url": "https://files.stg.iflow.intelliseq.com",
        "compute_url": "https://compute.stg.iflow.intelliseq.com",
        "admin_url": "https://admin.stg.iflow.intelliseq.com",
        "miner_url": "https://miner.stg.iflow.intelliseq.com",
        "zitadel_issuer": "https://zitadel.iflow.intelliseq.com",
        "zitadel_client_id": "354511658992861447",
    },
    "dev": {
        "name": "Development (local)",
        "domain": "flow.labpgx.com",
        "file_url": "https://files.flow.labpgx.com",
        "compute_url": "https://compute.flow.labpgx.com",
        "admin_url": "https://admin.flow.labpgx.com",
        "miner_url": "https://miner.flow.labpgx.com",
        "zitadel_issuer": "https://zitadel.iflow.intelliseq.com",
        "zitadel_client_id": "352780574336811032",  # Dev app
    },
}


class FlowConfig(BaseSettings):
    """CLI configuration with defaults."""

    # Current environment
    environment: str = "dev"

    # Default project context (saved after selection)
    project_id: str | None = None
    project_name: str | None = None
    org_id: str | None = None
    org_name: str | None = None
    bucket_name: str | None = None

    # API endpoints (can override per-service)
    file_url: str = "https://files.flow.labpgx.com"
    compute_url: str = "https://compute.flow.labpgx.com"
    admin_url: str = "https://admin.flow.labpgx.com"
    miner_url: str = "https://miner.flow.labpgx.com"

    # Legacy alias for backwards compatibility
    api_url: str = "https://files.flow.labpgx.com"

    # Zitadel OAuth settings
    zitadel_issuer: str = "https://zitadel.iflow.intelliseq.com"
    zitadel_client_id: str = "352780574336811032"

    # Token storage
    keyring_service: str = "iseq-flow"

    model_config = {
        "env_prefix": "FLOW_",
        "env_file": ".env",
        "extra": "ignore",
    }


def get_config_path() -> Path:
    """Get path to config file."""
    config_dir = Path.home() / ".config" / "iseq-flow"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"


def load_config() -> dict[str, Any]:
    """Load config from file."""
    config_path = get_config_path()
    if config_path.exists():
        return json.loads(config_path.read_text())
    return {}


def save_config(config: dict[str, Any]) -> None:
    """Save config to file."""
    config_path = get_config_path()
    config_path.write_text(json.dumps(config, indent=2))


def get_settings() -> FlowConfig:
    """Get settings with file overrides."""
    file_config = load_config()

    # Create settings, allowing file config to override defaults
    return FlowConfig(**file_config)


def get_default_project() -> str | None:
    """Get default project ID from config."""
    return get_settings().project_id


def set_project_context(
    project_id: str,
    project_name: str,
    org_id: str | None = None,
    org_name: str | None = None,
    bucket_name: str | None = None,
) -> None:
    """Save project context to config."""
    config = load_config()
    config["project_id"] = project_id
    config["project_name"] = project_name
    if org_id:
        config["org_id"] = org_id
    if org_name:
        config["org_name"] = org_name
    if bucket_name:
        config["bucket_name"] = bucket_name
    save_config(config)


def clear_project_context() -> None:
    """Clear saved project context."""
    config = load_config()
    config.pop("project_id", None)
    config.pop("project_name", None)
    config.pop("org_id", None)
    config.pop("org_name", None)
    config.pop("bucket_name", None)
    save_config(config)


def get_bucket_name() -> str | None:
    """Get bucket name from config."""
    return get_settings().bucket_name


def resolve_gcs_path(path: str) -> str:
    """Resolve a path to full GCS URI.

    If path starts with gs://, return as-is.
    Otherwise, prepend the project's bucket.
    """
    if path.startswith("gs://") or path.startswith("s3://"):
        return path

    bucket = get_bucket_name()
    if not bucket:
        # No bucket configured, return path as-is (will likely fail at API level)
        return path

    # Remove leading slash if present
    path = path.lstrip("/")
    return f"gs://{bucket}/{path}"


def require_project(project_option: str | None) -> str:
    """Get project ID from option or config, raise if not available."""
    if project_option:
        return project_option

    default_project = get_default_project()
    if default_project:
        return default_project

    raise click.ClickException(
        "No project specified. Either:\n"
        "  - Use -p/--project PROJECT_ID\n"
        "  - Set default with: flow config select-project"
    )


# Import click here to avoid circular import at module load
import click
