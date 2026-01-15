"""Integration tests for podkit library negative flows and error scenarios.

This test validates error handling and failure scenarios:
1. Read-only volume mount restrictions
2. Invalid operations and expected failures
3. Permission and access control

NOTE: Tests are numbered to ensure execution order.
"""

import shutil
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from podkit.core.manager import SimpleContainerManager
from podkit.core.models import ContainerConfig, ContainerStatus, Mount, ProcessResult
from podkit.core.session import BaseSessionManager


def assert_read_only_error(result: ProcessResult):
    """Assert that read-only volumes prevent write operations."""
    assert result.exit_code == 1
    assert "read-only file system" in result.stderr.lower() or "read-only file system" in result.stdout.lower()


@pytest.mark.integration
class TestPodkitIntegrationNegativeFlows:  # pylint: disable=too-few-public-methods
    """Integration tests for error handling and failure scenarios."""

    def test_01_readonly_volume_prevents_writes(self, backend, test_config, docker_client, test_user, test_session):
        """Test that read-only volumes prevent write operations.

        Verifies:
        1. Files in read-only volumes can be read
        2. Attempts to write to existing files in read-only volumes fail
        3. Attempts to create new files in read-only volumes fail
        4. Attempts to delete files in read-only volumes fail
        5. Docker mount is actually marked as read-only

        Note: Uses subdirectories of the shared test_workspace for Docker-in-Docker compatibility.
        """
        manager = SimpleContainerManager(
            backend=backend,
            container_prefix=f"{test_config['test_prefix']}-readonly-vol",
            workspace_base=test_config["test_workspace"],
            workspace_base_host=test_config["test_workspace_host"],
        )

        session_manager = BaseSessionManager(
            default_image=test_config["test_image"],
            container_manager=manager,
        )

        container_path = test_config["test_workspace"] / "readonly_vol" / test_session
        container_path.mkdir(parents=True, exist_ok=True)

        # For Docker-in-Docker, use host path for volume mount
        host_path = test_config["test_workspace_host"] / "readonly_vol" / test_session

        try:
            test_file = container_path / "readonly_file.txt"
            test_file.write_text("This file is read-only")

            # Create config with read-only volume
            config_with_readonly_volume = ContainerConfig(
                container_lifetime_seconds=3000,
                image=test_config["test_image"],
                volumes=[
                    Mount(type="bind", source=host_path, target=Path("/readonly"), read_only=True),
                ],
            )

            session = session_manager.create_session(
                user_id=test_user,
                session_id=test_session,
                config=config_with_readonly_volume,
            )
            container = docker_client.containers.get(session.container_id)
            assert container.status == "running"

            # Test 1: Verify file can be read from read-only volume
            result_read = session_manager.execute_command(
                user_id=test_user,
                session_id=test_session,
                command=["cat", "/readonly/readonly_file.txt"],
            )
            assert result_read.exit_code == 0
            assert "This file is read-only" in result_read.stdout

            # Test 2: Verify writing to existing file in read-only volume fails
            result_write = session_manager.execute_command(
                user_id=test_user,
                session_id=test_session,
                command=["sh", "-c", "echo 'new content' > /readonly/readonly_file.txt"],
            )
            assert_read_only_error(result_write)

            # Test 3: Verify creating new file in read-only volume fails
            result_create = session_manager.execute_command(
                user_id=test_user,
                session_id=test_session,
                command=["sh", "-c", "echo 'new file' > /readonly/new_file.txt"],
            )
            assert_read_only_error(result_create)

            # Test 4: Verify deleting file in read-only volume fails
            result_delete = session_manager.execute_command(
                user_id=test_user,
                session_id=test_session,
                command=["rm", "/readonly/readonly_file.txt"],
            )
            assert_read_only_error(result_delete)

            # Test 5: Verify original file still exists and unchanged
            result_verify = session_manager.execute_command(
                user_id=test_user,
                session_id=test_session,
                command=["cat", "/readonly/readonly_file.txt"],
            )
            assert result_verify.exit_code == 0
            assert "This file is read-only" in result_verify.stdout

            # Test 6: Verify the mount is actually marked as read-only in Docker
            container_attrs = container.attrs
            mounts = container_attrs.get("Mounts", [])
            readonly_mount = next((m for m in mounts if m.get("Destination") == "/readonly"), None)
            assert readonly_mount is not None, "Read-only mount not found"
            assert readonly_mount.get("RW") is False, "Mount should be marked as read-only (RW=False)"

        finally:
            session_manager.close_session(test_user, test_session)
            manager.cleanup_all()
            if container_path.parent.exists():
                shutil.rmtree(container_path.parent)

    def test_02_health_monitor_recovery_and_cleanup(self, backend, test_config, docker_client, test_user, test_session):
        """Test health monitor detects failures, attempts recovery, and handles cleanup.

        Verifies:
        1. Health monitor detects externally stopped containers
        2. RECOVERABLE states (exited): Try restart with verification
        3. If restart succeeds: Keep container
        4. UNRECOVERABLE states (dead): Remove and mark for recreation
        5. execute_command auto-recreates when needed
        6. Expired sessions auto-cleaned up
        """
        import time

        from podkit.monitors.health import ContainerHealthMonitor

        manager = SimpleContainerManager(
            backend=backend,
            container_prefix=f"{test_config['test_prefix']}-health",
            workspace_base=test_config["test_workspace"],
            workspace_base_host=test_config["test_workspace_host"],
        )

        # Create health monitor with fast checks
        health_monitor = ContainerHealthMonitor(
            container_manager=manager,
            check_interval=2,  # Fast checks for testing
            log_lines=50,
        )

        session_manager = BaseSessionManager(
            default_image=test_config["test_image"],
            container_manager=manager,
            health_monitor=health_monitor,  # Enable monitoring
        )

        try:
            # Test 1: Create session and verify it works
            config = ContainerConfig(
                image=test_config["test_image"],
                container_lifetime_seconds=3000,
            )
            session = session_manager.create_session(test_user, test_session, config)
            result1 = session_manager.execute_command(test_user, test_session, ["echo", "before_stop"])
            assert result1.exit_code == 0
            assert "before_stop" in result1.stdout

            original_container_id = session.container_id
            assert original_container_id is not None

            # Test 2: Stop container externally (simulates failure)
            container = docker_client.containers.get(original_container_id)
            container.stop()

            # Wait for health monitor to detect and attempt recovery
            time.sleep(4)  # 2s check interval + buffer

            # Test 3: Verify recovery was attempted (container should be restarted)
            container.reload()
            # Container should be running again (recovery successful for EXITED state)
            assert container.status == "running"

            # Session should still have same container (restart succeeded)
            session = session_manager.get_session(test_user, test_session)
            assert session.container_id == original_container_id

            # Test 4: Execute command should work (container was recovered)
            result2 = session_manager.execute_command(test_user, test_session, ["echo", "after_recovery"])
            assert result2.exit_code == 0
            assert "after_recovery" in result2.stdout

            # Test 5: Test UNRECOVERABLE state - kill container (makes it "dead")
            container.kill()
            time.sleep(4)  # Wait for detection

            # Health monitor should remove UNRECOVERABLE container and mark session
            session_before_recreation = session_manager.get_session(test_user, test_session)
            # Session should be marked ERROR with cleared container_id
            assert (
                session_before_recreation.container_id is None
                or session_before_recreation.status == ContainerStatus.ERROR
            )
            # Verify failure metadata captured (BEFORE recreation clears it)
            assert (
                "failure_status" in session_before_recreation.metadata
                or "failure_reason" in session_before_recreation.metadata
            )

            # Test 6: execute_command should auto-recreate
            result3 = session_manager.execute_command(test_user, test_session, ["echo", "recreated"])
            assert result3.exit_code == 0
            assert "recreated" in result3.stdout

            # Verify NEW container was created (different ID)
            session_after_recreation = session_manager.get_session(test_user, test_session)
            new_container_id = session_after_recreation.container_id
            assert new_container_id is not None
            assert new_container_id != original_container_id  # Must be different!
            # Metadata cleared after successful recreation
            assert session_after_recreation.status == ContainerStatus.RUNNING

            # Test 7: Session cleanup - create session and make it expire
            short_session_id = f"{test_session}_short"
            session2 = session_manager.create_session(test_user, short_session_id)
            assert session2 is not None

            # Get the session from manager's dict to modify it
            session2_from_dict = session_manager.get_session(test_user, short_session_id)
            assert session2_from_dict is not None

            # Manually set short timeout and old last_active_at to simulate expiration
            session2_from_dict.session_inactivity_timeout_seconds = 2  # 2 second timeout
            session2_from_dict.last_active_at = datetime.now(UTC) - timedelta(seconds=5)  # 5 seconds ago

            # Verify session is expired
            assert session2_from_dict.is_expired()

            # Wait for monitor check (multiple cycles to be safe)
            time.sleep(6)  # 3x check interval to ensure cleanup runs

            # Verify session cleaned up
            session2_after = session_manager.get_session(test_user, short_session_id)
            assert session2_after is None  # Should be auto-removed

        finally:
            health_monitor.stop()
            session_manager.cleanup_all()
            manager.cleanup_all()
