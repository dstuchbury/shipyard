from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from shipyard.paths import RUNTIME_PROJECTS_DIR, RUNTIME_CERTS_DIR


def slugify_project_name(name: str) -> str:
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    slug = slug.strip("-")

    if not slug:
        raise ValueError("Could not derive a valid project slug.")

    return slug


def is_laravel_project(path: Path) -> bool:
    if not path.is_dir():
        return False

    artisan_path = path / "artisan"
    composer_json_path = path / "composer.json"

    if not artisan_path.is_file():
        return False

    if not composer_json_path.is_file():
        return False

    try:
        composer = json.loads(composer_json_path.read_text(encoding="utf-8"))
    except Exception:
        return False

    require = composer.get("require", {})
    require_dev = composer.get("require-dev", {})

    return (
        "laravel/framework" in require
        or "laravel/framework" in require_dev
        or artisan_path.is_file()
    )


def detect_vite_config(path: Path) -> Path | None:
    candidates = [
        path / "vite.config.js",
        path / "vite.config.ts",
        path / "vite.config.mjs",
        path / "vite.config.cjs",
    ]

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    return None


def build_project_replacements(app_path: Path) -> dict[str, str]:
    app_path = app_path.resolve()
    slug = slugify_project_name(app_path.name)
    domain = f"{slug}.test"

    service_php = f"{slug}-php"
    service_nginx = f"{slug}-nginx"
    service_node = f"{slug}-node"
    service_queue = f"{slug}-queue"
    service_scheduler = f"{slug}-scheduler"

    container_php = f"shipyard_{slug}_php"
    container_nginx = f"shipyard_{slug}_nginx"
    container_node = f"shipyard_{slug}_node"
    container_queue = f"shipyard_{slug}_queue"
    container_scheduler = f"shipyard_{slug}_scheduler"

    vite_config = detect_vite_config(app_path)

    return {
        "__SHIPYARD_PROJECT_SLUG__": slug,
        "__SHIPYARD_PROJECT_DOMAIN__": domain,
        "__SHIPYARD_APP_PATH__": str(app_path),
        "__SHIPYARD_SERVICE_PHP__": service_php,
        "__SHIPYARD_SERVICE_NGINX__": service_nginx,
        "__SHIPYARD_SERVICE_NODE__": service_node,
        "__SHIPYARD_SERVICE_QUEUE__": service_queue,
        "__SHIPYARD_SERVICE_SCHEDULER__": service_scheduler,
        "__SHIPYARD_CONTAINER_PHP__": container_php,
        "__SHIPYARD_CONTAINER_NGINX__": container_nginx,
        "__SHIPYARD_CONTAINER_NODE__": container_node,
        "__SHIPYARD_CONTAINER_QUEUE__": container_queue,
        "__SHIPYARD_CONTAINER_SCHEDULER__": container_scheduler,
        "__SHIPYARD_PHP_UPSTREAM__": f"{container_php}:9000",
        "__SHIPYARD_VITE_CONFIG_PATH__": str(vite_config) if vite_config else "",
        "__SHIPYARD_VITE_CONFIG_DETECTED__": "true" if vite_config else "false",
        "__SHIPYARD_RUNTIME_CERTS_PATH__": str(RUNTIME_CERTS_DIR),
    }


def get_project_runtime_dir(slug: str) -> Path:
    project_dir = RUNTIME_PROJECTS_DIR / slug
    if not project_dir.is_dir():
        raise FileNotFoundError(f"Shipyard project not found: {slug}")
    return project_dir


def get_project_compose_file(slug: str) -> Path:
    compose_file = get_project_runtime_dir(slug) / "docker-compose.generated.yml"
    if not compose_file.is_file():
        raise FileNotFoundError(f"Compose file not found for project '{slug}': {compose_file}")
    return compose_file


def get_project_config_file(slug: str) -> Path:
    config_file = get_project_runtime_dir(slug) / "shipyard.yml"
    if not config_file.is_file():
        raise FileNotFoundError(f"Shipyard config not found for project '{slug}': {config_file}")
    return config_file


def load_project_config(slug: str) -> dict:
    config_file = get_project_config_file(slug)
    with config_file.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def get_project_service_name(slug: str, service_alias: str) -> str:
    config = load_project_config(slug)
    services = config.get("services", {})

    if service_alias not in services:
        valid = ", ".join(sorted(services.keys()))
        raise ValueError(
            f"Unknown service '{service_alias}' for project '{slug}'. Valid services: {valid}"
        )

    return services[service_alias]


def get_default_attach_service_alias(slug: str) -> str:
    config = load_project_config(slug)
    defaults = config.get("defaults", {})
    return defaults.get("attach_service", "php")
