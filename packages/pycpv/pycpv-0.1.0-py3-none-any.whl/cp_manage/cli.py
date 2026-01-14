"""
CPV Command-line Interface

Provides CLI commands for checkpoint management:
- cpv init - Initialize model repository
- cpv upload - Upload checkpoint to S3
- cpv download - Download checkpoint from S3
- cpv tag - Tag a checkpoint version
- cpv revert - Revert to previous checkpoint
- cpv list - List all versions
- cpv config - Configure credentials
"""

import click
from pathlib import Path
from typing import Optional

from cp_manage import (
    CPVConfig,
    ModelsCheckpointsManage,
    CombinedCheckpointsManage,
)


@click.group()
@click.version_option()
def cli():
    """CPV - Checkpoint Versioning for AI Teams"""
    pass


@cli.command()
@click.option('--credential-path', prompt='AWS credentials path', 
              default='~/.aws/credentials',
              help='Path to AWS credentials file')
@click.option('--aws-profile', default='default',
              help='AWS profile name')
@click.option('--bitbucket-user', prompt='Bitbucket username',
              help='Your Bitbucket username')
def config(credential_path: str, aws_profile: str, bitbucket_user: str):
    """Configure AWS and Bitbucket credentials"""
    click.echo("🔧 Configuring CPV...")
    
    cfg = CPVConfig()
    
    try:
        # Setup AWS
        click.echo(f"Setting up AWS profile '{aws_profile}'...")
        cfg.setup_aws_profile(
            credential_path=credential_path,
            aws_profile=aws_profile,
            verbose=True
        )
        
        # Setup Bitbucket SSH
        click.echo(f"Setting up Bitbucket SSH for user '{bitbucket_user}'...")
        cfg.setup_bitbucket_ssh(
            keygen_filename=f"id_rsa_{bitbucket_user}",
            bitbucket_user=bitbucket_user,
            verbose=True
        )
        
        # Validate
        if cfg.validate_credentials():
            click.secho("✓ All credentials configured successfully!", fg='green')
        else:
            click.secho("✗ Credential validation failed", fg='red')
    except Exception as e:
        click.secho(f"✗ Configuration failed: {e}", fg='red')


@cli.command()
@click.option('--team', required=True, prompt='Team name',
              help='AI team name (e.g., AI-Convo)')
@click.option('--model', required=True, prompt='Model name',
              help='Model name (e.g., faster-whisper)')
@click.option('--path', default=None,
              help='Repository path (default: ./{model})')
@click.option('--data-path', default=None,
              help='Path to training data')
def init(team: str, model: str, path: Optional[str], data_path: Optional[str]):
    """Initialize new model repository"""
    click.echo(f"🚀 Initializing model repository...")
    
    repo_path = path or f"./{model}"
    
    try:
        mcm = ModelsCheckpointsManage(
            team_name=team,
            model_name=model,
            repo_path=repo_path,
            verbose=True
        )
        
        mcm.import_model_init(data_path=data_path)
        
        click.secho(f"✓ Repository initialized at {repo_path}", fg='green')
        click.echo("\nNext steps:")
        click.echo(f"  1. cd {repo_path}")
        click.echo("  2. Edit train.py with your training code")
        click.echo("  3. Run: cpv upload -t {team} -m {model}")
    except Exception as e:
        click.secho(f"✗ Initialization failed: {e}", fg='red')


@cli.command()
@click.option('--team', '-t', required=True, prompt='Team name',
              help='AI team name')
@click.option('--model', '-m', required=True, prompt='Model name',
              help='Model name')
@click.option('--path', '-p', default=None,
              help='Repository path')
@click.option('--model-file', default='model.bin',
              help='Model file to upload')
def upload(team: str, model: str, path: Optional[str], model_file: str):
    """Upload model checkpoint to S3"""
    click.echo(f"📤 Uploading {model} checkpoint...")
    
    repo_path = path or f"./{model}"
    model_path = f"{repo_path}/{model_file}"
    
    try:
        mcm = ModelsCheckpointsManage(
            team_name=team,
            model_name=model,
            repo_path=repo_path,
            verbose=True
        )
        
        # For now, just show the command
        click.echo(f"Would upload: {model_path}")
        click.echo("Full implementation coming soon")
        
    except Exception as e:
        click.secho(f"✗ Upload failed: {e}", fg='red')


@cli.command()
@click.option('--team', '-t', required=True, prompt='Team name',
              help='AI team name')
@click.option('--model', '-m', required=True, prompt='Model name',
              help='Model name')
@click.option('--path', '-p', default=None,
              help='Repository path')
@click.option('--tag', '-T', default=None,
              help='Version tag (e.g., v1.0)')
def download(team: str, model: str, path: Optional[str], tag: Optional[str]):
    """Download model checkpoint from S3"""
    click.echo(f"📥 Downloading {model} checkpoint...")
    
    repo_path = path or f"./{model}"
    
    try:
        mcm = ModelsCheckpointsManage(
            team_name=team,
            model_name=model,
            repo_path=repo_path,
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
            tag = click.prompt("Select version")
        
        click.echo(f"Downloading version: {tag}")
        click.echo("Full implementation coming soon")
        
    except Exception as e:
        click.secho(f"✗ Download failed: {e}", fg='red')


@cli.command()
@click.option('--team', '-t', required=True, prompt='Team name',
              help='AI team name')
@click.option('--model', '-m', required=True, prompt='Model name',
              help='Model name')
@click.option('--path', '-p', default=None,
              help='Repository path')
@click.option('--message', '-M', default='',
              help='Tag message/description')
@click.option('--version', '-v', default=None,
              help='Version tag (auto-increment if not specified)')
def tag(team: str, model: str, path: Optional[str], message: str, version: Optional[str]):
    """Tag a model checkpoint version"""
    click.echo(f"🏷️  Tagging {model} checkpoint...")
    
    repo_path = path or f"./{model}"
    
    try:
        mcm = ModelsCheckpointsManage(
            team_name=team,
            model_name=model,
            repo_path=repo_path,
            verbose=True
        )
        
        tag_name = mcm.tag_model_checkpoint(
            version_tag=version,
            message=message or f"Checkpoint: {model}"
        )
        
        click.secho(f"✓ Tagged as: {tag_name}", fg='green')
        
    except Exception as e:
        click.secho(f"✗ Tagging failed: {e}", fg='red')


@cli.command()
@click.option('--team', '-t', required=True, prompt='Team name',
              help='AI team name')
@click.option('--model', '-m', required=True, prompt='Model name',
              help='Model name')
@click.option('--path', '-p', default=None,
              help='Repository path')
def list_versions(team: str, model: str, path: Optional[str]):
    """List all checkpoint versions"""
    repo_path = path or f"./{model}"
    
    try:
        mcm = ModelsCheckpointsManage(
            team_name=team,
            model_name=model,
            repo_path=repo_path
        )
        
        versions = mcm.read_checkpoint_tag()
        
        if not versions:
            click.echo("No versions available")
            return
        
        click.echo(f"Versions for {model}:")
        for v in versions:
            metadata = mcm.get_model_metadata(tag=v)
            size = metadata.get('model_size_mb', 'Unknown')
            timestamp = metadata.get('timestamp', 'Unknown')
            click.echo(f"  {v:8} - {size}MB - {timestamp}")
            
    except Exception as e:
        click.secho(f"✗ Failed to list versions: {e}", fg='red')


@cli.command()
@click.option('--team', '-t', required=True, prompt='Team name',
              help='AI team name')
@click.option('--model', '-m', required=True, prompt='Model name',
              help='Model name')
@click.option('--path', '-p', default=None,
              help='Repository path')
@click.option('--tag', '-T', required=True, prompt='Version tag',
              help='Version tag to revert to (e.g., v1.0)')
@click.confirmation_option(prompt='Revert all files to this version?')
def revert(team: str, model: str, path: Optional[str], tag: str):
    """Revert to a previous checkpoint version"""
    click.echo(f"⏮️  Reverting {model} to {tag}...")
    
    repo_path = path or f"./{model}"
    
    try:
        mcm = ModelsCheckpointsManage(
            team_name=team,
            model_name=model,
            repo_path=repo_path,
            verbose=True
        )
        
        mcm.revert_model_checkpoint(tag=tag)
        click.secho(f"✓ Reverted to {tag}", fg='green')
        
    except Exception as e:
        click.secho(f"✗ Revert failed: {e}", fg='red')


@cli.command()
@click.option('--team', '-t', required=True, prompt='Team name',
              help='AI team name')
@click.option('--model', '-m', required=True, prompt='Model name',
              help='Model name')
@click.option('--path', '-p', default=None,
              help='Repository path')
@click.option('--tag', '-T', required=True, prompt='Version tag',
              help='Version tag to view')
def metadata(team: str, model: str, path: Optional[str], tag: str):
    """Show metadata for a checkpoint"""
    repo_path = path or f"./{model}"
    
    try:
        mcm = ModelsCheckpointsManage(
            team_name=team,
            model_name=model,
            repo_path=repo_path
        )
        
        meta = mcm.get_model_metadata(tag=tag)
        
        click.echo(f"\nMetadata for {tag}:")
        for key, value in meta.items():
            click.echo(f"  {key}: {value}")
            
    except Exception as e:
        click.secho(f"✗ Failed to fetch metadata: {e}", fg='red')


if __name__ == '__main__':
    cli()
