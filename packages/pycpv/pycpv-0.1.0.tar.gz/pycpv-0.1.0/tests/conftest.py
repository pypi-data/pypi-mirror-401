"""Pytest configuration and fixtures for CPV tests"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch


@pytest.fixture
def tmp_home(tmp_path, monkeypatch):
    """Fixture providing a temporary home directory"""
    home_dir = tmp_path / "home"
    home_dir.mkdir()
    monkeypatch.setenv("HOME", str(home_dir))
    return home_dir


@pytest.fixture
def aws_credentials_file(tmp_path):
    """Fixture providing a temporary AWS credentials file"""
    creds_file = tmp_path / "aws_credentials"
    creds_file.write_text(
        "[default]\n"
        "aws_access_key_id = AKIAIOSFODNN7EXAMPLE\n"
        "aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY\n"
        "\n"
        "[prod]\n"
        "aws_access_key_id = AKIAIOSFODNN7PROD\n"
        "aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYPRODKEY\n"
    )
    return creds_file


@pytest.fixture
def mock_git_repo():
    """Fixture providing a mock git repository"""
    mock_repo = MagicMock()
    mock_repo.index = MagicMock()
    mock_repo.index.add = MagicMock()
    mock_repo.index.commit = MagicMock(return_value=MagicMock(hexsha="abc123def456"))
    mock_repo.create_tag = MagicMock()
    mock_repo.heads = MagicMock()
    mock_repo.remotes = MagicMock()
    return mock_repo


@pytest.fixture
def mock_aws_s3():
    """Fixture providing a mock AWS S3 client"""
    mock_s3 = MagicMock()
    mock_s3.head_bucket = MagicMock(return_value={})
    return mock_s3


@pytest.fixture
def test_model_path(tmp_path):
    """Fixture providing a test model directory"""
    model_dir = tmp_path / "test_model"
    model_dir.mkdir()
    
    # Create basic structure
    (model_dir / "data").mkdir()
    (model_dir / "model.bin").write_text("dummy model")
    (model_dir / "metrics.log").write_text("")
    (model_dir / "train.py").write_text("# training script")
    
    return model_dir


@pytest.fixture(autouse=True)
def reset_modules():
    """Reset imported modules between tests"""
    yield
    # Cleanup after each test if needed
