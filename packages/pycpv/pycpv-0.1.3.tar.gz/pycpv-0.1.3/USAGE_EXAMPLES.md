# CPV Package - Usage Examples

## Installation & Configuration

### 1. Initial Setup

```python
from cp_manage.utilities import CPVConfig

# One-time AWS configuration
config = CPVConfig()
config.setup_aws_profile(
    credential_path="~/.aws/credentials",
    aws_profile="default",
    verbose=True
)

# One-time Bitbucket SSH configuration
config.setup_bitbucket_ssh(
    keygen_filename="id_rsa_bitbucket",
    bitbucket_user="your_username"
)

# Validate connectivity
is_valid = config.validate_credentials(verbose=True)
```

## Model Checkpoint Management

### 2. Initialize New Model

```python
from cp_manage.utilities import ModelsCheckpointsManage

# Initialize new model repository
model_mcm = ModelsCheckpointsManage(
    team_name="AI-Convo",
    model_name="faster-whisper",
    repo_path="./faster-whisper",
    verbose=True
)

model_mcm.import_model_init(
    data_path="./raw_training_data",
    force=False
)

# This creates:
# faster-whisper/
# ├── .git/
# ├── .dvc/
# ├── data/                    (from raw_training_data)
# ├── model.bin                (placeholder)
# ├── metrics.log              (placeholder)
# ├── train.py                 (template)
# ├── README.md
# └── .gitignore
```

### 3. Upload Model Checkpoint

```python
# After training, upload model checkpoint
commit_hash = model_mcm.upload_model_checkpoint(
    model_path="./faster-whisper/model.bin",
    metrics={
        "loss": 0.245,
        "accuracy": 0.967,
        "wer": 0.042,
        "epochs": 50,
        "learning_rate": 0.0001
    },
    verbose=True
)

# Tag the checkpoint
tag = model_mcm.tag_model_checkpoint(
    version_tag="v1.0",
    message="Initial model trained on 10k hours of audio",
    verbose=True
)

# Or auto-increment from previous tag
tag = model_mcm.tag_model_checkpoint(
    # version_tag=None,  # Auto-increment: v0.1 → v0.2
    message="Improved preprocessing pipeline"
)
```

### 4. List Available Checkpoints

```python
# View all available model checkpoints
tags = model_mcm.read_checkpoint_tag()
print(f"Available versions: {tags}")
# Output: ['v0.1', 'v0.2', 'v1.0', 'v1.1']

# Get metadata for current model
metadata = model_mcm.get_model_metadata()
print(metadata)
# {
#   'tag': 'HEAD',
#   'model_size_mb': 1234.5,
#   'metrics': {'loss': 0.245, 'accuracy': 0.967, ...},
#   'timestamp': '2026-01-10T15:30:00',
#   'team_name': 'AI-Convo',
#   'model_name': 'faster-whisper'
# }

# Get metadata for specific version
metadata_v1 = model_mcm.get_model_metadata(tag="v1.0")
```

### 5. Download Specific Checkpoint

```python
# Download and checkout specific model version
artifacts = model_mcm.download_model_checkpoint(
    tag="v1.0",
    verbose=True
)

print(f"Model path: {artifacts.model_path}")
print(f"Metrics: {artifacts.metrics}")
print(f"Size: {artifacts.size_mb} MB")
# Output:
# Model path: /path/to/faster-whisper/model.bin
# Metrics: {'loss': 0.245, 'accuracy': 0.967, ...}
# Size: 1234.5 MB
```

### 6. Revert to Previous Version

```python
# Quick revert to specific checkpoint
model_mcm.revert_model_checkpoint(
    tag="v1.0",
    verbose=True
)

# Revert multiple steps (auto-detect)
model_mcm.revert_model_checkpoint(
    tag="v0.5",
    verbose=True
)
```

## Data Checkpoint Management

### 7. Upload Training Data

```python
from cp_manage.utilities import DataCheckpointsManage

data_mcm = DataCheckpointsManage(
    team_name="AI-Convo",
    model_name="faster-whisper",
    repo_path="./faster-whisper"
)

# Upload training data
data_commit = data_mcm.upload_data_checkpoint(
    data_path="./faster-whisper/data",
    verbose=True
)

# Tag data checkpoint
data_tag = data_mcm.tag_data_checkpoint(
    version_tag="v1.0",
    message="Training set: 10k hours of multilingual audio"
)
```

### 8. List & Download Data Versions

```python
# List available data versions
data_tags = data_mcm.read_data_checkpoint_tag()

# Get data metadata
data_metadata = data_mcm.get_data_metadata(tag="v1.0")

# Download specific data version
data_artifacts = data_mcm.download_data_checkpoint(
    tag="v1.0",
    output_dir="./downloaded_data"
)
```

### 9. Revert Data to Previous Version

```python
# Revert training data
data_mcm.revert_data_checkpoint(tag="v1.0")
```

## Combined Model & Data Management

### 10. Atomic Model + Data Tagging

```python
from cp_manage.utilities import CombinedCheckpointsManage

combined = CombinedCheckpointsManage(
    team_name="AI-Convo",
    model_name="faster-whisper",
    repo_path="./faster-whisper"
)

# Tag both model and data atomically
model_tag, data_tag = combined.tag_model_and_data(
    version_tag="v2.0",
    model_message="Faster-Whisper v2: multilingual improvements",
    data_message="Extended dataset with 20k hours of audio"
)

print(f"Model version: {model_tag}")
print(f"Data version: {data_tag}")
```

### 11. Revert Both Model & Data

```python
# Go back to specific snapshot
combined.revert_model_and_data(tag="v1.0")
```

### 12. Get Combined Metadata

```python
# Get metadata for both model and data at specific tag
metadata = combined.get_combined_metadata(tag="v1.0")

print(metadata)
# {
#   'model': {
#     'tag': 'v1.0',
#     'model_size_mb': 1234.5,
#     'metrics': {...},
#     ...
#   },
#   'data': {
#     'tag': 'v1.0',
#     'version': '1.0',
#     'size_mb': 450000.0,
#     ...
#   },
#   'timestamp': '2026-01-10T15:30:00'
# }
```

## Advanced Usage Patterns

### 13. Experiment Tracking

```python
# Track multiple experiments with different hyperparameters

experiments = [
    {"lr": 0.001, "batch_size": 32, "epochs": 50},
    {"lr": 0.0001, "batch_size": 64, "epochs": 100},
    {"lr": 0.00001, "batch_size": 128, "epochs": 150},
]

for i, params in enumerate(experiments, 1):
    # Train with parameters
    # ...
    
    model_mcm.upload_model_checkpoint(
        metrics={**params, "val_loss": 0.25, "val_acc": 0.96},
        verbose=True
    )
    
    tag = model_mcm.tag_model_checkpoint(
        message=f"Experiment {i}: LR={params['lr']}, BS={params['batch_size']}"
    )
    print(f"Checkpoint saved as: {tag}")
```

### 14. Dry Run Mode (Preview Changes)

```python
# Preview what would happen without making changes
tag = model_mcm.tag_model_checkpoint(
    version_tag="v2.0",
    message="New version",
    dry_run=True,  # No actual changes
    verbose=True
)

# Verify metrics would be correct
model_mcm.upload_model_checkpoint(
    metrics={"loss": 0.25},
    dry_run=True,  # Preview only
    verbose=True
)
```

### 15. Error Handling

```python
from pathlib import Path

try:
    model_mcm.import_model_init()
except FileNotFoundError as e:
    print(f"Data path not found: {e}")

try:
    model_mcm.revert_model_checkpoint("v99.0")
except git.exc.GitCommandError as e:
    print(f"Tag not found: {e}")

try:
    config.validate_credentials()
except Exception as e:
    print(f"Credentials invalid: {e}")
    print("Run: cpv aws-config && cpv bitbucket-config")
```

### 16. Multi-Team Management

```python
# Manage models across different teams

teams = ["AI-Convo", "AI-Vision", "AI-Planning"]
models = {
    "AI-Convo": ["faster-whisper", "openai-whisper"],
    "AI-Vision": ["yolov8", "efficientnet"],
    "AI-NLP": ["bert-large", "t5-base"]
}

# Manage each model
for team, model_list in models.items():
    for model in model_list:
        mcm = ModelsCheckpointsManage(team, model)
        
        # Check current state
        latest_tag = mcm.read_checkpoint_tag()[-1] if mcm.read_checkpoint_tag() else None
        print(f"{team}/{model}: {latest_tag}")
```

### 17. Batch Operations

```python
# Manage multiple versions at once

def backup_all_checkpoints(team_name, model_name):
    """Backup all checkpoints to external location"""
    mcm = ModelsCheckpointsManage(team_name, model_name)
    
    for tag in mcm.read_checkpoint_tag():
        artifacts = mcm.download_model_checkpoint(tag=tag)
        # Save artifacts to backup location
        print(f"Backed up {tag}: {artifacts.model_path}")

def compare_versions(team_name, model_name, tag1, tag2):
    """Compare metrics between two versions"""
    mcm = ModelsCheckpointsManage(team_name, model_name)
    
    meta1 = mcm.get_model_metadata(tag=tag1)
    meta2 = mcm.get_model_metadata(tag=tag2)
    
    print(f"Version {tag1} metrics: {meta1['metrics']}")
    print(f"Version {tag2} metrics: {meta2['metrics']}")
    
    # Calculate improvement
    if 'accuracy' in meta1['metrics'] and 'accuracy' in meta2['metrics']:
        improvement = meta2['metrics']['accuracy'] - meta1['metrics']['accuracy']
        print(f"Accuracy improvement: {improvement:.2%}")

# Usage
backup_all_checkpoints("AI-Convo", "faster-whisper")
compare_versions("AI-Convo", "faster-whisper", "v1.0", "v1.1")
```

## CLI Usage (Future)

```bash
# Configuration
cpv aws-config --credential-path ~/.aws/credentials
cpv bitbucket-config --keygen-filename id_rsa_bitbucket
cpv validate

# Initialize model
cpv init --team-name AI-Convo --model-name faster-whisper --data-path ./data

# Model operations
cpv model upload --tag v1.0 --message "Initial release"
cpv model list-tags
cpv model download --tag v1.0 --output-dir ./models
cpv model revert --tag v1.0
cpv model info --tag v1.0

# Data operations
cpv data upload --tag v1.0
cpv data list-tags
cpv data download --tag v1.0

# Combined operations
cpv checkpoint create --tag v1.0 --message "v1.0 release"
cpv checkpoint list
cpv checkpoint revert --tag v1.0
```

## Configuration File Location

CPV stores configuration at: `~/.cpv/config.json`

```json
{
  "aws_credential_path": "/home/user/.aws/credentials",
  "aws_profile": "default",
  "bitbucket_ssh_keyfile": "/home/user/.ssh/id_rsa_bitbucket",
  "last_updated": "2026-01-10T15:30:00.000000"
}
```

## Directory Structure Created by CPV

```
/home/user/
├── .cpv/
│   ├── config.json              # Main configuration
│   └── logs/                    # Operation logs
│
├── .ssh/
│   ├── config                   # SSH config for Bitbucket
│   └── id_rsa_bitbucket         # SSH key for Bitbucket
│
├── .aws/
│   └── credentials              # AWS credentials
│
└── projects/
    └── faster-whisper/          # Model workspace
        ├── .git/                # Git repo for versioning
        ├── .dvc/                # DVC configuration
        ├── data/                # Training data (synced via DVC)
        ├── model.bin            # Model weights (synced via DVC)
        ├── metrics.log          # Metrics log
        ├── train.py             # Training script
        ├── README.md            # Documentation
        ├── .gitignore           # Git ignore rules
        ├── data.dvc             # DVC pointer to data in S3
        ├── model.bin.dvc        # DVC pointer to model in S3
        └── metrics.log.dvc      # DVC pointer to metrics
```
