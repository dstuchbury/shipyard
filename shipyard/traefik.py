from __future__ import annotations

from pathlib import Path

from shipyard.paths import (
    RUNTIME_TRAEFIK_DIR,
    RUNTIME_TRAEFIK_DYNAMIC_DIR,
)
from shipyard.utils import ensure_dir


def ensure_runtime_traefik_dirs() -> None:
    ensure_dir(RUNTIME_TRAEFIK_DIR)
    ensure_dir(RUNTIME_TRAEFIK_DYNAMIC_DIR)


def write_project_tls_fragment(slug: str, domain: str) -> Path:
    ensure_runtime_traefik_dirs()

    target_path = RUNTIME_TRAEFIK_DYNAMIC_DIR / f"{slug}-tls.yml"
    temp_path = RUNTIME_TRAEFIK_DYNAMIC_DIR / f".{slug}-tls.yml.tmp"

    content = (
        "tls:\n"
        "  certificates:\n"
        f"    - certFile: /certs/{domain}.pem\n"
        f"      keyFile: /certs/{domain}-key.pem\n"
    )

    temp_path.write_text(content, encoding="utf-8")
    temp_path.replace(target_path)

    return target_path
