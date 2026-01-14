"""Main CLI entry point."""

import click
import sys
from pathlib import Path

from .config import Config
from .client import MCEClient
from .utils import print_error, print_success
from .exceptions import MCEError, MCEConfigError

# Import command groups
from .commands.project import project
from .commands.queue import queue
from .commands.compute_config import compute_config
from .commands.job import job
from .commands.logs import logs
from .commands.config import config
from .commands.upload import upload


@click.group()
@click.option('--config-file', '-c', help='Configuration file path')
@click.option('--server-url', '-s', help='MCE Server URL')
@click.option('--output', '-o', type=click.Choice(['list', 'table', 'json', 'yaml']), help='Output format')
@click.option('--no-color', is_flag=True, help='Disable colored output')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def cli(ctx, config_file, server_url, output, no_color, verbose):
    """MCE CLI - A Python client for MCE Server.
    
    MCE (Multi-modal Compute Engine) CLI provides a command-line interface
    for managing projects, queues, compute configurations, and jobs on MCE Server.
    """
    try:
        # Initialize configuration
        config_obj = Config(config_file)
        
        # Override config with command line options
        if server_url:
            config_obj.set('server.url', server_url)
        if output:
            config_obj.set('output.format', output)
        if no_color:
            config_obj.set('output.color', False)
        
        # Store config in context
        ctx.ensure_object(dict)
        ctx.obj['config'] = config_obj
        ctx.obj['verbose'] = verbose
        
    except Exception as e:
        print_error(f"Failed to initialize configuration: {str(e)}")
        sys.exit(1)


@cli.command()
@click.pass_context
def health(ctx):
    """Check MCE Server health."""
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
        result = client.health_check()
        print_success("MCE Server is healthy")
        
        if ctx.obj.get('verbose'):
            from .utils import print_output
            print_output(result, config.output_format, config.color_enabled)
        
    except MCEError as e:
        print_error(f"Health check failed: {str(e)}")
        ctx.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """Show version information."""
    from . import __version__
    click.echo(f"MCE CLI version: {__version__}")


# Add command groups
cli.add_command(project)
cli.add_command(queue)
cli.add_command(compute_config)
cli.add_command(job)
cli.add_command(logs)
cli.add_command(config)
cli.add_command(upload)


if __name__ == '__main__':
    cli()