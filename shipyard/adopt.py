from __future__ import annotations

from pathlib import Path

from shipyard.certs import (
    import_project_cert,
    print_windows_mkcert_instructions_for_project,
    wait_for_user_confirmation,
)
from shipyard.paths import RUNTIME_PROJECTS_DIR
from shipyard.projects import build_project_replacements, detect_vite_config, is_laravel_project
from shipyard.templates import render_project_templates
from shipyard.traefik import write_project_tls_fragment
from shipyard.utils import ensure_dir


def run_adopt(app_path_raw: str) -> None:
    app_path = Path(app_path_raw).expanduser().resolve()

    if not app_path.exists():
        raise FileNotFoundError(f"Project path does not exist: {app_path}")

    if not is_laravel_project(app_path):
        raise ValueError(f"Path is not a Laravel project: {app_path}")

    replacements = build_project_replacements(app_path)
    slug = replacements["__SHIPYARD_PROJECT_SLUG__"]
    domain = replacements["__SHIPYARD_PROJECT_DOMAIN__"]

    project_runtime_dir = RUNTIME_PROJECTS_DIR / slug

    if project_runtime_dir.exists():
        raise FileExistsError(
            f"Shipyard project already exists for slug '{slug}': {project_runtime_dir}"
        )

    ensure_dir(project_runtime_dir)

    print(f"Adopting Laravel project: {app_path}")
    print(f"Project slug: {slug}")
    print(f"Project domain: {domain}")
    print()

    print("Rendering project templates...")
    render_project_templates(project_runtime_dir, replacements)

    print_windows_mkcert_instructions_for_project(slug, domain)
    wait_for_user_confirmation()

    print("Importing project certificate...")
    import_project_cert(slug, domain)

    print("Writing Traefik TLS fragment...")
    tls_fragment = write_project_tls_fragment(slug, domain)

    vite_config = detect_vite_config(app_path)
    if vite_config:
        print()
        print(f"Vite config detected at: {vite_config}")
        print("Shipyard does not modify project files automatically.")
        print(
            "Please compare your project's Vite config with the generated example in "
            f"{project_runtime_dir / 'support' / 'vite.config.shipyard.example.js'}"
        )

    print()
    print("Project adopted successfully.")
    print(f"Runtime project directory: {project_runtime_dir}")
    print(f"TLS fragment: {tls_fragment}")
