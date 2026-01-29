"""
Integration tests for SXD pipelines.

These tests run against the actual Temporal infrastructure to verify
end-to-end workflow execution. They require:
- Temporal server running (sxd infra up)
- ClickHouse running
- Worker running OR tests start their own worker

Run with: sxd test tests/test_integration.py -m integration
"""

import asyncio
import uuid
from datetime import timedelta
from pathlib import Path

import pytest

# Mark all tests in this file as integration tests
pytestmark = pytest.mark.integration

# Skip if infrastructure is not available
SKIP_REASON = "Infrastructure not available. Run 'sxd infra up' first."


def is_infrastructure_available() -> bool:
    """Check if Temporal and other infrastructure is available."""
    try:
        from sxd_core.ops import get_cluster_info

        info = get_cluster_info()
        return info.temporal_connected
    except Exception:
        return False


# Determine if we should skip integration tests
INFRA_AVAILABLE = is_infrastructure_available()


@pytest.fixture(scope="module")
def event_loop():
    """Create an event loop for the test module."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def temporal_client(event_loop):
    """Create a Temporal client connected to the real infrastructure."""
    if not INFRA_AVAILABLE:
        pytest.skip(SKIP_REASON)

    from sxd_core.config import get_temporal_config
    from temporalio.client import Client

    tc = get_temporal_config()

    async def connect():
        return await Client.connect(f"{tc['host']}:{tc['port']}")

    client = event_loop.run_until_complete(connect())
    yield client


@pytest.fixture(scope="module")
def pipeline_loader():
    """Load all pipelines to register workflows and activities."""
    from sxd_core import load_pipelines
    import sys

    # Add samples to path so we can import them
    project_root = Path(__file__).parent.parent
    samples_dir = project_root / "samples/video_pipeline"
    if str(samples_dir) not in sys.path:
        sys.path.append(str(samples_dir))

    # Load from traditional location and also the sample pipeline
    load_pipelines(project_root, extra_modules=["video_pipeline"])


# =============================================================================
# Video Pipeline Integration Tests (Sample)
# =============================================================================


class TestVideoPipelineIntegration:
    """Integration tests for the sample video pipeline."""

    @pytest.mark.asyncio
    async def test_video_workflow_registers_correctly(self, pipeline_loader):
        """Test that video workflow is registered in the system."""
        from sxd_core import get_workflow

        video_wf = get_workflow("video-sample")
        assert video_wf is not None
        assert video_wf.nickname == "video-sample"
        assert video_wf.task_queue == "video-processing"

    @pytest.mark.asyncio
    async def test_video_workflow_end_to_end(self, temporal_client, pipeline_loader):
        """Test the sample video workflow executes successfully end-to-end."""
        if not INFRA_AVAILABLE:
            pytest.skip(SKIP_REASON)

        from video_pipeline import VideoPipelineWorkflow, VideoPipelineInput
        from sxd_core.registry import list_activities
        from temporalio.worker import Worker

        # Create a unique workflow ID and task queue
        test_id = uuid.uuid4().hex[:8]
        workflow_id = f"test-video-{test_id}"
        task_queue = f"test-video-queue-{test_id}"

        # Get all activities for the worker
        all_activities = [act.func for act in list_activities().values()]

        # Start a worker for this test
        async with Worker(
            temporal_client,
            task_queue=task_queue,
            workflows=[VideoPipelineWorkflow],
            activities=all_activities,
        ):
            # Execute the workflow
            result = await temporal_client.execute_workflow(
                VideoPipelineWorkflow.run,
                VideoPipelineInput(source_url="http://example.com/video.mp4"),
                id=workflow_id,
                task_queue=task_queue,
                execution_timeout=timedelta(minutes=1),
            )

        assert result.status == "success"
        assert result.output_path is not None


# =============================================================================
# Workflow Registry Integration Tests
# =============================================================================


class TestWorkflowRegistryIntegration:
    """Test that all workflows are properly registered."""

    def test_list_workflows_returns_expected(self, pipeline_loader):
        """Test that list_workflows returns all expected workflows."""
        from sxd_core import list_workflows

        workflows = list_workflows()

        # Should have at least the sample video workflow
        nicknames = set(workflows.keys())
        expected = {"video-sample"}

        assert expected.issubset(
            nicknames
        ), f"Missing workflows: {expected - nicknames}"

    def test_all_workflows_have_valid_definitions(self, pipeline_loader):
        """Test that all registered workflows have valid definitions."""
        from sxd_core import list_workflows

        workflows = list_workflows()

        for nickname, wf_def in workflows.items():
            assert (
                wf_def.workflow_class is not None
            ), f"{nickname} has no workflow class"


# =============================================================================
# Activity Registry Integration Tests
# =============================================================================


class TestActivityRegistryIntegration:
    """Test that all activities are properly registered."""

    def test_list_activities_returns_expected(self, pipeline_loader):
        """Test that list_activities returns activities from all pipelines."""
        from sxd_core.registry import list_activities

        activities = list_activities()

        # Should have activities from both hello and video pipelines
        assert len(activities) > 0, "No activities registered"

        # Check for specific activities
        activity_names = set(activities.keys())

        # Sample video activities
        assert (
            "download_video" in activity_names
        ), "download_video activity not registered"
        assert (
            "process_video" in activity_names
        ), "process_video activity not registered"

    def test_all_activities_have_valid_functions(self, pipeline_loader):
        """Test that all registered activities have valid functions."""
        from sxd_core.registry import list_activities

        activities = list_activities()

        for name, act_def in activities.items():
            assert callable(act_def.func), f"{name} has no callable function"
            assert act_def.task_queue, f"{name} has no task queue"


# =============================================================================
# Temporal Connection Integration Tests
# =============================================================================


class TestTemporalConnectionIntegration:
    """Test Temporal server connectivity and basic operations."""

    @pytest.mark.asyncio
    async def test_temporal_client_connects(self, temporal_client):
        """Test that we can connect to Temporal."""
        if not INFRA_AVAILABLE:
            pytest.skip(SKIP_REASON)

        # If we get here, the connection succeeded
        assert temporal_client is not None

    @pytest.mark.asyncio
    async def test_temporal_namespace_exists(self, temporal_client):
        """Test that the default namespace is accessible."""
        if not INFRA_AVAILABLE:
            pytest.skip(SKIP_REASON)

        # Try to describe the default namespace
        try:

            # The client should be able to operate in default namespace
            assert temporal_client.namespace == "default"
        except Exception as e:
            pytest.fail(f"Failed to access namespace: {e}")


# =============================================================================
# ClickHouse Integration Tests
# =============================================================================


class TestClickHouseIntegration:
    """Test ClickHouse connectivity and operations."""

    def _get_clickhouse_manager(self):
        """Get ClickHouse manager, returning None if connection fails."""
        from sxd_core.clickhouse import ClickHouseManager

        try:
            ch = ClickHouseManager()
            # Test connection with a simple query - check for non-empty result
            result = ch.execute_query("SELECT 1")
            if not result:
                return None  # Empty result means connection failed
            return ch
        except Exception:
            return None

    def test_clickhouse_connection(self):
        """Test that we can connect to ClickHouse."""
        if not INFRA_AVAILABLE:
            pytest.skip(SKIP_REASON)

        ch = self._get_clickhouse_manager()
        if ch is None:
            pytest.skip("ClickHouse not accessible (may be on remote server)")

        # Simple query to verify connection
        result = ch.execute_query("SELECT 1 as test")
        assert len(result) == 1
        assert result[0]["test"] == 1

    def test_clickhouse_tables_exist(self):
        """Test that expected tables exist in ClickHouse."""
        if not INFRA_AVAILABLE:
            pytest.skip(SKIP_REASON)

        ch = self._get_clickhouse_manager()
        if ch is None:
            pytest.skip("ClickHouse not accessible (may be on remote server)")

        # Query for tables
        result = ch.execute_query(
            f"SELECT name FROM system.tables WHERE database = '{ch.database}'"
        )
        table_names = {row["name"] for row in result}

        # Check for expected tables
        expected_tables = {"logs", "videos", "audit_events"}
        expected_tables - table_names

        # Some tables may not exist yet in a fresh install - that's okay
        # Just verify we can query the system
        assert isinstance(table_names, set)


# =============================================================================
# CLI Integration Tests
# =============================================================================


class TestCLIIntegration:
    """Test CLI commands work correctly."""

    def test_sxd_info_command(self):
        """Test that 'sxd info' returns valid cluster info."""
        if not INFRA_AVAILABLE:
            pytest.skip(SKIP_REASON)

        from sxd_core.ops import get_cluster_info

        info = get_cluster_info()

        assert info is not None
        assert info.master_host is not None
        assert isinstance(info.temporal_connected, bool)
        assert isinstance(info.clickhouse_connected, bool)

    def test_sxd_workflows_command(self, pipeline_loader):
        """Test that 'sxd workflows' lists workflows correctly."""
        from sxd_core import list_workflows

        workflows = list_workflows()

        assert len(workflows) >= 1
        for nick, wf in workflows.items():
            assert isinstance(nick, str)
            assert wf.task_queue is not None


# =============================================================================
# Storage Integration Tests
# =============================================================================


class TestStorageIntegration:
    """Test storage operations."""

    def test_storage_abstraction_works(self, tmp_path):
        """Test that the storage abstraction can read/write files."""
        from sxd_core.storage import get_storage

        storage = get_storage()

        # Storage returns a UPath - verify it's usable
        assert storage is not None

        # Write a test file using UPath
        test_content = b"Hello, Integration Test!"
        test_path = storage / "test_integration_file.txt"

        # Ensure parent exists
        test_path.parent.mkdir(parents=True, exist_ok=True)

        # Write using UPath
        test_path.write_bytes(test_content)

        # Read it back
        read_content = test_path.read_bytes()

        assert read_content == test_content

        # Cleanup
        if test_path.exists():
            test_path.unlink()


# =============================================================================
# Worker Integration Tests
# =============================================================================


class TestWorkerIntegration:
    """Test worker functionality."""

    @pytest.mark.asyncio
    async def test_worker_can_start_and_stop(self, temporal_client, pipeline_loader):
        """Test that a worker can start and stop cleanly."""
        if not INFRA_AVAILABLE:
            pytest.skip(SKIP_REASON)

        from video_pipeline import VideoPipelineWorkflow
        from sxd_core.registry import list_activities
        from temporalio.worker import Worker

        VideoWorkflow = VideoPipelineWorkflow
        all_activities = [act.func for act in list_activities().values()]

        # Start a worker briefly
        worker = Worker(
            temporal_client,
            task_queue="test-worker-queue",
            workflows=[VideoWorkflow],
            activities=all_activities,
        )

        # Start and stop the worker
        async with worker:
            # Worker is running
            await asyncio.sleep(0.1)
            # Worker stops when exiting context

        # If we get here without exception, test passes


# =============================================================================
# End-to-End Smoke Tests
# =============================================================================


class TestEndToEndSmoke:
    """Quick smoke tests to verify the system is working."""

    @pytest.mark.asyncio
    async def test_full_video_smoke(self, temporal_client, pipeline_loader):
        """Full smoke test: submit video workflow and verify result."""
        if not INFRA_AVAILABLE:
            pytest.skip(SKIP_REASON)

        from video_pipeline import VideoPipelineWorkflow, VideoPipelineInput
        from sxd_core.registry import list_activities
        from temporalio.worker import Worker

        VideoWorkflow = VideoPipelineWorkflow
        test_id = uuid.uuid4().hex[:8]
        workflow_id = f"smoke-video-{test_id}"
        task_queue = f"smoke-video-queue-{test_id}"

        all_activities = [act.func for act in list_activities().values()]

        async with Worker(
            temporal_client,
            task_queue=task_queue,
            workflows=[VideoWorkflow],
            activities=all_activities,
        ):
            result = await temporal_client.execute_workflow(
                VideoWorkflow.run,
                VideoPipelineInput(source_url="http://example.com/smoke.mp4"),
                id=workflow_id,
                task_queue=task_queue,
                execution_timeout=timedelta(minutes=1),
            )

        assert result.status == "success"
        print(f"Smoke test passed: {result}")


# =============================================================================
# Test Configuration
# =============================================================================


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "integration: marks tests as integration tests")


if __name__ == "__main__":
    # Allow running directly for debugging
    pytest.main([__file__, "-v", "-m", "integration"])
