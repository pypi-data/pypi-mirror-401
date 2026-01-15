# CPV (Checkpoints Versioning) - Complete Implementation Guide

## Project Structure

```
cpmodels_versioning/
├── cp_manage/
│   ├── __init__.py
│   ├── utilities.py                  # Core classes (✓ refactored)
│   ├── cli.py                        # CLI commands (TODO)
│   ├── exceptions.py                 # Custom exceptions (TODO)
│   └── constants.py                  # Constants & defaults (TODO)
├── tests/
│   ├── test_cpv_config.py            # Config tests (TODO)
│   ├── test_model_checkpoints.py     # Model checkpoint tests (TODO)
│   ├── test_data_checkpoints.py      # Data checkpoint tests (TODO)
│   └── test_integration.py           # Integration tests (TODO)
├── docs/
│   ├── API.md                        # API documentation (TODO)
│   ├── TUTORIAL.md                   # Step-by-step tutorial (TODO)
│   └── TROUBLESHOOTING.md            # Common issues (TODO)
├── examples/
│   ├── basic_model_versioning.py     # Basic example
│   ├── multi_team_management.py      # Multi-team example
│   └── experiment_tracking.py        # ML experiment tracking example
│
├── CPV_DESIGN.md                     # ✓ Design document
├── REFINEMENT_FEEDBACK.md            # ✓ Feedback & next steps
├── USAGE_EXAMPLES.md                 # ✓ Usage guide
├── pyproject.toml                    # ✓ Updated with new deps
├── README.md                         # TODO: Update with new design
└── main.py                           # Entry point (TODO: Update)
```

## Updated Dependencies

### Update pyproject.toml:

```toml
[project]
name = "cpv"
version = "0.1.0"
description = "Checkpoints Versioning - Model and Data Version Control using DVC, Git, and AWS S3"
readme = "README.md"
requires-python = ">=3.8"
authors = [
    {name = "VMO AI Team", email = "ai@vmo.ai"}
]
license = {text = "MIT"}

dependencies = [
    # Core dependencies
    "boto3>=1.26.0",                  # AWS S3 SDK
    "GitPython>=3.1.0",               # Git operations
    "dvc>=3.66.1",                    # Data versioning
    "dvc-s3>=3.2.2",                  # S3 backend for DVC
    
    # Configuration & validation
    "pydantic>=2.0.0",                # Data validation
    "pyyaml>=6.0.0",                  # YAML parsing
    
    # Utilities
    "tqdm>=4.67.1",                   # Progress bars
    "click>=8.0.0",                   # CLI framework
    "python-dotenv>=1.0.0",           # .env file support
    "requests>=2.28.0",               # HTTP requests
    
    # Logging & monitoring
    "colorlog>=6.7.0",                # Colored logging
    "rich>=13.0.0",                   # Rich terminal output
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
]

[project.scripts]
cpv = "cp_manage.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.black]
line-length = 100

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
```

## File-by-File Implementation Plan

### 1. `cp_manage/__init__.py`
```python
"""CPV - Checkpoints Versioning Package"""

__version__ = "0.1.0"

from .utilities import (
    CPVConfig,
    ModelsCheckpointsManage,
    DataCheckpointsManage,
    CombinedCheckpointsManage,
    ModelArtifacts,
    DataArtifacts,
)

__all__ = [
    "CPVConfig",
    "ModelsCheckpointsManage",
    "DataCheckpointsManage",
    "CombinedCheckpointsManage",
    "ModelArtifacts",
    "DataArtifacts",
]
```

### 2. `cp_manage/exceptions.py`
```python
"""CPV Custom Exceptions"""

class CPVError(Exception):
    """Base exception for CPV"""
    pass

class ConfigError(CPVError):
    """Configuration error"""
    pass

class AWSError(CPVError):
    """AWS S3 operation error"""
    pass

class GitError(CPVError):
    """Git operation error"""
    pass

class DVCError(CPVError):
    """DVC operation error"""
    pass

class CheckpointNotFoundError(CPVError):
    """Checkpoint/tag not found"""
    pass

class RepositoryError(CPVError):
    """Repository setup error"""
    pass

class CredentialError(CPVError):
    """Credential validation error"""
    pass
```

### 3. `cp_manage/constants.py`
```python
"""CPV Constants and Configuration"""

# AWS S3 Configuration
S3_BUCKET = "vmo-model-checkpoints"
S3_REGION = "us-east-1"

# Bitbucket Configuration
BITBUCKET_HOST = "bitbucket.org"
BITBUCKET_SSH_HOST = "altssh.bitbucket.org"
BITBUCKET_SSH_PORT = 443
BITBUCKET_PROJECT_TEMPLATE = "AI-{team_name}-model-checkpoints"

# DVC Configuration
DVC_REMOTE_NAME = "myremote"
DVC_AUTOSTAGE = True

# Version Format
VERSION_FORMAT = "v{major}.{minor}"
DEFAULT_START_VERSION = "v0.1"

# Files to Track
FILES_TO_TRACK = {
    "model": "model.bin",
    "data": "data",
    "metrics": "metrics.log",
}

# Configuration Directory
CONFIG_DIR = "~/.cpv"
CONFIG_FILE = "config.json"
LOGS_DIR = "logs"

# Git Configuration
GIT_USER_NAME = "CPV System"
GIT_USER_EMAIL = "cpv@vmo.ai"

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Operation Timeout (seconds)
OPERATION_TIMEOUT = 3600  # 1 hour
S3_UPLOAD_TIMEOUT = 7200  # 2 hours
SSH_TIMEOUT = 30

# Retry Configuration
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# File Size Limits (for validation)
MIN_MODEL_SIZE_MB = 0.1
MAX_MODEL_SIZE_MB = 50000  # 50GB

# Metadata
METADATA_VERSION = "1.0"
```

### 4. `cp_manage/cli.py` (TODO - Full implementation)
```python
"""CPV CLI Interface using Click"""

import click
from pathlib import Path
from .utilities import CPVConfig, ModelsCheckpointsManage, DataCheckpointsManage, CombinedCheckpointsManage

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def cli(ctx, verbose):
    """CPV - Checkpoints Versioning Tool"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose

@cli.command()
@click.option('--credential-path', '-c', help='Path to AWS credentials file')
@click.option('--profile', '-p', default='default', help='AWS profile name')
@click.pass_context
def aws_config(ctx, credential_path, profile):
    """Configure AWS S3 credentials"""
    config = CPVConfig()
    config.setup_aws_profile(
        credential_path=credential_path,
        aws_profile=profile,
        verbose=ctx.obj['verbose']
    )
    click.echo("✓ AWS configuration complete")

@cli.command()
@click.option('--keygen-filename', '-k', help='SSH key filename')
@click.option('--user', '-u', help='Bitbucket username')
@click.pass_context
def bitbucket_config(ctx, keygen_filename, user):
    """Configure Bitbucket SSH access"""
    config = CPVConfig()
    config.setup_bitbucket_ssh(
        keygen_filename=keygen_filename,
        bitbucket_user=user,
        verbose=ctx.obj['verbose']
    )
    click.echo("✓ Bitbucket configuration complete")

@cli.command()
@click.pass_context
def validate(ctx):
    """Validate AWS and Bitbucket credentials"""
    config = CPVConfig()
    if config.validate_credentials(verbose=ctx.obj['verbose']):
        click.echo("✓ All credentials valid")
    else:
        click.echo("✗ Credential validation failed")
        raise click.Exit(1)

@cli.group()
def init():
    """Initialize new model project"""
    pass

@init.command()
@click.option('--team-name', '-t', required=True, help='AI team name')
@click.option('--model-name', '-m', required=True, help='Model name')
@click.option('--data-path', '-d', help='Path to initial training data')
@click.option('--repo-path', '-r', help='Local repository path')
@click.pass_context
def model(ctx, team_name, model_name, data_path, repo_path):
    """Initialize new model repository"""
    kwargs = {
        'verbose': ctx.obj.get('verbose', False),
        'repo_path': repo_path
    }
    
    mcm = ModelsCheckpointsManage(team_name, model_name, **kwargs)
    mcm.import_model_init(data_path=data_path, **kwargs)
    
    click.echo(f"✓ Model '{model_name}' initialized successfully")

# Add similar commands for model, data, and checkpoint operations...

def main():
    """Entry point for CLI"""
    cli(obj={})

if __name__ == '__main__':
    main()
```

### 5. `tests/test_cpv_config.py` (Skeleton)
```python
"""Tests for CPV Configuration"""

import pytest
import tempfile
import json
from pathlib import Path
from cp_manage.utilities import CPVConfig

@pytest.fixture
def temp_config_dir(monkeypatch):
    """Temporary config directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(CPVConfig, 'CONFIG_DIR', Path(tmpdir))
        yield Path(tmpdir)

class TestCPVConfig:
    def test_config_initialization(self, temp_config_dir):
        """Test config initialization"""
        config = CPVConfig()
        assert config.CONFIG_DIR.exists()
    
    def test_config_save_load(self, temp_config_dir):
        """Test config persistence"""
        config = CPVConfig()
        config._config['test_key'] = 'test_value'
        config._save_config()
        
        config2 = CPVConfig()
        assert config2.get_config('test_key') == 'test_value'
    
    # Add more tests...
```

## Development Workflow

### 1. Setup Development Environment
```bash
# Clone repository
git clone <repo>
cd cpmodels_versioning

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### 2. Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cp_manage --cov-report=html

# Run specific test file
pytest tests/test_cpv_config.py

# Run with verbose output
pytest -v
```

### 3. Code Quality
```bash
# Format code
black cp_manage/

# Lint code
flake8 cp_manage/

# Type checking
mypy cp_manage/

# Run all checks
pre-commit run --all-files
```

### 4. Build & Release
```bash
# Build package
python -m build

# Upload to PyPI (test)
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*
```

## Migration from Old Code

### Old Structure vs New Structure
```
OLD (utilities.py):
- Broken imports
- Incomplete class definitions
- No implementation

NEW (utilities.py):
- ✓ Full implementation
- ✓ Type hints
- ✓ Error handling
- ✓ Dataclasses
- ✓ Comprehensive docstrings
```

### How to Migrate Existing Users
1. Backup current `.dvc` and `.git` directories
2. Install new `cpv` package
3. Run `cpv init --team-name X --model-name Y` to setup
4. Existing data and models will be discovered and tracked

## Next Immediate Steps

1. ✓ **Design Complete** - (This document)
2. **Complete Data Checkpoint Implementation**
   - Copy model checkpoint logic to data
   - Adjust for directory instead of single file
3. **Add CLI Interface**
   - Implement Click commands
   - Add progress bars
   - Interactive setup wizard
4. **Write Comprehensive Tests**
   - Unit tests for each class
   - Integration tests with mock AWS/Git
5. **Create Documentation**
   - API documentation
   - Tutorial notebook
   - Troubleshooting guide

---

## Success Criteria for MVP

- [ ] Config management working (AWS + Bitbucket)
- [ ] Model checkpoint CRUD operations
- [ ] Data checkpoint CRUD operations
- [ ] Auto-versioning working correctly
- [ ] Git and S3 integration seamless
- [ ] Error messages clear and helpful
- [ ] Basic CLI interface functional
- [ ] Unit tests passing (>80% coverage)
- [ ] Documentation complete
- [ ] Works on macOS, Linux, and Windows

