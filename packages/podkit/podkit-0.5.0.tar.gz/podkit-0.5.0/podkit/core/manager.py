"""Base container manager for managing container lifecycle."""

import logging
import re
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from threading import Lock
from typing import Any

from podkit.backends.base import BackendInterface
from podkit.constants import CONTAINER_WORKSPACE_PATH
from podkit.core.models import ContainerConfig, ContainerStatus, ProcessResult
from podkit.utils.mounts import get_standard_workspace_mounts
from podkit.utils.paths import (
    container_to_host_path,
    get_workspace_path,
    host_to_container_path,
    write_to_mounted_path,
)


class BaseContainerManager(ABC):
    """
    Base container manager that works with any backend.

    Projects extend this class and inject their chosen backend.
    """

    def __init__(
        self,
        backend: BackendInterface,
        container_prefix: str,
        workspace_base: Path,
        workspace_base_host: Path | None = None,
        logger: logging.Logger | None = None,
    ):
        """
        Initialize container manager.

        Args:
            backend: Backend implementation (Docker, K8s, etc.).
            container_prefix: Prefix for container names (e.g., "sandbox", "biomni").
            workspace_base: Base workspace directory for all sessions.
            workspace_base_host: Actual host path that Docker can access (for nested containers).
                                If None, assumes workspace_base is directly accessible by Docker.
            logger: Optional logger instance. If None, creates a default logger.
                   Accepts any Python logger for flexible integration with external logging systems.
        """
        self.backend = backend
        self.container_prefix = container_prefix
        self.workspace_base = Path(workspace_base)
        self.workspace_base_host = Path(workspace_base_host) if workspace_base_host else self.workspace_base
        self.logger = logger or logging.getLogger(f"podkit.{container_prefix}")
        self.lock = Lock()
        self.containers: dict[str, str] = {}  # {workload_id: workload_name}

        self.backend.connect()

    def _track_container(self, container_id: str, container_name: str) -> None:
        """Thread-safe method to add container to tracking dictionary.

        Args:
            container_id: Container ID to track.
            container_name: Container name.
        """
        with self.lock:
            self.containers[container_id] = container_name

    def _untrack_container(self, container_id: str) -> bool:
        """Thread-safe method to remove container from tracking dictionary.

        Args:
            container_id: Container ID to untrack.

        Returns:
            True if container was tracked (and removed), False otherwise.
        """
        with self.lock:
            if container_id in self.containers:
                del self.containers[container_id]
                return True
            return False

    def _is_tracked(self, container_id: str) -> bool:
        """Thread-safe method to check if container is tracked.

        Args:
            container_id: Container ID to check.

        Returns:
            True if container is tracked, False otherwise.
        """
        with self.lock:
            return container_id in self.containers

    def _get_tracked_containers(self) -> list[str]:
        """Thread-safe method to get list of tracked container IDs.

        Returns:
            List of container IDs currently tracked.
        """
        with self.lock:
            return list(self.containers.keys())

    def create_container(
        self,
        user_id: str,
        session_id: str,
        config: ContainerConfig,
    ) -> tuple[str, str]:
        """
        Create a new container.

        Args:
            user_id: User identifier.
            session_id: Session identifier.
            config: Container configuration.

        Returns:
            Tuple of (container_id, container_name).

        Raises:
            RuntimeError: If container creation fails.
        """
        user_session_slug = "-".join(re.sub(r"[^a-z0-9]", "", _id.lower()) for _id in (session_id, user_id))
        container_name = f"{self.container_prefix}-{user_session_slug}-{uuid.uuid4().hex[:4]}"

        mounts = self.get_mounts(user_id, session_id, config)

        # Add labels for session recovery
        labels = {
            "podkit.user_id": user_id,
            "podkit.session_id": session_id,
            "podkit.manager": self.container_prefix,
            "podkit.image": config.image,
        }

        # Create via backend with labels (outside lock - this may be slow)
        container_id = self.backend.create_workload(
            name=container_name,
            config=config,
            mounts=mounts,
            labels=labels,
        )

        # Add to tracking (minimize lock time)
        self._track_container(container_id, container_name)

        return container_id, container_name

    @abstractmethod
    def get_mounts(
        self,
        user_id: str,
        session_id: str,
        config: ContainerConfig,
    ) -> list[dict[str, Any]]:
        """
        Get volume mounts for container.

        Project-specific implementation (sandbox vs biomni have different needs).

        Args:
            user_id: User identifier.
            session_id: Session identifier.
            config: Container configuration.

        Returns:
            List of mount specifications in Docker format.
        """
        ...

    def start_container(self, container_id: str, config: ContainerConfig | None = None) -> None:
        """
        Start a container with optional startup verification.

        Backend automatically handles paused vs stopped states.

        Args:
            container_id: ID of the container to start.
            config: Optional config for verification settings.
                   If None or no startup_verification, verification is skipped.

        Raises:
            RuntimeError: If container start fails or verification fails.
        """
        # Delegate to backend - it handles start/unpause + verification
        verification_config = config.startup_verification if config else None
        self.backend.start_workload(container_id, verification_config)

    def remove_container(self, container_id: str) -> None:
        """
        Remove a container.

        Args:
            container_id: ID of the container to remove.

        Raises:
            RuntimeError: If container removal fails.
        """
        # Remove from backend (outside lock - slow operation)
        self.backend.remove_workload(container_id)

        # Remove from tracking (minimize lock time)
        self._untrack_container(container_id)

    def execute_command(
        self,
        container_id: str,
        command: str | list[str],
        working_dir: Path | None = None,
        environment: dict[str, str] | None = None,
        timeout: int | None = None,
    ) -> ProcessResult:
        """
        Execute command in container.

        Args:
            container_id: ID of the container.
            command: Command to execute.
            working_dir: Working directory for command execution.
            environment: Environment variables.
            timeout: Timeout in seconds.

        Returns:
            ProcessResult with exit code and output.

        Raises:
            RuntimeError: If command execution fails.
        """
        return self.backend.execute_command(
            workload_id=container_id,
            command=command,
            working_dir=working_dir,
            environment=environment,
            timeout=timeout,
        )

    @abstractmethod
    def write_file(
        self,
        container_id: str,
        container_path: Path | str,
        content: str,
        user_id: str,
        session_id: str,
    ) -> Path:
        """
        Write a file for a container.

        Implementation depends on mount strategy:
        - With mounts: Write to host filesystem (persists)
        - Without mounts: Write inside container via command (ephemeral)

        Args:
            container_id: ID of the container.
            container_path: Path inside the container where file should appear. Can be:
                           - Relative path (e.g., "file.txt") - auto-prepended with /workspace/
                           - Absolute path (e.g., "/workspace/file.txt") - used as-is
            content: Content to write.
            user_id: User identifier (for path resolution).
            session_id: Session identifier (for path resolution).

        Returns:
            The normalized container path where the file was written.

        Raises:
            RuntimeError: If file write fails.
        """
        ...

    def get_container_status(self, container_id: str, refresh: bool = True) -> ContainerStatus:
        """
        Get container status.

        Args:
            container_id: ID of the container.
            refresh: If True, refresh container state before checking status (default: True).
                    If False, use cached state (faster but may be stale).

        Returns:
            Current container status.
        """
        if refresh:
            self.backend.reload_workload(container_id)
        return self.backend.get_workload_status(container_id)

    def to_host_path(
        self,
        container_path: Path,
        user_id: str,
        session_id: str,
        real_host: bool = False,
    ) -> Path:
        """
        Convert a container path to a host path.

        Args:
            container_path: Path inside the container.
            user_id: User identifier.
            session_id: Session identifier.
            real_host: If False, return path valid for current process (default).
                      If True, return path on underlying host that Docker daemon can access.
                      Only makes a difference when running inside a container.

        Returns:
            Path on the host filesystem.

        Raises:
            ValueError: If path conversion fails.
        """
        workspace_path = get_workspace_path(self.workspace_base, user_id, session_id)
        host_path = container_to_host_path(
            container_path=Path(container_path),
            workspace_base=workspace_path,
            container_workspace=Path(CONTAINER_WORKSPACE_PATH),
        )

        # For nested Docker: translate from process-local path to actual host path
        if real_host and self.workspace_base_host != self.workspace_base:
            try:
                relative_path = host_path.relative_to(self.workspace_base)
                host_path = self.workspace_base_host / relative_path
            except ValueError as e:
                raise ValueError(
                    f"Host path must be under workspace_base '{self.workspace_base}', got '{host_path}' instead"
                ) from e

        return host_path

    def to_container_path(
        self,
        host_path: Path,
        user_id: str,
        session_id: str,
    ) -> Path:
        """
        Convert a host path to a container path.

        Args:
            host_path: Path on the host filesystem.
            user_id: User identifier.
            session_id: Session identifier.

        Returns:
            Path inside the container.

        Raises:
            ValueError: If path conversion fails.
        """
        workspace_path = get_workspace_path(self.workspace_base, user_id, session_id)
        return host_to_container_path(
            host_path=Path(host_path),
            workspace_base=workspace_path,
            container_workspace=Path(CONTAINER_WORKSPACE_PATH),
        )

    def discover_existing_containers(self) -> list[dict[str, str]]:
        """Discover existing containers managed by this manager.

        Discovered containers are automatically added to internal tracking.

        Returns:
            List of dicts with keys: container_id, container_name, user_id, session_id, image
        """
        try:
            containers = self.backend.list_workloads(filters={"name": f"{self.container_prefix}-"})

            discovered = []
            for container_info in containers:
                container_id = container_info["id"]
                container_name = container_info["name"]

                labels = self.backend.get_workload_labels(container_id)

                user_id = labels.get("podkit.user_id")
                session_id = labels.get("podkit.session_id")
                image = labels.get("podkit.image")

                if user_id and session_id:
                    # Add to tracking dict so cleanup_all() can find it
                    self._track_container(container_id, container_name)

                    discovered.append(
                        {
                            "container_id": container_id,
                            "container_name": container_name,
                            "user_id": user_id,
                            "session_id": session_id,
                            "image": image,
                        }
                    )

            return discovered
        except Exception:  # pylint: disable=broad-except
            return []

    def cleanup_all(self) -> None:
        """Clean up all tracked containers."""
        # Get snapshot (minimize lock time)
        container_ids = self._get_tracked_containers()

        for container_id in container_ids:
            try:
                self.remove_container(container_id)
            except Exception:  # pylint: disable=broad-except
                # Continue even if one fails
                pass


class SimpleContainerManager(BaseContainerManager):
    """
    Simple implementation of container manager.

    This is used for integration tests and provides a basic mount strategy.
    """

    def get_mounts(
        self,
        user_id: str,
        session_id: str,
        config: ContainerConfig,
    ) -> list[dict[str, Any]]:
        """
        Get volume mounts for test containers.

        Creates a workspace mount for the user's session.

        Note: For nested Docker containers, we need to use paths that Docker
        on the host can access. Uses to_host_path(real_host=True) from base class.

        Args:
            user_id: User identifier.
            session_id: Session identifier.
            config: Container configuration.

        Returns:
            List of mount specifications.
        """
        return get_standard_workspace_mounts(
            workspace_base=self.workspace_base,
            user_id=user_id,
            session_id=session_id,
            config=config,
            to_host_path_fn=self.to_host_path,
        )

    def write_file(
        self,
        container_id: str,
        container_path: Path | str,
        content: str,
        user_id: str,
        session_id: str,
    ) -> Path:
        """
        Write file to mounted filesystem (persists after container removal).

        Args:
            container_id: ID of the container.
            container_path: Path inside the container. Can be relative or absolute.
            content: Content to write.
            user_id: User identifier.
            session_id: Session identifier.

        Returns:
            The normalized container path where the file was written.

        Raises:
            RuntimeError: If file write fails.
        """
        return write_to_mounted_path(
            container_path,
            content,
            lambda path: self.to_host_path(path, user_id, session_id),
        )
