from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from shipyard.paths import RUNTIME_DOCKER_COMPOSE, RUNTIME_PROJECTS_DIR, RUNTIME_ROOT
from shipyard.projects import (
    get_default_attach_service_alias,
    get_project_compose_file,
    get_project_runtime_dir,
    get_project_service_name,
)


def _run(command: list[str], cwd: Path | None = None, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        cwd=cwd,
        check=True,
        text=True,
        capture_output=capture,
    )


def ensure_docker_compose_available() -> None:
    if shutil.which("docker") is None:
        raise RuntimeError("Docker is not installed or not on PATH.")

def ensure_core_up() -> None:
    if not is_core_up():
            print("Shipyard core runtime is not running. Starting it now...")
            up_core()

def core_runtime_exists() -> bool:
    return RUNTIME_DOCKER_COMPOSE.is_file()


def project_exists(slug: str) -> bool:
    return (RUNTIME_PROJECTS_DIR / slug).is_dir()


def get_all_project_slugs() -> list[str]:
    if not RUNTIME_PROJECTS_DIR.is_dir():
        return []

    return sorted(
        p.name
        for p in RUNTIME_PROJECTS_DIR.iterdir()
        if p.is_dir()
    )


def _docker_compose_ps_services(cwd: Path, compose_filename: str) -> list[str]:
    result = _run(
        ["docker", "compose", "-f", compose_filename, "ps", "--services", "--status", "running"],
        cwd=cwd,
        capture=True,
    )

    output = result.stdout.strip()
    if not output:
        return []

    return [line.strip() for line in output.splitlines() if line.strip()]


def is_core_up() -> bool:
    ensure_docker_compose_available()

    if not core_runtime_exists():
        return False

    try:
        services = _docker_compose_ps_services(RUNTIME_ROOT, RUNTIME_DOCKER_COMPOSE.name)
        return len(services) > 0
    except subprocess.CalledProcessError:
        return False


def is_project_up(slug: str) -> bool:
    ensure_docker_compose_available()

    if not project_exists(slug):
        return False

    try:
        project_dir = get_project_runtime_dir(slug)
        compose_file = get_project_compose_file(slug)
        services = _docker_compose_ps_services(project_dir, compose_file.name)
        return len(services) > 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def up_core() -> None:
    ensure_docker_compose_available()

    if not core_runtime_exists():
        raise FileNotFoundError(
            f"Shipyard runtime compose file not found: {RUNTIME_DOCKER_COMPOSE}"
        )

    _run(["docker", "compose", "up", "-d"], cwd=RUNTIME_ROOT)


def restart_core() -> None:
    ensure_docker_compose_available()

    if not core_runtime_exists():
        raise FileNotFoundError(
            f"Shipyard runtime compose file not found: {RUNTIME_DOCKER_COMPOSE}"
        )

    _run(["docker", "compose", "up", "-d", "--force-recreate"], cwd=RUNTIME_ROOT)


def rebuild_core() -> None:
    ensure_docker_compose_available()

    if not core_runtime_exists():
        raise FileNotFoundError(
            f"Shipyard runtime compose file not found: {RUNTIME_DOCKER_COMPOSE}"
        )

    _run(["docker", "compose", "up", "-d", "--build"], cwd=RUNTIME_ROOT)



def down_core() -> None:
    ensure_docker_compose_available()

    if not core_runtime_exists():
        raise FileNotFoundError(
            f"Shipyard runtime compose file not found: {RUNTIME_DOCKER_COMPOSE}"
        )

    _run(["docker", "compose", "down"], cwd=RUNTIME_ROOT)


def up_project(slug: str) -> None:
    ensure_docker_compose_available()
    ensure_core_up()

    project_dir = get_project_runtime_dir(slug)
    compose_file = get_project_compose_file(slug)

    _run(
        ["docker", "compose", "-f", compose_file.name, "up", "-d", "--remove-orphans"],
        cwd=project_dir,
    )


def restart_project(slug: str) -> None:
      ensure_docker_compose_available()
      ensure_core_up()

      project_dir = get_project_runtime_dir(slug)
      compose_file = get_project_compose_file(slug)

      _run(
          ["docker", "compose", "-f", compose_file.name, "restart"],
          cwd=project_dir,
      )


def rebuild_project(slug: str) -> None:
      ensure_docker_compose_available()
      ensure_core_up()

      project_dir = get_project_runtime_dir(slug)
      compose_file = get_project_compose_file(slug)

      _run(
          ["docker", "compose", "-f", compose_file.name, "up", "-d", "--build"],
          cwd=project_dir,
      )


def down_project(slug: str) -> None:
    ensure_docker_compose_available()

    project_dir = get_project_runtime_dir(slug)
    compose_file = get_project_compose_file(slug)

    _run(
        ["docker", "compose", "-f", compose_file.name, "down"],
        cwd=project_dir,
    )


def down_all() -> None:
    ensure_docker_compose_available()

    # Bring projects down first, then core runtime.
    for slug in get_all_project_slugs():
        if is_project_up(slug):
            down_project(slug)

    if is_core_up():
        down_core()


def attach_project(slug: str, service_alias: str | None = None) -> None:
    ensure_docker_compose_available()

    # If core runtime is not up, bring it up first.
    if not is_core_up():
        print("Shipyard core runtime is not running. Starting it now...")
        up_core()

    # If the project is not up, bring it up too.
    if not is_project_up(slug):
        print(f"Project '{slug}' is not running. Starting it now...")
        up_project(slug)

    project_dir = get_project_runtime_dir(slug)
    compose_file = get_project_compose_file(slug)

    if service_alias is None:
        service_alias = get_default_attach_service_alias(slug)

    service_name = get_project_service_name(slug, service_alias)

    shell_command = (
        f"docker compose -f {compose_file.name} exec {service_name} bash "
        f"|| docker compose -f {compose_file.name} exec {service_name} sh"
    )

    subprocess.run(
        ["sh", "-c", shell_command],
        cwd=project_dir,
        check=True,
    )


def list_status() -> None:
    ensure_docker_compose_available()

    core_status = "up" if is_core_up() else "down"
    print(f"core: {core_status}")

    project_slugs = get_all_project_slugs()
    if not project_slugs:
        print("projects: none")
        return

    print("projects:")
    for slug in project_slugs:
        status = "up" if is_project_up(slug) else "down"
        print(f"  - {slug}: {status}")
