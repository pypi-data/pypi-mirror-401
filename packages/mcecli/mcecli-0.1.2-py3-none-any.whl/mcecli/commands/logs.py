"""Log management commands."""

import click
import time
import websocket
import json
from typing import Optional
from urllib.parse import urljoin, urlparse

from ..client import MCEClient
from ..config import Config
from ..utils import print_output, print_error, print_success, print_warning, get_project_id
from ..exceptions import MCEError


@click.group()
def logs():
    """Manage job logs."""
    pass


@logs.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.argument('job_id')
@click.option('--lines', '-n', type=int, help='Number of lines to show')
@click.option('--since', '-s', help='Show logs since timestamp (ISO format)')
@click.pass_context
def get(ctx, project_id: str, job_id: str, lines: Optional[int], since: Optional[str]):
    """Get job logs."""
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        result = client.get_job_logs(project_id, job_id, lines=lines, since=since)
        
        # Extract log content if it's in the expected format
        if isinstance(result, dict):
            if 'data' in result and isinstance(result['data'], dict):
                logs_data = result['data']
                if 'logs' in logs_data:
                    # Print raw log content
                    click.echo(logs_data['logs'])
                    return
            
            # Fallback to formatted output
            print_output(result, config.output_format, config.color_enabled)
        else:
            click.echo(str(result))
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)


@logs.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.argument('job_id')
@click.option('--follow', '-f', is_flag=True, help='Follow log output')
@click.pass_context
def stream(ctx, project_id: str, job_id: str, follow: bool):
    """Stream job logs in real-time."""
    try:
        config = ctx.obj['config']
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        # Convert HTTP URL to WebSocket URL
        server_url = config.server_url
        parsed = urlparse(server_url)
        ws_scheme = 'wss' if parsed.scheme == 'https' else 'ws'
        ws_url = f"{ws_scheme}://{parsed.netloc}/api/v1/projects/{project_id}/jobs/{job_id}/logs/stream"
        
        print_success(f"Connecting to log stream for job '{job_id}'...")
        print_warning("Press Ctrl+C to stop streaming")
        
        def on_message(ws, message):
            try:
                data = json.loads(message)
                if 'log' in data:
                    click.echo(data['log'], nl=False)
                elif 'error' in data:
                    print_error(f"Stream error: {data['error']}")
                elif 'status' in data:
                    print_warning(f"Status: {data['status']}")
            except json.JSONDecodeError:
                click.echo(message, nl=False)
        
        def on_error(ws, error):
            print_error(f"WebSocket error: {error}")
        
        def on_close(ws, close_status_code, close_msg):
            print_warning("Log stream closed")
        
        def on_open(ws):
            print_success("Connected to log stream")
        
        # Create WebSocket connection
        ws = websocket.WebSocketApp(
            ws_url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        
        try:
            ws.run_forever()
        except KeyboardInterrupt:
            print_warning("\nStopping log stream...")
            ws.close()
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except Exception as e:
        print_error(f"Failed to stream logs: {str(e)}")
        
        # Fallback to polling if WebSocket fails
        if follow:
            print_warning("Falling back to polling mode...")
            _poll_logs(ctx, project_id, job_id)


def _poll_logs(ctx, project_id: str, job_id: str, interval: int = 2):
    """Poll logs periodically as fallback."""
    config = ctx.obj['config']
    client = MCEClient(config)
    
    last_timestamp = None
    
    try:
        while True:
            try:
                result = client.get_job_logs(
                    project_id, 
                    job_id, 
                    since=last_timestamp
                )
                
                if isinstance(result, dict) and 'data' in result:
                    logs_data = result['data']
                    if 'logs' in logs_data and logs_data['logs']:
                        click.echo(logs_data['logs'], nl=False)
                    
                    # Update timestamp for next request
                    if 'timestamp' in logs_data:
                        last_timestamp = logs_data['timestamp']
                
                time.sleep(interval)
                
            except MCEError as e:
                print_error(f"Error polling logs: {str(e)}")
                time.sleep(interval)
                
    except KeyboardInterrupt:
        print_warning("\nStopped polling logs")


@logs.command()
@click.option('--project-id', '-p', help='Project ID (uses default if not specified)')
@click.argument('job_id')
@click.pass_context
def info(ctx, project_id: str, job_id: str):
    """Get log file information."""
    try:
        config = ctx.obj['config']
        client = MCEClient(config)
        
        # Get project ID with fallback to default
        project_id = get_project_id(project_id, config)
        
        result = client.get_log_file_info(project_id, job_id)
        print_output(result.get('data', result), config.output_format, config.color_enabled)
        
    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except MCEError as e:
        print_error(str(e))
        ctx.exit(1)