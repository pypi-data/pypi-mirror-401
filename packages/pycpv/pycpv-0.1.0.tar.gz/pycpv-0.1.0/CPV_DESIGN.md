# CPV (Checkpoints Versioning) - Refined Design Document

## 1. Architecture Overview

### Storage Strategy
```
Bitbucket (Git):
  Project: AI-{TeamName}-model-checkpoints/
    └── {model_name}/
        ├── .git/
        ├── .dvc/
        ├── data/                    # training datasets (tracked by DVC)
        ├── model.bin                # model weights (tracked by DVC)
        ├── metrics.log              # metrics file (tracked by DVC)
        ├── train.py                 # training script
        ├── README.md
        ├── .gitignore
        ├── data.dvc                 # DVC pointers to S3
        ├── model.bin.dvc
        └── metrics.log.dvc

AWS S3:
  s3://vmo-model-checkpoints/
    └── {team_name}/
        └── {model_name}/
            ├── data/                # training data versions
            ├── model.bin            # model checkpoint versions
            └── metrics.log          # metrics history
```

## 2. Core Classes & Methods

### Class: `ModelsCheckpointsManage`
```python
Methods:
  __init__(team_name: str, model_name: str, **kwargs)
  
  # Initialization
  import_model_init(data_path=None, **kwargs) -> None
    """Initialize new model repo structure"""
    
  # Model operations
  load_model(tag: str = None, **kwargs) -> ModelArtifacts
    """Download specific model version from S3"""
    
  upload_model_checkpoint(model_path: str, metrics: dict = None, **kwargs) -> str
    """Upload model to S3 via DVC and commit to Git"""
    
  download_model_checkpoint(tag: str = None, **kwargs) -> ModelArtifacts
    """Fetch specific model checkpoint"""
    
  tag_model_checkpoint(version_tag: str = None, message: str = None, **kwargs) -> str
    """Tag current model state (git tag + dvc add model.bin)"""
    - Auto-increment: if version_tag is None, increment last tag by 0.1
    - Returns: new tag name (e.g., "v1.0", "v1.1")
    
  read_checkpoint_tag(**kwargs) -> List[str]
    """List all available model tags"""
    
  revert_model_checkpoint(tag: str, **kwargs) -> None
    """Checkout to specific model version"""
    - git checkout <tag>
    - dvc checkout
    
  get_model_metadata(tag: str = None, **kwargs) -> dict
    """Get model metadata (timestamp, metrics, size, etc)"""
```

### Class: `DataCheckpointsManage`
```python
Methods:
  __init__(team_name: str, model_name: str, **kwargs)
  
  import_data_init(data_path: str, **kwargs) -> None
    """Initialize training data directory"""
    
  upload_data_checkpoint(data_path: str, **kwargs) -> str
    """Upload training data to S3 via DVC"""
    
  download_data_checkpoint(tag: str = None, **kwargs) -> str
    """Download specific data version"""
    
  tag_data_checkpoint(version_tag: str = None, message: str = None, **kwargs) -> str
    """Tag data checkpoint with auto-increment"""
    
  read_data_checkpoint_tag(**kwargs) -> List[str]
    """List all data tags"""
    
  revert_data_checkpoint(tag: str, **kwargs) -> None
    """Revert to specific data version"""
    
  get_data_metadata(tag: str = None, **kwargs) -> dict
    """Get data metadata (size, version count, timestamp)"""
```

### Class: `CombinedCheckpointsManage`
```python
Methods:
  __init__(team_name: str, model_name: str, **kwargs)
  
  tag_model_and_data(version_tag: str = None, 
                     model_message: str = None,
                     data_message: str = None,
                     **kwargs) -> Tuple[str, str]
    """Atomically tag both model and data
    - DVC add model.bin, data/, metrics.log
    - git add *.dvc, .gitignore
    - git commit
    - git tag
    - Returns: (model_tag, data_tag)
    """
    
  revert_model_and_data(tag: str, **kwargs) -> None
    """Revert both model and data to specific version"""
    
  get_combined_metadata(tag: str = None, **kwargs) -> dict
    """Get metadata for both model and data at tag"""
```

## 3. Configuration Management

### Class: `CPVConfig`
```python
Methods:
  setup_aws_profile(credential_path: str = None, 
                    aws_profile: str = "default",
                    **kwargs) -> None
    """
    One-time AWS setup:
    1. Prompt for AWS credential file path (if not provided)
    2. Save path to ~/.cpv/config.json
    3. Load credential profile
    4. Configure DVC remote to S3
    5. Verify connectivity
    """
    
  setup_bitbucket_ssh(keygen_filename: str = None,
                      bitbucket_user: str = None,
                      **kwargs) -> None
    """
    One-time Bitbucket SSH setup:
    1. Generate/use SSH key
    2. Instruct user to add key to Bitbucket profile
    3. Create ~/.ssh/config entry
    4. Test SSH connectivity
    """
    
  get_config(key: str = None) -> dict
    """Retrieve stored configuration"""
    
  validate_credentials(**kwargs) -> bool
    """Verify AWS S3 and Bitbucket connectivity"""
```

## 4. CLI Commands

```
# Main commands:
cpv init [--team-name] [--model-name] [--data-path]
cpv aws-config [--credential-path] [--profile]
cpv bitbucket-config [--keygen-filename]
cpv validate

# Model operations:
cpv model upload [--tag] [--message]
cpv model download [--tag] [--output-dir]
cpv model list-tags
cpv model revert [--tag]
cpv model info [--tag]

# Data operations:
cpv data upload [--tag] [--message]
cpv data download [--tag] [--output-dir]
cpv data list-tags
cpv data revert [--tag]
cpv data info [--tag]

# Combined operations:
cpv checkpoint create [--tag] [--message]
cpv checkpoint list
cpv checkpoint revert [--tag]
```

## 5. Key Design Decisions

### Version Tagging Strategy
- **Default behavior**: Auto-increment from previous tag
  - v0.0 → v0.1 → v0.2 (patch increment)
  - Allow manual specification: v1.0, v2.0
- **Tag format**: `v{major}.{minor}` with semantic meaning
- **Stored in**: Git tags + metadata in .dvc files

### DVC Integration Points
```
1. dvc add <file>           # Track model, data, metrics
2. dvc push                 # Upload to S3
3. dvc pull                 # Download from S3
4. dvc checkout             # Switch versions
5. dvc remote add           # Configure S3 backend
```

### Git Integration Points
```
1. git add *.dvc
2. git commit -m "Model v1.0: {description}"
3. git tag -a "v1.0" -m "{message}"
4. git checkout <tag>
```

### Error Handling Strategy
- Atomic operations: if any step fails, rollback
- Validation before operations (S3 connectivity, Git repo state)
- Clear error messages with recovery suggestions
- Logging for debugging

### Configuration Persistence
```
~/.cpv/
├── config.json              # Paths, profiles, settings
├── aws_credentials          # Symlink to user's AWS credentials
└── logs/                    # Operation logs
```

## 6. Kwargs Patterns

### Common Kwargs
```python
# Logging
verbose: bool = False
log_file: str = None

# Dry run
dry_run: bool = False       # Show what would happen without doing it

# Force operations
force: bool = False         # Skip confirmations

# Notifications
notify: bool = False        # Send notifications on completion

# Caching
use_cache: bool = True      # Use local cache before fetching S3

# Custom paths
repo_path: str = None       # Override default repo path
working_dir: str = None     # Custom working directory
```

## 7. File Structure Template for `cpv init`

```
{model_name}/
├── README.md               # Instructions for training
├── train.py                # Placeholder training script
├── data/                   # Training data directory (tracked by DVC)
│   └── .gitkeep
├── model.bin               # Initial model weights (tracked by DVC)
├── metrics.log             # Metrics tracking file (tracked by DVC)
├── .gitignore              # Git ignore patterns
├── .dvc/.gitignore         # DVC-specific ignore
└── dvc.yaml                # DVC pipeline definition (optional)
```

## 8. Validation Checklist

Before each operation:
- [ ] AWS S3 bucket accessible
- [ ] Git repository clean (no uncommitted changes)
- [ ] DVC remote configured
- [ ] Sufficient disk space
- [ ] Network connectivity
- [ ] Required files exist (model.bin, data/, etc.)
- [ ] Tag format valid and unique

## 9. Dependencies

```
Required:
- boto3              # AWS S3 API
- gitpython          # Git operations
- dvc>=3.66.1        # Data versioning
- dvc-s3>=3.2.2      # S3 backend for DVC
- pydantic           # Config validation
- click              # CLI framework
- tqdm               # Progress bars

Optional:
- pyyaml             # YAML parsing for dvc.yaml
- python-dotenv      # .env file support
- requests           # HTTP requests for validation
```

## 10. Naming Conventions

- **Variables**: `snake_case`
- **Classes**: `PascalCase`
- **Methods**: `snake_case`
- **Exceptions**: `{Action}Error`, `{Action}Exception`
- **Git tags**: `v{major}.{minor}` (e.g., `v1.0`, `v2.5`)
- **S3 paths**: `s3://vmo-model-checkpoints/{team_name}/{model_name}/`
- **Config keys**: `snake_case_lowercase`

---

## Questions for Refinement

1. **Semantic vs. Patch Versioning**: Should we support full semantic versioning (v1.2.3)?
2. **Model Artifacts**: Besides .bin and metrics, what other files should be tracked?
3. **Data Splitting**: Should different data versions be tagged separately from models?
4. **Rollback Safety**: Should we maintain backup before reverting, or trust Git history?
5. **Batch Operations**: Need ability to manage multiple models at once?
6. **Permissions**: Need team-based access control in Bitbucket integration?
7. **Metrics Tracking**: Should metrics be stored separately (e.g., database) or in metrics.log?
