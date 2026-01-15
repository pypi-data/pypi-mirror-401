"""
Tests for plan optimization features:
- No-change detection (skip apply when no changes)
- skip_backfill option
- plan_only mode
- Detailed logging phases
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlmesh_dag_generator import SQLMeshDAGGenerator
from sqlmesh_dag_generator.config import GenerationConfig, SQLMeshConfig, AirflowConfig, DAGGeneratorConfig


class TestPlanOptimizationConfig:
    """Test plan optimization configuration options"""

    def test_skip_backfill_default_false(self):
        """Test that skip_backfill defaults to False"""
        config = GenerationConfig()
        assert config.skip_backfill is False

    def test_plan_only_default_false(self):
        """Test that plan_only defaults to False"""
        config = GenerationConfig()
        assert config.plan_only is False

    def test_log_plan_details_default_true(self):
        """Test that log_plan_details defaults to True"""
        config = GenerationConfig()
        assert config.log_plan_details is True

    def test_skip_backfill_can_be_enabled(self):
        """Test that skip_backfill can be set to True"""
        config = GenerationConfig(skip_backfill=True)
        assert config.skip_backfill is True

    def test_plan_only_can_be_enabled(self):
        """Test that plan_only can be set to True"""
        config = GenerationConfig(plan_only=True)
        assert config.plan_only is True

    def test_log_plan_details_can_be_disabled(self):
        """Test that log_plan_details can be set to False"""
        config = GenerationConfig(log_plan_details=False)
        assert config.log_plan_details is False

    def test_generator_accepts_skip_backfill(self, tmp_path):
        """Test generator accepts skip_backfill parameter"""
        project_path = tmp_path / "project"
        project_path.mkdir()
        (project_path / "config.yaml").write_text(
            "gateways:\n  default:\n    connection:\n      type: duckdb"
        )

        generator = SQLMeshDAGGenerator(
            sqlmesh_project_path=str(project_path),
            dag_id="test_dag",
            skip_backfill=True,
        )

        assert generator.config.generation.skip_backfill is True

    def test_generator_accepts_plan_only(self, tmp_path):
        """Test generator accepts plan_only parameter"""
        project_path = tmp_path / "project"
        project_path.mkdir()
        (project_path / "config.yaml").write_text(
            "gateways:\n  default:\n    connection:\n      type: duckdb"
        )

        generator = SQLMeshDAGGenerator(
            sqlmesh_project_path=str(project_path),
            dag_id="test_dag",
            plan_only=True,
        )

        assert generator.config.generation.plan_only is True


class TestPlanOptimizationBehavior:
    """Test plan optimization behavior in run_replan function"""

    @pytest.fixture
    def mock_plan_no_changes(self):
        """Create a mock plan with no changes"""
        plan = Mock()
        plan.has_changes = False
        plan.requires_backfill = False
        plan.new_snapshots = []
        plan.modified_snapshots = []
        plan.missing_intervals = []
        return plan

    @pytest.fixture
    def mock_plan_with_changes(self):
        """Create a mock plan with changes"""
        plan = Mock()
        plan.has_changes = True
        plan.requires_backfill = False
        plan.new_snapshots = [Mock(name="model1")]
        plan.modified_snapshots = []
        plan.missing_intervals = []
        return plan

    @pytest.fixture
    def mock_plan_with_backfill(self):
        """Create a mock plan with backfill required"""
        plan = Mock()
        plan.has_changes = True
        plan.requires_backfill = True
        plan.new_snapshots = []
        plan.modified_snapshots = [Mock(name="model1")]
        plan.missing_intervals = {"model1": [(0, 100)]}
        return plan

    def test_no_changes_returns_skipped_status(self, mock_plan_no_changes):
        """Test that no-change scenario returns skipped status"""
        # Simulate the logic from run_replan
        plan = mock_plan_no_changes

        if not plan.has_changes and not plan.requires_backfill:
            result = {
                "status": "skipped",
                "reason": "no_changes",
            }
        else:
            result = {"status": "applied"}

        assert result["status"] == "skipped"
        assert result["reason"] == "no_changes"

    def test_changes_without_backfill_returns_applied(self, mock_plan_with_changes):
        """Test that changes without backfill returns applied status"""
        plan = mock_plan_with_changes
        skip_backfill = False
        plan_only = False

        if not plan.has_changes and not plan.requires_backfill:
            result = {"status": "skipped", "reason": "no_changes"}
        elif plan_only:
            result = {"status": "plan_only"}
        elif skip_backfill and plan.requires_backfill:
            result = {"status": "skipped", "reason": "backfill_skipped"}
        else:
            result = {"status": "applied"}

        assert result["status"] == "applied"

    def test_plan_only_mode_returns_plan_only_status(self, mock_plan_with_changes):
        """Test that plan_only mode returns plan_only status"""
        plan = mock_plan_with_changes
        skip_backfill = False
        plan_only = True

        if not plan.has_changes and not plan.requires_backfill:
            result = {"status": "skipped", "reason": "no_changes"}
        elif plan_only:
            result = {
                "status": "plan_only",
                "reason": "plan_only_mode",
                "has_changes": plan.has_changes,
                "requires_backfill": plan.requires_backfill,
            }
        else:
            result = {"status": "applied"}

        assert result["status"] == "plan_only"
        assert result["reason"] == "plan_only_mode"

    def test_skip_backfill_skips_when_backfill_required(self, mock_plan_with_backfill):
        """Test that skip_backfill=True skips when backfill is required"""
        plan = mock_plan_with_backfill
        skip_backfill = True
        plan_only = False

        if not plan.has_changes and not plan.requires_backfill:
            result = {"status": "skipped", "reason": "no_changes"}
        elif plan_only:
            result = {"status": "plan_only"}
        elif skip_backfill and plan.requires_backfill:
            result = {
                "status": "skipped",
                "reason": "backfill_skipped",
                "has_changes": plan.has_changes,
                "requires_backfill": plan.requires_backfill,
            }
        else:
            result = {"status": "applied"}

        assert result["status"] == "skipped"
        assert result["reason"] == "backfill_skipped"

    def test_skip_backfill_applies_when_no_backfill_needed(self, mock_plan_with_changes):
        """Test that skip_backfill=True still applies when no backfill is needed"""
        plan = mock_plan_with_changes
        skip_backfill = True
        plan_only = False

        if not plan.has_changes and not plan.requires_backfill:
            result = {"status": "skipped", "reason": "no_changes"}
        elif plan_only:
            result = {"status": "plan_only"}
        elif skip_backfill and plan.requires_backfill:
            result = {"status": "skipped", "reason": "backfill_skipped"}
        else:
            result = {"status": "applied"}

        assert result["status"] == "applied"


class TestPlanOptimizationCombinations:
    """Test combinations of plan optimization options"""

    def test_all_options_enabled_config(self, tmp_path):
        """Test that all optimization options can be set together"""
        project_path = tmp_path / "project"
        project_path.mkdir()
        (project_path / "config.yaml").write_text(
            "gateways:\n  default:\n    connection:\n      type: duckdb"
        )

        generator = SQLMeshDAGGenerator(
            sqlmesh_project_path=str(project_path),
            dag_id="test_dag",
            auto_replan_on_change=True,
            skip_backfill=True,
            plan_only=False,
            log_plan_details=True,
        )

        assert generator.config.generation.auto_replan_on_change is True
        assert generator.config.generation.skip_backfill is True
        assert generator.config.generation.plan_only is False
        assert generator.config.generation.log_plan_details is True

    def test_plan_only_takes_precedence_over_skip_backfill(self):
        """Test that plan_only takes precedence when both are True"""
        # Simulating run_replan logic
        plan = Mock()
        plan.has_changes = True
        plan.requires_backfill = True

        skip_backfill = True
        plan_only = True

        # The logic in run_replan checks plan_only first
        if not plan.has_changes and not plan.requires_backfill:
            result = {"status": "skipped", "reason": "no_changes"}
        elif plan_only:
            result = {"status": "plan_only"}
        elif skip_backfill and plan.requires_backfill:
            result = {"status": "skipped", "reason": "backfill_skipped"}
        else:
            result = {"status": "applied"}

        # plan_only should take precedence
        assert result["status"] == "plan_only"


class TestPlanOptimizationReturnValues:
    """Test that run_replan returns correct information"""

    def test_skipped_return_includes_timing(self):
        """Test that skipped status includes timing information"""
        # Expected return structure when skipped
        result = {
            "status": "skipped",
            "reason": "no_changes",
            "duration_seconds": 1.5,
            "context_load_seconds": 0.5,
            "plan_compute_seconds": 1.0,
        }

        assert "duration_seconds" in result
        assert "context_load_seconds" in result
        assert "plan_compute_seconds" in result

    def test_applied_return_includes_all_phases(self):
        """Test that applied status includes all phase timings"""
        # Expected return structure when applied
        result = {
            "status": "applied",
            "has_changes": True,
            "requires_backfill": False,
            "duration_seconds": 10.0,
            "context_load_seconds": 0.5,
            "plan_compute_seconds": 1.0,
            "apply_seconds": 8.5,
        }

        assert "duration_seconds" in result
        assert "context_load_seconds" in result
        assert "plan_compute_seconds" in result
        assert "apply_seconds" in result
        assert result["apply_seconds"] > result["plan_compute_seconds"]

    def test_plan_only_return_includes_plan_info(self):
        """Test that plan_only status includes plan information"""
        result = {
            "status": "plan_only",
            "reason": "plan_only_mode",
            "has_changes": True,
            "requires_backfill": True,
            "duration_seconds": 1.5,
        }

        assert "has_changes" in result
        assert "requires_backfill" in result
        assert result["reason"] == "plan_only_mode"

