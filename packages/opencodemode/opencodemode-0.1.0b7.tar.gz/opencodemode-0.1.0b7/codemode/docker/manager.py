"""
Docker manager for Codemode executor containers.

This module provides utilities to check Docker availability and manage
executor containers for secure code execution.
"""

from __future__ import annotations

import logging
import os
import subprocess
from typing import Any

logger = logging.getLogger(__name__)


class DockerNotAvailableError(Exception):
    """Raised when Docker is not available or not running."""

    pass


class DockerBuildError(Exception):
    """Raised when Docker image build fails."""

    pass


class DockerManager:
    """
    Manages Docker containers for Codemode execution.

    This class provides methods to check Docker availability, spin up executor
    containers, and manage container lifecycle.

    Example:
        >>> manager = DockerManager()
        >>> if manager.is_available():
        ...     result = manager.build_executor_image()
        ...     if result.get("success"):
        ...         print("Image built successfully!")
    """

    DEFAULT_EXECUTOR_IMAGE = "codemode-executor:latest"
    DEFAULT_CONTAINER_NAME = "codemode-executor"
    DEFAULT_REQUIREMENTS = ["fastapi", "uvicorn", "pydantic", "pyyaml"]

    def __init__(self) -> None:
        """Initialize the Docker manager."""
        self.docker_available = False
        self._check_docker()

    def _check_docker(self) -> None:
        """Check if Docker is available and running."""
        try:
            result = subprocess.run(
                ["docker", "version"], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                self.docker_available = True
                logger.info("Docker is available and running")
            else:
                logger.warning("Docker command exists but returned error")
        except FileNotFoundError:
            logger.error("Docker is not installed")
        except subprocess.TimeoutExpired:
            logger.error("Docker command timed out")
        except Exception as e:
            logger.error(f"Error checking Docker: {e}")

    def is_available(self) -> bool:
        """
        Check if Docker is available.

        Returns:
            True if Docker is available, False otherwise.

        Example:
            >>> manager = DockerManager()
            >>> if manager.is_available():
            ...     print("Docker is ready!")
        """
        return self.docker_available

    def get_docker_info(self) -> dict[str, Any]:
        """
        Get Docker version and system information.

        Returns:
            Docker information including version, OS, and availability status.

        Example:
            >>> manager = DockerManager()
            >>> info = manager.get_docker_info()
            >>> print(f"Docker version: {info.get('version', 'N/A')}")
        """
        if not self.docker_available:
            return {"error": "Docker is not available"}

        try:
            # Get Docker version
            version_result = subprocess.run(
                ["docker", "version", "--format", "{{.Server.Version}}"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            # Get Docker system info
            info_result = subprocess.run(
                ["docker", "info", "--format", "{{.OperatingSystem}}"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            return {
                "version": (
                    version_result.stdout.strip() if version_result.returncode == 0 else "Unknown"
                ),
                "os": info_result.stdout.strip() if info_result.returncode == 0 else "Unknown",
                "available": True,
            }
        except Exception as e:
            logger.error(f"Error getting Docker info: {e}")
            return {"error": str(e)}

    def check_container_exists(self, container_name: str) -> bool:
        """
        Check if a container exists (running or stopped).

        Args:
            container_name: Name of the container to check.

        Returns:
            True if container exists, False otherwise.
        """
        if not self.docker_available:
            return False

        try:
            result = subprocess.run(
                [
                    "docker",
                    "ps",
                    "-a",
                    "--filter",
                    f"name={container_name}",
                    "--format",
                    "{{.Names}}",
                ],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return container_name in result.stdout.strip()
        except Exception as e:
            logger.error(f"Error checking container: {e}")
            return False

    def check_image_exists(self, image_name: str) -> bool:
        """
        Check if a Docker image exists locally.

        Args:
            image_name: Name of the image to check (e.g., "codemode-executor:latest").

        Returns:
            True if image exists, False otherwise.
        """
        if not self.docker_available:
            return False

        try:
            result = subprocess.run(
                ["docker", "images", "-q", image_name],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return bool(result.stdout.strip())
        except Exception as e:
            logger.error(f"Error checking image: {e}")
            return False

    def _find_dockerfile(self, dockerfile_path: str | None = None) -> str | None:
        """
        Find the Dockerfile in common locations.

        Args:
            dockerfile_path: Explicit path to Dockerfile, or None to auto-detect.

        Returns:
            Path to Dockerfile if found, None otherwise.
        """
        if dockerfile_path and os.path.exists(dockerfile_path):
            return dockerfile_path

        # Try common locations
        possible_paths = [
            "docker_sidecar/Dockerfile",  # Repo layout
            "Dockerfile",  # Current directory (exported bundle)
            "executor-sidecar/Dockerfile",  # Common export destination
            "sidecar/Dockerfile",  # Another common name
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path

        return None

    def _get_build_context(self, dockerfile_path: str) -> str:
        """
        Determine the appropriate build context for a Dockerfile.

        For the new PyPI-based Dockerfile, the build context is the directory
        containing the Dockerfile (not the repo root).

        Args:
            dockerfile_path: Path to the Dockerfile.

        Returns:
            Path to the build context directory.
        """
        dockerfile_abs = os.path.abspath(dockerfile_path)
        dockerfile_dir = os.path.dirname(dockerfile_abs)

        # For the new Dockerfile that installs from PyPI, the context is just
        # the directory containing the Dockerfile
        return dockerfile_dir

    def build_executor_image(
        self,
        dockerfile_path: str | None = None,
        image_name: str | None = None,
        codemode_version: str = "latest",
    ) -> dict[str, Any]:
        """
        Build the executor Docker image from Dockerfile.

        The Dockerfile installs codemode from PyPI, so no source checkout is needed.
        Just ensure the Dockerfile is present (via `codemode docker assets`).

        Args:
            dockerfile_path: Path to Dockerfile. If None, auto-detects from common locations.
            image_name: Name and tag for the image (default: codemode-executor:latest).
            codemode_version: Version of codemode to install (default: latest).

        Returns:
            Dict with build result. Contains 'success' and 'image_name' on success,
            or 'error' and optionally 'suggestion' on failure.

        Example:
            >>> manager = DockerManager()
            >>> result = manager.build_executor_image()
            >>> if result.get("success"):
            ...     print(f"Image built: {result['image_name']}")
        """
        if not self.docker_available:
            return {"error": "Docker is not available"}

        image_name = image_name or self.DEFAULT_EXECUTOR_IMAGE

        # Find Dockerfile
        dockerfile = self._find_dockerfile(dockerfile_path)

        if not dockerfile:
            return {
                "error": "Dockerfile not found",
                "suggestion": (
                    "To build the executor image:\n"
                    "  1. Export assets:  codemode docker assets --dest ./sidecar\n"
                    "  2. Build image:    docker build -t codemode-executor ./sidecar\n"
                    "\n"
                    "Or specify Dockerfile path:\n"
                    "  codemode docker build --dockerfile /path/to/Dockerfile"
                ),
            }

        # Get build context
        build_context = self._get_build_context(dockerfile)

        # Validate build context exists
        if not os.path.isdir(build_context):
            return {
                "error": f"Build context directory not found: {build_context}",
                "suggestion": "Ensure the Dockerfile directory exists and is accessible.",
            }

        try:
            dockerfile_abs = os.path.abspath(dockerfile)
            logger.info(f"Building image {image_name} from {dockerfile}")
            logger.info(f"Build context: {build_context}")
            logger.info(f"Codemode version: {codemode_version}")

            # Build command with version arg
            build_cmd = [
                "docker",
                "build",
                "-f",
                dockerfile_abs,
                "-t",
                image_name,
                "--build-arg",
                f"CODEMODE_VERSION={codemode_version}",
                build_context,
            ]

            result = subprocess.run(
                build_cmd,
                capture_output=True,
                text=True,
                timeout=600,  # 10 minutes for build (includes pip install)
            )

            if result.returncode == 0:
                logger.info(f"Image built successfully: {image_name}")
                return {
                    "success": True,
                    "image_name": image_name,
                    "message": f"Image '{image_name}' built successfully",
                    "version": codemode_version,
                }
            else:
                error_msg = result.stderr.strip()
                logger.error(f"Failed to build image: {error_msg}")

                # Provide helpful suggestions based on error
                suggestion = None
                if "Cannot connect to the Docker daemon" in error_msg:
                    suggestion = "Ensure Docker daemon is running: docker info"
                elif "permission denied" in error_msg.lower():
                    suggestion = (
                        "Permission denied. Try:\n"
                        "  - Running with sudo\n"
                        "  - Adding user to docker group: sudo usermod -aG docker $USER"
                    )
                elif "network" in error_msg.lower():
                    suggestion = (
                        "Network error during build. Check:\n"
                        "  - Internet connectivity\n"
                        "  - Docker network settings\n"
                        "  - Firewall/proxy configuration"
                    )

                result_dict: dict[str, Any] = {"error": error_msg}
                if suggestion:
                    result_dict["suggestion"] = suggestion
                return result_dict

        except subprocess.TimeoutExpired:
            return {
                "error": "Image build timed out (exceeded 10 minutes)",
                "suggestion": (
                    "Build is taking too long. This may indicate:\n"
                    "  - Slow network connection\n"
                    "  - Large dependencies being installed\n"
                    "Try building manually: docker build -t codemode-executor ."
                ),
            }
        except Exception as e:
            logger.error(f"Error building image: {e}")
            return {"error": str(e)}

    def spin_up_executor(
        self,
        config_path: str | None = None,
        requirements_file: str | None = None,
        additional_packages: list[str] | None = None,
        container_name: str | None = None,
        port: int = 8001,
        env_vars: dict[str, str] | None = None,
        image_name: str | None = None,
        network_mode: str = "none",
        tool_service_url: str = "host.docker.internal:50051",
    ) -> dict[str, Any]:
        """
        Spin up a new executor container.

        Args:
            config_path: Path to codemode-sidecar.yaml config file (will be mounted).
            requirements_file: Path to requirements.txt for additional dependencies (legacy).
            additional_packages: List of additional pip packages to install (legacy).
            container_name: Name for the container (default: codemode-executor).
            port: Port to expose for the executor service (default: 8001).
            env_vars: Environment variables to set in the container.
            image_name: Docker image to use (default: codemode-executor:latest).
            network_mode: Code execution network mode from config (none/restricted/all).
            tool_service_url: ToolService gRPC URL for the executor to connect to.

        Returns:
            Dict with container information including ID, name, port, and status.

        Example:
            >>> manager = DockerManager()
            >>> result = manager.spin_up_executor(port=8001)
            >>> if result.get("success"):
            ...     print(f"Container ID: {result['container_id']}")
        """
        if not self.docker_available:
            return {"error": "Docker is not available"}

        container_name = container_name or self.DEFAULT_CONTAINER_NAME
        image_name = image_name or self.DEFAULT_EXECUTOR_IMAGE

        # Check if container already exists
        if self.check_container_exists(container_name):
            return {
                "error": f"Container '{container_name}' already exists",
                "suggestion": (
                    f"Stop and remove the existing container first:\n"
                    f"  docker stop {container_name}\n"
                    f"  docker rm {container_name}\n"
                    f"\n"
                    f"Or use a different name:\n"
                    f"  codemode docker start --name my-executor"
                ),
            }

        # Check if image exists
        if not self.check_image_exists(image_name):
            return {
                "error": f"Image '{image_name}' not found",
                "suggestion": (
                    "Build the image first:\n"
                    "  1. Export assets:  codemode docker assets --dest ./sidecar\n"
                    "  2. Build image:    docker build -t codemode-executor ./sidecar\n"
                    "\n"
                    "Or use docker-compose:\n"
                    "  cd ./sidecar && docker-compose up -d"
                ),
            }

        # Build docker run command
        # Note: Always use bridge network for port mapping and gRPC communication.
        # Network restrictions (none/restricted/all) are enforced at the executor level.
        docker_cmd = [
            "docker",
            "run",
            "-d",  # Detached mode
            "--name",
            container_name,
            "--add-host=host.docker.internal:host-gateway",  # Enable host access
            "-p",
            f"{port}:8001",
            # Using default bridge network (not --network none) for port mapping
        ]

        # Build environment variables - always include essential ones
        docker_env = {
            "CODEMODE_API_KEY": os.getenv("CODEMODE_API_KEY", ""),
            "MAIN_APP_GRPC_TARGET": tool_service_url,
            "EXECUTOR_NETWORK_MODE": network_mode,
        }
        if env_vars:
            docker_env.update(env_vars)

        for key, value in docker_env.items():
            docker_cmd.extend(["-e", f"{key}={value}"])

        # Mount config file if provided
        if config_path:
            config_path_abs = os.path.abspath(config_path)
            if os.path.exists(config_path_abs):
                # Mount as codemode-sidecar.yaml for the new config format
                docker_cmd.extend(["-v", f"{config_path_abs}:/app/codemode-sidecar.yaml:ro"])
            else:
                logger.warning(f"Config file not found: {config_path}")

        # Set resource limits and security options
        docker_cmd.extend(
            [
                "--memory",
                "512m",
                "--cpus",
                "1.0",
                "--cap-drop",
                "ALL",  # Drop all capabilities for security
                "--security-opt",
                "no-new-privileges:true",
                "--tmpfs",
                "/tmp:rw,noexec,nosuid,size=100m",  # Writable tmp directory
            ]
        )

        # Specify image
        docker_cmd.append(image_name)

        try:
            logger.info(f"Starting executor container: {container_name}")
            result = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                container_id = result.stdout.strip()
                logger.info(f"Container started successfully: {container_id[:12]}")
                return {
                    "success": True,
                    "container_id": container_id,
                    "container_name": container_name,
                    "port": port,
                    "status": "running",
                }
            else:
                error_msg = result.stderr.strip()
                logger.error(f"Failed to start container: {error_msg}")
                return {"error": error_msg}

        except subprocess.TimeoutExpired:
            return {"error": "Container startup timed out"}
        except Exception as e:
            logger.error(f"Error starting container: {e}")
            return {"error": str(e)}

    def stop_executor(self, container_name: str | None = None) -> dict[str, Any]:
        """
        Stop a running executor container.

        Args:
            container_name: Name of the container to stop.

        Returns:
            Dict with status information.
        """
        if not self.docker_available:
            return {"error": "Docker is not available"}

        container_name = container_name or self.DEFAULT_CONTAINER_NAME

        try:
            result = subprocess.run(
                ["docker", "stop", container_name], capture_output=True, text=True, timeout=30
            )

            if result.returncode == 0:
                return {"success": True, "message": f"Container '{container_name}' stopped"}
            else:
                return {"error": result.stderr.strip()}

        except Exception as e:
            logger.error(f"Error stopping container: {e}")
            return {"error": str(e)}

    def remove_executor(self, container_name: str | None = None) -> dict[str, Any]:
        """
        Remove an executor container.

        Args:
            container_name: Name of the container to remove.

        Returns:
            Dict with status information.
        """
        if not self.docker_available:
            return {"error": "Docker is not available"}

        container_name = container_name or self.DEFAULT_CONTAINER_NAME

        try:
            result = subprocess.run(
                ["docker", "rm", "-f", container_name], capture_output=True, text=True, timeout=30
            )

            if result.returncode == 0:
                return {"success": True, "message": f"Container '{container_name}' removed"}
            else:
                return {"error": result.stderr.strip()}

        except Exception as e:
            logger.error(f"Error removing container: {e}")
            return {"error": str(e)}

    def get_container_status(self, container_name: str | None = None) -> dict[str, Any]:
        """
        Get the status of an executor container.

        Args:
            container_name: Name of the container.

        Returns:
            Dict with container status information.
        """
        if not self.docker_available:
            return {"error": "Docker is not available"}

        container_name = container_name or self.DEFAULT_CONTAINER_NAME

        try:
            result = subprocess.run(
                [
                    "docker",
                    "ps",
                    "-a",
                    "--filter",
                    f"name={container_name}",
                    "--format",
                    "{{.Status}}",
                ],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                status = result.stdout.strip()
                if status:
                    return {"container_name": container_name, "status": status, "exists": True}
                else:
                    return {"container_name": container_name, "exists": False}
            else:
                return {"error": result.stderr.strip()}

        except Exception as e:
            logger.error(f"Error getting container status: {e}")
            return {"error": str(e)}
