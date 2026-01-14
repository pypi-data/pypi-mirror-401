"""Project management commands."""

import click
from typing import Optional

from ..client import MCEClient
from ..config import Config
from ..utils import (
    print_output, print_error, print_success, confirm_action,
    load_config_from_file, merge_config_with_args, validate_required_fields
)
from ..exceptions import MCEError


@click.group()
def project():
    """Manage projects."""
    pass


@project.command()
@click.option('--file', '-f', help='Load project configuration from file (YAML/JSON)')
@click.option('--name', '-n', help='Project name')
@click.option('--description', '-d', help='Project description')
@click.option('--region', '-r', help='Project region')
@click.option('--tag', '-t', multiple=True, help='Project tags in key=value format')
@click.pass_context
def create(ctx, file: Optional[str], name: Optional[str], description: Optional[str], 
          region: Optional[str], tag: tuple):
    """Create a new project.
    
    You can specify project configuration either via command line options or by loading
    from a configuration file using --file option. Command line options take precedence
    over file configuration.
    
    Example file format (YAML):
    \b
    name: "my-project"
    description: "My project description"
    region: "us-west-1"
    tags:
      env: "production"
      team: "backend"
    
    Example file format (JSON):
    \b
    {
      "name": "my-project",
      "description": "My project description", 
      "region": "us-west-1",
      "tags": {
        "env": "production",
        "team": "backend"
      }
    }
    """
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
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
            description=description,
            region=region
        )
        
        # Handle tags from both file and command line
        tags = {}
        
        # Tags from file
        if 'tags' in file_config and isinstance(file_config['tags'], dict):
            tags.update(file_config['tags'])
        
        # Tags from command line (override file tags)
        for tag_str in tag:
            if '=' in tag_str:
                key, value = tag_str.split('=', 1)
                tags[key.strip()] = value.strip()
            else:
                click.echo(f"Warning: Invalid tag format '{tag_str}', expected key=value")
        
        # Validate required fields
        validate_required_fields(merged_config, ['name'], 'project')
        
        # Set defaults
        final_config = {
            'name': merged_config['name'],
            'description': merged_config.get('description', ''),
            'region': merged_config.get('region', 'default'),
            'tags': tags if tags else None
        }
        
        result = client.create_project(**final_config)
        
        print_success(f"Project '{final_config['name']}' created successfully")
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@project.command()
@click.option('--page', '-p', default=1, help='Page number')
@click.option('--page-size', '-s', default=20, help='Page size')
@click.pass_context
def list(ctx, page: int, page_size: int):
    """List projects."""
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
        result = client.list_projects(page=page, page_size=page_size)
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@project.command()
@click.argument('project_id')
@click.pass_context
def get(ctx, project_id: str):
    """Get project details."""
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
        result = client.get_project(project_id)
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@project.command()
@click.argument('project_id')
@click.option('--file', '-f', help='Load project configuration from file (YAML/JSON)')
@click.option('--name', '-n', help='New project name')
@click.option('--description', '-d', help='New project description')
@click.option('--tag', '-t', multiple=True, help='Project tags in key=value format')
@click.pass_context
def update(ctx, project_id: str, file: Optional[str], name: Optional[str], 
          description: Optional[str], tag: tuple):
    """Update project.
    
    You can specify updates either via command line options or by loading
    from a configuration file using --file option. Command line options take precedence
    over file configuration.
    """
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
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
            description=description
        )
        
        # Handle tags from both file and command line
        tags = None
        if 'tags' in file_config and isinstance(file_config['tags'], dict):
            tags = file_config['tags'].copy()
        
        # Tags from command line (override file tags)
        if tag:
            if tags is None:
                tags = {}
            for tag_str in tag:
                if '=' in tag_str:
                    key, value = tag_str.split('=', 1)
                    tags[key.strip()] = value.strip()
                else:
                    click.echo(f"Warning: Invalid tag format '{tag_str}', expected key=value")
        
        result = client.update_project(
            project_id=project_id,
            name=merged_config.get('name'),
            description=merged_config.get('description'),
            tags=tags
        )
        
        print_success(f"Project '{project_id}' updated successfully")
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@project.command()
@click.argument('project_id')
@click.option('--force', '-f', is_flag=True, help='Force delete without confirmation')
@click.pass_context
def delete(ctx, project_id: str, force: bool):
    """Delete project."""
    try:
        if not force:
            if not confirm_action(f"Are you sure you want to delete project '{project_id}'?"):
                click.echo("Operation cancelled.")
                return
        
        config = ctx.obj['config']
        client = MCEClient(config)
        
        client.delete_project(project_id)
        print_success(f"Project '{project_id}' deleted successfully")
        
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)