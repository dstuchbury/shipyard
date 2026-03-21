from __future__ import annotations

import shutil
from pathlib import Path

from shipyard.paths import CORE_CERT_FILES, RUNTIME_CERTS_DIR, WINDOWS_CERT_EXPORT_DIR_WSL
from shipyard.utils import ensure_dir, require_file


def print_windows_mkcert_instructions_for_core() -> None:
    print()
    print("Shipyard needs trusted local certificates for its core services.")
    print()
    print("Please run the following in Windows PowerShell:")
    print()
    print(r"  mkdir C:\shipyard-certs -Force")
    print(r"  cd C:\shipyard-certs")
    print(r"  mkcert traefik.test")
    print(r"  mkcert mailpit.test")
    print()
    print("When the files have been created, come back here and press Enter.")
    print()


def print_windows_mkcert_instructions_for_project(slug: str, domain: str) -> None:
    print()
    print(f"Shipyard needs a trusted local certificate for project '{slug}'.")
    print()
    print("Please run the following in Windows PowerShell:")
    print()
    print(rf"  mkdir C:\shipyard-certs\{slug} -Force")
    print(rf"  cd C:\shipyard-certs\{slug}")
    print(rf"  mkcert {domain}")
    print()
    print("When the files have been created, come back here and press Enter.")
    print()


def wait_for_user_confirmation() -> None:
    input("Press Enter to continue once the certificate files exist... ")


def validate_windows_exported_core_certs() -> None:
    for filename in CORE_CERT_FILES.values():
        require_file(
            WINDOWS_CERT_EXPORT_DIR_WSL / filename,
            f"Windows-exported certificate file '{filename}'",
        )


def import_core_certs() -> None:
    ensure_dir(RUNTIME_CERTS_DIR)

    for filename in CORE_CERT_FILES.values():
        src = WINDOWS_CERT_EXPORT_DIR_WSL / filename
        dest = RUNTIME_CERTS_DIR / filename
        shutil.copy2(src, dest)
        dest.chmod(0o644)


def validate_windows_exported_project_cert(slug: str, domain: str) -> tuple[Path, Path]:
    export_dir = WINDOWS_CERT_EXPORT_DIR_WSL / slug
    cert_path = export_dir / f"{domain}.pem"
    key_path = export_dir / f"{domain}-key.pem"

    require_file(cert_path, f"Windows-exported project certificate '{cert_path.name}'")
    require_file(key_path, f"Windows-exported project key '{key_path.name}'")

    return cert_path, key_path


def import_project_cert(slug: str, domain: str) -> tuple[Path, Path]:
    ensure_dir(RUNTIME_CERTS_DIR)

    src_cert, src_key = validate_windows_exported_project_cert(slug, domain)

    dest_cert = RUNTIME_CERTS_DIR / f"{domain}.pem"
    dest_key = RUNTIME_CERTS_DIR / f"{domain}-key.pem"

    shutil.copy2(src_cert, dest_cert)
    shutil.copy2(src_key, dest_key)

    dest_cert.chmod(0o644)
    dest_key.chmod(0o644)

    return dest_cert, dest_key
