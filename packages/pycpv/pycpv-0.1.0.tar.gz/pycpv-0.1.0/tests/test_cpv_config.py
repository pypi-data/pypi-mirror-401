"""Tests for CPV Configuration Management (CPVConfig)"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from cp_manage.utilities import CPVConfig


class TestCPVConfigInitialization:
    """Test CPVConfig initialization and basic operations"""
    
    def test_config_dir_created(self, tmp_path, monkeypatch):
        """Test that config directory is created on initialization"""
        config_dir = tmp_path / ".cpv"
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        
        config = CPVConfig()
        assert config.CONFIG_DIR.exists()
    
    def test_default_config_structure(self, tmp_path, monkeypatch):
        """Test default configuration structure"""
        config_dir = tmp_path / ".cpv"
        config_file = config_dir / "config.json"
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        monkeypatch.setattr(CPVConfig, "CONFIG_FILE", config_file)
        
        config = CPVConfig()
        default_config = config._config
        
        assert "aws_credential_path" in default_config
        assert "aws_profile" in default_config
        assert "bitbucket_ssh_keyfile" in default_config
        assert default_config["aws_profile"] == "default"
    
    def test_load_existing_config(self, tmp_path, monkeypatch):
        """Test loading existing configuration from disk"""
        config_dir = tmp_path / ".cpv"
        config_dir.mkdir()
        config_file = config_dir / "config.json"
        
        test_config = {
            "aws_credential_path": "/home/user/.aws/credentials",
            "aws_profile": "prod",
            "bitbucket_ssh_keyfile": "/home/user/.ssh/id_rsa",
            "last_updated": "2026-01-10T00:00:00"
        }
        
        with open(config_file, 'w') as f:
            json.dump(test_config, f)
        
        # Mock both CONFIG_DIR and CONFIG_FILE to use tmp_path
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        monkeypatch.setattr(CPVConfig, "CONFIG_FILE", config_file)
        config = CPVConfig()
        
        assert config._config["aws_profile"] == "prod"
        assert config._config["aws_credential_path"] == "/home/user/.aws/credentials"


class TestAWSConfiguration:
    """Test AWS credential setup and validation"""
    
    def test_setup_aws_profile_with_valid_path(self, tmp_path, monkeypatch):
        """Test AWS profile setup with valid credentials file"""
        config_dir = tmp_path / ".cpv"
        config_dir.mkdir()
        
        # Create fake credentials file
        cred_dir = tmp_path / ".aws"
        cred_dir.mkdir()
        cred_file = cred_dir / "credentials"
        cred_file.write_text("[default]\naws_access_key_id = AKIAIOSFODNN7EXAMPLE\n")
        
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        config = CPVConfig()
        
        config.setup_aws_profile(
            credential_path=str(cred_file),
            aws_profile="default",
            verbose=False
        )
        
        assert config._config["aws_credential_path"] == str(cred_file)
        assert config._config["aws_profile"] == "default"
    
    def test_setup_aws_profile_with_invalid_path(self, tmp_path, monkeypatch):
        """Test AWS profile setup with invalid credentials file"""
        config_dir = tmp_path / ".cpv"
        config_dir.mkdir()
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        
        config = CPVConfig()
        
        with pytest.raises(FileNotFoundError):
            config.setup_aws_profile(
                credential_path="/nonexistent/path/credentials",
                aws_profile="default"
            )
    
    def test_setup_aws_profile_missing_profile(self, tmp_path, monkeypatch):
        """Test AWS setup when profile doesn't exist in credentials"""
        config_dir = tmp_path / ".cpv"
        config_dir.mkdir()
        
        cred_file = tmp_path / "credentials"
        cred_file.write_text("[default]\naws_access_key_id = AKIAIOSFODNN7EXAMPLE\n")
        
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        config = CPVConfig()
        
        with pytest.raises(ValueError, match="Profile 'prod' not found"):
            config.setup_aws_profile(
                credential_path=str(cred_file),
                aws_profile="prod"
            )
    
    def test_setup_aws_profile_dry_run(self, tmp_path, monkeypatch):
        """Test AWS profile setup in dry-run mode (no changes)"""
        config_dir = tmp_path / ".cpv"
        config_dir.mkdir()
        
        cred_file = tmp_path / "credentials"
        cred_file.write_text("[default]\naws_access_key_id = AKIAIOSFODNN7EXAMPLE\n")
        
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        config = CPVConfig()
        
        original_config = config._config.copy()
        
        config.setup_aws_profile(
            credential_path=str(cred_file),
            aws_profile="default",
            dry_run=True
        )
        
        # Config should not be modified in dry-run mode
        assert config._config == original_config


class TestBitbucketConfiguration:
    """Test Bitbucket SSH setup"""
    
    def test_setup_bitbucket_ssh_creates_config(self, tmp_path, monkeypatch):
        """Test Bitbucket SSH configuration creation"""
        config_dir = tmp_path / ".cpv"
        config_dir.mkdir()
        ssh_dir = tmp_path / ".ssh"
        ssh_dir.mkdir()
        
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        monkeypatch.setenv("HOME", str(tmp_path))
        
        config = CPVConfig()
        
        # Capture stdout to avoid printing
        config.setup_bitbucket_ssh(
            keygen_filename="id_rsa_bitbucket",
            bitbucket_user="testuser",
            verbose=False,
            dry_run=False
        )
        
        assert config._config["bitbucket_ssh_keyfile"]
        assert "id_rsa_bitbucket" in config._config["bitbucket_ssh_keyfile"]
    
    def test_setup_bitbucket_ssh_dry_run(self, tmp_path, monkeypatch):
        """Test Bitbucket SSH setup in dry-run mode"""
        config_dir = tmp_path / ".cpv"
        config_dir.mkdir()
        ssh_dir = tmp_path / ".ssh"
        ssh_dir.mkdir()
        
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        monkeypatch.setenv("HOME", str(tmp_path))
        
        config = CPVConfig()
        original_config = config._config.copy()
        
        config.setup_bitbucket_ssh(
            keygen_filename="id_rsa_bitbucket",
            bitbucket_user="testuser",
            verbose=False,
            dry_run=True
        )
        
        # Config should not be modified in dry-run mode
        assert config._config == original_config


class TestConfigPersistence:
    """Test configuration save and load"""
    
    def test_save_and_load_config(self, tmp_path, monkeypatch):
        """Test saving and loading configuration"""
        config_dir = tmp_path / ".cpv"
        config_dir.mkdir()
        config_file = config_dir / "config.json"
        
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        monkeypatch.setattr(CPVConfig, "CONFIG_FILE", config_file)
        
        # Create and save config
        config1 = CPVConfig()
        config1._config["aws_profile"] = "prod"
        config1._config["custom_key"] = "custom_value"
        config1._save_config()
        
        # Load config in new instance
        config2 = CPVConfig()
        
        assert config2._config["aws_profile"] == "prod"
        assert config2._config["custom_key"] == "custom_value"
    
    def test_get_config(self, tmp_path, monkeypatch):
        """Test retrieving configuration values"""
        config_dir = tmp_path / ".cpv"
        config_dir.mkdir()
        config_file = config_dir / "config.json"
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        monkeypatch.setattr(CPVConfig, "CONFIG_FILE", config_file)
        
        config = CPVConfig()
        config._config["aws_profile"] = "dev"
        
        # Get specific key
        profile = config.get_config("aws_profile")
        assert profile == "dev"
        
        # Get all config
        all_config = config.get_config()
        assert isinstance(all_config, dict)
        assert all_config["aws_profile"] == "dev"
    
    def test_get_config_nonexistent_key(self, tmp_path, monkeypatch):
        """Test getting non-existent config key returns None"""
        config_dir = tmp_path / ".cpv"
        config_dir.mkdir()
        config_file = config_dir / "config.json"
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        monkeypatch.setattr(CPVConfig, "CONFIG_FILE", config_file)
        
        config = CPVConfig()
        result = config.get_config("nonexistent_key")
        
        assert result is None


class TestCredentialValidation:
    """Test credential validation"""
    
    @patch('cp_manage.utilities.boto3.Session')
    def test_validate_credentials_aws_missing(self, mock_session, tmp_path, monkeypatch):
        """Test validation fails when AWS not configured"""
        config_dir = tmp_path / ".cpv"
        config_dir.mkdir()
        config_file = config_dir / "config.json"
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        monkeypatch.setattr(CPVConfig, "CONFIG_FILE", config_file)
        
        config = CPVConfig()
        
        # AWS not configured
        assert not config.validate_credentials()
    
    @patch('cp_manage.utilities.boto3.Session')
    def test_validate_credentials_aws_success(self, mock_session, tmp_path, monkeypatch):
        """Test successful AWS validation"""
        config_dir = tmp_path / ".cpv"
        config_dir.mkdir()
        config_file = config_dir / "config.json"
        
        cred_file = tmp_path / "credentials"
        cred_file.write_text("[default]\naws_access_key_id = AKIAIOSFODNN7EXAMPLE\n")
        
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        monkeypatch.setattr(CPVConfig, "CONFIG_FILE", config_file)
        
        # Mock boto3 session and s3 client
        mock_s3 = MagicMock()
        mock_session.return_value.client.return_value = mock_s3
        mock_s3.head_bucket.return_value = {}
        
        config = CPVConfig()
        config._config["aws_credential_path"] = str(cred_file)
        config._config["aws_profile"] = "default"
        # Add SSH key to avoid that check failing
        ssh_file = config_dir / "test_key"
        ssh_file.write_text("dummy key")
        config._config["bitbucket_ssh_keyfile"] = str(ssh_file)
        
        # Validation should succeed
        assert config.validate_credentials()


class TestConfigIntegration:
    """Integration tests for configuration"""
    
    def test_full_setup_workflow(self, tmp_path, monkeypatch):
        """Test complete setup workflow"""
        config_dir = tmp_path / ".cpv"
        config_dir.mkdir()
        
        cred_file = tmp_path / "credentials"
        cred_file.write_text("[default]\naws_access_key_id = AKIAIOSFODNN7EXAMPLE\n")
        
        ssh_dir = tmp_path / ".ssh"
        ssh_dir.mkdir()
        
        config_file = config_dir / "config.json"
        monkeypatch.setattr(CPVConfig, "CONFIG_DIR", config_dir)
        monkeypatch.setattr(CPVConfig, "CONFIG_FILE", config_file)
        monkeypatch.setenv("HOME", str(tmp_path))
        
        config = CPVConfig()
        
        # Step 1: Setup AWS
        config.setup_aws_profile(
            credential_path=str(cred_file),
            aws_profile="default"
        )
        assert config._config["aws_credential_path"] == str(cred_file)
        
        # Step 2: Setup Bitbucket SSH
        config.setup_bitbucket_ssh(
            keygen_filename="id_rsa",
            bitbucket_user="testuser",
            dry_run=False
        )
        assert "id_rsa" in config._config["bitbucket_ssh_keyfile"]
        
        # Step 3: Verify config is saved
        config2 = CPVConfig()
        assert config2._config["aws_profile"] == "default"
