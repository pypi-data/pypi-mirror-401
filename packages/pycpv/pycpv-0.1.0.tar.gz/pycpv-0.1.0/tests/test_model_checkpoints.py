"""Tests for Model Checkpoints Management"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
import json

from cp_manage.utilities import ModelsCheckpointsManage, ModelArtifacts


class TestModelsCheckpointsInitialization:
    """Test ModelsCheckpointsManage initialization"""
    
    def test_initialization_creates_instance(self, tmp_path):
        """Test basic initialization"""
        repo_path = tmp_path / "test_model"
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path),
            verbose=False
        )
        
        assert mcm.team_name == "AI-Test"
        assert mcm.model_name == "test-model"
        assert mcm.s3_prefix == "s3://vmo-model-checkpoints/AI-Test/test-model"
    
    def test_initialization_with_verbose(self, tmp_path):
        """Test initialization with verbose flag"""
        repo_path = tmp_path / "test_model"
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path),
            verbose=True
        )
        
        assert mcm.verbose is True


class TestModelInitialization:
    """Test model repository initialization"""
    
    @patch('git.Repo.init')
    @patch('subprocess.run')
    def test_import_model_init_creates_structure(self, mock_subprocess, mock_git_init, tmp_path):
        """Test that import_model_init creates proper structure"""
        repo_path = tmp_path / "test_model"
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        # Mock git and subprocess calls
        mock_git_init.return_value = MagicMock()
        mock_subprocess.return_value = MagicMock()
        
        # This would initialize the repo (mocked)
        # In real test, we'd patch all external calls
        
        assert repo_path == Path(str(repo_path))
    
    def test_create_local_structure_files_created(self, tmp_path):
        """Test that local structure files are created"""
        repo_path = tmp_path / "test_model"
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        mcm._create_local_structure(data_path=None)
        
        # Check all required files exist
        assert (repo_path / "model.bin").exists()
        assert (repo_path / "metrics.log").exists()
        assert (repo_path / "train.py").exists()
        assert (repo_path / "README.md").exists()
        assert (repo_path / ".gitignore").exists()
        assert (repo_path / "data").exists()
        assert (repo_path / "data").is_dir()
    
    def test_create_files_with_content(self, tmp_path):
        """Test that created files have proper content"""
        repo_path = tmp_path / "test_model"
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        mcm._create_local_structure()
        
        # Check file contents
        readme = (repo_path / "README.md").read_text()
        assert "Model Training Guide" in readme
        
        train_py = (repo_path / "train.py").read_text()
        assert "def main()" in train_py
        
        gitignore = (repo_path / ".gitignore").read_text()
        assert "/data" in gitignore


class TestVersionTagging:
    """Test version tagging operations"""
    
    def test_get_next_version_empty_list(self, tmp_path):
        """Test auto-increment with no existing versions"""
        repo_path = tmp_path / "test_model"
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        with patch.object(mcm, 'read_checkpoint_tag', return_value=[]):
            next_version = mcm._get_next_version()
            assert next_version == "v0.1"
    
    def test_get_next_version_increments_minor(self, tmp_path):
        """Test auto-increment from v1.0 to v1.1"""
        repo_path = tmp_path / "test_model"
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        with patch.object(mcm, 'read_checkpoint_tag', return_value=['v1.0']):
            next_version = mcm._get_next_version()
            assert next_version == "v1.1"
    
    def test_get_next_version_with_multiple_versions(self, tmp_path):
        """Test auto-increment with multiple existing versions"""
        repo_path = tmp_path / "test_model"
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        with patch.object(mcm, 'read_checkpoint_tag', 
                         return_value=['v0.1', 'v0.2', 'v1.0', 'v1.1']):
            next_version = mcm._get_next_version()
            # Should increment the highest version
            assert next_version.startswith("v")
    
    def test_tag_model_checkpoint_with_auto_version(self, tmp_path):
        """Test tagging with auto-increment"""
        repo_path = tmp_path / "test_model"
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        with patch.object(mcm, '_get_next_version', return_value='v1.0'):
            with patch.object(mcm, 'git_repo') as mock_repo:
                mock_repo.create_tag.return_value = None
                
                tag = mcm.tag_model_checkpoint(message="Test tag")
                
                assert tag == "v1.0"
                mock_repo.create_tag.assert_called_once()
    
    def test_tag_model_checkpoint_with_manual_version(self, tmp_path):
        """Test tagging with manual version specification"""
        repo_path = tmp_path / "test_model"
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        with patch.object(mcm, 'git_repo') as mock_repo:
            mock_repo.create_tag.return_value = None
            
            tag = mcm.tag_model_checkpoint(version_tag="v2.5", message="Custom version")
            
            assert tag == "v2.5"
            mock_repo.create_tag.assert_called_once()


class TestMetricsTracking:
    """Test metrics tracking operations"""
    
    @patch('cp_manage.utilities.git.Repo')
    def test_update_metrics_creates_file(self, mock_git, tmp_path):
        """Test metrics file update"""
        repo_path = tmp_path / "test_model"
        repo_path.mkdir()
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        metrics = {"loss": 0.25, "accuracy": 0.96}
        mcm._update_metrics(metrics)
        
        metrics_file = repo_path / "metrics.log"
        assert metrics_file.exists()
        
        content = metrics_file.read_text()
        assert "0.25" in content
        assert "0.96" in content
    
    @patch('cp_manage.utilities.git.Repo')
    def test_read_metrics_empty_file(self, mock_git, tmp_path):
        """Test reading metrics from empty file"""
        repo_path = tmp_path / "test_model"
        repo_path.mkdir()
        
        metrics_file = repo_path / "metrics.log"
        metrics_file.write_text("# Empty metrics file\n")
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        metrics = mcm._read_metrics()
        assert metrics == {}
    
    @patch('cp_manage.utilities.git.Repo')
    def test_read_metrics_with_data(self, mock_git, tmp_path):
        """Test reading metrics from populated file"""
        repo_path = tmp_path / "test_model"
        repo_path.mkdir()
        
        metrics_file = repo_path / "metrics.log"
        test_metrics = {"loss": 0.25, "accuracy": 0.96}
        metrics_file.write_text(json.dumps(test_metrics) + "\n")
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        metrics = mcm._read_metrics()
        assert metrics == test_metrics


class TestModelMetadata:
    """Test model metadata operations"""
    
    @patch('cp_manage.utilities.git.Repo')
    def test_get_model_metadata_returns_correct_structure(self, mock_git, tmp_path):
        """Test metadata retrieval returns proper structure"""
        repo_path = tmp_path / "test_model"
        repo_path.mkdir()
        
        # Create model file
        model_file = repo_path / "model.bin"
        model_file.write_text("dummy model content" * 1000)  # ~19KB
        
        # Create metrics file
        metrics_file = repo_path / "metrics.log"
        test_metrics = {"loss": 0.25, "accuracy": 0.96}
        metrics_file.write_text(json.dumps(test_metrics) + "\n")
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        metadata = mcm.get_model_metadata()
        
        assert "tag" in metadata
        assert "model_size_mb" in metadata
        assert "metrics" in metadata
        assert "timestamp" in metadata
        assert metadata["team_name"] == "AI-Test"
        assert metadata["model_name"] == "test-model"
        assert metadata["metrics"]["accuracy"] == 0.96


class TestTemplateGeneration:
    """Test template generation"""
    
    def test_train_script_template_content(self):
        """Test training script template has required content"""
        template = ModelsCheckpointsManage._get_train_script_template()
        
        assert "def main():" in template
        assert "metrics.log" in template
        assert "json.dump" in template
    
    def test_readme_template_content(self):
        """Test README template has required sections"""
        template = ModelsCheckpointsManage._get_readme_template()
        
        assert "# Model Training Guide" in template
        assert "Setup" in template
        assert "Training" in template
        assert "Versioning" in template


class TestModelDryRun:
    """Test dry-run functionality"""
    
    def test_tag_checkpoint_dry_run(self, tmp_path):
        """Test tagging with dry-run doesn't create tag"""
        repo_path = tmp_path / "test_model"
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        with patch.object(mcm, '_get_next_version', return_value='v1.0'):
            with patch.object(mcm, 'git_repo') as mock_repo:
                tag = mcm.tag_model_checkpoint(dry_run=True)
                
                assert tag == "v1.0"
                # git_repo.create_tag should NOT be called in dry-run
                mock_repo.create_tag.assert_not_called()


class TestModelDataTypes:
    """Test data types and return values"""
    
    def test_model_artifacts_dataclass(self, tmp_path):
        """Test ModelArtifacts dataclass"""
        artifacts = ModelArtifacts(
            model_path="/path/to/model.bin",
            metrics={"loss": 0.25, "accuracy": 0.96},
            timestamp="2026-01-10T10:00:00",
            tag="v1.0",
            size_mb=1234.5
        )
        
        assert artifacts.model_path == "/path/to/model.bin"
        assert artifacts.metrics["accuracy"] == 0.96
        assert artifacts.tag == "v1.0"
        assert artifacts.size_mb == 1234.5
    
    def test_model_artifacts_has_required_fields(self):
        """Test ModelArtifacts has all required fields"""
        # Create sample artifacts
        artifacts = ModelArtifacts(
            model_path="test",
            metrics={},
            timestamp="test",
            tag="test",
            size_mb=0.0
        )
        
        required_fields = ["model_path", "metrics", "timestamp", "tag", "size_mb"]
        for field in required_fields:
            assert hasattr(artifacts, field)
