"""Compute configuration management commands."""

import click
import json
from typing import Optional, Dict, Any

from ..client import MCEClient
from ..config import Config
from ..utils import (
    print_output, print_error, print_success, confirm_action, get_project_id,
    load_config_from_file, merge_config_with_args, validate_required_fields
)
from ..exceptions import MCEError


@click.group()
def compute_config():
    """Manage compute configurations."""
    pass


@compute_config.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.option('--file', '-f', help='Load compute configuration from file (YAML/JSON)')
@click.option('--name', '-n', help='Configuration name')
@click.option('--ray-version', '-r', help='Ray version')
@click.option('--head-config', '-h', help='Head node configuration (JSON string)')
@click.option('--worker-config', '-w', help='Worker node configuration (JSON string)')
@click.pass_context
def create(ctx, project_id: str, file: Optional[str], name: Optional[str], 
          ray_version: Optional[str], head_config: Optional[str], worker_config: Optional[str]):
    """Create a new compute configuration.
    
    You can specify compute configuration either via command line options or by loading
    from a configuration file using --file option. Command line options take precedence
    over file configuration.
    
    Example file format (YAML):
    \b
    name: "my-compute-config"
    ray_version: "2.8.0"
    head_config:
      rayStartParams:
        dashboard-host: "0.0.0.0"
        dashboard-port: 8265
      resources:
        CPU: 4
        memory: 8Gi
    worker_config:
      rayStartParams: {}
      resources:
        CPU: 2
        memory: 4Gi
      replicas: 3
    
    Example file format (JSON):
    \b
    {
      "name": "my-compute-config",
      "ray_version": "2.8.0",
      "head_config": {
        "rayStartParams": {
          "dashboard-host": "0.0.0.0",
          "dashboard-port": 8265
        },
        "resources": {
          "CPU": 4,
          "memory": "8Gi"
        }
      },
      "worker_config": {
        "rayStartParams": {},
        "resources": {
          "CPU": 2,
          "memory": "4Gi"
        },
        "replicas": 3
      }
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
        
        # Handle JSON string arguments from command line
        parsed_head_config = None
        parsed_worker_config = None
        
        if head_config:
            try:
                parsed_head_config = json.loads(head_config)
            except json.JSONDecodeError as e:
                print_error(f"Invalid head configuration JSON: {e}")
                ctx.exit(1)
        
        if worker_config:
            try:
                parsed_worker_config = json.loads(worker_config)
            except json.JSONDecodeError as e:
                print_error(f"Invalid worker configuration JSON: {e}")
                ctx.exit(1)
        
        # Merge file config with command line arguments
        merged_config = merge_config_with_args(
            file_config,
            name=name,
            ray_version=ray_version,
            head_config=parsed_head_config,
            worker_config=parsed_worker_config
        )
        
        # Validate required fields
        validate_required_fields(
            merged_config, 
            ['name', 'ray_version', 'head_config', 'worker_config'], 
            'compute configuration'
        )
        
        result = client.create_compute_config(
            project_id=project_id,
            name=merged_config['name'],
            ray_version=merged_config['ray_version'],
            head_config=merged_config['head_config'],
            worker_config=merged_config['worker_config']
        )
        
        print_success(f"Compute configuration '{merged_config['name']}' created successfully")
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
        
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@compute_config.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.option('--page', default=1, help='Page number')
@click.option('--page-size', '-s', default=20, help='Page size')
@click.pass_context
def list(ctx, project_id: str, page: int, page_size: int):
    """List compute configurations in project."""
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        result = client.list_compute_configs(project_id=project_id, page=page, page_size=page_size)
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@compute_config.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.argument('config_id')
@click.pass_context
def get(ctx, project_id: str, config_id: str):
    """Get compute configuration details."""
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        result = client.get_compute_config(project_id, config_id)
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@compute_config.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.argument('config_id')
@click.option('--file', '-f', help='Load compute configuration from file (YAML/JSON)')
@click.option('--name', '-n', help='New configuration name')
@click.option('--ray-version', '-r', help='New Ray version')
@click.option('--head-config', '-h', help='New head node configuration (JSON string)')
@click.option('--worker-config', '-w', help='New worker node configuration (JSON string)')
@click.pass_context
def update(ctx, project_id: str, config_id: str, file: Optional[str], name: Optional[str], 
          ray_version: Optional[str], head_config: Optional[str], worker_config: Optional[str]):
    """Update compute configuration.
    
    You can specify updates either via command line options or by loading
    from a configuration file using --file option. Command line options take precedence
    over file configuration.
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
        
        # Handle JSON string arguments from command line
        parsed_head_config = None
        parsed_worker_config = None
        
        if head_config:
            try:
                parsed_head_config = json.loads(head_config)
            except json.JSONDecodeError as e:
                print_error(f"Invalid head configuration JSON: {e}")
                ctx.exit(1)
        
        if worker_config:
            try:
                parsed_worker_config = json.loads(worker_config)
            except json.JSONDecodeError as e:
                print_error(f"Invalid worker configuration JSON: {e}")
                ctx.exit(1)
        
        # Merge file config with command line arguments
        merged_config = merge_config_with_args(
            file_config,
            name=name,
            ray_version=ray_version,
            head_config=parsed_head_config,
            worker_config=parsed_worker_config
        )
        
        result = client.update_compute_config(
            project_id=project_id,
            config_id=config_id,
            name=merged_config.get('name'),
            ray_version=merged_config.get('ray_version'),
            head_config=merged_config.get('head_config'),
            worker_config=merged_config.get('worker_config')
        )
        
        print_success(f"Compute configuration '{config_id}' updated successfully")
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@compute_config.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.argument('config_id')
@click.option('--force', '-f', is_flag=True, help='Force delete without confirmation')
@click.pass_context
def delete(ctx, project_id: str, config_id: str, force: bool):
    """Delete compute configuration."""
    try:
        config = ctx.obj['config']
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        if not force:
            if not confirm_action(f"Are you sure you want to delete compute configuration '{config_id}'?"):
                click.echo("Operation cancelled.")
                return
        
        client = MCEClient(config)
        
        client.delete_compute_config(project_id, config_id)
        print_success(f"Compute configuration '{config_id}' deleted successfully")
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@compute_config.command()
@click.pass_context
def template(ctx):
    """Show compute configuration template."""
    template = {
        "head_config": {
            "rayStartParams": {
                "dashboard-host": "0.0.0.0",
                "metrics-export-port": "8080"
            },
            "resources": {
                "cpu": "2",
                "memory": "4Gi"
            },
            "image": "rayproject/ray:2.8.0",
            "env": []
        },
        "worker_config": {
            "minReplicas": 1,
            "maxReplicas": 3,
            "rayStartParams": {},
            "resources": {
                "cpu": "1",
                "memory": "2Gi"
            },
            "image": "rayproject/ray:2.8.0",
            "env": []
        }
    }
    
    config = ctx.obj['config']
    print_output(template, config.output_format, config.color_enabled)