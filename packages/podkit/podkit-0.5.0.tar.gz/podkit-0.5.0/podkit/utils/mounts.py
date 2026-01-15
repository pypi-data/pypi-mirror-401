"""Shared mount configuration utilities for container managers."""

from pathlib import Path
from typing import Any

from podkit.constants import CONTAINER_WORKSPACE_PATH
from podkit.core.models import ContainerConfig
from podkit.utils.paths import get_workspace_path


def get_standard_workspace_mounts(
    workspace_base: Path,
    user_id: str,
    session_id: str,
    config: ContainerConfig,
    to_host_path_fn,
) -> list[dict[str, Any]]:
    """Generate standard workspace mounts for a container.

    This is the common mount strategy used by both SimpleContainerManager
    and _MountedContainerManager. It creates a workspace mount and adds
    any custom volumes from the config.

    Args:
        workspace_base: Base workspace directory.
        user_id: User identifier.
        session_id: Session identifier.
        config: Container configuration with optional custom volumes.
        to_host_path_fn: Function to convert container path to host path.
            Should accept (container_path, user_id, session_id, real_host=True).

    Returns:
        List of mount specifications in Docker format.

    Example:
        >>> mounts = get_standard_workspace_mounts(
        ...     workspace_base=Path("/tmp/workspace"),
        ...     user_id="user1",
        ...     session_id="session1",
        ...     config=ContainerConfig(image="python:3.11-alpine"),
        ...     to_host_path_fn=manager.to_host_path
        ... )
    """
    workspace_path = get_workspace_path(workspace_base, user_id, session_id)
    workspace_path.mkdir(parents=True, exist_ok=True)

    # Use provided function for nested Docker scenarios
    # real_host=True gets the actual host path Docker can access
    host_workspace_path = to_host_path_fn(Path(CONTAINER_WORKSPACE_PATH), user_id, session_id, real_host=True)

    mounts = [
        {
            "Type": "bind",
            "Source": str(host_workspace_path),
            "Target": CONTAINER_WORKSPACE_PATH,
        }
    ]

    for volume in config.volumes or []:
        mount_dict = {
            "Type": volume.type,
            "Source": str(volume.source),
            "Target": str(volume.target),
        }
        if volume.read_only:
            mount_dict["ReadOnly"] = True
        mounts.append(mount_dict)

    return mounts
