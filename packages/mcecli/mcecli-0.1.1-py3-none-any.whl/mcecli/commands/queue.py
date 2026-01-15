"""Queue management commands."""

import click
from typing import Optional

from ..client import MCEClient
from ..config import Config
from ..utils import (
    print_output, print_error, print_success, confirm_action, get_project_id,
    load_config_from_file, merge_config_with_args, validate_required_fields
)
from ..exceptions import MCEError


@click.group()
def queue():
    """Manage queues."""
    pass


@queue.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.option('--file', '-f', help='Load queue configuration from file (YAML/JSON)')
@click.option('--name', '-n', help='Queue name')
@click.option('--weight', '-w', type=int, help='Queue weight')
@click.option('--flavor-name', help='Flavor name')
@click.pass_context
def create(ctx, project_id: str, file: Optional[str], name: Optional[str], 
          weight: Optional[int], flavor_name: Optional[str]):
    """Create a new queue.
    
    You can specify queue configuration either via command line options or by loading
    from a configuration file using --file option. Command line options take precedence
    over file configuration.
    
    Example file format (YAML):
    \b
    name: "my-queue"
    weight: 10
    flavor_name: "gpu-flavor"
    
    Example file format (JSON):
    \b
    {
      "name": "my-queue",
      "weight": 10,
      "flavor_name": "gpu-flavor"
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
            weight=weight,
            flavor_name=flavor_name
        )
        
        # Validate required fields
        validate_required_fields(merged_config, ['name'], 'queue')
        
        # Set defaults
        final_config = {
            'project_id': project_id,
            'name': merged_config['name'],
            'weight': merged_config.get('weight', 1),
            'flavor_name': merged_config.get('flavor_name', 'default')
        }
        
        result = client.create_queue(**final_config)
        
        print_success(f"Queue '{final_config['name']}' created successfully in project '{project_id}'")
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@queue.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.option('--page', default=1, help='Page number')
@click.option('--page-size', '-s', default=20, help='Page size')
@click.pass_context
def list(ctx, project_id: str, page: int, page_size: int):
    """List queues in project."""
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        result = client.list_queues(project_id=project_id, page=page, page_size=page_size)
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@queue.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.argument('queue_id')
@click.pass_context
def get(ctx, project_id: str, queue_id: str):
    """Get queue details."""
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        result = client.get_queue(project_id, queue_id)
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@queue.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.argument('queue_id')
@click.option('--file', '-f', help='Load queue configuration from file (YAML/JSON)')
@click.option('--name', '-n', help='New queue name')
@click.option('--weight', '-w', type=int, help='New queue weight')
@click.pass_context
def update(ctx, project_id: str, queue_id: str, file: Optional[str], 
          name: Optional[str], weight: Optional[int]):
    """Update queue.
    
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
        
        # Merge file config with command line arguments
        merged_config = merge_config_with_args(
            file_config,
            name=name,
            weight=weight
        )
        
        result = client.update_queue(
            project_id=project_id,
            queue_id=queue_id,
            name=merged_config.get('name'),
            weight=merged_config.get('weight')
        )
        
        print_success(f"Queue '{queue_id}' updated successfully")
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@queue.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.argument('queue_id')
@click.option('--force', '-f', is_flag=True, help='Force delete without confirmation')
@click.pass_context
def delete(ctx, project_id: str, queue_id: str, force: bool):
    """Delete queue."""
    try:
        config = ctx.obj['config']
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        if not force:
            if not confirm_action(f"Are you sure you want to delete queue '{queue_id}'?"):
                click.echo("Operation cancelled.")
                return
        
        client = MCEClient(config)
        
        client.delete_queue(project_id, queue_id)
        print_success(f"Queue '{queue_id}' deleted successfully")
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@queue.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.argument('queue_id')
@click.pass_context
def status(ctx, project_id: str, queue_id: str):
    """Get queue status."""
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        result = client.get_queue_status(project_id, queue_id)
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)