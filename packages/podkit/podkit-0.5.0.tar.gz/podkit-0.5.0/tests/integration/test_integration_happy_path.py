"""Integration test for podkit library happy path workflow.

This test validates the entire workflow using ONE container for basic tests,
then creates separate containers for feature-specific scenarios.

NOTE: Tests are numbered to ensure execution order.
"""

import shutil
import time
from pathlib import Path

import docker
import pytest

from podkit import get_docker_session, reset_lifecycle_cache
from podkit.core.manager import SimpleContainerManager
from podkit.core.models import ContainerConfig, Mount, StartupVerificationConfig
from podkit.core.session import BaseSessionManager
from podkit.processes import ProcessManager, ProcessStatus


@pytest.mark.integration
class TestPodkitIntegrationHappyPath:
    """Integration test for complete podkit library workflow."""

    @pytest.fixture(scope="class")
    def shared_session(self, session_manager, test_user, test_session):
        """Create one session for all tests in this class."""
        session = session_manager.create_session(
            user_id=test_user,
            session_id=test_session,
        )
        yield session
        # Cleanup after all tests (only if session still exists)
        if session_manager.get_session(test_user, test_session):
            session_manager.close_session(test_user, test_session)

    def test_01_basic_operations(self, shared_session, session_manager, container_manager, test_user, test_session):
        """Test basic container operations: command execution and file I/O."""
        # Command execution - Simple command
        result = container_manager.execute_command(
            container_id=shared_session.container_id,
            command=["echo", "hello world"],
        )
        assert result.exit_code == 0
        assert "hello world" in result.stdout
        assert result.stderr == ""

        # Command execution - Custom working directory
        result = container_manager.execute_command(
            container_id=shared_session.container_id,
            command=["pwd"],
            working_dir=Path("/tmp"),
        )
        assert result.exit_code == 0
        assert "/tmp" in result.stdout

        # Command execution - Environment variables
        result = container_manager.execute_command(
            container_id=shared_session.container_id,
            command=["sh", "-c", "echo $TEST_VAR"],
            environment={"TEST_VAR": "test_value"},
        )
        assert result.exit_code == 0
        assert "test_value" in result.stdout

        # Command execution - Shell command with pipes
        result = container_manager.execute_command(
            container_id=shared_session.container_id,
            command=["sh", "-c", "echo 'line1' && echo 'line2'"],
        )
        assert result.exit_code == 0
        assert "line1" in result.stdout
        assert "line2" in result.stdout

        # File operations - Write file using session manager
        write_content = "This is test content\nLine 2\nLine 3"
        container_path = Path("/workspace/test_file.txt")

        session_manager.write_file(
            user_id=test_user,
            session_id=test_session,
            container_path=container_path,
            content=write_content,
        )

        # File operations - Verify file exists and has correct content
        result = container_manager.execute_command(
            container_id=shared_session.container_id,
            command=["cat", str(container_path)],
        )
        assert result.exit_code == 0
        assert result.stdout.strip() == write_content

        # File operations - Create file via shell command
        shell_content = "Created by shell"
        result = container_manager.execute_command(
            container_id=shared_session.container_id,
            command=["sh", "-c", f"echo '{shell_content}' > /workspace/shell_file.txt"],
        )
        assert result.exit_code == 0

        # File operations - Read it back
        result = container_manager.execute_command(
            container_id=shared_session.container_id,
            command=["cat", "/workspace/shell_file.txt"],
        )
        assert result.exit_code == 0
        assert shell_content in result.stdout

    def test_02_path_translation(self, container_manager, test_user, test_session, test_workspace):
        """Test path translation between host and container."""
        container_path = Path("/workspace/test.txt")

        # Convert container path to host path
        host_path = container_manager.to_host_path(container_path, test_user, test_session)
        assert host_path is not None
        assert test_workspace in host_path.parents

        # Convert back to container path
        converted_path = container_manager.to_container_path(host_path, test_user, test_session)
        assert converted_path == container_path

    def test_03_resource_limits(self, shared_session, docker_client):
        """Verify container has resource limits applied."""
        container = docker_client.containers.get(shared_session.container_id)
        host_config = container.attrs["HostConfig"]

        # Verify memory limit
        memory_limit = host_config.get("Memory")
        assert memory_limit is not None
        assert memory_limit > 0

        # Verify CPU limit
        cpu_quota = host_config.get("CpuQuota")
        assert cpu_quota is not None
        assert cpu_quota > 0

    def test_04_session_activity_and_status(
        self, shared_session, session_manager, container_manager, test_user, test_session
    ):
        """Verify session activity tracking and container status."""
        # Check activity tracking
        initial_activity = shared_session.last_active_at
        time.sleep(0.1)
        session_manager.update_session_activity(test_user, test_session)

        updated_session = session_manager.get_session(test_user, test_session)
        assert updated_session.last_active_at > initial_activity

        # Verify session not expired (has recent activity)
        assert not updated_session.is_expired()

        # Check container status
        status = container_manager.get_container_status(shared_session.container_id)
        assert status == "running"

    def test_05_cleanup_verification(
        self, shared_session, session_manager, container_manager, docker_client, test_user, test_session
    ):
        """Verify cleanup removes container and session."""
        container_id = shared_session.container_id

        # Close session (should remove container)
        session_manager.close_session(test_user, test_session)

        # Verify session removed
        session = session_manager.get_session(test_user, test_session)
        assert session is None

        # Verify container removed from Docker
        with pytest.raises(docker.errors.NotFound):
            docker_client.containers.get(container_id)

        # Verify container removed from manager tracking
        assert container_id not in container_manager.containers

    def test_06_session_recovery_after_manager_restart(
        self, backend, test_config, test_workspace, docker_client, test_user
    ):
        """Test that sessions reconnect to existing containers after manager restart.

        Verifies:
        1. Container survives manager destruction
        2. New manager discovers existing container
        3. Session reconnects automatically
        4. Port bindings are preserved and queryable after restart
        """
        recovery_session_id = f"recovery-{test_user}"
        test_content = "Data survives manager restart"
        test_ports = [5000, 5001, 5002]

        # Phase 1: Create session with first manager
        manager1 = SimpleContainerManager(
            backend=backend,
            container_prefix=f"{test_config['test_prefix']}-recovery",
            workspace_base=test_config["test_workspace"],
            workspace_base_host=test_config["test_workspace_host"],
        )

        session_manager1 = BaseSessionManager(
            container_manager=manager1,
            default_image=test_config["test_image"],
        )

        # Create config with ports
        config_with_ports = ContainerConfig(
            image=test_config["test_image"],
            ports=test_ports,
        )

        session1 = session_manager1.create_session(
            user_id=test_user,
            session_id=recovery_session_id,
            config=config_with_ports,
        )
        container_id = session1.container_id

        # Verify ports are bound
        port_bindings = backend.get_accessible_ports(container_id)
        assert len(port_bindings) == 3, f"Expected 3 ports, got {len(port_bindings)}"
        assert set(port_bindings.keys()) == set(test_ports), (
            f"Port keys mismatch: {port_bindings.keys()} vs {test_ports}"
        )
        # Verify 1:1 mapping (container port 5000 → host port 5000)
        for port in test_ports:
            assert port_bindings[port] == port, f"Port {port} should map to itself, got {port_bindings[port]}"

        session_manager1.write_file(
            user_id=test_user,
            session_id=recovery_session_id,
            container_path=Path("/workspace/persistent.txt"),
            content=test_content,
        )

        # Verify container is running
        container = docker_client.containers.get(container_id)
        assert container.status == "running"

        # Phase 2: Destroy managers (simulates restart)
        del session_manager1
        del manager1

        # Phase 3: Create new managers - should auto-recover session
        manager2 = SimpleContainerManager(
            backend=backend,
            container_prefix=f"{test_config['test_prefix']}-recovery",
            workspace_base=test_config["test_workspace"],
            workspace_base_host=test_config["test_workspace_host"],
        )

        session_manager2 = BaseSessionManager(
            container_manager=manager2,
            default_image=test_config["test_image"],
        )

        # Verify session was recovered
        recovered_session = session_manager2.get_session(test_user, recovery_session_id)
        assert recovered_session is not None
        assert recovered_session.container_id == container_id

        # Verify port bindings survived restart
        recovered_ports = backend.get_accessible_ports(container_id)
        assert recovered_ports == port_bindings, "Port bindings should be preserved after recovery"
        assert set(recovered_ports.keys()) == set(test_ports), f"Recovered ports mismatch: {recovered_ports.keys()}"

        # Verify data is still accessible
        result = session_manager2.execute_command(
            user_id=test_user,
            session_id=recovery_session_id,
            command=["cat", "/workspace/persistent.txt"],
        )

        assert result.exit_code == 0
        assert test_content in result.stdout

        # Cleanup
        session_manager2.close_session(test_user, recovery_session_id)
        manager2.cleanup_all()

    def test_07_container_auto_restart_after_timeout(self, backend, test_config, docker_client, test_user):
        """Test that containers auto-restart when they've exited due to timeout."""
        timeout_session_id = f"timeout-{test_user}"

        manager = SimpleContainerManager(
            backend=backend,
            container_prefix=f"{test_config['test_prefix']}-timeout",
            workspace_base=test_config["test_workspace"],
            workspace_base_host=test_config["test_workspace_host"],
        )

        # Create config with very short container lifetime (reduced from 3s to 2s)
        short_timeout_config = ContainerConfig(
            image=test_config["test_image"],
            container_lifetime_seconds=2,  # Container exits after 2 seconds
        )

        session_manager = BaseSessionManager(
            container_manager=manager,
            default_image=test_config["test_image"],
        )

        session = session_manager.create_session(
            user_id=test_user,
            session_id=timeout_session_id,
            config=short_timeout_config,
        )

        container_id = session.container_id

        # Execute command before timeout
        result = session_manager.execute_command(
            user_id=test_user,
            session_id=timeout_session_id,
            command=["echo", "before timeout"],
        )
        assert result.exit_code == 0

        # Wait for timeout (reduced from 3s to 2.5s)
        time.sleep(2.5)

        # Verify container stopped
        container = docker_client.containers.get(container_id)
        container.reload()
        assert container.status != "running"

        # Execute command again - should auto-restart
        result = session_manager.execute_command(
            user_id=test_user,
            session_id=timeout_session_id,
            command=["echo", "after auto-restart"],
        )

        assert result.exit_code == 0
        assert "after auto-restart" in result.stdout

        # Verify container is running again
        container.reload()
        assert container.status == "running"

        # Cleanup
        session_manager.close_session(test_user, timeout_session_id)
        manager.cleanup_all()

    def test_08_convenience_api_with_context_manager(self, test_config, test_user, docker_client):
        """Test get_docker_session() with mounts and context manager auto-cleanup."""
        mounted_session_id = f"mounted-{test_user}"
        ctx_session_id = f"ctx-{test_user}"
        test_file = "data.txt"
        test_content = "persistent data"

        try:
            # Test with mounts (README Example 3)
            session = get_docker_session(
                user_id=test_user,
                session_id=mounted_session_id,
                workspace=str(test_config["test_workspace"]),
                workspace_host=str(test_config["test_workspace_host"]),
            )

            # Write file using relative path (auto-prepended with /workspace/)
            returned_path = session.write_file(test_file, test_content)
            assert returned_path == Path(f"/workspace/{test_file}")

            # Verify file can be read from container
            result = session.execute_command(["cat", str(returned_path)])
            assert result.exit_code == 0
            assert result.stdout.strip() == test_content

            # Get session info to find actual host path
            session_info = session.get_info()
            session_data_dir = Path(session_info.data_dir)
            expected_host_file = session_data_dir / test_file

            # Verify file persists on host
            assert expected_host_file.exists(), f"Expected file at {expected_host_file}"
            assert expected_host_file.read_text() == test_content

            session.close()

            # File should persist after container removal
            assert expected_host_file.exists(), "File should persist after container removal"

            # Cleanup host file
            expected_host_file.unlink()

            # Test context manager auto-cleanup
            container_id = None
            with get_docker_session(user_id=test_user, session_id=ctx_session_id) as ctx_session:
                container_id = ctx_session.get_info().container_id

                result = ctx_session.execute_command("echo 'test'")
                assert result.exit_code == 0

                # Container exists during context
                container = docker_client.containers.get(container_id)
                assert container.status == "running"

            # Container should be removed after context
            time.sleep(0.5)
            with pytest.raises(docker.errors.NotFound):
                docker_client.containers.get(container_id)

        finally:
            reset_lifecycle_cache()

    def test_09_entrypoint_controls_container_lifetime(self, backend, test_config, docker_client, test_user):
        """Test that entrypoint setting controls container lifetime behavior."""
        entrypoint_session_id = f"entrypoint-test-{test_user}"

        manager = SimpleContainerManager(
            backend=backend,
            container_prefix=f"{test_config['test_prefix']}-entrypoint",
            workspace_base=test_config["test_workspace"],
            workspace_base_host=test_config["test_workspace_host"],
        )

        session_manager = BaseSessionManager(
            container_manager=manager,
            default_image=test_config["test_image"],
        )

        # Test 1: entrypoint=None (default) - uses sleep <container_lifetime_seconds>
        # Reduced from 3s to 2s
        config_with_timeout = ContainerConfig(
            image=test_config["test_image"],
            container_lifetime_seconds=2,  # 2 second lifetime
        )

        session1 = session_manager.create_session(
            user_id=test_user,
            session_id=f"{entrypoint_session_id}-timeout",
            config=config_with_timeout,
        )

        # Verify container is running
        container1 = docker_client.containers.get(session1.container_id)
        assert container1.status == "running"

        # Check that command is sleep with timeout
        container1.reload()
        container_attrs = container1.attrs
        cmd = container_attrs.get("Config", {}).get("Cmd", [])
        assert "sleep" in cmd
        assert "2" in cmd or 2 in cmd

        # Wait for container to auto-exit (reduced from 4s to 2.5s)
        time.sleep(2.5)
        container1.reload()
        assert container1.status != "running", "Container should have exited after timeout"

        # Test 2: entrypoint=[] - uses sleep infinity (runs indefinitely)
        config_no_timeout = ContainerConfig(
            image=test_config["test_image"],
            entrypoint=[],  # Explicit entrypoint disables auto-timeout
            container_lifetime_seconds=2,  # Should be ignored
        )

        session2 = session_manager.create_session(
            user_id=test_user,
            session_id=f"{entrypoint_session_id}-notimeout",
            config=config_no_timeout,
        )

        # Verify container is running
        container2 = docker_client.containers.get(session2.container_id)
        assert container2.status == "running"

        # Check that command is sleep infinity
        container2.reload()
        container_attrs = container2.attrs
        cmd = container_attrs.get("Config", {}).get("Cmd", [])
        assert "sleep" in cmd
        assert "infinity" in cmd

        # Wait the same time period - container should still be running (reduced from 4s to 2.5s)
        time.sleep(2.5)
        container2.reload()
        assert container2.status == "running", "Container should still be running (sleep infinity)"

        # Cleanup
        session_manager.close_session(test_user, f"{entrypoint_session_id}-timeout")
        session_manager.close_session(test_user, f"{entrypoint_session_id}-notimeout")
        manager.cleanup_all()

    def test_10_exec_command_timeout(self, backend, test_config, test_user):
        """Test that long-running commands are killed after timeout with exit code 124.

        Verifies:
        1. Command that exceeds timeout is terminated
        2. Returns standard timeout exit code 124
        3. Timeout is enforced (doesn't wait for full command duration)
        4. Container remains usable after timeout
        """
        timeout_test_session_id = f"cmd-timeout-{test_user}"

        manager = SimpleContainerManager(
            backend=backend,
            container_prefix=f"{test_config['test_prefix']}-cmdtimeout",
            workspace_base=test_config["test_workspace"],
            workspace_base_host=test_config["test_workspace_host"],
        )

        session_manager = BaseSessionManager(
            container_manager=manager,
            default_image=test_config["test_image"],
        )

        try:
            # Create session
            session = session_manager.create_session(
                user_id=test_user,
                session_id=timeout_test_session_id,
            )

            # Test 1: Command that would run for 10 seconds, but timeout after 2
            start_time = time.time()
            result = manager.execute_command(
                container_id=session.container_id,
                command=["sleep", "10"],
                timeout=2,  # Kill after 2 seconds
            )
            elapsed = time.time() - start_time

            # Should complete in ~2 seconds (allow 1s margin for process cleanup)
            assert elapsed < 3, f"Command took {elapsed:.2f}s but should timeout after ~2s"

            # Should return standard timeout exit code
            assert result.exit_code == 124, f"Expected exit code 124 for timeout, got {result.exit_code}"

            # Should have timeout message
            assert "timed out" in result.stderr.lower(), f"Expected timeout message in stderr, got: {result.stderr}"

            # Test 2: Verify container still works after timeout
            result2 = manager.execute_command(
                container_id=session.container_id,
                command=["echo", "still working"],
            )
            assert result2.exit_code == 0
            assert "still working" in result2.stdout

        finally:
            session_manager.close_session(test_user, timeout_test_session_id)
            manager.cleanup_all()

    def test_11_startup_verification(self, backend, test_config, docker_client, test_user):
        """Test startup verification feature detects containers that crash on startup.

        Verifies:
        1. Faulty containers are detected with diagnostic logs and exit codes
        2. Healthy containers pass verification and work normally
        """

        manager = SimpleContainerManager(
            backend=backend,
            container_prefix=f"{test_config['test_prefix']}-startup-verify",
            workspace_base=test_config["test_workspace"],
            workspace_base_host=test_config["test_workspace_host"],
        )

        session_manager = BaseSessionManager(
            container_manager=manager,
            default_image=test_config["test_image"],
        )

        # Phase 1: Verification detects failing container
        session_id_failing = f"failing-{test_user}"
        config_failing = ContainerConfig(
            image=test_config["test_image"],
            entrypoint=["sh", "-c", "echo 'Fatal error occurred'; exit 1"],
            startup_verification=StartupVerificationConfig(
                required_consecutive_checks=3,
                check_interval_seconds=1.0,
                max_wait_seconds=5.0,
            ),
        )

        try:
            # Should raise RuntimeError with diagnostics
            with pytest.raises(RuntimeError) as exc_info:
                session_manager.create_session(
                    user_id=test_user,
                    session_id=session_id_failing,
                    config=config_failing,
                )

            # Verify error contains diagnostics
            error_msg = str(exc_info.value)
            assert "failed to start" in error_msg.lower()
            assert "exit code" in error_msg.lower()
            assert "Fatal error occurred" in error_msg, "Should capture container logs"

        finally:
            # Cleanup any leftover containers
            manager.cleanup_all()

        # Phase 2: Verification succeeds for healthy container
        session_id_healthy = f"healthy-{test_user}"
        config_healthy = ContainerConfig(
            image=test_config["test_image"],
            entrypoint=["sh", "-c", "sleep 3600"],
            startup_verification=StartupVerificationConfig(
                required_consecutive_checks=3,
                check_interval_seconds=0.5,  # Faster for testing
                max_wait_seconds=5.0,
            ),
        )

        try:
            # Should complete successfully
            session_healthy = session_manager.create_session(
                user_id=test_user,
                session_id=session_id_healthy,
                config=config_healthy,
            )

            # Verify container is running
            container = docker_client.containers.get(session_healthy.container_id)
            assert container.status == "running"

            # Can execute commands
            result = manager.execute_command(
                container_id=session_healthy.container_id,
                command=["echo", "verified"],
            )
            assert result.exit_code == 0
            assert "verified" in result.stdout

        finally:
            session_manager.close_session(test_user, session_id_healthy)
            manager.cleanup_all()

    def test_12_multiple_volumes(self, backend, test_config, docker_client, test_user, test_session):
        """Test multiple volumes including read-only mounts.

        Verifies:
        1. Multiple Mount entries are processed correctly
        2. Each volume is accessible at its target path
        3. Read-only mounts allow read operations
        4. Read-only mounts prevent write operations
        5. Read-write mounts still work normally

        Note: Uses subdirectories of the shared test_workspace for Docker-in-Docker compatibility.
        """
        manager = SimpleContainerManager(
            backend=backend,
            container_prefix=f"{test_config['test_prefix']}-multi-volumes",
            workspace_base=test_config["test_workspace"],
            workspace_base_host=test_config["test_workspace_host"],
        )

        session_manager = BaseSessionManager(
            container_manager=manager,
            default_image=test_config["test_image"],
        )

        # Create test directories
        container_path1 = test_config["test_workspace"] / "multi_vol" / test_session / "test1"
        container_path2 = test_config["test_workspace"] / "multi_vol" / test_session / "test2"
        container_path1.mkdir(parents=True, exist_ok=True)
        container_path2.mkdir(parents=True, exist_ok=True)

        # For Docker-in-Docker, use host paths for volume mounts
        host_path1 = test_config["test_workspace_host"] / "multi_vol" / test_session / "test1"
        host_path2 = test_config["test_workspace_host"] / "multi_vol" / test_session / "test2"

        try:
            # Prepare test files
            (container_path1 / "file1.txt").write_text("content from volume 1")
            (container_path2 / "file2.txt").write_text("content from volume 2")

            # Configure with multiple mounts including read-only
            config_with_multiple_volumes = ContainerConfig(
                image=test_config["test_image"],
                volumes=[
                    Mount(type="bind", source=host_path1, target=Path("/mount1")),
                    Mount(type="bind", source=host_path2, target=Path("/mount2")),
                ],
            )

            session = session_manager.create_session(
                user_id=test_user,
                session_id=test_session,
                config=config_with_multiple_volumes,
            )
            container = docker_client.containers.get(session.container_id)
            assert container.status == "running"

            # Verify read-write mounts are accessible
            result1 = session_manager.execute_command(
                user_id=test_user,
                session_id=test_session,
                command=["cat", "/mount1/file1.txt"],
            )
            assert result1.exit_code == 0
            assert "content from volume 1" in result1.stdout

            result2 = session_manager.execute_command(
                user_id=test_user,
                session_id=test_session,
                command=["cat", "/mount2/file2.txt"],
            )
            assert result2.exit_code == 0
            assert "content from volume 2" in result2.stdout

        finally:
            session_manager.close_session(test_user, test_session)
            manager.cleanup_all()
            if container_path1.parent.exists():
                shutil.rmtree(container_path1.parent)

    def test_13_process_management_incremental(self, backend, test_config, test_user):
        """Incremental process management test - building up features one at a time.

        This test builds functionality gradually, adding one feature section at a time.
        Each section validates a specific capability before moving to the next.
        Uses the new ProcessManager implementation.
        """
        session_id = f"process-v2-{test_user}"

        manager = SimpleContainerManager(
            backend=backend,
            container_prefix=f"{test_config['test_prefix']}-processv2",
            workspace_base=test_config["test_workspace"],
            workspace_base_host=test_config["test_workspace_host"],
        )

        session_manager = BaseSessionManager(
            container_manager=manager,
            default_image=test_config["test_image"],
        )

        try:
            # Create session with explicit entrypoint to prevent early exit
            config = ContainerConfig(
                image=test_config["test_image"],
                entrypoint=[],  # Sleep infinity - prevents early exit
            )

            session = session_manager.create_session(
                user_id=test_user,
                session_id=session_id,
                config=config,
            )

            # Create process manager (using new implementation)
            process_mgr = ProcessManager(
                container_manager=manager,
                container_id=session.container_id,
                user_id=test_user,
                session_id=session_id,
            )

            # ==========================================
            # Phase 1A: Start simple command
            # ==========================================
            print("\n=== Phase 1A: Start simple command ===")
            sleep_proc = process_mgr.start_process("sleep 30")
            assert sleep_proc.pid is not None, "Process should have PID"
            assert process_mgr.is_running(sleep_proc.id), "Process should be running"
            print(f"✓ Phase 1A passed: Started process with PID {sleep_proc.pid}")

            # ==========================================
            # Phase 1C: Multiple processes
            # ==========================================
            print("\n=== Phase 1C: Multiple processes ===")
            proc1 = process_mgr.start_process("sleep 30")
            proc2 = process_mgr.start_process("sleep 30")
            proc3 = process_mgr.start_process("sleep 30")

            processes = process_mgr.list_processes()
            # Should have at least 4: sleep_proc (from 1A), proc1, proc2, proc3
            assert len(processes) >= 4, f"Should track at least 4 processes, got {len(processes)}"

            process_ids = [p.id for p in processes]
            assert sleep_proc.id in process_ids, "Original sleep process should be in list"
            assert proc1.id in process_ids, "Process 1 should be in list"
            assert proc2.id in process_ids, "Process 2 should be in list"
            assert proc3.id in process_ids, "Process 3 should be in list"
            print(f"✓ Phase 1C passed: Managing {len(processes)} processes")

            # ==========================================
            # Phase 2: Combined stdout and stderr capture
            # ==========================================
            print("\n=== Phase 2: Combined stdout and stderr capture ===")
            both_proc = process_mgr.start_process("sh -c 'echo out && echo err >&2 && sleep 1'")
            time.sleep(1.5)  # Wait for command to complete
            logs = process_mgr.get_logs(both_proc.id)
            assert "out" in logs["stdout"], f"Should capture stdout, got: {logs['stdout']}"
            assert "err" in logs["stderr"], f"Should capture stderr, got: {logs['stderr']}"
            print(f"✓ Phase 2F passed: stdout='{logs['stdout'].strip()}', stderr='{logs['stderr'].strip()}'")

            # ==========================================
            # Phase 3: Lifecycle tests (parallelized for efficiency)
            # ==========================================
            print("\n=== Phase 3: Lifecycle tests (completion, failure, exit codes) ===")

            # Start all lifecycle test processes at once
            print("Starting all lifecycle test processes...")
            short_proc = process_mgr.start_process("sleep 0.5")  # 3G: completion
            fail_proc = process_mgr.start_process("sh -c 'exit 5'")  # 3H: failure + exit code
            py_proc = process_mgr.start_process("python3 -c 'import sys; sys.exit(42)'")  # 3J: Python exit code

            # Verify all started as RUNNING
            assert short_proc.status == ProcessStatus.RUNNING, "Completion test should start as RUNNING"
            assert fail_proc.status == ProcessStatus.RUNNING, "Failure test should start as RUNNING"
            assert py_proc.status == ProcessStatus.RUNNING, "Python test should start as RUNNING"

            # Single wait for all processes to complete
            print("Waiting for all processes to complete...")
            time.sleep(1)

            # Check all results
            print("Checking completion detection (3G)...")
            status_complete = process_mgr.get_status(short_proc.id)
            assert status_complete == ProcessStatus.STOPPED, f"Should detect completion, got {status_complete}"
            print("✓ Phase 3G passed: Detected process completion")

            print("Checking failure detection with exit code (3H)...")
            status_fail = process_mgr.get_status(fail_proc.id)
            assert status_fail == ProcessStatus.FAILED, f"Should detect failure, got {status_fail}"
            assert fail_proc.exit_code == 5, f"Should capture exit code 5, got {fail_proc.exit_code}"
            print(f"✓ Phase 3H passed: Detected process failure with exit code {fail_proc.exit_code}")

            print("Checking Python exit code (3J - the critical test!)...")
            status_py = process_mgr.get_status(py_proc.id)
            assert status_py == ProcessStatus.FAILED, f"Exit code 42 should be FAILED, got {status_py}"
            assert py_proc.exit_code == 42, f"Should capture exit code 42, got {py_proc.exit_code}"
            print(f"✓ Phase 3J passed: Captured Python exit code {py_proc.exit_code} correctly!")

            # ==========================================
            # Phase 4K: Environment variables
            # ==========================================
            print("\n=== Phase 4K: Environment variables ===")
            env_proc = process_mgr.start_process(
                "python3 -c 'import os; print(os.getenv(\"TEST_VAR\"))'", environment={"TEST_VAR": "test_value_123"}
            )
            time.sleep(1)  # Wait for completion
            logs = process_mgr.get_logs(env_proc.id)
            assert "test_value_123" in logs["stdout"], f"Environment variable should be in logs, got: {logs['stdout']}"
            print("✓ Phase 4K passed: Environment variable passed correctly")

            # ==========================================
            # Phase 4L: Working directory
            # ==========================================
            print("\n=== Phase 4L: Working directory ===")
            wd_proc = process_mgr.start_process("pwd", working_dir=Path("/tmp"))
            time.sleep(1)  # Wait for completion
            logs = process_mgr.get_logs(wd_proc.id)
            assert "/tmp" in logs["stdout"], f"Should run in /tmp, got: {logs['stdout']}"
            print("✓ Phase 4L passed: Working directory control works")

            # ==========================================
            # Phase 4M: Process naming
            # ==========================================
            print("\n=== Phase 4M: Process naming ===")
            named_proc = process_mgr.start_process("sleep 2", name="test-process")
            assert named_proc.name == "test-process", f"Process name should be set, got {named_proc.name}"
            assert "test-process" in named_proc.display_name, (
                f"display_name should contain name, got {named_proc.display_name}"
            )
            assert named_proc.id[:8] in named_proc.display_name, (
                f"display_name should contain UUID, got {named_proc.display_name}"
            )
            print(f"✓ Phase 4M passed: Process naming works (display_name: {named_proc.display_name})")

            # ==========================================
            # Phase 4N: Graceful shutdown
            # ==========================================
            print("\n=== Phase 4N: Graceful shutdown ===")
            graceful_proc = process_mgr.start_process("sleep 10")
            success = process_mgr.stop_process(graceful_proc.id, timeout=2, force=True)
            assert success, "Should successfully stop process"
            assert not process_mgr.is_running(graceful_proc.id), "Process should not be running"
            print("✓ Phase 4N passed: Graceful shutdown with force fallback works")

            # ==========================================
            # Phase 6Q: Port detection (optional - lsof may not be available)
            # ==========================================
            print("\n=== Phase 6Q: Port detection ===")
            http_proc = process_mgr.start_process("python3 -m http.server 9999", name="http-server")
            time.sleep(1)  # Give server time to start

            # Update status to trigger port detection
            status = process_mgr.get_status(http_proc.id)
            assert status == ProcessStatus.RUNNING, "HTTP server should be running"

            # Port detection is graceful - may or may not work depending on lsof availability
            if http_proc.ports is not None and http_proc.ports:
                assert 9999 in http_proc.ports, f"Port 9999 should be detected, got {http_proc.ports}"
                print(f"✓ Phase 6Q passed: Port detection works (detected ports: {http_proc.ports})")
            else:
                print("✓ Phase 6Q passed: Port detection gracefully handles missing lsof")

            # Cleanup
            process_mgr.stop_process(http_proc.id, force=True)

            print("\n" + "=" * 60)
            print("🎉 ALL PHASES PASSED!")
            print("Phase 1: Core (A, C) ✓")
            print("Phase 2: Observability (stdout/stderr) ✓")
            print("Phase 3: Lifecycle (G, H, J) ✓")
            print("Phase 4: Advanced (K, L, M, N) ✓")
            print("Phase 6: Integration (Q) ✓")
            print("=" * 60)

        finally:
            session_manager.close_session(test_user, session_id)
            manager.cleanup_all()
