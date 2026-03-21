from __future__ import annotations

import re
from pathlib import Path

from shipyard.paths import (
    RUNTIME_DOCKER_COMPOSE,
    RUNTIME_TRAEFIK_DIR,
    RUNTIME_TRAEFIK_DYNAMIC_DIR,
    TEMPLATE_PROJECT_DIR,
    TEMPLATE_RUNTIME_DOCKER_COMPOSE,
    TEMPLATE_TRAEFIK_DYNAMIC_DIR,
    TEMPLATE_TRAEFIK_FILE,
)
from shipyard.utils import copy_file, copy_tree_contents, ensure_dir


TOKEN_PATTERN = re.compile(r"__SHIPYARD_[A-Z0-9_]+__")


def install_runtime_templates() -> None:
    copy_file(TEMPLATE_RUNTIME_DOCKER_COMPOSE, RUNTIME_DOCKER_COMPOSE)
    copy_file(TEMPLATE_TRAEFIK_FILE, RUNTIME_TRAEFIK_DIR / "traefik.yml")
    copy_tree_contents(TEMPLATE_TRAEFIK_DYNAMIC_DIR, RUNTIME_TRAEFIK_DYNAMIC_DIR)


def render_string(content: str, replacements: dict[str, str]) -> str:
    rendered = content

    for token, value in replacements.items():
        rendered = rendered.replace(token, value)

    return rendered


def find_unresolved_tokens(content: str) -> list[str]:
    return sorted(set(TOKEN_PATTERN.findall(content)))


def render_file(template_path: Path, output_path: Path, replacements: dict[str, str]) -> None:
    content = template_path.read_text(encoding="utf-8")
    rendered = render_string(content, replacements)

    unresolved = find_unresolved_tokens(rendered)
    if unresolved:
        raise ValueError(
            f"Unresolved tokens in rendered file {output_path}: {', '.join(unresolved)}"
        )

    ensure_dir(output_path.parent)
    output_path.write_text(rendered, encoding="utf-8")


def render_tree(template_root: Path, output_root: Path, replacements: dict[str, str]) -> None:
    ensure_dir(output_root)

    for path in template_root.rglob("*"):
        relative_path = path.relative_to(template_root)
        target_path = output_root / relative_path

        if path.is_dir():
            ensure_dir(target_path)
            continue

        render_file(path, target_path, replacements)


def render_project_templates(project_runtime_dir: Path, replacements: dict[str, str]) -> None:
    render_tree(TEMPLATE_PROJECT_DIR, project_runtime_dir, replacements)
