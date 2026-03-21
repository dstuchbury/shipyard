from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_ROOT = REPO_ROOT / "templates"

RUNTIME_ROOT = Path.home() / "shipyard"
RUNTIME_TRAEFIK_DIR = RUNTIME_ROOT / "traefik"
RUNTIME_TRAEFIK_DYNAMIC_DIR = RUNTIME_TRAEFIK_DIR / "dynamic"
RUNTIME_CERTS_DIR = RUNTIME_ROOT / "certs"
RUNTIME_PROJECTS_DIR = RUNTIME_ROOT / "projects"
RUNTIME_DOCKER_COMPOSE = RUNTIME_ROOT / "docker-compose.yml"

WINDOWS_CERT_EXPORT_DIR_WSL = Path("/mnt/c/shipyard-certs")

TEMPLATE_RUNTIME_DIR = TEMPLATES_ROOT / "runtime"
TEMPLATE_RUNTIME_DOCKER_COMPOSE = TEMPLATE_RUNTIME_DIR / "docker-compose.yml"

TEMPLATE_TRAEFIK_DIR = TEMPLATES_ROOT / "traefik"
TEMPLATE_TRAEFIK_FILE = TEMPLATE_TRAEFIK_DIR / "traefik.yml"
TEMPLATE_TRAEFIK_DYNAMIC_DIR = TEMPLATE_TRAEFIK_DIR / "dynamic"
TEMPLATE_CORE_TLS_FILE = TEMPLATE_TRAEFIK_DYNAMIC_DIR / "shipyard-core-tls.yml"

TEMPLATE_PROJECT_DIR = TEMPLATES_ROOT / "project"
TEMPLATE_PROJECT_DOCKER_DIR = TEMPLATE_PROJECT_DIR / "docker"
TEMPLATE_PROJECT_NGINX_DIR = TEMPLATE_PROJECT_DIR / "nginx"
TEMPLATE_PROJECT_PHP_DIR = TEMPLATE_PROJECT_DIR / "php"
TEMPLATE_PROJECT_SUPPORT_DIR = TEMPLATE_PROJECT_DIR / "support"
TEMPLATE_PROJECT_SHIPYARD_FILE = TEMPLATE_PROJECT_DIR / "shipyard.yml"
TEMPLATE_PROJECT_COMPOSE_FILE = TEMPLATE_PROJECT_DIR / "docker-compose.generated.yml"

CORE_CERT_FILES = {
    "traefik_cert": "traefik.test.pem",
    "traefik_key": "traefik.test-key.pem",
    "mailpit_cert": "mailpit.test.pem",
    "mailpit_key": "mailpit.test-key.pem",
}
