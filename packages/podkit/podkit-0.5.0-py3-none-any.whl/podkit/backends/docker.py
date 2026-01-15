"""Docker implementation of the backend interface."""

import logging
import os
import signal
import time
import traceback
from collections.abc import Callable
from multiprocessing import Process, Queue
from pathlib import Path
from typing import Any

import docker
from docker.errors import DockerException, ImageNotFound, NotFound

from podkit.backends.base import BackendInterface
from podkit.constants import DOCKER_CPU_QUOTA_MULTIPLIER, DOCKER_STOP_TIMEOUT
from podkit.core.models import ContainerConfig, ContainerStatus, ProcessResult, StartupVerificationConfig
from podkit.utils.network import get_parent_container_networks


def _run_docker_exec_in_process(container_id, exec_kwargs, result_queue):
    """Helper function to run docker exec in separate process.

    Must be at module level for multiprocessing pickling.

    Args:
        container_id: Container ID to execute command in
        exec_kwargs: Arguments for container.exec_run()
        result_queue: Queue to put result into
    """
    try:
        client = docker.from_env()
        container = client.containers.get(container_id)
        exec_result = container.exec_run(**exec_kwargs)

        result_queue.put(
            {
                "exit_code": exec_result.exit_code,
                "output": exec_result.output,
                "error": None,
            }
        )
    except Exception as e:
        result_queue.put(
            {
                "exit_code": 1,
                "output": b"",
                "error": str(e),
                "error_type": type(e).__name__,
                "traceback": traceback.format_exc(),
            }
        )


class DockerBackend(BackendInterface):
    """Docker implementation of the backend interface."""

    def __init__(self, logger: logging.Logger | None = None):
        """Initialize Docker backend.

        Args:
            logger: Optional logger instance. If None, creates a default logger.
        """
        self.client = None
        self.logger = logger or logging.getLogger("podkit.docker")

    def connect(self) -> None:
        """Initialize Docker client and verify connection."""
        try:
            self.client = docker.from_env()
            self.client.ping()
        except DockerException as e:
            raise RuntimeError(
                f"Docker is not running or not accessible: {e}.\n"
                "Tips: 1) Check that docker is running\n"
                "2) Check if '/var/run/docker.sock' socket is available"
            ) from e

    def _ensure_image_available(self, image_name: str) -> None:
        """Ensure Docker image is available locally, pull if necessary.

        Args:
            image_name: Name of the Docker image.

        Raises:
            RuntimeError: If image cannot be pulled.
        """
        try:
            self.client.images.get(image_name)
            self.logger.debug(f"Image {image_name} found locally")
        except ImageNotFound:
            self.logger.warning(f"Image {image_name} not found locally, pulling...")
            try:
                self.client.images.pull(image_name)
                self.logger.info(f"Successfully pulled image: {image_name}")
            except DockerException as e:
                raise RuntimeError(
                    f"Image '{image_name}' not found locally and failed to pull: {e}\n"
                    f"Please pull it manually: docker pull {image_name}"
                ) from e

    def create_workload(
        self,
        name: str,
        config: ContainerConfig,
        mounts: list[dict[str, Any]],
        **kwargs,
    ) -> str:
        """
        Create a Docker container.

        Args:
            name: Container name.
            config: Container configuration.
            mounts: Volume mount specifications.
            **kwargs: Additional Docker-specific options (can include 'labels').

        Returns:
            Container ID.

        Raises:
            RuntimeError: If container creation fails.
        """
        try:
            self._ensure_image_available(config.image)

            port_bindings = {}
            for port in config.ports:
                port_bindings[f"{port}/tcp"] = ("0.0.0.0", port)

            networks_to_use = config.networks
            if config.inherit_parent_networks and not networks_to_use:
                networks_to_use = get_parent_container_networks()

            create_params = {
                "image": config.image,
                "name": name,
                "detach": True,
                "mounts": mounts,
                "environment": config.environment,
                "working_dir": config.working_dir,
                "cpu_quota": int(config.cpu_limit * DOCKER_CPU_QUOTA_MULTIPLIER),
                "mem_limit": config.memory_limit,
                "user": config.user,
                "tty": config.tty,
                "stdin_open": config.stdin_open,
                "ports": port_bindings,
                **kwargs,
            }

            # Set primary network (Docker limitation: only one network during create)
            if networks_to_use:
                create_params["network"] = networks_to_use[0]
                self.logger.info(f"Creating container {name} on network: {networks_to_use[0]}")

            # Handle command with priority: config.command > kwargs["command"] > auto-generated
            # Note: kwargs already spread into create_params above via **kwargs
            if config.command is not None:
                # Explicit command in config takes highest priority
                create_params["command"] = config.command
            elif "command" not in create_params:
                # No command specified - auto-generate based on entrypoint
                if config.entrypoint is not None:
                    # Explicit entrypoint set
                    if config.entrypoint == []:
                        # Empty entrypoint - use sleep infinity to keep container alive
                        create_params["command"] = ["sleep", "infinity"]
                    # else: non-empty entrypoint - don't set command (use image's default)
                else:
                    # No entrypoint specified - use sleep with timeout for auto-shutdown
                    lifetime_seconds = config.container_lifetime_seconds
                    create_params["command"] = ["sleep", str(lifetime_seconds)]
            # else: command already in create_params from kwargs

            # Set entrypoint if specified (after command logic)
            if config.entrypoint is not None:
                create_params["entrypoint"] = config.entrypoint

            container = self.client.containers.create(**create_params)

            # Attach additional networks (Docker limitation: only one during create)
            if len(networks_to_use) > 1:
                for network_name in networks_to_use[1:]:
                    try:
                        network = self.client.networks.get(network_name)
                        network.connect(container)
                        self.logger.info(f"Connected container {name} to network: {network_name}")
                    except Exception as e:
                        self.logger.warning(f"Failed to connect to network {network_name}: {e}")

            return container.id
        except DockerException as e:
            raise RuntimeError(f"Failed to create container: {e}") from e

    def start_workload(self, workload_id: str, verification_config: StartupVerificationConfig | None = None) -> None:
        """
        Start a Docker container (or unpause if paused).

        Automatically detects if container is paused and unpauses instead.
        Optionally verifies startup with consecutive running checks.

        Args:
            workload_id: Container ID.
            verification_config: Optional verification to ensure sustained running state.

        Raises:
            RuntimeError: If container start or verification fails.
        """
        try:
            container = self.client.containers.get(workload_id)

            # Check current state and take appropriate action
            if container.status == "paused":
                self.logger.info(f"Container {workload_id[:12]} is paused, unpausing...")
                container.unpause()
            elif container.status in ("created", "exited"):
                self.logger.info(f"Container {workload_id[:12]} is {container.status}, starting...")
                container.start()
            elif container.status == "running":
                self.logger.debug(f"Container {workload_id[:12]} already running")
            else:
                # restarting, removing, dead - try start anyway
                self.logger.warning(
                    f"Container {workload_id[:12]} in unexpected state {container.status}, attempting start..."
                )
                container.start()

            # Optional verification with consecutive checks
            if verification_config:
                self._verify_workload_startup(workload_id, verification_config)

        except DockerException as e:
            raise RuntimeError(f"Failed to start container: {e}") from e

    def _verify_workload_startup(self, workload_id: str, verification_config: StartupVerificationConfig) -> None:
        """Verify container reaches and maintains running state.

        Polls status with consecutive checks to avoid race conditions.

        Args:
            workload_id: Container ID.
            verification_config: Verification settings.

        Raises:
            RuntimeError: If container fails to start or exits immediately.
        """
        required_checks = verification_config.required_consecutive_checks
        check_interval = verification_config.check_interval_seconds
        max_wait = verification_config.max_wait_seconds
        max_checks = int(max_wait / check_interval)

        consecutive_running = 0

        for i in range(max_checks):
            time.sleep(check_interval)

            status = self.get_workload_status(workload_id)

            if status == ContainerStatus.RUNNING:
                consecutive_running += 1
                self.logger.debug(
                    f"Container {workload_id[:12]} running "
                    f"(check {i + 1}/{max_checks}, consecutive: {consecutive_running}/{required_checks})"
                )

                if consecutive_running >= required_checks:
                    self.logger.info(
                        f"Container {workload_id[:12]} verified running after {required_checks} consecutive checks"
                    )
                    return  # Success!
            else:
                consecutive_running = 0  # Reset if not running

            # Failed state
            if status in (
                ContainerStatus.EXITED,
                ContainerStatus.ERROR,
                ContainerStatus.DEAD,
                ContainerStatus.REMOVING,
            ):
                error_parts = [f"Container {workload_id[:12]} failed to start (status: {status.value})."]

                if verification_config.capture_logs_on_failure:
                    logs = self.get_workload_logs(workload_id, tail=verification_config.log_tail_lines)
                    error_parts.append(f"\nLogs:\n{logs}")

                exit_code = self.get_workload_exit_code(workload_id)
                if exit_code is not None:
                    error_parts.insert(1, f"\nExit code: {exit_code}")

                error_parts.append(f"\nFailed after: {(i + 1) * check_interval:.1f}s")

                raise RuntimeError("".join(error_parts))

        # Timeout without verification
        self.logger.warning(f"Container {workload_id[:12]} still initializing after {max_wait:.1f}s")

    def execute_command(
        self,
        workload_id: str,
        command: str | list[str],
        working_dir: Path | None = None,
        environment: dict[str, str] | None = None,
        timeout: int | None = None,
        stream_callback: Callable[[str], None] | None = None,
    ) -> ProcessResult:
        """
        Execute command in Docker container.

        Automatically restarts container if it has stopped (e.g., due to timeout).

        Args:
            workload_id: Container ID.
            command: Command to execute.
            working_dir: Working directory.
            environment: Environment variables.
            timeout: Timeout in seconds. If specified, uses multiprocessing for reliable enforcement.
            stream_callback: Streaming callback (not implemented yet).

        Returns:
            ProcessResult with exit code and output. Returns exit code 124 on timeout.

        Raises:
            RuntimeError: If command execution fails.
        """
        try:
            container = self.client.containers.get(workload_id)

            # Auto-restart if container has stopped
            if container.status != "running":
                self.logger.warning(
                    f"Container {workload_id[:12]} was stopped (status: {container.status}), "
                    f"restarting automatically. This may indicate the container reached its timeout."
                )
                container.start()
                self.logger.info(f"Container {workload_id[:12]} restarted successfully")

            exec_kwargs = {
                "cmd": command,
                "stdout": True,
                "stderr": True,
                "stdin": False,
            }

            if working_dir:
                exec_kwargs["workdir"] = str(working_dir)
            if environment:
                exec_kwargs["environment"] = environment

            # Fast path: no timeout
            if timeout is None:
                result = container.exec_run(**exec_kwargs)
                return ProcessResult(
                    exit_code=result.exit_code,
                    stdout=result.output.decode("utf-8", errors="replace"),
                    stderr="",  # Docker SDK doesn't separate stdout and stderr
                )

            # Timeout enforcement: use multiprocessing
            result_queue = Queue()
            process = Process(
                target=_run_docker_exec_in_process,
                args=(workload_id, exec_kwargs, result_queue),
            )
            process.daemon = True
            process.start()

            # Wait for process with timeout
            process.join(timeout)

            if process.is_alive():
                # Timeout occurred
                process.terminate()
                process.join(1)

                if process.is_alive():
                    # Force kill
                    try:
                        os.kill(process.pid, signal.SIGKILL)
                        process.join()
                    except (PermissionError, OSError):
                        pass

                return ProcessResult(
                    exit_code=124,  # Standard timeout exit code
                    stdout="",
                    stderr=f"Command timed out after {timeout} seconds",
                )

            if not result_queue.empty():
                result = result_queue.get()
                if result["error"]:
                    error_msg = f"Failed to execute command: {result['error']}"
                    if "error_type" in result:
                        error_msg += f" ({result['error_type']})"
                    if "traceback" in result:
                        self.logger.debug(f"Subprocess traceback:\n{result['traceback']}")
                    raise RuntimeError(error_msg)

                return ProcessResult(
                    exit_code=result["exit_code"],
                    stdout=result["output"].decode("utf-8", errors="replace"),
                    stderr="",
                )

            # Should not happen, but handle it
            return ProcessResult(
                exit_code=1,
                stdout="",
                stderr="Process completed but no result was returned",
            )

        except DockerException as e:
            raise RuntimeError(f"Failed to execute command: {e}") from e

    def remove_workload(self, workload_id: str, force: bool = True) -> None:
        """
        Remove a Docker container.

        Args:
            workload_id: Container ID.
            force: Force removal even if running.

        Raises:
            RuntimeError: If container removal fails.
        """
        try:
            container = self.client.containers.get(workload_id)
            if container.status == "running" and force:
                container.stop(timeout=DOCKER_STOP_TIMEOUT)
            container.remove()
        except NotFound:
            pass
        except DockerException as e:
            raise RuntimeError(f"Failed to remove container: {e}") from e

    def get_workload_status(self, workload_id: str) -> ContainerStatus:
        """
        Get Docker container status.

        Args:
            workload_id: Container ID.

        Returns:
            Container status.
        """
        try:
            container = self.client.containers.get(workload_id)

            # Direct mapping of Docker statuses to podkit enum
            status_map = {
                "created": ContainerStatus.CREATING,
                "running": ContainerStatus.RUNNING,
                "paused": ContainerStatus.PAUSED,
                "exited": ContainerStatus.EXITED,
                "restarting": ContainerStatus.RESTARTING,
                "removing": ContainerStatus.REMOVING,
                "dead": ContainerStatus.DEAD,
            }

            return status_map.get(container.status, ContainerStatus.ERROR)

        except NotFound:
            return ContainerStatus.ERROR
        except DockerException:
            return ContainerStatus.ERROR

    def list_workloads(self, filters: dict[str, str] | None = None) -> list[dict]:
        """
        List Docker containers.

        Args:
            filters: Filter criteria.

        Returns:
            List of container information dicts.

        Raises:
            RuntimeError: If listing fails.
        """
        try:
            containers = self.client.containers.list(all=True, filters=filters or {})
            return [
                {
                    "id": c.id,
                    "name": c.name,
                    "status": c.status,
                    "created": c.attrs["Created"],
                }
                for c in containers
            ]
        except DockerException as e:
            raise RuntimeError(f"Failed to list containers: {e}") from e

    def get_workload_labels(self, workload_id: str) -> dict[str, str]:
        """
        Get labels for a Docker container.

        Args:
            workload_id: Container ID.

        Returns:
            Dictionary of labels.

        Raises:
            RuntimeError: If retrieval fails.
        """
        try:
            container = self.client.containers.get(workload_id)
            return container.labels
        except NotFound:
            return {}
        except DockerException as e:
            raise RuntimeError(f"Failed to get container labels: {e}") from e

    def reload_workload(self, workload_id: str) -> None:
        """
        Refresh container state from Docker daemon.

        Args:
            workload_id: Container ID.

        Raises:
            RuntimeError: If refresh fails.
        """
        try:
            container = self.client.containers.get(workload_id)
            container.reload()
        except NotFound:
            pass
        except DockerException as e:
            raise RuntimeError(f"Failed to reload container: {e}") from e

    def get_workload_logs(self, workload_id: str, tail: int = 100) -> str:
        """
        Get logs from a Docker container.

        Args:
            workload_id: Container ID.
            tail: Number of lines to retrieve from end of logs.

        Returns:
            Log output as string.

        Raises:
            RuntimeError: If log retrieval fails.
        """
        try:
            container = self.client.containers.get(workload_id)
            logs = container.logs(tail=tail)
            return logs.decode("utf-8", errors="replace")
        except NotFound:
            return "Container not found"
        except DockerException as e:
            return f"Failed to retrieve logs: {e}"

    def get_workload_exit_code(self, workload_id: str) -> int | None:
        """
        Get exit code of a stopped Docker container.

        Args:
            workload_id: Container ID.

        Returns:
            Exit code if available, None otherwise.

        Raises:
            RuntimeError: If retrieval fails.
        """
        try:
            container = self.client.containers.get(workload_id)
            return container.attrs.get("State", {}).get("ExitCode")
        except NotFound:
            return None
        except DockerException as e:
            raise RuntimeError(f"Failed to get exit code: {e}") from e

    def get_accessible_ports(self, workload_id: str) -> dict[int, int]:
        """Get accessible port mappings for Docker container.

        Implements BackendInterface.get_accessible_ports() for Docker.
        Returns mapping of container ports to host ports.

        Args:
            workload_id: Container ID.

        Returns:
            Dict mapping container_port → host_port.
            Example: {80: 8080, 443: 8443}
            Empty dict if container not found or no ports bound.

        Raises:
            RuntimeError: If retrieval fails.
        """
        try:
            container = self.client.containers.get(workload_id)
            port_bindings = container.attrs.get("HostConfig", {}).get("PortBindings", {})

            # Parse Docker format: {"3000/tcp": [{"HostPort": "5000"}]}
            result = {}
            for container_port_str, bindings in port_bindings.items():
                if bindings and len(bindings) > 0:
                    port_num = int(container_port_str.split("/")[0])
                    host_port = int(bindings[0]["HostPort"])
                    result[port_num] = host_port

            return result
        except NotFound:
            return {}
        except (KeyError, ValueError, IndexError):
            return {}
        except DockerException as e:
            self.logger.warning(f"Failed to get port bindings for {workload_id[:12]}: {e}")
            return {}

    def detect_current_image(self) -> str | None:
        """Detect container image of the current process.

        Implements BackendInterface.detect_current_image() for Docker.
        Checks if current process is running in a Docker container and returns its image.

        Returns:
            Image name/tag if running in container and detection succeeds.
            None if not running in container or detection fails.
        """
        try:
            hostname = os.uname().nodename
            container = self.client.containers.get(hostname)
            return container.image.tags[0] if container.image.tags else container.image.id
        except Exception:
            return None
