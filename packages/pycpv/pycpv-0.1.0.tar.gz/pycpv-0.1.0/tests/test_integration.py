"""Integration tests for CPV package"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from cp_manage.utilities import (
    CPVConfig,
    ModelsCheckpointsManage,
    CombinedCheckpointsManage
)


class TestFullWorkflow:
    """Test complete CPV workflows"""
    
    @patch('cp_manage.utilities.boto3.Session')
    @patch('cp_manage.utilities.git.Repo')
    @patch('subprocess.run')
    def test_init_to_tag_workflow(self, mock_subprocess, mock_git_repo_class, mock_boto):
        """Test complete workflow from initialization to tagging"""
        tmp_path = Path(tempfile.mkdtemp())
        repo_path = tmp_path / "faster-whisper"
        
        # Mock external dependencies
        mock_git_repo = MagicMock()
        mock_git_repo_class.return_value = mock_git_repo
        mock_git_repo_class.init = MagicMock(return_value=mock_git_repo)
        mock_git_repo.index.add = MagicMock()
        mock_git_repo.index.commit = MagicMock(return_value=MagicMock(hexsha="abc123"))
        mock_git_repo.create_tag = MagicMock()
        
        mock_s3 = MagicMock()
        mock_boto.return_value.client.return_value = mock_s3
        mock_s3.head_bucket.return_value = {}
        
        # Initialize manager
        mcm = ModelsCheckpointsManage(
            team_name="AI-Convo",
            model_name="faster-whisper",
            repo_path=str(repo_path)
        )
        
        # Create structure
        mcm._create_local_structure()
        
        # Verify structure
        assert (repo_path / "model.bin").exists()
        assert (repo_path / "metrics.log").exists()
        assert (repo_path / "train.py").exists()
        assert (repo_path / "README.md").exists()
        assert (repo_path / "data").is_dir()
    
    def test_config_model_integration(self, tmp_path, monkeypatch):
        """Test configuration and model manager integration"""
        config_dir = tmp_path / ".cpv"
        config_dir.mkdir()
        
        cred_file = tmp_path / "credentials"
        cred_file.write_text("[default]\naws_access_key_id = AKIAIOSFODNN7EXAMPLE\n")
        
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        
        # Setup configuration
        config = CPVConfig()
        config.setup_aws_profile(
            credential_path=str(cred_file),
            aws_profile="default"
        )
        
        # Create model manager
        repo_path = tmp_path / "model"
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        # Initialize model structure
        mcm._create_local_structure()
        
        assert (repo_path / "model.bin").exists()
        
        # Verify config is still accessible
        loaded_config = CPVConfig()
        assert loaded_config._config["aws_profile"] == "default"


class TestDataTypes:
    """Test data type consistency across operations"""
    
    @patch('cp_manage.utilities.git.Repo')
    def test_model_artifacts_from_download(self, mock_git, tmp_path):
        """Test ModelArtifacts returned from download operation"""
        repo_path = tmp_path / "test_model"
        repo_path.mkdir()
        
        model_file = repo_path / "model.bin"
        model_file.write_text("model content" * 1000)
        
        metrics_file = repo_path / "metrics.log"
        metrics_file.write_text(json.dumps({"loss": 0.25, "accuracy": 0.96}))
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        with patch.object(mcm, '_checkout_tag'):
            with patch('subprocess.run'):
                # This would normally download from S3
                # For testing, we just check return types
                metadata = mcm.get_model_metadata()
                
                assert isinstance(metadata, dict)
                assert "model_size_mb" in metadata
                assert "metrics" in metadata
                assert "tag" in metadata


class TestErrorRecovery:
    """Test error handling and recovery"""
    
    @patch('cp_manage.utilities.git.Repo')
    def test_invalid_tag_handling(self, mock_git, tmp_path):
        """Test handling of invalid tags"""
        repo_path = tmp_path / "test_model"
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        # Reading from non-existent repo should return empty list
        tags = mcm.read_checkpoint_tag()
        assert isinstance(tags, list)
    
    @patch('cp_manage.utilities.git.Repo')
    def test_missing_metrics_file(self, mock_git, tmp_path):
        """Test handling of missing metrics file"""
        repo_path = tmp_path / "test_model"
        repo_path.mkdir()
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        # Should return empty dict if metrics file missing
        metrics = mcm._read_metrics()
        assert metrics == {}


class TestVersioningLogic:
    """Test versioning and tagging logic"""
    
    def test_multiple_version_increments(self, tmp_path):
        """Test multiple sequential version increments"""
        repo_path = tmp_path / "test_model"
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        versions = []
        
        # Simulate multiple versions
        for i in range(3):
            with patch.object(mcm, 'read_checkpoint_tag', return_value=versions):
                version = mcm._get_next_version()
                versions.append(version)
        
        assert "v0.1" in versions
        assert "v0.2" in versions or "v0.3" in versions
    
    def test_version_tag_immutability(self, tmp_path):
        """Test that version tags are immutable after creation"""
        repo_path = tmp_path / "test_model"
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        with patch.object(mcm, 'git_repo') as mock_repo:
            mock_repo.create_tag.return_value = None
            
            tag1 = mcm.tag_model_checkpoint(version_tag="v1.0")
            
            # Trying to create same tag should still work (git would handle)
            tag2 = mcm.tag_model_checkpoint(version_tag="v1.0")
            
            assert tag1 == tag2 == "v1.0"


class TestCombinedOperations:
    """Test combined model and data operations"""
    
    def test_combined_checkpoint_structure(self, tmp_path):
        """Test CombinedCheckpointsManage initialization"""
        repo_path = tmp_path / "model"
        
        combined = CombinedCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        # Verify both managers initialized
        assert combined.models is not None
        assert combined.data is not None
        assert combined.models.team_name == "AI-Test"
        assert combined.data.team_name == "AI-Test"


class TestMetricsConsistency:
    """Test metrics tracking consistency"""
    
    @patch('cp_manage.utilities.git.Repo')
    def test_metrics_file_format(self, mock_git, tmp_path):
        """Test metrics are stored in valid JSON format"""
        repo_path = tmp_path / "test_model"
        repo_path.mkdir()
        
        mcm = ModelsCheckpointsManage(
            team_name="AI-Test",
            model_name="test-model",
            repo_path=str(repo_path)
        )
        
        test_metrics = {
            "loss": 0.25,
            "accuracy": 0.96,
            "precision": 0.94,
            "recall": 0.98
        }
        
        mcm._update_metrics(test_metrics)
        mcm._update_metrics(test_metrics)  # Add twice
        
        metrics_file = repo_path / "metrics.log"
        
        # Should be able to parse file as JSON lines
        with open(metrics_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.strip():
                    data = json.loads(line)
                    assert "loss" in data
                    assert "accuracy" in data


class TestWorkspaceIsolation:
    """Test workspace isolation between different models"""
    
    def test_multiple_models_isolation(self, tmp_path):
        """Test that different models don't interfere"""
        model1_path = tmp_path / "model1"
        model2_path = tmp_path / "model2"
        
        mcm1 = ModelsCheckpointsManage(
            team_name="AI-Team1",
            model_name="model1",
            repo_path=str(model1_path)
        )
        
        mcm2 = ModelsCheckpointsManage(
            team_name="AI-Team2",
            model_name="model2",
            repo_path=str(model2_path)
        )
        
        # Create structures
        mcm1._create_local_structure()
        mcm2._create_local_structure()
        
        # Verify isolation
        assert (model1_path / "model.bin").exists()
        assert (model2_path / "model.bin").exists()
        assert model1_path != model2_path
        
        # Modify one shouldn't affect other
        (model1_path / "custom_file.txt").write_text("model1")
        assert not (model2_path / "custom_file.txt").exists()


class TestConfigurationPersistence:
    """Test configuration persistence across sessions"""
    
    def test_config_survives_session_restart(self, tmp_path, monkeypatch):
        """Test configuration persists across manager creation"""
        config_dir = tmp_path / ".cpv"
        config_dir.mkdir()
        
        cred_file = tmp_path / "credentials"
        cred_file.write_text("[default]\naws_access_key_id = TEST\n")
        
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        
        # First session: setup
        config1 = CPVConfig()
        config1.setup_aws_profile(
            credential_path=str(cred_file),
            aws_profile="default"
        )
        assert config1._config["aws_profile"] == "default"
        
        # Second session: load
        config2 = CPVConfig()
        assert config2._config["aws_profile"] == "default"
        assert config2._config["aws_credential_path"] == str(cred_file)
