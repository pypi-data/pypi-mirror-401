"""
CPV Command-line Interface

Provides CLI commands for checkpoint management:
- cpv config - Configure AWS and Bitbucket credentials
- cpv init - Initialize model repository
- cpv upload - Upload checkpoint to S3
- cpv download - Download checkpoint from S3
- cpv tag - Tag a checkpoint version
- cpv revert - Revert to previous checkpoint
- cpv list - List all versions
- cpv show - Show checkpoint metadata
"""

from importlib.resources import path
import click
import logging
from pathlib import Path
from typing import Optional

from cp_manage import (
    CPVConfig,
    ModelsCheckpointsManage,
    CombinedCheckpointsManage,
)

logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
def cli():
    """CPV - Checkpoint Versioning for Data and Models Management"""
    pass


@cli.command()
@click.option('--credential-path', default=None,
              help='Path to AWS credentials file')
@click.option('--aws-profile', default='default',
              help='AWS profile name')
@click.option('--bitbucket-user', default=None,
              help='Your Bitbucket username')
def config(credential_path: Optional[str], aws_profile: str, bitbucket_user: Optional[str]):
    """Configure AWS and Bitbucket credentials"""
    click.echo("🔧 Configuring CPV...")
    
    cfg = CPVConfig()
    
    try:
        # Check what's already configured
        aws_configured = cfg.is_aws_configured()
        bitbucket_configured = cfg.is_bitbucket_configured()
        
        # Setup AWS if not configured or if user wants to reconfigure
        if not aws_configured:
            if credential_path is None:
                credential_path = click.prompt('AWS credentials path', default='~/.aws/credentials')
            
            click.echo(f"Setting up AWS profile '{aws_profile}'...")
            cfg.setup_aws_profile(
                credential_path=credential_path,
                aws_profile=aws_profile,
                verbose=True
            )
        else:
            # Offer to reconfigure AWS (in case token expired)
            reconfigure = click.confirm('AWS already configured. Reconfigure?', default=False)
            if reconfigure:
                if credential_path is None:
                    credential_path = click.prompt('AWS credentials path', default=cfg.get_config('aws_credential_path'))
                aws_profile = click.prompt('AWS profile name', default=cfg.get_config('aws_profile'))
                
                cfg.setup_aws_profile(
                    credential_path=credential_path,
                    aws_profile=aws_profile,
                    verbose=True
                )
        
        # Setup Bitbucket SSH if not configured
        if not bitbucket_configured:
            if bitbucket_user is None:
                bitbucket_user = click.prompt('Bitbucket username')
            
            click.echo(f"Setting up Bitbucket SSH for user '{bitbucket_user}'...")
            cfg.setup_bitbucket_ssh(
                keygen_filename=f"id_rsa_{bitbucket_user}",
                bitbucket_user=bitbucket_user,
                verbose=True
            )
        else:
            click.secho("✓ Bitbucket SSH already configured", fg='green')
        
        # Validate
        is_valid, error_msg = cfg.validate_credentials(verbose=True)
        if is_valid:
            click.secho("✓ All credentials configured and validated successfully!", fg='green')
        else:
            click.secho(f"✗ Credential validation failed: {error_msg}", fg='red')
    except Exception as e:
        click.secho(f"✗ Configuration failed: {e}", fg='red')


@cli.command()
@click.option('--team', default=None, help='AI team name (e.g., AI-Convo)')
@click.option('--model', default=None, help='Model name (e.g., faster-whisper)')
def init(team: Optional[str], model: Optional[str]):
    """Initialize new model repository
    
    Interactive flow:
    1. Check if CPV is configured (if not, prompt for config)
    2. Prompt for team name and model name
    3. Clone Bitbucket repository (prompts for git URL)
    4. Create local structure with placeholder files
    5. Initialize DVC with S3 remote
    6. Provide instructions for next steps
    """
    click.echo("🚀 Initializing CPV model repository...\n")
    
    cfg = CPVConfig()
    
    # Step 1: Check if configured
    if not cfg.is_configured():
        click.secho("⚠️  CPV is not configured yet. Running configuration...", fg='yellow')
        if click.confirm('Do you want to configure now?', default=True):
            try:
                credential_path = click.prompt('AWS credentials path', default='~/.aws/credentials')
                aws_profile = click.prompt('AWS profile name', default='default')
                bitbucket_user = click.prompt('Bitbucket username')
                
                cfg.setup_aws_profile(
                    credential_path=credential_path,
                    aws_profile=aws_profile,
                    verbose=True
                )
                
                cfg.setup_bitbucket_ssh(
                    keygen_filename=f"id_rsa_{bitbucket_user}",
                    bitbucket_user=bitbucket_user,
                    verbose=True
                )
                
                is_valid, error_msg = cfg.validate_credentials(verbose=True)
                if not is_valid:
                    click.secho(f"✗ Configuration validation failed: {error_msg}", fg='red')
                    return
                    
            except Exception as e:
                click.secho(f"✗ Configuration failed: {e}", fg='red')
                return
        else:
            click.secho("⚠️  CPV requires configuration. Run 'cpv config' first.", fg='yellow')
            return
    
    # Step 2: Prompt for team and model
    if team is None:
        team = click.prompt('Team name (e.g., AI-Convo)')
    
    if model is None:
        model = click.prompt('Model name (e.g., faster-whisper)')
    
    suggested_folder = f"{team}_{model}"
    
    try:
        # Step 3-5: Create ModelsCheckpointsManage (which handles git clone, init, DVC setup)
        click.echo(f"\n📁 Setting up model '{model}' for team '{team}'...\n")
        
        mcm = ModelsCheckpointsManage(
            team_name=team,
            model_name=model,
            verbose=True
        )
        
        click.echo(f"\n✓ Repository cloned to: {mcm.repo_path}\n")
        
        # Initialize the model structure
        click.echo("📦 Initializing model structure...")
        mcm.import_model_init(force=True)
        
        # Step 6: Provide next steps
        click.secho("\n✓ Model repository initialized successfully!", fg='green')
        click.echo("\n📋 Next steps:")
        click.echo(f"  1. cd {mcm.repo_path}")
        click.echo("  2. Replace placeholder files with your own:")
        click.echo("     - Replace 'model.bin' with your actual model file (.bin, .h5, .pt, etc.)")
        click.echo("     - Replace 'data/' folder with your training data")
        click.echo("     - Update 'train.py' with your training script")
        click.echo("  3. Test the setup:")
        click.echo(f"     cpv upload -t {team} -m {model}")
        click.echo("  4. Tag your first version:")
        click.echo(f"     cpv tag -t {team} -m {model}")
        
    except Exception as e:
        click.secho(f"✗ Initialization failed: {e}", fg='red')
        logger.exception("Init failed")


@cli.command()
@click.option('--team', '-t', required=True, prompt='Team name',
              help='AI team name')
@click.option('--model', '-m', required=True, prompt='Model name',
              help='Model name')
@click.option('--model-file', default='model.bin',
              help='Model file to upload (default: model.bin)')
@click.option('--message', '-M', default=None,
              help='Commit message')
def upload(team: str, model: str, model_file: str, message: Optional[str]):
    """Upload model checkpoint to S3
    
    Uploads the current model from the repository to S3 via DVC.
    Works from within a CPV-initialized repository directory.
    """
    click.echo(f"📤 Uploading {model} checkpoint to S3...\n")
    
    cfg = CPVConfig()
    
    try:
        # Validate credentials
        is_valid, error_msg = cfg.validate_credentials(verbose=True)
        if not is_valid:
            click.secho(f"\n✗ Credential validation failed: {error_msg}", fg='red')
            click.echo("Run 'cpv config' to reconfigure credentials.")
            return
        
        # Use current directory as repo
        repo_path = Path.cwd()
        
        mcm = ModelsCheckpointsManage(
            team_name=team,
            model_name=model,
            use_current_dir=True,  # Use existing repo in current directory
            verbose=True
        )
        
        # Upload checkpoint
        commit_hash = mcm.upload_model_checkpoint(
            model_path=model_file,
            verbose=True
        )
        
        click.secho(f"✓ Checkpoint uploaded successfully!", fg='green')
        click.echo(f"  Commit: {commit_hash[:8]}")
        click.echo(f"\nNext: Tag this version with 'cpv tag -t {team} -m {model}'")
        
    except Exception as e:
        if "S3.HeadBucket" in str(e) or "NoCredentialsError" in str(e.__class__.__name__):
            click.secho(f"✗ AWS S3 error: {e}", fg='red')
            click.echo("Your AWS token may have expired. Run: cpv config")
        else:
            click.secho(f"✗ Upload failed: {e}", fg='red')
        logger.exception("Upload failed")


@cli.command()
@click.option('--team', '-t', required=True, prompt='Team name',
              help='AI team name')
@click.option('--model', '-m', required=True, prompt='Model name',
              help='Model name')
@click.option('--tag', '-T', default=None,
              help='Version tag (e.g., v1.0). If not specified, lists available versions')
def download(team: str, model: str, tag: Optional[str]):
    """Download model checkpoint from S3
    
    Downloads a specific version of the model checkpoint.
    If no tag specified, lists available versions.
    """
    click.echo(f"📥 Downloading {model} checkpoint...")
    
    cfg = CPVConfig()
    
    try:
        # Validate credentials
        is_valid, error_msg = cfg.validate_credentials(verbose=False)
        if not is_valid:
            click.secho(f"✗ Credential validation failed: {error_msg}", fg='red')
            return
        
        repo_path = Path.cwd()
        
        mcm = ModelsCheckpointsManage(
            team_name=team,
            model_name=model,
            git_url=f"file://{repo_path}/.git",
            verbose=True
        )
        
        if not tag:
            versions = mcm.read_checkpoint_tag()
            if not versions:
                click.secho("✗ No versions available", fg='red')
                return
            
            click.echo("Available versions:")
            for v in versions:
                click.echo(f"  - {v}")
            tag = click.prompt("Select version to download")
        
        click.echo(f"Downloading version: {tag}...")
        artifacts = mcm.download_model_checkpoint(tag=tag, verbose=True)
        
        click.secho(f"✓ Downloaded to: {artifacts.model_path}", fg='green')
        click.echo(f"  Size: {artifacts.size_mb:.2f} MB")
        
    except Exception as e:
        if "S3.HeadBucket" in str(e) or "NoCredentialsError" in str(e.__class__.__name__):
            click.secho(f"✗ AWS S3 error: {e}", fg='red')
            click.echo("Your AWS token may have expired. Run: cpv config")
        else:
            click.secho(f"✗ Download failed: {e}", fg='red')
        logger.exception("Download failed")


@cli.command()
@click.option('--team', '-t', required=True, prompt='Team name',
              help='AI team name')
@click.option('--model', '-m', required=True, prompt='Model name',
              help='Model name')
@click.option('--message', '-M', default='',
              help='Tag message/description')
@click.option('--version', '-v', default=None,
              help='Version tag (auto-increment if not specified)')
def tag(team: str, model: str, message: str, version: Optional[str]):
    """Tag a model checkpoint version
    
    Creates a version tag for the current model checkpoint.
    If no version specified, auto-increments from last tag.
    """
    click.echo(f"🏷️  Tagging {model} checkpoint...")
    
    try:
        repo_path = Path.cwd()
        
        mcm = ModelsCheckpointsManage(
            team_name=team,
            model_name=model,
            use_current_dir=True,
            verbose=True
        )
        
        tag_name = mcm.tag_model_checkpoint(
            version_tag=version,
            message=message or f"Checkpoint: {model}"
        )
        
        click.secho(f"✓ Tagged as: {tag_name}", fg='green')
        
    except Exception as e:
        click.secho(f"✗ Tagging failed: {e}", fg='red')
        logger.exception("Tag failed")


@cli.command()
@click.option('--team', '-t', required=True, prompt='Team name',
              help='AI team name')
@click.option('--model', '-m', required=True, prompt='Model name',
              help='Model name')
def list_versions(team: str, model: str):
    """List all checkpoint versions
    
    Shows all available versions with metadata for the model.
    """
    click.echo(f"📋 Versions of {model}:")
    
    try:
        repo_path = Path.cwd()
        
        mcm = ModelsCheckpointsManage(
            team_name=team,
            model_name=model,
            use_current_dir=True,
            verbose=False
        )
        
        versions = mcm.read_checkpoint_tag()
        
        if not versions:
            click.echo("No versions available")
            return
        
        click.echo(f"\n{'Version':<10} {'Size (MB)':<12} {'Timestamp':<25}")
        click.echo("-" * 50)
        
        for v in versions:
            try:
                metadata = mcm.get_model_metadata(tag=v)
                size = metadata.get('model_size_mb', 0)
                timestamp = metadata.get('timestamp', 'Unknown')[:19]
                click.echo(f"{v:<10} {size:<12.2f} {timestamp:<25}")
            except:
                click.echo(f"{v:<10} {'N/A':<12} {'N/A':<25}")
            
    except Exception as e:
        click.secho(f"✗ Failed to list versions: {e}", fg='red')
        logger.exception("List versions failed")


@cli.command()
@click.option('--team', '-t', required=True, prompt='Team name',
              help='AI team name')
@click.option('--model', '-m', required=True, prompt='Model name',
              help='Model name')
@click.option('--tag', '-T', required=True, prompt='Version tag',
              help='Version tag to revert to (e.g., v1.0)')
@click.confirmation_option(prompt='⚠️  This will overwrite current files. Continue?')
def revert(team: str, model: str, tag: str):
    """Revert to a previous checkpoint version
    
    Reverts both Git and DVC files to a previous version.
    This will overwrite current files!
    """
    click.echo(f"⏮️  Reverting {model} to {tag}...")
    
    cfg = CPVConfig()
    
    try:
        # Validate credentials (needed for S3 if using DVC pull)
        is_valid, error_msg = cfg.validate_credentials(verbose=False)
        if not is_valid:
            click.secho(f"✗ Credential validation failed: {error_msg}", fg='red')
            return
        
        repo_path = Path.cwd()
        
        mcm = ModelsCheckpointsManage(
            team_name=team,
            model_name=model,
            use_current_dir=True,
            verbose=True
        )
        
        mcm.revert_model_checkpoint(tag=tag)
        click.secho(f"✓ Reverted to {tag}", fg='green')
        
    except Exception as e:
        if "S3.HeadBucket" in str(e) or "NoCredentialsError" in str(e.__class__.__name__):
            click.secho(f"✗ AWS S3 error: {e}", fg='red')
            click.echo("Your AWS token may have expired. Run: cpv config")
        else:
            click.secho(f"✗ Revert failed: {e}", fg='red')
        logger.exception("Revert failed")


@cli.command()
@click.option('--team', '-t', default=None, help='Team name')
@click.option('--model', '-m', default=None, help='Model name')
@click.option('--tag', '-T', default=None, help='Version tag (optional, defaults to HEAD)')
def show(team: Optional[str], model: Optional[str], tag: Optional[str]):
    """Show checkpoint metadata for current or specified version
    
    Displays metadata about the current model checkpoint including:
    - Git tag/commit
    - DVC file tracking
    - File size
    - Training metrics
    - Timestamp
    """
    try:
        # If team/model not provided, try to infer from current directory
        if not team or not model:
            click.secho("ℹ️  Team and model are required. Provide with -t and -m options.", fg='yellow')
            return
        
        repo_path = Path.cwd()
        
        mcm = ModelsCheckpointsManage(
            team_name=team,
            model_name=model,
            use_current_dir=True,
            verbose=False
        )
        
        meta = mcm.get_model_metadata(tag=tag)
        
        click.echo(f"\n📊 Checkpoint Metadata")
        click.echo("=" * 50)
        click.echo(f"Tag:          {meta.get('tag', 'N/A')}")
        click.echo(f"Model:        {meta.get('model_name', 'N/A')}")
        click.echo(f"Team:         {meta.get('team_name', 'N/A')}")
        click.echo(f"Size:         {meta.get('model_size_mb', 0):.2f} MB")
        click.echo(f"Timestamp:    {meta.get('timestamp', 'N/A')}")
        
        metrics = meta.get('metrics', {})
        if metrics:
            click.echo(f"\nMetrics:")
            for key, value in metrics.items():
                click.echo(f"  {key}: {value}")
        
        click.echo("=" * 50)
        
    except Exception as e:
        click.secho(f"✗ Failed to fetch metadata: {e}", fg='red')
        logger.exception("Show failed")


if __name__ == '__main__':
    cli()
