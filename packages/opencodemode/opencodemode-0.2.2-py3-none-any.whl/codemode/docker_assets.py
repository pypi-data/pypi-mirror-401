"""
Utilities for distributing the Docker sidecar bundle.

This module lets users export the `docker_sidecar/` folder even when the
package is installed from PyPI/uv (no repo checkout required).

The exported bundle is self-contained and can be used to build the executor
Docker image without any additional files.

Usage:
    # Via CLI (recommended)
    codemode docker assets --dest ./executor-sidecar

    # Via Python module
    python -m codemode.docker_assets export --dest ./executor-sidecar

    # Programmatic usage
    from codemode.docker_assets import export_bundle
    dest = export_bundle("./executor-sidecar")
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from importlib.abc import Traversable


def _find_sidecar_source() -> Path:
    """
    Locate the packaged docker_sidecar directory.

    Preference order:
        1. Repository layout (../docker_sidecar relative to this file)
        2. Installed package data (codemode/docker_sidecar)
        3. importlib.resources fallback for wheel/egg installs

    Returns:
        Path to the docker_sidecar directory.

    Raises:
        FileNotFoundError: If docker_sidecar bundle cannot be found.
    """
    here = Path(__file__).resolve()
    candidates = [
        here.parent.parent / "docker_sidecar",  # repo root
        here.parent / "docker_sidecar",  # packaged alongside codemode
    ]

    for path in candidates:
        if path.exists():
            return path

    # Final fallback: importlib.resources (in case build packs resources)
    try:
        from importlib import resources

        resource_files: Traversable = resources.files("codemode")
        resource_path = resource_files.joinpath("docker_sidecar")
        # Check if it's a real path we can use
        if hasattr(resource_path, "is_dir") and resource_path.is_dir():
            # For resources that support direct path access
            return Path(str(resource_path))
    except Exception:
        pass

    raise FileNotFoundError(
        "docker_sidecar bundle not found in installed package.\n"
        "\n"
        "This can happen if:\n"
        "  - The package was installed without the docker extras\n"
        "  - The package data was not included in the build\n"
        "\n"
        "Try reinstalling with: pip install 'opencodemode[docker]'"
    )


def _get_sidecar_config_template() -> str:
    """
    Return a template sidecar configuration file.

    Returns:
        YAML configuration template string.
    """
    return """# Codemode Sidecar Configuration
# For the executor sidecar service running in Docker
# Documentation: https://github.com/mldlwizard/codemode

# Service binding
port: 8001
host: "0.0.0.0"
main_app_grpc_target: ${CODEMODE_MAIN_APP_TARGET:-host.docker.internal:50051}
api_key: ${CODEMODE_API_KEY}

# Execution limits
limits:
  code_timeout: 30      # Maximum execution time in seconds (1-300)
  max_code_length: 10000  # Maximum code length in characters

# Security settings
security:
  allow_direct_execution: false
  allowed_commands: []  # e.g., [grep, cat, ls]

# TLS configuration for incoming connections
tls:
  enabled: false
  mode: system  # 'system' or 'custom'
  # cert_file: /certs/server.crt
  # key_file: /certs/server.key
  # ca_file: /certs/ca.crt
  # require_client_auth: false

# TLS for callbacks to main app
callback_tls:
  enabled: false
  # ca_file: /certs/ca.crt
  # client_cert: /certs/client.crt
  # client_key: /certs/client.key

# Logging
log_level: INFO
"""


def _get_env_template() -> str:
    """
    Return a template .env file for docker-compose.

    Returns:
        Template .env file content.
    """
    return """# Codemode Executor Environment Variables
# Copy to .env and customize for your deployment

# Required: API key for authentication (change this!)
CODEMODE_API_KEY=your-secret-api-key

# Main app callback target (for ToolService callbacks)
# Use host.docker.internal for Docker on Mac/Windows
# Use the actual IP/hostname for Linux
CODEMODE_MAIN_APP_TARGET=host.docker.internal:50051

# Optional: Codemode version to install
# CODEMODE_VERSION=latest

# Optional: Execution limits
# CODEMODE_CODE_TIMEOUT=30
# CODEMODE_MAX_CODE_LENGTH=10000

# Optional: Security settings
# CODEMODE_ALLOW_DIRECT_EXECUTION=false

# Optional: Logging
# CODEMODE_LOG_LEVEL=INFO
"""


def export_bundle(dest: str | Path, overwrite: bool = False) -> Path:
    """
    Copy the docker_sidecar bundle to a destination directory.

    The exported bundle includes:
        - Dockerfile: Builds executor image from PyPI
        - docker-compose.yml: Production-ready compose configuration
        - README.md: Usage instructions
        - codemode-sidecar.yaml.template: Configuration template
        - .env.template: Environment variable template

    Args:
        dest: Destination directory path.
        overwrite: If True, overwrite existing files. If False and destination
            exists with files, raises FileExistsError.

    Returns:
        Path to the destination directory.

    Raises:
        FileExistsError: If destination exists and is not empty (and overwrite=False).
        FileNotFoundError: If source docker_sidecar bundle cannot be found.

    Example:
        >>> from codemode.docker_assets import export_bundle
        >>> dest = export_bundle("./executor-sidecar")
        >>> print(f"Exported to {dest}")
        Exported to /path/to/executor-sidecar
    """
    src = _find_sidecar_source()
    dest_path = Path(dest).expanduser().resolve()

    if dest_path.exists() and dest_path.is_dir() and not overwrite:
        # Prevent accidental overwrite
        if any(dest_path.iterdir()):
            raise FileExistsError(
                f"Destination '{dest_path}' already exists and is not empty.\n"
                "Pass --force to overwrite existing files."
            )

    dest_path.mkdir(parents=True, exist_ok=True)

    # Copy the docker_sidecar contents
    shutil.copytree(src, dest_path, dirs_exist_ok=True)

    # Add template files if they don't exist
    sidecar_config_template = dest_path / "codemode-sidecar.yaml.template"
    if not sidecar_config_template.exists() or overwrite:
        sidecar_config_template.write_text(_get_sidecar_config_template())

    env_template = dest_path / ".env.template"
    if not env_template.exists() or overwrite:
        env_template.write_text(_get_env_template())

    return dest_path


def list_bundle_contents(dest: str | Path | None = None) -> list[str]:
    """
    List the contents of the docker_sidecar bundle.

    Args:
        dest: Optional destination to check. If None, checks the source bundle.

    Returns:
        List of file paths relative to the bundle root.
    """
    if dest:
        bundle_path = Path(dest).expanduser().resolve()
    else:
        bundle_path = _find_sidecar_source()

    if not bundle_path.exists():
        return []

    contents = []
    for item in bundle_path.rglob("*"):
        if item.is_file():
            contents.append(str(item.relative_to(bundle_path)))

    return sorted(contents)


def _build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Export Codemode docker sidecar bundle.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export to ./sidecar directory
  python -m codemode.docker_assets export --dest ./sidecar

  # Overwrite existing files
  python -m codemode.docker_assets export --dest ./sidecar --force

  # List bundle contents
  python -m codemode.docker_assets list

After exporting, build the image:
  cd ./sidecar
  docker build -t codemode-executor .
  docker run -p 8001:8001 -e CODEMODE_API_KEY=secret codemode-executor
""",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    export_parser = sub.add_parser("export", help="Export docker_sidecar to a destination folder.")
    export_parser.add_argument("--dest", required=True, help="Destination directory")
    export_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite destination contents if they already exist.",
    )

    list_parser = sub.add_parser("list", help="List contents of the sidecar bundle.")
    list_parser.add_argument("--dest", help="Check exported bundle at this path instead of source.")

    return parser


def main(argv: list[str] | None = None) -> None:
    """CLI entry point for docker_assets module."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "export":
        try:
            dest = export_bundle(args.dest, overwrite=args.force)
            print(f"Exported docker sidecar to {dest}")
            print()
            print("Next steps:")
            print(f"  1. cd {dest}")
            print("  2. cp .env.template .env && edit .env")
            print("  3. docker-compose up -d")
            print()
            print("Or build manually:")
            print(f"  docker build -t codemode-executor {dest}")
        except FileExistsError as e:
            print(f"Error: {e}")
            raise SystemExit(1) from e
        except FileNotFoundError as e:
            print(f"Error: {e}")
            raise SystemExit(1) from e

    elif args.command == "list":
        try:
            contents = list_bundle_contents(args.dest)
            if contents:
                print("Bundle contents:")
                for item in contents:
                    print(f"  {item}")
            else:
                print("Bundle is empty or not found.")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            raise SystemExit(1) from e


if __name__ == "__main__":
    main()
