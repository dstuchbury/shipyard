from __future__ import annotations

from shipyard.certs import (
    import_core_certs,
    print_windows_mkcert_instructions_for_core,
    validate_windows_exported_core_certs,
    wait_for_user_confirmation,
)
from shipyard.paths import (
    RUNTIME_CERTS_DIR,
    RUNTIME_PROJECTS_DIR,
    RUNTIME_ROOT,
)
from shipyard.templates import install_runtime_templates
from shipyard.traefik import ensure_runtime_traefik_dirs
from shipyard.utils import ensure_dir


def run_init() -> None:
    print("Initialising Shipyard runtime...")
    ensure_dir(RUNTIME_ROOT)
    ensure_runtime_traefik_dirs()
    ensure_dir(RUNTIME_CERTS_DIR)
    ensure_dir(RUNTIME_PROJECTS_DIR)

    print("Installing Shipyard runtime templates...")
    install_runtime_templates()

    print_windows_mkcert_instructions_for_core()
    wait_for_user_confirmation()

    print("Validating exported certificate files...")
    validate_windows_exported_core_certs()

    print("Importing certificates into Shipyard runtime...")
    import_core_certs()

    print()
    print("Shipyard runtime initialised successfully.")
    print(f"Runtime root: {RUNTIME_ROOT}")
