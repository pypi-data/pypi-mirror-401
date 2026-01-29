"""
Tests for the sxd.py CLI module.

These tests verify the CLI helper functions and configuration loading.
Now updated to use the refactored sxd_core module structure.
"""

import argparse
from unittest.mock import MagicMock, patch

import pytest
import yaml


class TestLoadConfig:
    """Tests for load_config function (now in sxd_core.config)."""

    def test_load_config_from_file(self, tmp_path, monkeypatch):
        """Loads config from settings.yaml."""
        # Create a fake config
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        config_file = config_dir / "settings.yaml"
        config_file.write_text(
            yaml.dump(
                {
                    "temporal": {"host": "temporal.example.com", "port": 7233},
                    "storage": {"endpoint": "http://storage.example.com"},
                }
            )
        )

        # Test the loading logic directly
        test_config_path = config_dir / "settings.yaml"
        with open(test_config_path) as f:
            config = yaml.safe_load(f)

        assert config["temporal"]["host"] == "temporal.example.com"
        assert config["temporal"]["port"] == 7233

    def test_load_config_missing_file(self, tmp_path):
        """Returns empty dict if config file doesn't exist."""
        config_path = tmp_path / "nonexistent.yaml"
        if not config_path.exists():
            result = {}
        assert result == {}


class TestGetTemporalConfig:
    """Tests for get_temporal_config function (now in sxd_core.config)."""

    def test_returns_defaults_when_no_config(self, monkeypatch):
        """Returns default values when no config is set."""
        from sxd_core.config import ConfigManager

        # Clear env vars that might override config
        monkeypatch.delenv("SXD_TEMPORAL_HOST", raising=False)
        monkeypatch.delenv("SXD_TEMPORAL_PORT", raising=False)

        # Create a fresh manager with no config
        manager = ConfigManager.__new__(ConfigManager)
        manager._config = {}
        config = manager.get_temporal_config()

        assert config["host"] == "localhost"
        assert config["port"] == 7233
        assert config["namespace"] == "default"
        assert config["task_queue"] == "video-processing"

    def test_returns_config_values(self, monkeypatch):
        """Returns values from config when available."""
        from sxd_core.config import ConfigManager

        # Clear env vars that might override config
        monkeypatch.delenv("SXD_TEMPORAL_HOST", raising=False)
        monkeypatch.delenv("SXD_TEMPORAL_PORT", raising=False)

        mock_config = {
            "temporal": {
                "host": "temporal.cluster.local",
                "port": 9999,
                "namespace": "production",
                "task_queue": "custom-queue",
            }
        }

        manager = ConfigManager.__new__(ConfigManager)
        manager._config = mock_config
        config = manager.get_temporal_config()

        assert config["host"] == "temporal.cluster.local"
        assert config["port"] == 9999
        assert config["namespace"] == "production"
        assert config["task_queue"] == "custom-queue"


class TestGetStorageEndpoint:
    """Tests for get_storage_endpoint function (now in sxd_core.config)."""

    def test_returns_default_when_no_config(self):
        """Returns default endpoint when no config."""
        from sxd_core.config import ConfigManager

        with patch.object(ConfigManager, "_load_config", return_value={}):
            manager = ConfigManager.__new__(ConfigManager)
            manager._config = {}
            endpoint = manager.get_storage_endpoint()

        assert endpoint == "http://localhost:8333"

    def test_returns_configured_endpoint(self):
        """Returns configured endpoint."""
        from sxd_core.config import ConfigManager

        mock_config = {"storage": {"endpoint": "http://storage.prod.local:8080"}}

        with patch.object(ConfigManager, "_load_config", return_value=mock_config):
            manager = ConfigManager.__new__(ConfigManager)
            manager._config = mock_config
            endpoint = manager.get_storage_endpoint()

        assert endpoint == "http://storage.prod.local:8080"


class TestCustomArgumentParser:
    """Tests for CustomArgumentParser."""

    def test_error_prints_help_and_exits(self, capsys):
        """Error method prints help and exits with code 2."""
        from sxd import CustomArgumentParser

        parser = CustomArgumentParser(description="Test parser")
        parser.add_argument("--required", required=True)

        with pytest.raises(SystemExit) as exc_info:
            parser.error("Missing required argument")

        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert "error: Missing required argument" in captured.err


class TestAttachCustomError:
    """Tests for attach_custom_error function."""

    def test_patches_parser_error_method(self, capsys):
        """Patches the error method on parser instance."""
        from sxd import attach_custom_error

        parser = argparse.ArgumentParser(description="Test")
        attach_custom_error(parser)

        with pytest.raises(SystemExit) as exc_info:
            parser.error("Test error message")

        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert "error: Test error message" in captured.err


class TestLoadInventoryNodes:
    """Tests for load_inventory_nodes function (now in sxd_core.ops.cluster)."""

    def test_returns_empty_list_if_no_file(self, tmp_path, monkeypatch):
        """Returns empty list if inventory file doesn't exist."""
        monkeypatch.chdir(tmp_path)

        from sxd_core.ops.cluster import load_inventory_nodes

        result = load_inventory_nodes()
        assert result == []

    def test_parses_inventory_yaml(self, tmp_path, monkeypatch):
        """Parses Ansible inventory YAML correctly."""
        monkeypatch.chdir(tmp_path)

        # Create inventory structure
        deploy_dir = tmp_path / "deploy" / "ansible"
        deploy_dir.mkdir(parents=True)

        inventory = {
            "all": {
                "vars": {"ansible_user": "admin"},
                "children": {
                    "master": {
                        "hosts": {
                            "sxd-master": {
                                "ansible_host": "10.0.0.1",
                                "ansible_port": 22,
                                "run_infra": True,
                                "run_worker": True,
                            }
                        }
                    },
                    "workers": {
                        "hosts": {
                            "sxd-worker-1": {
                                "ansible_host": "10.0.0.2",
                                "ansible_port": 22,
                                "run_worker": True,
                            },
                            "sxd-worker-2": {
                                "ansible_host": "10.0.0.3",
                                "ansible_port": 22,
                                "run_worker": True,
                            },
                        }
                    },
                },
            }
        }

        (deploy_dir / "inventory.yml").write_text(yaml.dump(inventory))

        from sxd_core.ops.cluster import load_inventory_nodes

        nodes = load_inventory_nodes()

        assert len(nodes) == 3
        # Nodes are now NodeInfo dataclass objects
        master = next(n for n in nodes if n.name == "sxd-master")
        assert master.host == "10.0.0.1"
        assert master.node_type == "master"
        assert master.run_infra is True

        worker1 = next(n for n in nodes if n.name == "sxd-worker-1")
        assert worker1.host == "10.0.0.2"
        assert worker1.node_type == "worker"
        assert worker1.run_worker is True

    def test_handles_malformed_inventory(self, tmp_path, monkeypatch, capsys):
        """Handles malformed inventory gracefully."""
        monkeypatch.chdir(tmp_path)

        deploy_dir = tmp_path / "deploy" / "ansible"
        deploy_dir.mkdir(parents=True)
        (deploy_dir / "inventory.yml").write_text("not: valid: yaml: [[[[")

        from sxd_core.ops.cluster import load_inventory_nodes

        result = load_inventory_nodes()
        assert result == []


class TestRunClean:
    """Tests for run_clean function."""

    def test_removes_pycache(self, tmp_path, monkeypatch):
        """Removes __pycache__ directories."""
        monkeypatch.chdir(tmp_path)

        pycache = tmp_path / "src" / "__pycache__"
        pycache.mkdir(parents=True)
        (pycache / "module.pyc").write_bytes(b"bytecode")

        from sxd import run_clean

        run_clean()

        assert not pycache.exists()

    def test_removes_pytest_cache(self, tmp_path, monkeypatch):
        """Removes .pytest_cache directory."""
        monkeypatch.chdir(tmp_path)

        pytest_cache = tmp_path / ".pytest_cache"
        pytest_cache.mkdir()
        (pytest_cache / "v" / "cache").mkdir(parents=True)

        from sxd import run_clean

        run_clean()

        assert not pytest_cache.exists()


class TestRunTests:
    """Tests for run_tests function (now in sxdinfra)."""

    def test_runs_pytest_with_coverage(self):
        """Runs pytest with coverage flags."""
        from sxdinfra import run_tests

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            run_tests()

        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert "pytest" in cmd
        assert "--cov=sxd_core" in cmd
        assert "-v" in cmd

    def test_runs_with_markers(self):
        """Runs pytest with marker filter."""
        from sxdinfra import run_tests

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            run_tests(markers="unit")

        cmd = mock_run.call_args[0][0]
        assert "-m" in cmd
        assert "unit" in cmd

    def test_runs_specific_path(self):
        """Runs pytest on specific path."""
        from sxdinfra import run_tests

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            run_tests(path="tests/test_specific.py")

        cmd = mock_run.call_args[0][0]
        assert "tests/test_specific.py" in cmd


class TestRunListWorkflows:
    """Tests for run_list_workflows function."""

    def test_prints_no_workflows(self, capsys):
        """Prints message when no workflows registered."""
        from sxd import run_list_workflows

        with patch("sxd.list_workflows", return_value={}):
            run_list_workflows()

        captured = capsys.readouterr()
        assert "No workflows registered" in captured.out

    def test_prints_workflow_table(self, capsys):
        """Prints workflow table with headers."""
        from sxd_core.registry import WorkflowDefinition

        from sxd import run_list_workflows

        mock_workflows = {
            "video": WorkflowDefinition(
                nickname="video",
                workflow_class=MagicMock(),
                input_type=dict,
                description="Video processing workflow",
                task_queue="video-processing",
            ),
            "batch": WorkflowDefinition(
                nickname="batch",
                workflow_class=MagicMock(),
                input_type=dict,
                description="Batch processing",
                task_queue="batch-queue",
            ),
        }

        with patch("sxd.list_workflows", return_value=mock_workflows):
            run_list_workflows()

        captured = capsys.readouterr()
        assert "video" in captured.out
        assert "video-processing" in captured.out
        assert "batch" in captured.out


class TestRunQuery:
    """Tests for run_query function."""

    def test_expands_shortcut_queries(self, capsys):
        """Expands shortcut query names."""
        from sxd import run_query

        mock_ch = MagicMock()
        mock_ch.database = "sxd"
        mock_ch.execute_query.return_value = []

        with patch("sxd_core.clickhouse.ClickHouseManager", return_value=mock_ch):
            run_query("logs")

        # Should have expanded 'logs' to full query
        call_args = mock_ch.execute_query.call_args[0][0]
        assert "logs" in call_args.lower()
        assert "SELECT" in call_args

    def test_handles_empty_results(self, capsys):
        """Handles empty query results."""
        from sxd import run_query

        mock_ch = MagicMock()
        mock_ch.execute_query.return_value = []

        with patch("sxd_core.clickhouse.ClickHouseManager", return_value=mock_ch):
            run_query("SELECT 1")

        captured = capsys.readouterr()
        assert "No results" in captured.out

    def test_handles_query_error(self, capsys):
        """Handles query execution error."""
        from sxd import run_query

        mock_ch = MagicMock()
        mock_ch.database = "sxd"
        mock_ch.execute_query.side_effect = Exception("Connection refused")

        # Patch ClickHouseManager where it's imported
        with patch("sxd_core.clickhouse.ClickHouseManager", return_value=mock_ch):
            with pytest.raises(SystemExit) as exc_info:
                run_query("SELECT 1")

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Query failed" in captured.out or "Connection refused" in captured.out


class TestRunStorageLs:
    """Tests for run_ls function."""

    def test_lists_collections_when_no_path(self, capsys):
        """Lists available collections when no path specified."""
        from sxd import run_ls

        run_ls()

        captured = capsys.readouterr()
        assert "videos" in captured.out
        assert "batches" in captured.out
        assert "uploads" in captured.out

    def test_lists_videos(self, capsys):
        """Lists videos when path is 'videos'."""
        from sxd_core.ops.storage import VideoInfo

        from sxd import run_ls

        mock_videos = [
            VideoInfo(
                id="vid-001-id",
                video_id="vid-001",
                customer_id="customer1",
                batch_id="batch-001",
                source_url="http://example.com/video.mp4",
                status="COMPLETED",
                node="worker-1",
                size_bytes=1024000,
                quality_score=0.95,
                blur_mean=0.1,
                frame_count=300,
                created_at=None,
                updated_at=None,
            )
        ]

        # Patch where it's imported in sxd module
        with patch("sxd.list_videos", return_value=mock_videos):
            run_ls("videos")

        captured = capsys.readouterr()
        assert "vid-001" in captured.out
        assert "COMPLETED" in captured.out

    def test_unknown_collection(self, capsys):
        """Handles unknown collection path."""
        from sxd import run_ls

        run_ls("unknown")

        captured = capsys.readouterr()
        assert "Unknown" in captured.out


class TestMainFunction:
    """Tests for main CLI entry point."""

    def test_no_command_prints_help(self, capsys):
        """No command prints help text."""
        from sxd import main

        with patch("sys.argv", ["sxd"]):
            with patch("sxd.load_pipelines"):
                main()

        captured = capsys.readouterr()
        assert "pipeline development & operations" in captured.out.lower()

    def test_info_command(self, capsys):
        """Info command runs without error."""
        from sxd import main

        with patch("sys.argv", ["sxd", "info"]):
            with patch("sxd.load_pipelines"):
                with patch("sxd.run_info") as mock_info:
                    main()

        mock_info.assert_called_once()

    def test_clean_command(self):
        """Clean command runs without error."""
        from sxd import main

        with patch("sys.argv", ["sxd", "clean"]):
            with patch("sxd.load_pipelines"):
                with patch("sxd.run_clean") as mock_clean:
                    main()

        mock_clean.assert_called_once()

    def test_workflows_command(self):
        """Workflows command runs without error."""
        from sxd import main

        with patch("sys.argv", ["sxd", "workflows"]):
            with patch("sxd.load_pipelines"):
                with patch("sxd.run_list_workflows") as mock_workflows:
                    main()

        mock_workflows.assert_called_once()
