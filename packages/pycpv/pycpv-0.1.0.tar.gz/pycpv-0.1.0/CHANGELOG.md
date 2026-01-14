# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-13

### Added
- **CPVConfig**: Configuration management for AWS and Bitbucket
  - One-time setup for AWS credentials
  - SSH key configuration for Bitbucket
  - Credential validation and verification
  - Configuration persistence in ~/.cpv/config.json

- **ModelsCheckpointsManage**: Complete model versioning system
  - Repository initialization with git and DVC
  - Model checkpoint upload to S3
  - Model checkpoint download with artifacts
  - Semantic versioning with auto-increment (v0.1, v0.2, v1.0, etc.)
  - Git tagging and version history
  - Metrics tracking and metadata storage
  - Model revert to previous versions
  - Template generation (train.py, README.md)

- **DataCheckpointsManage**: Data versioning (skeleton implementation)
  - Upload/download data checkpoints
  - Version tagging and history
  - Revert capabilities
  - Ready for full implementation

- **CombinedCheckpointsManage**: Atomic operations
  - Simultaneous model and data tagging
  - Combined metadata retrieval
  - Synchronized versioning to prevent mismatches

- **Logging System**
  - Console output (INFO level)
  - File logging (DEBUG level)
  - Per-model log files at {repo_path}/.cpv.log
  - Formatted timestamps and log levels

- **Type Safety**
  - 100% type hints throughout codebase
  - Dataclass-based return types (ModelArtifacts, DataArtifacts)
  - Comprehensive docstrings (Google-style)

- **Testing Suite**
  - 45 comprehensive unit and integration tests
  - 100% test pass rate
  - Test isolation using pytest fixtures
  - Mocked external dependencies (Git, boto3)
  - Configuration, model, data, and workflow tests

- **Documentation**
  - Comprehensive README with quick start
  - API reference documentation
  - Architecture diagrams
  - Usage examples with code snippets
  - Design documentation
  - Implementation guide

### Features
- Semantic versioning with automatic increment
- AWS S3 backend for model storage
- Bitbucket integration for version control
- DVC for large file tracking
- Metrics and metadata per checkpoint
- One-time configuration setup
- Dry-run mode for testing
- Verbose logging options
- Kwargs-based flexible method signatures

### Architecture
- Git (Bitbucket) → DVC pointers → AWS S3
- S3 bucket: s3://vmo-model-checkpoints/
- Config location: ~/.cpv/config.json
- Log location: {repo_path}/.cpv.log
- Bitbucket projects: AI-{team_name}-model-checkpoints

### Testing
- 15 configuration tests
- 19 model checkpoint tests
- 11 integration tests
- Fixtures for AWS credentials, Git mocks, file systems
- 100% code coverage for core functionality

[0.1.0]: https://github.com/yourusername/cpv/releases/tag/0.1.0
