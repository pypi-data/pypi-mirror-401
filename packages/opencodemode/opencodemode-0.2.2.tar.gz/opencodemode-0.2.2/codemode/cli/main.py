"""Codemode command-line interface."""

import os

import click

from codemode import __version__


@click.group()
@click.version_option(version=__version__, prog_name="codemode")
@click.pass_context
def cli(ctx):
    """Codemode - Secure code execution for multi-agent AI systems."""
    ctx.ensure_object(dict)


@cli.command()
def version():
    """Show version information."""
    click.echo(f"codemode version {__version__}")


@cli.command()
@click.option("--config", "-c", default="codemode.yaml", help="Config file path")
def validate(config):
    """Validate configuration file."""
    from codemode.config.loader import ConfigLoader

    try:
        cfg = ConfigLoader.load(config)
        click.echo(f"✓ Configuration valid: {config}")
        click.echo(f"  Project: {cfg.project.name}")
        click.echo(f"  Framework: {cfg.framework.type}")
    except Exception as e:
        click.echo(f"✗ Configuration invalid: {e}", err=True)
        raise click.Abort() from e


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=8001, help="Port to bind to")
@click.option("--config", "-c", default="codemode.yaml", help="Config file path")
def serve(host, port, config):
    """Start the gRPC executor service (sidecar)."""
    import os

    from codemode.config.loader import ConfigLoader

    try:
        cfg = ConfigLoader.load(config)
        click.echo(f"Starting executor gRPC service on {host}:{port}")
        click.echo(f"Project: {cfg.project.name}")

        # Configure environment for executor service BEFORE importing
        # (the service module reads these at import time)
        os.environ["EXECUTOR_PORT"] = str(port)
        # Optional: allow users to set MAIN_APP_GRPC_TARGET via env or config.config
        maybe_target = cfg.config.get("tool_service_grpc") if hasattr(cfg, "config") else None
        if maybe_target:
            os.environ["MAIN_APP_GRPC_TARGET"] = str(maybe_target)

        # Import AFTER setting environment variables
        from codemode.executor import service as executor_service

        executor_service.main()
    except Exception as e:
        click.echo(f"✗ Failed to start service: {e}", err=True)
        raise click.Abort() from e


# =============================================================================
# Init Command Group
# =============================================================================

# Client configuration template
CLIENT_CONFIG_TEMPLATE = """# Codemode Client Configuration
# For applications connecting to the codemode executor sidecar
# Documentation: https://github.com/mldlwizard/codemode

# Executor connection settings
executor_url: ${CODEMODE_EXECUTOR_URL:-http://localhost:8001}
executor_api_key: ${CODEMODE_EXECUTOR_API_KEY}
executor_timeout: 35  # Request timeout in seconds (1-600)

# Code limits (validated before sending to executor)
max_code_length: 10000  # Maximum code length in characters

# Retry configuration for transient failures
retry:
  enabled: true
  max_attempts: 3
  backoff_base_ms: 100
  backoff_max_ms: 5000

# TLS configuration for secure connections
tls:
  enabled: false
  mode: system  # 'system' or 'custom'
  # ca_file: /path/to/ca.crt           # For custom CA verification
  # client_cert_file: /path/to/client.crt  # For mTLS
  # client_key_file: /path/to/client.key   # For mTLS

# Observability settings
observability:
  log_level: INFO
  include_correlation_id: true
  correlation_id_prefix: cm
  traceback_limit: 5
"""

# Sidecar configuration template
SIDECAR_CONFIG_TEMPLATE = """# Codemode Sidecar Configuration
# For the executor sidecar service running in Docker
# Documentation: https://github.com/mldlwizard/codemode

# Service binding
port: 8001
host: "0.0.0.0"
main_app_grpc_target: ${CODEMODE_MAIN_APP_TARGET:-localhost:50051}
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
  # cert_file: /path/to/server.crt
  # key_file: /path/to/server.key
  # ca_file: /path/to/ca.crt         # For client verification
  # require_client_auth: false       # Require mTLS

# TLS for callbacks to main app
callback_tls:
  enabled: false
  # ca_file: /path/to/ca.crt
  # client_cert: /path/to/client.crt  # For mTLS callbacks
  # client_key: /path/to/client.key

# Logging
log_level: INFO
"""


@cli.group(invoke_without_command=True)
@click.pass_context
def init(ctx):
    """Initialize codemode configuration files.

    Without a subcommand, creates both client and sidecar configs interactively.
    Use 'init client' or 'init sidecar' to create specific configs.

    Examples:
        codemode init           # Interactive: asks which to create
        codemode init client    # Create codemode-client.yaml
        codemode init sidecar   # Create codemode-sidecar.yaml
    """
    if ctx.invoked_subcommand is None:
        # Interactive mode - ask what to create
        click.echo("Codemode Configuration Setup")
        click.echo("=" * 40)
        click.echo("\nConfiguration types:")
        click.echo("  1. client  - For main applications connecting to executor")
        click.echo("  2. sidecar - For executor sidecar service")
        click.echo("  3. both    - Create both configuration files")
        click.echo("")

        choice = click.prompt(
            "Which configuration would you like to create?",
            type=click.Choice(["client", "sidecar", "both", "cancel"]),
            default="both",
        )

        if choice == "cancel":
            click.echo("Cancelled.")
            return

        if choice in ("client", "both"):
            _create_client_config()

        if choice in ("sidecar", "both"):
            _create_sidecar_config()

        _print_next_steps(choice)


@init.command("client")
@click.option("--force", "-f", is_flag=True, help="Overwrite existing config")
def init_client(force):
    """Create client configuration file (codemode-client.yaml).

    This configuration is for main applications that connect to the
    codemode executor sidecar.
    """
    _create_client_config(force=force)
    _print_next_steps("client")


@init.command("sidecar")
@click.option("--force", "-f", is_flag=True, help="Overwrite existing config")
def init_sidecar(force):
    """Create sidecar configuration file (codemode-sidecar.yaml).

    This configuration is for the executor sidecar service that runs
    code in isolation (typically in Docker).
    """
    _create_sidecar_config(force=force)
    _print_next_steps("sidecar")


def _create_client_config(force: bool = False) -> None:
    """Create the client configuration file."""
    config_file = "codemode-client.yaml"

    if os.path.exists(config_file) and not force:
        click.echo(f"  {config_file} already exists (use --force to overwrite)", err=True)
        return

    with open(config_file, "w") as f:
        f.write(CLIENT_CONFIG_TEMPLATE)

    click.echo(f"  Created {config_file}")


def _create_sidecar_config(force: bool = False) -> None:
    """Create the sidecar configuration file."""
    config_file = "codemode-sidecar.yaml"

    if os.path.exists(config_file) and not force:
        click.echo(f"  {config_file} already exists (use --force to overwrite)", err=True)
        return

    with open(config_file, "w") as f:
        f.write(SIDECAR_CONFIG_TEMPLATE)

    click.echo(f"  Created {config_file}")


def _print_next_steps(config_type: str) -> None:
    """Print next steps after creating configuration."""
    click.echo("\n" + "=" * 40)
    click.echo("Next steps:")

    if config_type in ("client", "both"):
        click.echo("\nFor client configuration:")
        click.echo("  1. Set required environment variables:")
        click.echo("     export CODEMODE_EXECUTOR_URL=http://executor:8001")
        click.echo("     export CODEMODE_EXECUTOR_API_KEY=your-secret-key")
        click.echo("\n  2. Or update codemode-client.yaml with your values")

    if config_type in ("sidecar", "both"):
        click.echo("\nFor sidecar configuration:")
        click.echo("  1. Set required environment variables:")
        click.echo("     export CODEMODE_API_KEY=your-secret-key")
        click.echo("     export CODEMODE_MAIN_APP_TARGET=your-app:50051")
        click.echo("\n  2. Build and run the executor:")
        click.echo("     codemode docker assets --dest ./sidecar")
        click.echo("     docker build -t codemode-executor ./sidecar")
        click.echo("     docker run -p 8001:8001 codemode-executor")

    click.echo("\nDocumentation:")
    click.echo("  https://github.com/mldlwizard/codemode")


# Legacy init command for backward compatibility
@cli.command("init-legacy")
@click.option("--force", "-f", is_flag=True, help="Overwrite existing config")
def init_legacy(force):
    """[Deprecated] Initialize a legacy codemode.yaml project file.

    This creates the old-style unified configuration file.
    For new projects, use 'codemode init' instead.
    """
    legacy_template = """# Codemode Configuration File (Legacy Format)
# NOTE: This format is deprecated. Use 'codemode init' for new projects.
# For full documentation: https://github.com/mldlwizard/codemode

project:
  name: my-project
  version: "1.0.0"

framework:
  type: crewai
  auto_discover: true

executor:
  # Executor service URL (use localhost for 'codemode docker start')
  url: http://localhost:8001
  api_key: ${CODEMODE_API_KEY:-dev-secret-key}
  timeout: 35
  limits:
    code_timeout: 30
    # Maximum code length in characters (100-100000)
    max_code_length: 10000
    # Container memory limit
    memory_limit: "512Mi"

  # Network configuration for code execution (not Docker networking)
  network:
    # Options: none (default, secure), restricted (allow-list), all (full network)
    mode: none
  execution:
    # Allow direct execution of system commands
    allow_direct_execution: false
    # allowed_commands:  # Uncomment to allow specific commands
    #   - grep
    #   - cat
    #   - ls
    #   - find
    #   - head
    #   - tail

  # Filesystem configuration (for Docker volumes)
  # filesystem:
  #   workspace:
  #     mount: ./project_files
  #     readonly: true
  #   sandbox:
  #     mount: /sandbox
  #     readonly: false
  #     max_size: 1GB
  #   outputs:
  #     mount: ./outputs
  #     readonly: false

# gRPC configuration
grpc:
  # ToolService URL - where executor connects to call tools
  # Use 'localhost:50051' for local dev, auto-converted to 'host.docker.internal:50051' for Docker
  tool_service_url: localhost:50051

  # TLS/mTLS configuration (uncomment for secure gRPC)
  # tls:
  #   enabled: true
  #   mode: custom  # Options: 'system' or 'custom'
  #   cert_file: ./certs/server.crt
  #   key_file: ./certs/server.key
  #   ca_file: ./certs/ca.crt
  #   # For mutual TLS (mTLS):
  #   # client_cert_file: ./certs/client.crt
  #   # client_key_file: ./certs/client.key

# Additional configuration
config:
  environment: development

# Logging configuration
logging:
  level: INFO
"""

    config_file = "codemode.yaml"
    if os.path.exists(config_file) and not force:
        click.echo(f"  {config_file} already exists (use --force to overwrite)", err=True)
        raise click.Abort()

    with open(config_file, "w") as f:
        f.write(legacy_template)

    click.echo(f"  Created {config_file}")
    click.echo("\nNote: This is the legacy configuration format.")
    click.echo("For new projects, we recommend using 'codemode init' instead.")


@cli.group()
def docker():
    """Docker management commands for executor containers."""
    pass


@docker.command("check")
def docker_check():
    """Check if Docker is available and get system information."""
    from codemode.docker import DockerManager

    manager = DockerManager()

    if manager.is_available():
        click.echo("✓ Docker is available and running")

        info = manager.get_docker_info()
        if "error" not in info:
            click.echo("\nDocker Information:")
            click.echo(f"  Version: {info.get('version', 'N/A')}")
            click.echo(f"  OS: {info.get('os', 'N/A')}")
        else:
            click.echo(f"✗ Error getting Docker info: {info['error']}", err=True)
    else:
        click.echo("✗ Docker is not available", err=True)
        click.echo("\nPlease ensure Docker is installed and running:")
        click.echo("  - Install Docker: https://docs.docker.com/get-docker/")
        click.echo("  - Start Docker daemon")
        raise click.Abort()


@docker.command("build")
@click.option(
    "--dockerfile",
    "-f",
    help="Path to Dockerfile (default: auto-detect)",
)
@click.option(
    "--image",
    "-i",
    default="codemode-executor:latest",
    help="Image name and tag (default: codemode-executor:latest)",
)
@click.option(
    "--version",
    "-v",
    "codemode_version",
    default="latest",
    help="Codemode version to install in the image (default: latest)",
)
def docker_build(dockerfile, image, codemode_version):
    """Build the executor Docker image from Dockerfile.

    The Dockerfile installs codemode from PyPI, so no source checkout is needed.
    If Dockerfile is not found, use 'codemode docker assets' to export it first.

    Examples:
        codemode docker build
        codemode docker build --version 0.2.0
        codemode docker build --dockerfile ./my-sidecar/Dockerfile
    """
    from codemode.docker import DockerManager

    manager = DockerManager()

    if not manager.is_available():
        click.echo("✗ Docker is not available", err=True)
        click.echo("\nPlease ensure Docker is installed and running:")
        click.echo("  - Install Docker: https://docs.docker.com/get-docker/")
        click.echo("  - Start Docker daemon")
        click.echo("\nRun 'codemode docker check' for more information")
        raise click.Abort()

    click.echo(f"Building executor image '{image}'...")
    if dockerfile:
        click.echo(f"Using Dockerfile: {dockerfile}")
    click.echo(f"Codemode version: {codemode_version}")
    click.echo()

    result = manager.build_executor_image(
        dockerfile_path=dockerfile, image_name=image, codemode_version=codemode_version
    )

    if result.get("success"):
        click.echo(f"✓ {result['message']}")
        click.echo()
        click.echo("You can now start the executor with:")
        click.echo("  codemode docker start")
        click.echo()
        click.echo("Or run directly:")
        click.echo(f"  docker run -p 8001:8001 -e CODEMODE_API_KEY=secret {image}")
    else:
        click.echo(f"✗ Build failed: {result.get('error', 'Unknown error')}", err=True)
        if result.get("suggestion"):
            click.echo()
            click.echo(result["suggestion"], err=True)
        raise click.Abort()


@docker.command("start")
@click.option(
    "--config",
    "-c",
    default=None,
    help="Config file path to mount (codemode-sidecar.yaml)",
)
@click.option("--requirements", "-r", help="Requirements.txt file for additional dependencies")
@click.option(
    "--packages",
    "-p",
    multiple=True,
    help="Additional packages to install (can be used multiple times)",
)
@click.option("--name", "-n", default="codemode-executor", help="Container name")
@click.option("--port", default=8001, help="Port to expose for executor service")
@click.option(
    "--image",
    "-i",
    default="codemode-executor:latest",
    help="Docker image to use (default: codemode-executor:latest)",
)
@click.option(
    "--api-key",
    envvar="CODEMODE_API_KEY",
    help="API key for authentication (or set CODEMODE_API_KEY env var)",
)
def docker_start(config, requirements, packages, name, port, image, api_key):
    """Start an executor container for code execution.

    Examples:
        # Basic start (requires image to be built first)
        codemode docker start

        # Start with custom port and API key
        codemode docker start --port 9001 --api-key my-secret

        # Start with config file
        codemode docker start --config ./codemode-sidecar.yaml
    """
    from codemode.docker import DockerManager

    manager = DockerManager()

    if not manager.is_available():
        click.echo("✗ Docker is not available", err=True)
        click.echo("\nPlease ensure Docker is installed and running:")
        click.echo("  - Install Docker: https://docs.docker.com/get-docker/")
        click.echo("  - Start Docker daemon")
        click.echo("\nRun 'codemode docker check' for more information")
        raise click.Abort()

    click.echo(f"Starting executor container '{name}'...")

    # Defaults (match config model defaults)
    network_mode = "none"
    tool_service_url = "host.docker.internal:50051"

    # Check if config file exists and load settings
    if config and os.path.exists(config):
        try:
            from codemode.config.loader import ConfigLoader

            cfg = ConfigLoader.load(config)
            network_mode = cfg.executor.network.mode
            # Auto-convert localhost to host.docker.internal for Docker
            url = getattr(cfg.grpc, "tool_service_url", "localhost:50051")
            if url.startswith("localhost"):
                tool_service_url = url.replace("localhost", "host.docker.internal")
            else:
                tool_service_url = url
            click.echo(f"  Config loaded: network.mode={network_mode}")
        except Exception as e:
            click.echo(f"  Warning: Could not load config: {e}")
    elif config:
        click.echo(f"✗ Config file '{config}' not found", err=True)
        click.echo()
        click.echo("To create a config file, run:")
        click.echo("  codemode init sidecar")
        click.echo()
        click.echo("Or specify a different config file:")
        click.echo("  codemode docker start --config /path/to/codemode-sidecar.yaml")
        click.echo()
        click.echo("To start without config file (using env vars only):")
        click.echo("  codemode docker start --api-key your-secret-key")
        raise click.Abort()

    # Build environment variables
    env_vars = {}
    if api_key:
        env_vars["CODEMODE_API_KEY"] = api_key

    result = manager.spin_up_executor(
        config_path=config,
        requirements_file=requirements,
        additional_packages=list(packages) if packages else None,
        container_name=name,
        port=port,
        image_name=image,
        env_vars=env_vars if env_vars else None,
        network_mode=network_mode,
        tool_service_url=tool_service_url,
    )

    if result.get("success"):
        click.echo("✓ Container started successfully")
        click.echo()
        click.echo("Container Information:")
        click.echo(f"  ID: {result['container_id'][:12]}")
        click.echo(f"  Name: {result['container_name']}")
        click.echo(f"  Port: {result['port']}")
        click.echo(f"  Status: {result['status']}")
        click.echo(f"  ToolService: {tool_service_url}")
        click.echo()
        click.echo(f"Executor URL: http://localhost:{result['port']}")
        click.echo()
        click.echo(f"To view logs:  docker logs -f {name}")
        click.echo(f"To stop:       codemode docker stop --name {name}")
    else:
        click.echo(f"✗ Failed to start container: {result.get('error', 'Unknown error')}", err=True)
        if result.get("suggestion"):
            click.echo()
            click.echo(result["suggestion"], err=True)
        raise click.Abort()


@docker.command("stop")
@click.option("--name", "-n", default="codemode-executor", help="Container name")
def docker_stop(name):
    """Stop a running executor container."""
    from codemode.docker import DockerManager

    manager = DockerManager()

    if not manager.is_available():
        click.echo("✗ Docker is not available", err=True)
        raise click.Abort()

    click.echo(f"Stopping container '{name}'...")

    result = manager.stop_executor(container_name=name)

    if result.get("success"):
        click.echo(f"✓ {result['message']}")
    else:
        click.echo(f"✗ Error: {result.get('error', 'Unknown error')}", err=True)
        raise click.Abort()


@docker.command("remove")
@click.option("--name", "-n", default="codemode-executor", help="Container name")
def docker_remove(name):
    """Remove an executor container."""
    from codemode.docker import DockerManager

    manager = DockerManager()

    if not manager.is_available():
        click.echo("✗ Docker is not available", err=True)
        raise click.Abort()

    click.echo(f"Removing container '{name}'...")

    result = manager.remove_executor(container_name=name)

    if result.get("success"):
        click.echo(f"✓ {result['message']}")
    else:
        click.echo(f"✗ Error: {result.get('error', 'Unknown error')}", err=True)
        raise click.Abort()


@docker.command("status")
@click.option("--name", "-n", default="codemode-executor", help="Container name")
def docker_status(name):
    """Get status of an executor container."""
    from codemode.docker import DockerManager

    manager = DockerManager()

    if not manager.is_available():
        click.echo("✗ Docker is not available", err=True)
        raise click.Abort()

    result = manager.get_container_status(container_name=name)

    if result.get("exists"):
        click.echo(f"Container '{name}' status:")
        click.echo(f"  Status: {result['status']}")
    elif "error" in result:
        click.echo(f"✗ Error: {result['error']}", err=True)
    else:
        click.echo(f"Container '{name}' does not exist")


@docker.command("assets")
@click.option("--dest", required=True, help="Destination directory for sidecar bundle")
@click.option(
    "--force", is_flag=True, default=False, help="Overwrite destination if it already exists"
)
def docker_assets(dest, force):
    """Export docker sidecar assets to a local folder.

    This exports all files needed to build and run the executor container:
      - Dockerfile (installs codemode from PyPI)
      - docker-compose.yml
      - README.md with usage instructions
      - Configuration templates

    Examples:
        codemode docker assets --dest ./sidecar
        codemode docker assets --dest ./sidecar --force

    After exporting, build and run:
        cd ./sidecar
        cp .env.template .env
        # Edit .env with your settings
        docker-compose up -d
    """
    from codemode.docker_assets import export_bundle

    try:
        target = export_bundle(dest, overwrite=force)
        click.echo(f"✓ Exported docker sidecar to {target}")
        click.echo()
        click.echo("Next steps:")
        click.echo(f"  1. cd {target}")
        click.echo("  2. cp .env.template .env && edit .env")
        click.echo("  3. docker-compose up -d")
        click.echo()
        click.echo("Or build manually:")
        click.echo(f"  docker build -t codemode-executor {target}")
        click.echo("  docker run -p 8001:8001 -e CODEMODE_API_KEY=secret codemode-executor")
    except FileExistsError as e:
        click.echo(f"✗ {e}", err=True)
        raise click.Abort() from e
    except FileNotFoundError as e:
        click.echo(f"✗ {e}", err=True)
        raise click.Abort() from e
    except Exception as e:
        click.echo(f"✗ Failed to export assets: {e}", err=True)
        raise click.Abort() from e


@docker.command("env")
@click.option("--config", "-c", default="codemode.yaml", help="Config file to read")
@click.option("--output", "-o", default=".env", help="Output .env file path")
def docker_env(config, output):
    """Generate .env file from codemode.yaml for Docker/docker-compose.

    This bridges the gap between codemode.yaml (main app config) and
    Docker environment variables (executor config).

    Example:
        codemode docker env --config codemode.yaml --output .env
        docker-compose --env-file .env up -d
    """
    if not os.path.exists(config):
        click.echo(f"✗ Config file '{config}' not found", err=True)
        raise click.Abort()

    try:
        from codemode.config.loader import ConfigLoader

        cfg = ConfigLoader.load(config)

        # Build env vars from config
        env_lines = [
            "# Generated by: codemode docker env",
            f"# Source: {config}",
            "",
            "# Required",
            f"CODEMODE_API_KEY={cfg.executor.api_key}",
            "",
            "# ToolService URL (auto-converted for Docker)",
        ]

        # Convert localhost to host.docker.internal for Docker
        tool_url = getattr(cfg.grpc, "tool_service_url", "localhost:50051")
        if tool_url.startswith("localhost"):
            tool_url = tool_url.replace("localhost", "host.docker.internal")
        env_lines.append(f"MAIN_APP_GRPC_TARGET={tool_url}")

        env_lines.extend(
            [
                "",
                "# Network mode for code execution",
                f"EXECUTOR_NETWORK_MODE={cfg.executor.network.mode}",
                "",
                "# Optional",
                f"EXECUTOR_PORT={8001}",
                "LOG_LEVEL=INFO",
            ]
        )

        # Add TLS config if enabled
        if cfg.grpc.tls.enabled:
            env_lines.extend(
                [
                    "",
                    "# TLS Configuration",
                    f"CODEMODE_GRPC_TLS_ENABLED={str(cfg.grpc.tls.enabled).lower()}",
                    f"CODEMODE_GRPC_TLS_MODE={cfg.grpc.tls.mode}",
                ]
            )
            if cfg.grpc.tls.cert_file:
                env_lines.append(f"CODEMODE_GRPC_TLS_CERT_FILE={cfg.grpc.tls.cert_file}")
            if cfg.grpc.tls.key_file:
                env_lines.append(f"CODEMODE_GRPC_TLS_KEY_FILE={cfg.grpc.tls.key_file}")
            if cfg.grpc.tls.ca_file:
                env_lines.append(f"CODEMODE_GRPC_TLS_CA_FILE={cfg.grpc.tls.ca_file}")

        # Write .env file
        env_content = "\n".join(env_lines) + "\n"
        with open(output, "w") as f:
            f.write(env_content)

        click.echo(f"✓ Generated {output} from {config}")
        click.echo("\nUsage:")
        click.echo(f"  docker-compose --env-file {output} up -d")

    except Exception as e:
        click.echo(f"✗ Failed to generate env file: {e}", err=True)
        raise click.Abort() from e


@cli.group()
def tls():
    """TLS/mTLS certificate management commands."""
    pass


@tls.command("generate-certs")
@click.option(
    "--output",
    "-o",
    default="./test_certs",
    help="Output directory for certificates (default: ./test_certs)",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=False,
    help="Overwrite existing certificates",
)
def tls_generate_certs(output, force):
    """Generate self-signed certificates for TLS testing and development.

    This command generates a complete certificate chain for testing:
    - Certificate Authority (CA)
    - Server certificate (with localhost, executor, host.docker.internal SANs)
    - Client certificate (for mTLS)

    Note: These certificates are for DEVELOPMENT/TESTING only.
    For production, use certificates from a trusted CA.
    """
    import subprocess
    from pathlib import Path

    output_path = Path(output)

    # Check if directory exists and has certificates
    if output_path.exists() and not force:
        existing_files = list(output_path.glob("*.crt")) + list(output_path.glob("*.key"))
        if existing_files:
            click.echo(f"✗ Certificates already exist in {output}", err=True)
            click.echo("\nUse --force to overwrite existing certificates:")
            click.echo(f"  codemode tls generate-certs --output {output} --force")
            raise click.Abort()

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    click.echo(f"🔐 Generating TLS certificates in {output}")
    click.echo("")

    try:
        # Generate CA
        click.echo("📝 Generating Certificate Authority (CA)...")
        subprocess.run(
            [
                "openssl",
                "req",
                "-x509",
                "-newkey",
                "rsa:4096",
                "-days",
                "365",
                "-nodes",
                "-keyout",
                str(output_path / "ca.key"),
                "-out",
                str(output_path / "ca.crt"),
                "-subj",
                "/CN=Codemode Test CA/O=Codemode",
            ],
            check=True,
            capture_output=True,
        )
        click.echo(f"   ✓ CA certificate: {output_path / 'ca.crt'}")
        click.echo(f"   ✓ CA key: {output_path / 'ca.key'}")
        click.echo("")

        # Generate server certificate
        click.echo("📝 Generating server certificate...")
        subprocess.run(
            [
                "openssl",
                "req",
                "-newkey",
                "rsa:4096",
                "-nodes",
                "-keyout",
                str(output_path / "server.key"),
                "-out",
                str(output_path / "server.csr"),
                "-subj",
                "/CN=localhost/O=Codemode",
            ],
            check=True,
            capture_output=True,
        )

        # Create temp file for SAN extension
        san_ext = "subjectAltName=DNS:localhost,DNS:executor,DNS:host.docker.internal,IP:127.0.0.1"
        subprocess.run(
            [
                "openssl",
                "x509",
                "-req",
                "-in",
                str(output_path / "server.csr"),
                "-CA",
                str(output_path / "ca.crt"),
                "-CAkey",
                str(output_path / "ca.key"),
                "-CAcreateserial",
                "-out",
                str(output_path / "server.crt"),
                "-days",
                "365",
                "-extfile",
                "/dev/stdin",
            ],
            input=san_ext.encode(),
            check=True,
            capture_output=True,
        )
        (output_path / "server.csr").unlink()
        click.echo(f"   ✓ Server certificate: {output_path / 'server.crt'}")
        click.echo(f"   ✓ Server key: {output_path / 'server.key'}")
        click.echo("")

        # Generate client certificate
        click.echo("📝 Generating client certificate for mTLS...")
        subprocess.run(
            [
                "openssl",
                "req",
                "-newkey",
                "rsa:4096",
                "-nodes",
                "-keyout",
                str(output_path / "client.key"),
                "-out",
                str(output_path / "client.csr"),
                "-subj",
                "/CN=client/O=Codemode",
            ],
            check=True,
            capture_output=True,
        )

        subprocess.run(
            [
                "openssl",
                "x509",
                "-req",
                "-in",
                str(output_path / "client.csr"),
                "-CA",
                str(output_path / "ca.crt"),
                "-CAkey",
                str(output_path / "ca.key"),
                "-CAcreateserial",
                "-out",
                str(output_path / "client.crt"),
                "-days",
                "365",
            ],
            check=True,
            capture_output=True,
        )
        (output_path / "client.csr").unlink()
        click.echo(f"   ✓ Client certificate: {output_path / 'client.crt'}")
        click.echo(f"   ✓ Client key: {output_path / 'client.key'}")
        click.echo("")

        # Set permissions
        import os

        for key_file in output_path.glob("*.key"):
            os.chmod(key_file, 0o600)
        for crt_file in output_path.glob("*.crt"):
            os.chmod(crt_file, 0o644)

        click.echo("✅ Test certificates generated successfully!")
        click.echo("")
        click.echo("🔧 To use these certificates:")
        click.echo("")
        click.echo("1. Update your codemode.yaml:")
        click.echo("   grpc:")
        click.echo("     tls:")
        click.echo("       enabled: true")
        click.echo("       mode: custom")
        click.echo(f"       cert_file: {output}/server.crt")
        click.echo(f"       key_file: {output}/server.key")
        click.echo(f"       ca_file: {output}/ca.crt")
        click.echo("")
        click.echo("2. For mTLS (mutual authentication), also add:")
        click.echo(f"       client_cert_file: {output}/client.crt")
        click.echo(f"       client_key_file: {output}/client.key")
        click.echo("")
        click.echo("3. Or use environment variables:")
        click.echo("   export CODEMODE_GRPC_TLS_ENABLED=true")
        click.echo("   export CODEMODE_GRPC_TLS_MODE=custom")
        click.echo(f"   export CODEMODE_GRPC_TLS_CERT_FILE={output}/server.crt")
        click.echo(f"   export CODEMODE_GRPC_TLS_KEY_FILE={output}/server.key")
        click.echo(f"   export CODEMODE_GRPC_TLS_CA_FILE={output}/ca.crt")
        click.echo("")
        click.echo("⚠️  Note: These are self-signed certificates for TESTING only.")
        click.echo("   For production, obtain certificates from a trusted CA.")
        click.echo("")
        click.echo("📖 Documentation: docs/features/tls-encryption.md")

    except subprocess.CalledProcessError as e:
        click.echo(f"✗ Failed to generate certificates: {e}", err=True)
        if e.stderr:
            click.echo(f"\nError output: {e.stderr.decode()}", err=True)
        raise click.Abort() from e
    except FileNotFoundError as e:
        click.echo("✗ OpenSSL not found", err=True)
        click.echo("\nPlease install OpenSSL:")
        click.echo("  macOS:   brew install openssl")
        click.echo("  Ubuntu:  sudo apt-get install openssl")
        click.echo("  Windows: https://slproweb.com/products/Win32OpenSSL.html")
        raise click.Abort() from e


if __name__ == "__main__":
    cli()
