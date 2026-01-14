# CPV Quick Reference Card

## Installation & Setup

```python
# Install CPV
pip install cpv

# One-time configuration
cpv aws-config --credential-path ~/.aws/credentials
cpv bitbucket-config --keygen-filename id_rsa_bitbucket
cpv validate
```

## Common Operations

### Initialize New Model
```python
from cp_manage.utilities import ModelsCheckpointsManage

mcm = ModelsCheckpointsManage("AI-Convo", "faster-whisper")
mcm.import_model_init(data_path="./training_data")
```

### Upload Model Checkpoint
```python
mcm.upload_model_checkpoint(
    model_path="./model.bin",
    metrics={"loss": 0.25, "accuracy": 0.96}
)

tag = mcm.tag_model_checkpoint(
    version_tag="v1.0",
    message="Baseline model"
)
```

### Download Model
```python
artifacts = mcm.download_model_checkpoint(tag="v1.0")
print(artifacts.model_path)      # Path to downloaded model
print(artifacts.metrics)          # Metrics dict
print(artifacts.size_mb)          # File size
```

### List & Revert Versions
```python
# List all versions
versions = mcm.read_checkpoint_tag()

# Revert to previous version
mcm.revert_model_checkpoint(tag="v1.0")
```

### Combined Model + Data Versioning
```python
from cp_manage.utilities import CombinedCheckpointsManage

combined = CombinedCheckpointsManage("AI-Convo", "faster-whisper")

# Tag both atomically
model_tag, data_tag = combined.tag_model_and_data(
    version_tag="v1.0",
    model_message="Model improvements",
    data_message="Extended dataset"
)

# Revert both
combined.revert_model_and_data(tag="v1.0")
```

## Folder Structure

```
model_name/
├── data/                 # Training data (tracked by DVC)
│   ├── train/
│   ├── validation/
│   └── test/
├── model.bin             # Model weights (tracked by DVC)
├── metrics.log           # Metrics file (tracked by DVC)
├── train.py              # Training script
├── README.md             # Documentation
├── .gitignore            # Git ignore rules
└── .dvc/                 # DVC metadata
```

## Configuration Location

- **Config File**: `~/.cpv/config.json`
- **SSH Key**: `~/.ssh/id_rsa_bitbucket`
- **AWS Credentials**: `~/.aws/credentials`

## Git Tags
- **Format**: `v{major}.{minor}` (e.g., `v1.0`, `v1.1`)
- **Auto-increment**: v1.0 → v1.1 → v2.0
- **Manual**: Can specify any tag name

## Error Handling

```python
from cp_manage.utilities import CredentialError

try:
    mcm.download_model_checkpoint(tag="v1.0")
except CredentialError:
    print("Run: cpv aws-config && cpv bitbucket-config")
```

## Key Method Parameters

### Common kwargs
- `verbose: bool = False` - Detailed logging
- `dry_run: bool = False` - Preview without making changes
- `force: bool = False` - Skip confirmations

### Model Operations
```python
mcm.upload_model_checkpoint(
    model_path="./model.bin",      # Required: path to model
    metrics={"loss": 0.25},        # Optional: metrics dict
    verbose=True,                  # Optional: logging
    dry_run=False                  # Optional: preview mode
)

mcm.tag_model_checkpoint(
    version_tag="v1.0",            # Optional: auto-increment if None
    message="Release v1.0",        # Optional: tag message
    verbose=True,
    dry_run=False
)

mcm.download_model_checkpoint(
    tag="v1.0",                    # Optional: defaults to HEAD
    verbose=True
)

mcm.revert_model_checkpoint(
    tag="v1.0",                    # Required: tag to revert to
    verbose=True,
    dry_run=False
)

mcm.get_model_metadata(
    tag="v1.0"                     # Optional: defaults to HEAD
)
```

## Data Operations
```python
from cp_manage.utilities import DataCheckpointsManage

data_mcm = DataCheckpointsManage("AI-Convo", "faster-whisper")

data_mcm.upload_data_checkpoint(data_path="./data")
data_tag = data_mcm.tag_data_checkpoint(version_tag="v1.0")
data_artifacts = data_mcm.download_data_checkpoint(tag="v1.0")
data_mcm.revert_data_checkpoint(tag="v1.0")
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AWS credentials error | Run: `cpv aws-config` |
| Bitbucket SSH error | Run: `cpv bitbucket-config` |
| Tag not found | Check with: `mcm.read_checkpoint_tag()` |
| S3 not accessible | Verify with: `config.validate_credentials()` |
| Model too large | Check S3 bucket limits (default: 50GB max) |

## Return Types

### ModelArtifacts
```python
artifacts = mcm.download_model_checkpoint(tag="v1.0")
# Returns:
# artifacts.model_path: str        # Path to downloaded model
# artifacts.metrics: Dict[str, Any] # Metrics dictionary
# artifacts.timestamp: str         # ISO timestamp
# artifacts.tag: str              # Git tag
# artifacts.size_mb: float        # File size in MB
```

### Metadata Dictionary
```python
metadata = mcm.get_model_metadata(tag="v1.0")
# Returns dict with:
# - tag: Version tag
# - model_size_mb: File size
# - metrics: Training metrics
# - timestamp: Creation time
# - team_name: Team name
# - model_name: Model name
```

## File Operations

```python
# What gets created by import_model_init()
model.bin              # 1KB placeholder (replaced by real model)
metrics.log            # Empty metrics file
train.py               # Template training script
README.md              # Getting started guide
.gitignore             # Ignore patterns
data/                  # Training data directory
.dvc/                  # DVC configuration

# What gets created by upload/tag operations
model.bin.dvc          # DVC pointer to S3 model
data.dvc               # DVC pointer to S3 data
metrics.log.dvc        # DVC pointer to S3 metrics
```

## CLI Commands (Available Soon)

```bash
# Configuration
cpv aws-config
cpv bitbucket-config
cpv validate

# Initialize
cpv init --team-name AI-Convo --model-name faster-whisper

# Model operations
cpv model upload --tag v1.0
cpv model list-tags
cpv model download --tag v1.0
cpv model revert --tag v1.0

# Data operations
cpv data upload --tag v1.0
cpv data list-tags
cpv data download --tag v1.0

# Combined
cpv checkpoint create --tag v1.0
cpv checkpoint revert --tag v1.0
```

## Performance Tips

1. **Compress data** before upload for faster transfers
2. **Use `dry_run=True`** to preview large operations
3. **Tag incrementally** rather than all at once
4. **Keep metrics.log** concise (reasonable size limit)
5. **Use `verbose=True`** for troubleshooting

## Best Practices

1. ✅ **Commit before tagging**: Ensure git repo is clean
2. ✅ **Include meaningful messages**: Describe what changed
3. ✅ **Tag after training**: Not during training
4. ✅ **Use semantic versions**: v1.0 for major, v1.1 for minor
5. ✅ **Document metrics**: Log exact metrics used for comparison
6. ✅ **Backup important models**: Tag production releases
7. ✅ **Review metadata**: Before downloading large models

## Related Documentation

- **Full Design**: See `CPV_DESIGN.md`
- **Usage Examples**: See `USAGE_EXAMPLES.md` (17 detailed examples)
- **Refinement Details**: See `REFINEMENT_FEEDBACK.md`
- **Implementation Steps**: See `IMPLEMENTATION_GUIDE.md`
- **Executive Summary**: See `EXECUTIVE_SUMMARY.md`

---

**Last Updated**: January 10, 2026
**CPV Version**: 0.1.0 (MVP)
**Status**: Ready for Phase 1 Implementation
