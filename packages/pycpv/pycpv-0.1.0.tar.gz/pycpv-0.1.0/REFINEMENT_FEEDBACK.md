# CPV Design Refinement & Feedback

## Issues Found in Original Design

### 1. **Syntax Errors in utilities.py**
- **Issue**: Missing indentation in `DataCheckpointsManage` class definition
- **Impact**: Code won't run
- **Fixed**: ✓ Rewritten with proper Python syntax

### 2. **Circular/Unclear Imports**
- **Issue**: Original code had comments like `# import_model_init` without implementation
- **Impact**: Methods wouldn't actually do anything
- **Fixed**: ✓ Implemented all methods with actual DVC/Git operations

### 3. **Missing Error Handling**
- **Issue**: No try-catch blocks for S3, Git, or DVC operations
- **Impact**: Cryptic errors for users
- **Fixed**: ✓ Added comprehensive error handling and logging

---

## Key Design Refinements Made

### 1. **Configuration Management Extracted**
**Before**: No clear configuration setup
**After**: Dedicated `CPVConfig` class that handles:
- One-time AWS credential setup
- One-time Bitbucket SSH setup
- Configuration persistence in `~/.cpv/config.json`
- Validation of credentials

**Benefits**:
- Users only configure once
- Credentials stored securely
- Easy to validate setup

### 2. **Semantic Versioning Strategy Clarified**
**Before**: Vague mention of "increase by 0.1"
**After**: Clear algorithm:
- Extract last Git tag (e.g., `v1.2`)
- Auto-increment minor version: `v1.2` → `v1.3`
- Full version string: `v{major}.{minor}`
- Users can manually specify any version

**Code**:
```python
def _get_next_version(self) -> str:
    tags = self.read_checkpoint_tag()
    if not tags:
        return "v0.1"
    
    last_tag = max(tags)  # ['v0.1', 'v0.2', 'v1.0'] → 'v1.0'
    parts = last_tag.lstrip('v').split('.')
    minor = int(parts[-1]) + 1
    major = '.'.join(parts[:-1])
    return f"v{major}.{minor}"
```

### 3. **Dataclass-Based Return Values**
**Before**: Not specified what functions return
**After**: Typed dataclasses:
```python
@dataclass
class ModelArtifacts:
    model_path: str
    metrics: Dict[str, Any]
    timestamp: str
    tag: str
    size_mb: float

@dataclass
class DataArtifacts:
    data_path: str
    version: str
    timestamp: str
    tag: str
    size_mb: float
    sample_count: int = None
```

**Benefits**:
- Type safety
- IDE autocompletion
- Clear contract for users

### 4. **Kwargs Pattern for Flexibility**
**Before**: Methods with fixed parameters
**After**: Consistent `**kwargs` pattern for optional behavior:
```python
def tag_model_checkpoint(self, version_tag=None, message=None, **kwargs):
    verbose = kwargs.get('verbose', self.verbose)
    dry_run = kwargs.get('dry_run', False)
    force = kwargs.get('force', False)
```

**Common kwargs added**:
- `verbose: bool` - Detailed logging
- `dry_run: bool` - Preview without changes
- `force: bool` - Skip confirmations
- `notify: bool` - Send notifications
- `use_cache: bool` - Use local cache

### 5. **Template Files for Initialization**
**Before**: Not specified what gets created
**After**: Explicit templates:
```python
@staticmethod
def _get_train_script_template() -> str:
    """Returns complete Python training script template"""

@staticmethod
def _get_readme_template() -> str:
    """Returns formatted README with instructions"""
```

**Benefits**:
- Users have working starting point
- Clear documentation
- Fewer setup errors

### 6. **Combined Operations Class**
**Before**: Separate model and data classes, unclear how to tag both
**After**: `CombinedCheckpointsManage` for atomic operations:
```python
def tag_model_and_data(self, version_tag=None, ...):
    """Atomically tag both model and data"""
    model_tag = self.models.tag_model_checkpoint(...)
    data_tag = self.data.tag_data_checkpoint(...)
    return model_tag, data_tag
```

**Benefits**:
- Single version for both model and data
- Atomicity guaranteed
- Prevents mismatches

### 7. **Metadata Methods Added**
**Before**: No way to query checkpoint information
**After**: `get_model_metadata()` and `get_data_metadata()` methods:
```python
metadata = model_mcm.get_model_metadata(tag="v1.0")
# Returns: {tag, model_size_mb, metrics, timestamp, team_name, model_name}
```

**Benefits**:
- Compare versions easily
- Track model size changes
- Audit trail

---

## Recommended Next Steps

### Phase 1: Core Implementation (Weeks 1-2)
1. ✓ Design finalized (this document)
2. **TODO**: Complete `DataCheckpointsManage` implementation
3. **TODO**: Add unit tests for core functionality
4. **TODO**: Test AWS S3 and Git integration
5. **TODO**: Add proper logging configuration

### Phase 2: CLI & User Experience (Weeks 3-4)
1. **TODO**: Implement Click-based CLI interface
2. **TODO**: Add progress bars (tqdm) for uploads/downloads
3. **TODO**: Interactive setup wizard
4. **TODO**: Configuration validation before operations

### Phase 3: Advanced Features (Weeks 5-6)
1. **TODO**: Batch operations (manage multiple models)
2. **TODO**: Model comparison dashboard
3. **TODO**: Metrics visualization
4. **TODO**: Webhook notifications (Slack/Teams)
5. **TODO**: Database for metadata (optional)

### Phase 4: Documentation & Release (Weeks 7-8)
1. **TODO**: API documentation
2. **TODO**: Tutorial notebooks
3. **TODO**: Troubleshooting guide
4. **TODO**: Release on PyPI

---

## Questions & Decisions for Review

### 1. **Version Format**
**Options**:
- A) `v{major}.{minor}` (current: `v1.0`, `v1.1`)
- B) `v{major}.{minor}.{patch}` (semantic: `v1.0.0`, `v1.0.1`)
- C) `{YYYY-MM-DD-HH-MM}` (timestamp: `2026-01-10-15-30`)

**Recommendation**: Option A (current) - Simple, intuitive, works for most use cases

**Alternative**: Allow manual format in `tag_model_checkpoint()`

### 2. **Metrics Storage**
**Options**:
- A) JSON lines in `metrics.log` (current)
- B) CSV file with columns
- C) SQLite database
- D) External metrics platform (MLflow, Weights & Biases)

**Recommendation**: Option A for MVP, Option D as future enhancement

### 3. **Team/Model Naming Convention**
**Current**: `AI-{TeamName}` and `{model_name}` lowercase

**Questions**:
- Should team names be enforced? (e.g., must match Bitbucket project names)
- Should model names be enforced? (lowercase, no spaces)
- Should we validate against existing Bitbucket projects?

### 4. **Data Organization on S3**
**Current Structure**:
```
s3://vmo-model-checkpoints/
  ├── AI-Convo/
  │   ├── faster-whisper/
  │   └── gpt-whisper/
  ├── AI-Vision/
  │   └── yolov8/
  └── AI-NLP/
```

**Alternative**:
```
s3://vmo-model-checkpoints/
  ├── AI-Convo-faster-whisper/
  ├── AI-Convo-gpt-whisper/
  └── AI-Vision-yolov8/
```

**Recommendation**: Current structure (more intuitive, easier to navigate)

### 5. **Git Repository per Model or Shared Team Repo?**
**Current Design**: One Git repo per model
```
Bitbucket Project: AI-Convo-model-checkpoints
  ├── faster-whisper (repo)
  └── gpt-whisper (repo)
```

**Pros**:
- Each model has independent history
- Easier to manage permissions per model
- Cleaner git logs

**Cons**:
- More repositories to manage
- Can't easily compare across models in one team

**Recommendation**: Keep current (per-model repos)

### 6. **Atomic Tagging Requirements**
**Question**: Should `tag_model_and_data()` fail if either operation fails?

**Options**:
- A) Fail atomically (rollback if either fails)
- B) Partial success (tag whichever succeeds)
- C) Ask user on failure

**Recommendation**: Option A (atomic) - prevents inconsistent states

### 7. **Dry Run Behavior**
**Proposed**: `dry_run=True` shows what would happen without making changes

**Question**: Should dry run also validate that changes would succeed?

**Recommendation**: Yes - validate S3 access, git state, disk space, etc.

### 8. **Data Splitting Strategy**
**Question**: How to handle training/validation/test splits?

**Options**:
- A) All in `data/` directory, tracker by DVC
- B) Separate directories for each split
- C) Metadata file describing splits

**Recommendation**: Option B - cleaner, easier to manage

```
data/
├── train/
│   ├── audio/
│   └── labels/
├── validation/
│   ├── audio/
│   └── labels/
└── test/
    ├── audio/
    └── labels/
```

### 9. **Rollback Safety**
**Question**: Should we keep backups before reverting?

**Current**: Git history is backup
**Recommendation**: Sufficient for MVP. Future: Add backup command

### 10. **Multi-Account AWS Support**
**Question**: Should we support multiple AWS accounts/profiles?

**Current**: Single profile per setup
**Recommendation**: Current sufficient. Future: Multi-account support in config

---

## Implementation Checklist

### Core Classes
- [x] `CPVConfig` - Configuration management
- [x] `ModelsCheckpointsManage` - Model versioning (80% complete)
- [ ] `DataCheckpointsManage` - Data versioning (skeleton)
- [x] `CombinedCheckpointsManage` - Combined operations

### Key Methods
- [x] `__init__()` with kwargs
- [x] `import_model_init()` / `import_data_init()`
- [x] `upload_model_checkpoint()` / `upload_data_checkpoint()`
- [x] `download_model_checkpoint()` / `download_data_checkpoint()`
- [x] `tag_model_checkpoint()` / `tag_data_checkpoint()`
- [x] `read_checkpoint_tag()`
- [x] `revert_model_checkpoint()` / `revert_data_checkpoint()`
- [x] `get_model_metadata()` / `get_data_metadata()`

### Configuration
- [x] AWS S3 setup
- [x] Bitbucket SSH setup
- [x] Credential validation
- [x] Configuration persistence

### Features
- [x] Auto-versioning
- [x] Dry run mode
- [x] Verbose logging
- [ ] Progress bars (tqdm)
- [ ] Interactive setup wizard
- [ ] Batch operations
- [ ] Error recovery suggestions

---

## Testing Strategy

### Unit Tests
```python
# test_cpv_config.py
- test_config_save_load()
- test_aws_profile_setup()
- test_bitbucket_ssh_setup()
- test_credential_validation()

# test_model_checkpoints.py
- test_model_init()
- test_model_upload()
- test_model_download()
- test_model_tagging()
- test_model_revert()
- test_auto_versioning()

# test_data_checkpoints.py
- Similar to model tests

# test_combined_checkpoints.py
- test_atomic_tagging()
- test_combined_revert()
```

### Integration Tests
```python
# test_integration.py
- test_full_workflow_init_to_tag()
- test_multi_version_management()
- test_s3_and_git_sync()
- test_concurrent_operations()
```

### Manual Testing
- [ ] Test on macOS, Linux, Windows
- [ ] Test with large models (>1GB)
- [ ] Test with slow network
- [ ] Test with missing S3 bucket
- [ ] Test with invalid Git credentials

---

## Dependencies Review

### Required
```
boto3 >= 1.26         # AWS S3 (already in pyproject.toml)
GitPython >= 3.1      # Git operations (need to add)
dvc >= 3.66.1         # Data versioning (already present)
dvc-s3 >= 3.2.2       # S3 backend (already present)
pydantic >= 2.0       # Config validation (need to add)
click >= 8.0          # CLI framework (need to add - future)
```

### Optional
```
tqdm >= 4.67.1        # Progress bars (already present)
pyyaml >= 6.0         # YAML parsing (need to add)
python-dotenv >= 1.0  # .env support (nice to have)
requests >= 2.28      # HTTP validation (nice to have)
```

### Missing from pyproject.toml
```toml
dependencies = [
    "aws>=0.2.5",           # ✓ Existing
    "dvc>=3.66.1",          # ✓ Existing
    "dvc-s3>=3.2.2",        # ✓ Existing
    "scipy>=1.16.3",        # ✓ Existing
    "tqdm>=4.67.1",         # ✓ Existing
    "tree>=0.2.4",          # ✓ Existing
    # Add these:
    "boto3>=1.26.0",        # AWS SDK
    "GitPython>=3.1.0",     # Git operations
    "pydantic>=2.0.0",      # Config validation
    "click>=8.0.0",         # CLI (for future)
    "pyyaml>=6.0.0",        # YAML parsing
]
```

---

## Summary

The **cpv** package design provides:

1. **Clear Architecture** - Separation of concerns (config, models, data)
2. **Type Safety** - Typed dataclasses and proper return types
3. **Flexibility** - kwargs pattern for optional features
4. **User Experience** - Dry run, verbose logging, auto-increment versioning
5. **Error Handling** - Comprehensive validation and logging
6. **Atomicity** - Combined operations prevent inconsistent states
7. **Extensibility** - Easy to add features (notifications, dashboards, etc.)

The implementation is ready for Phase 1 (Core Implementation) with most core logic complete and ready for testing.
