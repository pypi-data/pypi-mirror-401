"""Job management commands."""

import click
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

from ..client import MCEClient
from ..config import Config
from ..utils import (
    print_output, print_error, print_success, confirm_action, get_project_id,
    load_config_from_file, merge_config_with_args, validate_required_fields
)
from ..exceptions import MCEError
from .upload import _create_code_package, _upload_to_cos


@click.group()
def job():
    """Manage jobs."""
    pass


@job.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.option('--file', '-f', help='Load job configuration from file (YAML/JSON)')
@click.option('--name', '-n', help='Job name')
@click.option('--entrypoint', '-e', help='Job entrypoint command')
@click.option('--image', '-i', help='Container image')
@click.option('--queue-id', '-q', help='Queue ID')
@click.option('--compute-config-id', '-c', help='Compute configuration ID')
@click.option('--ray-version', '-r', help='Ray version')
@click.option('--pip-package', multiple=True, help='Pip packages to install')
@click.option('--env', '-E', multiple=True, help='Environment variables in key=value format')
@click.option('--working-dir', '-w', help='Working directory')
@click.option('--volume-mount', '-v', multiple=True, help='Volume mounts (JSON format)')
@click.pass_context
def create(ctx, project_id: str, file: Optional[str], name: Optional[str], entrypoint: Optional[str], 
          image: Optional[str], queue_id: Optional[str], compute_config_id: Optional[str], 
          ray_version: Optional[str], pip_package: tuple, env: tuple, working_dir: Optional[str], 
          volume_mount: tuple):
    """Create a new job.
    
    You can specify job configuration either via command line options or by loading
    from a configuration file using --file option. Command line options take precedence
    over file configuration.
    
    Example file format (YAML):
    \b
    name: "my-training-job"
    entrypoint: "python train.py --epochs 100"
    image: "rayproject/ray:2.8.0"
    queue_id: "gpu-queue"
    compute_config_id: "gpu-config"
    ray_version: "2.8.0"
    pip_packages:
      - "torch"
      - "transformers"
      - "datasets"
    env_vars:
      CUDA_VISIBLE_DEVICES: "0"
      WANDB_PROJECT: "my-project"
    working_dir: "/workspace"
    volume_mounts:
      - type: "COS"
        mountPath: "/data"
        readOnly: false
        remotePath: "cos://my-bucket/data/"
        cosOptions:
          region: "ap-beijing"
          secretId: "your-secret-id"
          secretKey: "your-secret-key"
    
    Example file format (JSON):
    \b
    {
      "name": "my-training-job",
      "entrypoint": "python train.py --epochs 100",
      "image": "rayproject/ray:2.8.0",
      "queue_id": "gpu-queue",
      "compute_config_id": "gpu-config",
      "ray_version": "2.8.0",
      "pip_packages": ["torch", "transformers", "datasets"],
      "env_vars": {
        "CUDA_VISIBLE_DEVICES": "0",
        "WANDB_PROJECT": "my-project"
      },
      "working_dir": "/workspace",
      "volume_mounts": [
        {
          "type": "COS",
          "mountPath": "/data",
          "readOnly": false,
          "remotePath": "cos://my-bucket/data/",
          "cosOptions": {
            "region": "ap-beijing",
            "secretId": "your-secret-id",
            "secretKey": "your-secret-key"
          }
        }
      ]
    }
    """
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        # Load configuration from file if provided
        if file:
            try:
                file_config = load_config_from_file(file)
                print_success(f"Loaded configuration from {file}")
            except (FileNotFoundError, ValueError) as e:
                print_error(str(e))
                ctx.exit(1)
        else:
            file_config = {}
        
        # Merge file config with command line arguments
        merged_config = merge_config_with_args(
            file_config,
            name=name,
            entrypoint=entrypoint,
            image=image,
            queue_id=queue_id,
            compute_config_id=compute_config_id,
            ray_version=ray_version,
            working_dir=working_dir
        )
        
        # Handle pip packages from both file and command line
        pip_packages = []
        if 'pip_packages' in file_config and isinstance(file_config['pip_packages'], list):
            pip_packages.extend(file_config['pip_packages'])
        if pip_package:
            pip_packages.extend(list(pip_package))
        
        # Handle environment variables from both file and command line
        env_vars = {}
        if 'env_vars' in file_config and isinstance(file_config['env_vars'], dict):
            env_vars.update(file_config['env_vars'])
        
        # Environment variables from command line (override file env vars)
        for env_str in env:
            if '=' in env_str:
                key, value = env_str.split('=', 1)
                env_vars[key.strip()] = value.strip()
            else:
                click.echo(f"Warning: Invalid env format '{env_str}', expected key=value")
        
        # Handle volume mounts from both file and command line
        volume_mounts = []
        if 'volume_mounts' in file_config and isinstance(file_config['volume_mounts'], list):
            volume_mounts.extend(file_config['volume_mounts'])
        
        # Volume mounts from command line
        for vm_str in volume_mount:
            try:
                vm = json.loads(vm_str)
                volume_mounts.append(vm)
            except json.JSONDecodeError as e:
                print_error(f"Invalid volume mount JSON '{vm_str}': {e}")
                ctx.exit(1)
        
        # Handle working directory code upload
        if working_dir:
            # Check if COS is configured
            if not config.is_cos_configured():
                print_error("Working directory specified but COS is not configured. Run 'mcecli config cos' first.")
                ctx.exit(1)
            
            # Upload specified working directory as code package
            print_success(f"Uploading working directory as code package: {working_dir}")
            
            try:
                # Use specified working directory as source
                source_path = Path(working_dir).resolve()
                
                # Check if the working directory exists
                if not source_path.exists():
                    print_error(f"Working directory does not exist: {working_dir}")
                    ctx.exit(1)
                
                if not source_path.is_dir():
                    print_error(f"Working directory is not a directory: {working_dir}")
                    ctx.exit(1)
                
                # Generate package name with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                package_name = f"job_code_{merged_config['name']}_{timestamp}"
                
                # Default exclude patterns
                exclude_patterns = [
                    '*.pyc', '*.pyo', '*.pyd', '__pycache__',
                    '.git', '.gitignore', '.DS_Store', '*.log',
                    '.pytest_cache', '.coverage', 'htmlcov',
                    'node_modules', '.npm', '.yarn',
                    '*.egg-info', 'dist', 'build'
                ]
                
                # Create code package
                tar_path = _create_code_package(
                    source_path, package_name, exclude_patterns, False, False
                )
                
                # Upload to COS
                cos_key = _upload_to_cos(config, tar_path, package_name, True)
                
                # Clean up temporary file
                if tar_path.exists():
                    tar_path.unlink()
                
                print_success(f"Code uploaded successfully to COS: {cos_key}")
                
                # Generate download URL
                cos_config_obj = config.cos_config
                download_url = f"https://{cos_config_obj['bucket']}.cos.{cos_config_obj['region']}.myqcloud.com/{cos_key}"
                
                # Use the directory name as the container working directory
                container_working_dir = f"/home/ray/workspace/{source_path.name}"
                
                # Modify entrypoint to download and extract code first
                init_commands = [
                    f"mkdir -p {container_working_dir}",
                    f"cd {container_working_dir}",
                    f"wget -O code.tar.gz '{download_url}'",
                    "tar -xzf code.tar.gz",
                    "rm code.tar.gz",
                    merged_config['entrypoint']
                ]
                
                # Update entrypoint
                merged_config['entrypoint'] = " && ".join(init_commands)
                
                print_success(f"Modified entrypoint to include code download and extraction to {container_working_dir}")
                
            except Exception as e:
                print_error(f"Failed to upload code: {e}")
                ctx.exit(1)
        
        # Validate required fields
        validate_required_fields(merged_config, ['name', 'entrypoint', 'image'], 'job')
        
        # Prepare final configuration
        final_config = {
            'project_id': project_id,
            'name': merged_config['name'],
            'entrypoint': merged_config['entrypoint'],
            'image': merged_config['image'],
            'queue_id': merged_config.get('queue_id'),
            'compute_config_id': merged_config.get('compute_config_id'),
            'ray_version': merged_config.get('ray_version'),
            'pip_packages': pip_packages if pip_packages else None,
            'env_vars': env_vars if env_vars else None,
            'volume_mounts': volume_mounts if volume_mounts else None
        }
        
        result = client.create_job(**final_config)
        
        print_success(f"Job '{final_config['name']}' created successfully")
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@job.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.option('--page', default=1, help='Page number')
@click.option('--page-size', '-s', default=20, help='Page size')
@click.pass_context
def list(ctx, project_id: str, page: int, page_size: int):
    """List jobs in project."""
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        result = client.list_jobs(project_id=project_id, page=page, page_size=page_size)
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@job.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.argument('job_id')
@click.pass_context
def get(ctx, project_id: str, job_id: str):
    """Get job details."""
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        result = client.get_job(project_id, job_id)
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@job.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.argument('job_id')
@click.option('--force', '-f', is_flag=True, help='Force stop without confirmation')
@click.pass_context
def stop(ctx, project_id: str, job_id: str, force: bool):
    """Stop a running job."""
    try:
        config = ctx.obj['config']
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        if not force:
            if not confirm_action(f"Are you sure you want to stop job '{job_id}'?"):
                click.echo("Operation cancelled.")
                return
        
        client = MCEClient(config)
        
        result = client.stop_job(project_id, job_id)
        print_success(f"Job '{job_id}' stop request sent")
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@job.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.argument('job_id')
@click.pass_context
def retry(ctx, project_id: str, job_id: str):
    """Retry a failed job."""
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        result = client.retry_job(project_id, job_id)
        print_success(f"Job '{job_id}' retry request sent")
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@job.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.argument('job_id')
@click.option('--force', '-f', is_flag=True, help='Force delete without confirmation')
@click.pass_context
def delete(ctx, project_id: str, job_id: str, force: bool):
    """Delete a job."""
    try:
        config = ctx.obj['config']
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        if not force:
            if not confirm_action(f"Are you sure you want to delete job '{job_id}'?"):
                click.echo("Operation cancelled.")
                return
        
        client = MCEClient(config)
        
        client.delete_job(project_id, job_id)
        print_success(f"Job '{job_id}' deleted successfully")
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@job.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.argument('job_id')
@click.pass_context
def events(ctx, project_id: str, job_id: str):
    """Get job events."""
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        result = client.get_job_events(project_id, job_id)
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@job.command()
@click.pass_context
def template(ctx):
    """Show job creation template."""
    template = {
        "volume_mount_examples": [
            {
                "type": "COS",
                "mountPath": "/data",
                "readOnly": False,
                "remotePath": "cos://bucket-name/path/",
                "cosOptions": {
                    "region": "ap-beijing",
                    "secretId": "your-secret-id",
                    "secretKey": "your-secret-key"
                }
            },
            {
                "type": "CFS",
                "mountPath": "/shared",
                "readOnly": False,
                "remotePath": "cfs://file-system-id/path/"
            },
            {
                "type": "HostPath",
                "mountPath": "/host-data",
                "readOnly": True,
                "remotePath": "/host/path"
            }
        ],
        "example_command": "mcecli job create --project-id proj-123 --name my-job --entrypoint 'python train.py' --image rayproject/ray:2.8.0 --pip-package torch --pip-package transformers --env CUDA_VISIBLE_DEVICES=0 --working-dir /workspace"
    }
    
    config = ctx.obj['config']
    print_output(template, config.output_format, config.color_enabled)