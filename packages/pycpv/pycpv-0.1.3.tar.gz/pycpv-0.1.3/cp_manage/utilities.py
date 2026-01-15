"""
CPV (Checkpoints Versioning) - Utilities Module

Handles model and data checkpoint management using DVC and Git.
AWS S3 backend: s3://vmo-test-checkpoint-bucket/{team_name}/{model_name}/
Git backend: Bitbucket project AI-{team_name}-model-checkpoints
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
import subprocess
import git
import boto3
# from dvc.exceptions import DVCError


logger = logging.getLogger(__name__)


def setup_file_logging(log_path: Path) -> None:
    """
    Setup file logging for CPV operations
    
    Args:
        log_path: Path to log file (e.g., {model_repo_path}/.cpv.log)
    """
    if not logger.handlers:  # Only setup if not already configured
        # Ensure log directory exists
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # File handler
        file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)


@dataclass
class ModelArtifacts:
    """Container for model checkpoint artifacts"""
    model_path: str
    metrics: Dict[str, Any]
    timestamp: str
    tag: str
    size_mb: float


@dataclass
class DataArtifacts:
    """Container for data checkpoint artifacts"""
    data_path: str
    version: str
    timestamp: str
    tag: str
    size_mb: float
    sample_count: int = None


class CPVConfig:
    """Manages CPV configuration and credentials"""
    
    CONFIG_DIR = Path.home() / ".cpv"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    
    def __init__(self):
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self._config: Dict[str, Any] = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from disk"""
        if self.CONFIG_FILE.exists():
            with open(self.CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {
            "aws_credential_path": None,
            "aws_profile": "default",
            "bitbucket_ssh_keyfile": None,
            "last_updated": None
        }
    
    def _save_config(self) -> None:
        """Save configuration to disk"""
        self._config["last_updated"] = datetime.now().isoformat()
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self._config, f, indent=2)
    
    def setup_aws_profile(self, 
                         credential_path: Optional[str] = None,
                         aws_profile: str = "default",
                         **kwargs) -> None:
        """
        Configure AWS S3 credentials for DVC
        
        Args:
            credential_path: Path to AWS credentials file
            aws_profile: AWS profile name to use
            **kwargs: Additional options (verbose, dry_run, etc.)
        """
        verbose = kwargs.get('verbose', False)
        dry_run = kwargs.get('dry_run', False)
        
        if credential_path is None:
            credential_path = input("Enter path to AWS credentials file: ")
        
        cred_path = Path(credential_path).expanduser()
        if not cred_path.exists():
            raise FileNotFoundError(f"Credentials file not found: {cred_path}")
        
        if verbose:
            logger.info(f"Loading AWS credentials from {cred_path}")
        
        # Validate credential file
        try:
            with open(cred_path, 'r') as f:
                content = f.read()
                if aws_profile not in content:
                    raise ValueError(f"Profile '{aws_profile}' not found in credentials")
        except Exception as e:
            raise ValueError(f"Failed to read credentials: {e}")
        
        if not dry_run:
            self._config["aws_credential_path"] = str(cred_path)
            self._config["aws_profile"] = aws_profile
            self._save_config()
        
        if verbose:
            logger.info(f"AWS profile '{aws_profile}' configured successfully")
            # print(f"AWS profile '{aws_profile}' configured successfully")
    
    def setup_bitbucket_ssh(self,
                           keygen_filename: Optional[str] = None,
                           bitbucket_user: Optional[str] = None,
                           **kwargs) -> None:
        """
        Configure Bitbucket SSH access
        
        Args:
            keygen_filename: Name of SSH key file (e.g., 'id_rsa_bitbucket')
            bitbucket_user: Bitbucket username
            **kwargs: Additional options
        """
        verbose = kwargs.get('verbose', False)
        dry_run = kwargs.get('dry_run', False)
        
        if keygen_filename is None:
            keygen_filename = input("Enter SSH key filename (e.g., id_rsa_bitbucket): ")
        
        ssh_path = Path.home() / ".ssh" / keygen_filename
        
        if verbose:
            logger.info(f"SSH key path: {ssh_path}")
        
        # Instructions for user
        print("\n" + "="*60)
        print("BITBUCKET SSH SETUP INSTRUCTIONS")
        print("="*60)
        print(f"\n1. Generate SSH key (if not already done):")
        print(f"   ssh-keygen -t ed25519 -C 'bitbucket' -f {ssh_path}")
        print(f"\n2. Add key to Bitbucket:")
        print(f"   - Go to https://bitbucket.org/account/settings/ssh-keys/")
        print(f"   - Copy contents of {ssh_path}.pub")
        print(f"   - Add as new SSH key")
        print(f"\n3. Configure SSH client...")
        
        # Create SSH config entry
        ssh_config_path = Path.home() / ".ssh" / "config"
        ssh_config_entry = f"""Host bitbucket.org
                Hostname altssh.bitbucket.org
                Port 443
                AddKeysToAgent yes
                IdentityFile {ssh_path}
                """
        
        if not dry_run:
            # Append to SSH config
            if not ssh_config_path.exists():
                ssh_config_path.touch(mode=0o600)
            
            with open(ssh_config_path, 'a') as f:
                f.write("\n" + ssh_config_entry)
            
            self._config["bitbucket_ssh_keyfile"] = str(ssh_path)
            self._save_config()
            
            print(f"\n✓ SSH configuration added to {ssh_config_path}")
        
        print("="*60 + "\n")
    
    def is_configured(self) -> bool:
        """Check if CPV is already configured"""
        return (
            self._config.get("aws_credential_path") is not None and
            self._config.get("bitbucket_ssh_keyfile") is not None
        )
    
    def is_aws_configured(self) -> bool:
        """Check if AWS is configured"""
        return self._config.get("aws_credential_path") is not None
    
    def is_bitbucket_configured(self) -> bool:
        """Check if Bitbucket SSH is configured"""
        return self._config.get("bitbucket_ssh_keyfile") is not None
    
    def validate_credentials(self, **kwargs) -> Tuple[bool, Optional[str]]:
        """
        Verify AWS S3 and Bitbucket SSH connectivity
        
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        import subprocess
        
        verbose = kwargs.get('verbose', False)
        
        # Validate AWS
        try:
            if not self._config.get("aws_credential_path"):
                msg = "AWS not configured. Run: cpv config"
                if verbose:
                    logger.error(msg)
                return False, msg
            
            session = boto3.Session(profile_name=self._config.get("aws_profile"))
            s3 = session.client('s3')
            s3.head_bucket(Bucket='vmo-test-checkpoint-bucket')
            
            if verbose:
                logger.info("✓ AWS S3 credentials valid")
        except Exception as e:
            msg = f"AWS S3 validation failed: {e}. Your AWS token may have expired. Run: cpv config"
            if verbose:
                logger.error(msg)
            return False, msg
        
        # Validate Bitbucket SSH
        try:
            if not self._config.get("bitbucket_ssh_keyfile"):
                msg = "Bitbucket SSH not configured. Run: cpv config"
                if verbose:
                    logger.error(msg)
                return False, msg
            
            ssh_path = Path(self._config.get("bitbucket_ssh_keyfile"))
            if not ssh_path.exists():
                msg = f"SSH key not found: {ssh_path}"
                if verbose:
                    logger.error(msg)
                return False, msg
            
            # Try SSH connection
            result = subprocess.run(
                ['ssh', '-T', 'git@bitbucket.org:vinmotion/team-name_model-name.git'],
                capture_output=True,
                timeout=20,
                text=True
            )
            
            if verbose:
                logger.info("✓ Bitbucket SSH connection valid")
        except Exception as e:
            msg = f"Bitbucket SSH validation failed: {e}"
            if verbose:
                logger.error(msg)
            return False, msg
        
        return True, None
    
    def get_config(self, key: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve stored configuration"""
        if key:
            return self._config.get(key)
        return self._config


class ModelsCheckpointsManage:
    """Manages model checkpoint versioning using DVC and Git"""
    
    S3_BUCKET = "vmo-test-checkpoint-bucket"
    BITBUCKET_PROJECT_TEMPLATE = "AI-{team_name}-{model_name}-checkpoints"
    
    def __init__(self, team_name: str, model_name: str, **kwargs):
        """
        Initialize model checkpoint manager
        
        Flow for new repos (init):
        1. Prompt user for Bitbucket git URL (preferred format: team-name_model-name)
        2. Clone the repository
        3. cd into the cloned folder
        4. Set repo_path to that folder
        5. Setup logging in that folder
        
        Flow for existing repos (upload/download/etc):
        1. Use current directory as repo_path
        2. Skip cloning
        
        Args:
            team_name: AI team name (e.g., 'AI-Convo')
            model_name: Model name (e.g., 'faster-whisper')
            **kwargs: Additional options (git_url, verbose, use_current_dir, etc.)
        """
        import subprocess

        self.team_name = team_name
        self.model_name = model_name
        self.verbose = kwargs.get('verbose', False)
        self.config = CPVConfig()
        self.git_repo: Optional[git.Repo] = None
        
        # Check if we should use current directory (for upload/download commands)
        use_current_dir = kwargs.get('use_current_dir', False)
        git_url = kwargs.get('git_url')
        
        # If git_url starts with "file://", we're using an existing local repo
        if git_url and git_url.startswith('file://'):
            use_current_dir = True
        
        if use_current_dir:
            # Use current directory as repository
            self.repo_path = Path.cwd()
            
            # Verify it's a git repository
            if not (self.repo_path / ".git").exists():
                raise ValueError(f"Current directory {self.repo_path} is not a git repository")
            
            self.git_repo = git.Repo(str(self.repo_path))
            
            if self.verbose:
                logger.info(f"Using existing repository at: {self.repo_path}")
        else:
            # Standard folder name format: team-name_model-name
            suggested_folder = f"{team_name}_{model_name}"
            
            # Prompt user for Bitbucket repository URL
            if not git_url:
                git_url = input(
                    f"Enter Bitbucket repository URL\n"
                    f"(Preferred folder format: {suggested_folder})\n"
                    f"Example: git@bitbucket.org:vinmotion/{suggested_folder}.git\n"
                    f"URL: "
                ).strip()
            
            if not git_url:
                raise ValueError("Bitbucket repository URL is required")
            
            # Extract folder name from git URL
            # git@bitbucket.org:vinmotion/team-name_model-name.git -> team-name_model-name
            folder_name = git_url.rstrip('/').split('/')[-1].replace('.git', '')
            
            if self.verbose:
                logger.info(f"Cloning repository from: {git_url}")
                logger.info(f"Target folder: {folder_name}")
            
            # Clone repository
            try:
                result = subprocess.run(
                    ['git', 'clone', git_url, folder_name],
                    check=True,
                    capture_output=True,
                    text=True
                )
                
                if self.verbose:
                    logger.info(f"✓ Repository cloned successfully")
            except subprocess.CalledProcessError as e:
                if "already exists" in e.stderr:
                    logger.warning(f"Folder {folder_name} already exists, using existing folder")
                else:
                    logger.error(f"Failed to clone repository: {e.stderr}")
                    raise
            except Exception as e:
                logger.error(f"Failed to clone repository: {e}")
                raise
            
            # Set repo_path to the cloned folder
            self.repo_path = Path(folder_name).resolve()
            
            # Change directory to the cloned folder
            os.chdir(str(self.repo_path))
            
            # Initialize git.Repo object
            self.git_repo = git.Repo(str(self.repo_path))
        
        # Setup S3 prefix
        self.s3_prefix = f"s3://{self.S3_BUCKET}/{team_name}/{model_name}"
        
        # Setup file logging to {repo_path}/.cpv.log
        log_file = self.repo_path / ".cpv.log"
        setup_file_logging(log_file)
        
        if self.verbose:
            logger.info(f"✓ CPV initialized for model: {model_name}")
            logger.info(f"✓ Working directory: {self.repo_path}")
            logger.info(f"✓ Logging to: {log_file}")
    
    def import_model_init(self, data_path: Optional[str] = None, **kwargs) -> None:
        """
        Initialize model repository structure after cloning
        
        Creates:
        - Local folder structure with placeholder files
        - DVC initialization with S3 remote configuration
        - S3 storage location verification
        
        Args:
            data_path: Optional path to initial training data
            **kwargs: verbose, dry_run, force
        """
        verbose = kwargs.get('verbose', self.verbose)
        dry_run = kwargs.get('dry_run', False)
        force = kwargs.get('force', False)
        
        logger.info(f"Initializing model structure for '{self.model_name}' in {self.repo_path}")
        
        # Create local directory structure
        if not (self.repo_path / "model.bin").exists() or force:
            self._create_local_structure(data_path, dry_run=dry_run)
            if verbose:
                logger.info(f"✓ Local structure created at {self.repo_path}")
        elif verbose:
            logger.info(f"✓ Local structure already exists at {self.repo_path}")
        
        # Initialize DVC and configure S3 remote
        if not dry_run:
            if not (self.repo_path / ".dvc").exists() or force:
                self._init_dvc()
                if verbose:
                    logger.info(f"✓ DVC initialized with S3 remote")
            else:
                logger.info(f"✓ DVC already initialized at {self.repo_path}")

        # Verify S3 location
        if not dry_run:
            self._create_s3_location()
            if verbose:
                logger.info(f"✓ S3 location verified: {self.s3_prefix}")

        logger.info(f"✓ Model '{self.model_name}' initialized successfully")
        
    
    def _create_local_structure(self, data_path: Optional[str] = None, **kwargs) -> None:
        """Create local folder structure"""
        self.repo_path.mkdir(parents=True, exist_ok=True)
        
        # Create directories
        data_dir = self.repo_path / "data"
        if not data_dir.exists():
            data_dir.mkdir(parents=True, exist_ok=True)
        
        # Create placeholder files
        self._create_file(self.repo_path / "model.bin", "dummy model weights")
        self._create_file(self.repo_path / "metrics.log", "# Training metrics log\n")
        self._create_file(self.repo_path / "train.py", self._get_train_script_template())
        self._create_file(self.repo_path / "README.md", self._get_readme_template())
        self._create_file(self.repo_path / ".gitignore", "/data\n*!.dvc\n.dvc/cache\n")
        
        if data_path and Path(data_path).exists():
            import shutil
            shutil.copytree(data_path, self.repo_path / "data", dirs_exist_ok=True)
    
    def _create_file(self, filename: str, content: str) -> None:
        """Create file with content"""
        file_path = self.repo_path / filename
        with open(file_path, 'w') as f:
            f.write(content)
    
    def _init_git_repo(self, **kwargs) -> None:
        """Initialize Git repository"""
        force = kwargs.get('force', False)
        
        try:
            self.git_repo = git.Repo.init(str(self.repo_path))
            self.git_repo.config_writer().set_value("user", "name", "CPV System").release()
            self.git_repo.config_writer().set_value("user", "email", "cpv@vmo.ai").release()
            logger.info(f"✓ Git repository initialized at {self.repo_path}")
        except Exception as e:
            logger.error(f"Failed to initialize Git repo: {e}")
            raise
    
    def _init_dvc(self) -> None:
        """Initialize DVC in repository and configure S3 remote"""
        import subprocess
        
        # Ensure we're in the repo directory
        os.chdir(str(self.repo_path))
        
        try:
            # Initialize DVC
            subprocess.run(['dvc', 'init'], check=True, capture_output=True, text=True)
            logger.info("✓ DVC initialized")
            
            # Configure autostage
            subprocess.run(['dvc', 'config', 'core.autostage', 'true'], check=True)
            
            # Configure S3 remote
            s3_remote_path = f's3://{self.S3_BUCKET}/{self.team_name}/{self.model_name}'
            subprocess.run([
                'dvc', 'remote', 'add', '-d', 'myremote', s3_remote_path
            ], check=True)
            logger.info(f"✓ DVC S3 remote configured: {s3_remote_path}")
            
            # Configure AWS profile for DVC
            aws_profile = self.config.get_config('aws_profile')
            if aws_profile:
                subprocess.run([
                    'dvc', 'remote', 'modify', 'myremote', 'profile', aws_profile
                ], check=True)
                logger.info(f"✓ DVC configured to use AWS profile: {aws_profile}")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to initialize DVC: {e.stderr if e.stderr else str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error during DVC initialization: {e}")
            raise
    
    def _create_s3_location(self) -> None:
        """Create S3 bucket location for model"""
        try:
            session = boto3.Session(profile_name=self.config.get_config('aws_profile'))
            s3 = session.client('s3')
            
            # Verify bucket exists
            s3.head_bucket(Bucket=self.S3_BUCKET)
            logger.info(f"✓ S3 location verified: {self.s3_prefix}")
            # Create a marker object in S3 to initialize the location
            s3.put_object(
                Bucket=self.S3_BUCKET,
                Key=f"{self.team_name}/{self.model_name}/.initialized",
                Body=b"Model checkpoint location initialized"
            )
        except Exception as e:
            logger.error(f"Failed to create S3 location: {e}")
            raise

        # Implementation using Bitbucket API to create repo
    def _create_bitbucket_repo(self) -> None:

        """Create Bitbucket repository for model checkpoints"""
        
        # Construct Bitbucket repo URL
        # repo_name = f"{self.team_name}_{self.model_name}"
        repo_name = f"team-name_model-name"

        bitbucket_url = f"git@bitbucket.org:vinmotion/{repo_name}.git"
        
        try:
            # Clone empty repo to initialize remote
            subprocess.run(
                ['git', 'clone', bitbucket_url],
                check=True,
                capture_output=True
            )
            
            self.git_repo = git.Repo(str(self.repo_path))
            
            if self.verbose:
                logger.info(f"✓ Bitbucket repository created: {bitbucket_url}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create Bitbucket repo: {e.stderr.decode()}")
            raise
        except Exception as e:
            logger.error(f"Failed to create Bitbucket repository: {e}")
            raise
    pass
    
    def upload_model_checkpoint(self, 
                               model_path: Optional[str] = None,
                               metrics: Optional[Dict[str, Any]] = None,
                               **kwargs) -> str:
        """
        Upload model checkpoint to S3 via DVC
        
        Args:
            model_path: Path to model file (default: model.bin)
            metrics: Dictionary of metrics to save
            **kwargs: verbose, dry_run
            
        Returns:
            Commit hash
        """
        verbose = kwargs.get('verbose', self.verbose)
        dry_run = kwargs.get('dry_run', False)
        
        if model_path is None:
            model_path = "model.bin"
        
        # Update metrics if provided
        if metrics:
            self._update_metrics(metrics, dry_run=dry_run)
        
        if not dry_run:
            # DVC add
            import subprocess
            subprocess.run(['dvc', 'add', str(model_path)], check=True)
            print(f"✓ Model added to DVC: {model_path}")
            # Git commit
            self.git_repo.index.add([f"{model_path}.dvc", ".gitignore"])
            commit = self.git_repo.index.commit(f"Upload model checkpoint")
            # Validate AWS credentials before push
            self.config.validate_credentials(verbose=verbose)
            # DVC push
            subprocess.run(['dvc', 'push'], check=True)
            
            if verbose:
                logger.info(f"✓ Model uploaded: {commit.hexsha[:8]}")
            
            return commit.hexsha
    
    def download_model_checkpoint(self, tag: Optional[str] = None, **kwargs) -> ModelArtifacts:
        """
        Download specific model checkpoint from S3
        
        Args:
            tag: Git tag (e.g., 'v1.0'). If None, uses HEAD
            **kwargs: verbose, output_dir
            
        Returns:
            ModelArtifacts object
        """
        verbose = kwargs.get('verbose', self.verbose)
        
        if tag:
            self._checkout_tag(tag)
        
        import subprocess
        os.chdir(str(self.repo_path))
        subprocess.run(['dvc', 'pull'], check=True)
        
        model_path = self.repo_path / "model.bin"
        metrics = self._read_metrics()
        
        size_mb = model_path.stat().st_size / (1024 * 1024) if model_path.exists() else 0
        
        return ModelArtifacts(
            model_path=str(model_path),
            metrics=metrics,
            timestamp=datetime.now().isoformat(),
            tag=tag or "HEAD",
            size_mb=size_mb
        )
    
    def tag_model_checkpoint(self,
                            version_tag: Optional[str] = None,
                            message: Optional[str] = None,
                            **kwargs) -> str:
        """
        Tag current model checkpoint
        
        Args:
            version_tag: Git tag (e.g., 'v1.0'). If None, auto-increment
            message: Tag message
            **kwargs: verbose, dry_run
            
        Returns:
            New tag name
        """
        verbose = kwargs.get('verbose', self.verbose)
        dry_run = kwargs.get('dry_run', False)
        
        # Auto-increment if not provided
        if version_tag is None:
            version_tag = self._get_next_version()
        
        if not dry_run:
            try:
                self.git_repo.create_tag(
                    version_tag,
                    message=message or f"Checkpoint {version_tag}"
                )
                if verbose:
                    logger.info(f"✓ Tagged as {version_tag}")
            except Exception as e:
                logger.error(f"Failed to create tag: {e}")
                raise
        
        return version_tag
    
    def read_checkpoint_tag(self, **kwargs) -> List[str]:
        """List all available model tags"""
        if not self.git_repo:
            return []
        
        tags = [str(tag) for tag in self.git_repo.tags]
        return sorted(tags)
    
    def revert_model_checkpoint(self, tag: str, **kwargs) -> None:
        """
        Revert to specific model checkpoint version
        
        Args:
            tag: Git tag to revert to
            **kwargs: verbose, dry_run
        """
        verbose = kwargs.get('verbose', self.verbose)
        dry_run = kwargs.get('dry_run', False)
        
        if not dry_run:
            self._checkout_tag(tag)
            
            import subprocess
            os.chdir(str(self.repo_path))
            subprocess.run(['dvc', 'checkout'], check=True)
            
            if verbose:
                logger.info(f"✓ Reverted to {tag}")
    
    def get_model_metadata(self, tag: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Get metadata for model checkpoint"""
        if tag:
            self._checkout_tag(tag)
        
        model_path = self.repo_path / "model.bin"
        metrics = self._read_metrics()
        
        return {
            "tag": tag or "HEAD",
            "model_size_mb": model_path.stat().st_size / (1024 * 1024) if model_path.exists() else 0,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat(),
            "team_name": self.team_name,
            "model_name": self.model_name
        }
    
    def _get_next_version(self) -> str:
        """Auto-increment version from last tag"""
        tags = self.read_checkpoint_tag()
        
        if not tags:
            return "v0.1"
        
        last_tag = max(tags)  # Should be sorted
        try:
            parts = last_tag.lstrip('v').split('.')
            minor = int(parts[-1]) + 1
            major = '.'.join(parts[:-1])
            return f"v{major}.{minor}"
        except:
            return "v0.1"
    
    def _checkout_tag(self, tag: str) -> None:
        """Checkout specific Git tag"""
        try:
            self.git_repo.heads.master.checkout()
            self.git_repo.remotes.origin.fetch(tag)
            self.git_repo.create_head(tag, f'origin/{tag}').checkout()
        except Exception as e:
            logger.error(f"Failed to checkout tag {tag}: {e}")
            raise
    
    def _update_metrics(self, metrics: Dict[str, Any], **kwargs) -> None:
        """Update metrics file"""
        metrics_file = self.repo_path / "metrics.log"
        
        with open(metrics_file, 'a') as f:
            f.write(f"\n{json.dumps(metrics)}\n")
    
    def _read_metrics(self) -> Dict[str, Any]:
        """Read metrics from file"""
        metrics_file = self.repo_path / "metrics.log"
        
        if not metrics_file.exists():
            return {}
        
        # Parse last JSON object in file
        with open(metrics_file, 'r') as f:
            lines = f.readlines()
            for line in reversed(lines):
                try:
                    return json.loads(line.strip())
                except:
                    continue
        
        return {}
    
    @staticmethod
    def _get_train_script_template() -> str:
        """Get template training script"""
        return """#!/usr/bin/env python3
\"\"\"Training script template for model training\"\"\"

import json
import logging
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Training started...")
    
    # TODO: Implement your training logic here
    metrics = {
        "loss": 0.5,
        "accuracy": 0.95,
        "epochs": 10
    }
    
    # Save metrics to metrics.log
    with open("metrics.log", "a") as f:
        json.dump(metrics, f)
        f.write("\\n")
    
    logger.info("Training completed!")

if __name__ == "__main__":
    main()
"""
    
    @staticmethod
    def _get_readme_template() -> str:
        """Get template README"""
        return """# Model Training Guide

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure AWS and Bitbucket: `cpv aws-config && cpv bitbucket-config`

## Training
1. Prepare training data in `data/` directory
2. Update metrics logging in `train.py`
3. Run: `python train.py`

## Versioning
1. Upload checkpoint: `cpv model upload --message "Training v1"`
2. List checkpoints: `cpv model list-tags`
3. Revert to version: `cpv model revert --tag v1.0`

## Metrics
- Training metrics logged in `metrics.log`
- Model weights stored in `model.bin`
"""


class DataCheckpointsManage:
    """Manages data checkpoint versioning using DVC and Git"""
    
    def __init__(self, team_name: str, model_name: str, **kwargs):
        """
        Initialize data checkpoint manager
        
        Args:
            team_name: AI team name
            model_name: Model name
            **kwargs: Additional options
        """
        self.team_name = team_name
        self.model_name = model_name
        self.verbose = kwargs.get('verbose', False)
        self.repo_path = Path(kwargs.get('repo_path', f"./{model_name}"))
        
        # Setup file logging to {repo_path}/.cpv.log
        log_file = self.repo_path / ".cpv.log"
        setup_file_logging(log_file)
        
        self.config = CPVConfig()
    
    def upload_data_checkpoint(self, data_path: Optional[str] = None, **kwargs) -> str:
        """Upload training data to S3"""
        # Implementation similar to ModelsCheckpointsManage.upload_model_checkpoint
        pass
    
    def download_data_checkpoint(self, tag: Optional[str] = None, **kwargs) -> DataArtifacts:
        """Download specific data checkpoint"""
        pass
    
    def tag_data_checkpoint(self,
                           version_tag: Optional[str] = None,
                           message: Optional[str] = None,
                           **kwargs) -> str:
        """Tag data checkpoint"""
        pass
    
    def read_data_checkpoint_tag(self, **kwargs) -> List[str]:
        """List all data checkpoint tags"""
        pass
    
    def revert_data_checkpoint(self, tag: str, **kwargs) -> None:
        """Revert to specific data version"""
        pass
    
    def get_data_metadata(self, tag: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Get data checkpoint metadata"""
        pass


class CombinedCheckpointsManage:
    """Manages combined model and data checkpoint versioning"""
    
    def __init__(self, team_name: str, model_name: str, **kwargs):
        """Initialize combined checkpoint manager"""
        self.models = ModelsCheckpointsManage(team_name, model_name, **kwargs)
        self.data = DataCheckpointsManage(team_name, model_name, **kwargs)
    
    def tag_model_and_data(self,
                          version_tag: Optional[str] = None,
                          model_message: Optional[str] = None,
                          data_message: Optional[str] = None,
                          **kwargs) -> Tuple[str, str]:
        """Atomically tag both model and data"""
        # Tag model
        model_tag = self.models.tag_model_checkpoint(version_tag, model_message, **kwargs)
        
        # Tag data with same version
        data_tag = self.data.tag_data_checkpoint(version_tag, data_message, **kwargs)
        
        return model_tag, data_tag
    
    def revert_model_and_data(self, tag: str, **kwargs) -> None:
        """Revert both model and data to specific version"""
        self.models.revert_model_checkpoint(tag, **kwargs)
        self.data.revert_data_checkpoint(tag, **kwargs)
    
    def get_combined_metadata(self, tag: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Get metadata for both model and data"""
        return {
            "model": self.models.get_model_metadata(tag, **kwargs),
            "data": self.data.get_data_metadata(tag, **kwargs),
            "timestamp": datetime.now().isoformat()
        }