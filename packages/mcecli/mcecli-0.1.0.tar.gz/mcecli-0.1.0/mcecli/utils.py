"""Utility functions for MCE CLI."""

import json
import yaml
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from tabulate import tabulate


console = Console()


def load_config_from_file(file_path: str) -> Dict[str, Any]:
    """Load configuration from YAML or JSON file.
    
    Args:
        file_path: Path to the configuration file
        
    Returns:
        Dictionary containing the loaded configuration
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file format is not supported or invalid
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            if suffix in ['.yaml', '.yml']:
                return yaml.safe_load(f) or {}
            elif suffix == '.json':
                return json.load(f)
            else:
                # Try to auto-detect format
                content = f.read()
                f.seek(0)
                
                # Try JSON first
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    pass
                
                # Try YAML
                try:
                    return yaml.safe_load(content) or {}
                except yaml.YAMLError:
                    pass
                
                raise ValueError(f"Unsupported file format: {suffix}. Supported formats: .yaml, .yml, .json")
    
    except (json.JSONDecodeError, yaml.YAMLError) as e:
        raise ValueError(f"Invalid file format in {file_path}: {str(e)}")


def merge_config_with_args(file_config: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """Merge file configuration with command line arguments.
    
    Command line arguments take precedence over file configuration.
    
    Args:
        file_config: Configuration loaded from file
        **kwargs: Command line arguments
        
    Returns:
        Merged configuration dictionary
    """
    merged = file_config.copy()
    
    # Override with command line arguments (non-None values)
    for key, value in kwargs.items():
        if value is not None:
            merged[key] = value
    
    return merged


def validate_required_fields(config: Dict[str, Any], required_fields: List[str], resource_type: str = "resource") -> None:
    """Validate that required fields are present in configuration.
    
    Args:
        config: Configuration dictionary
        required_fields: List of required field names
        resource_type: Type of resource for error messages
        
    Raises:
        ValueError: If any required field is missing
    """
    missing_fields = []
    for field in required_fields:
        if field not in config or config[field] is None:
            missing_fields.append(field)
    
    if missing_fields:
        raise ValueError(
            f"Missing required fields for {resource_type}: {', '.join(missing_fields)}"
        )


def get_project_id(project_id_arg: Optional[str], config) -> str:
    """Get project ID with priority: command argument > config default.
    
    Args:
        project_id_arg: Project ID from command line argument
        config: Configuration object
        
    Returns:
        Project ID string
        
    Raises:
        ValueError: If no project ID is available
    """
    if project_id_arg:
        return project_id_arg
    
    default_project_id = config.default_project_id
    if default_project_id:
        return default_project_id
    
    raise ValueError(
        "No project ID specified. Use --project-id flag or set default project ID with 'mcecli config login'"
    )


def format_output(data: Any, output_format: str = "list", color: bool = True) -> str:
    """Format output data according to specified format."""
    if output_format == "json":
        return json.dumps(data, indent=2, ensure_ascii=False)
    elif output_format == "yaml":
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)
    elif output_format == "table":
        return format_table(data)
    elif output_format == "list":
        return format_list(data)
    else:
        return str(data)


def format_table(data: Any) -> str:
    """Format data as a table."""
    if isinstance(data, dict):
        if "items" in data and isinstance(data["items"], list):
            # Handle paginated response
            items = data["items"]
            if items:
                return _format_list_as_table(items)
            else:
                return "No items found."
        else:
            # Handle single object
            return _format_dict_as_table(data)
    elif isinstance(data, list):
        return _format_list_as_table(data)
    else:
        return str(data)


def _format_dict_as_table(data: Dict[str, Any]) -> str:
    """Format dictionary as a two-column table."""
    rows = []
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        rows.append([key, str(value)])
    
    return tabulate(rows, headers=["Field", "Value"], tablefmt="grid")


def _format_list_as_table(data: List[Dict[str, Any]]) -> str:
    """Format list of dictionaries as a table."""
    if not data:
        return "No data available."
    
    # Get all unique keys from all dictionaries
    all_keys = set()
    for item in data:
        if isinstance(item, dict):
            all_keys.update(item.keys())
    
    headers = sorted(all_keys)
    rows = []
    
    for item in data:
        if isinstance(item, dict):
            row = []
            for header in headers:
                value = item.get(header, "")
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False)
                row.append(str(value))
            rows.append(row)
        else:
            rows.append([str(item)])
    
    return tabulate(rows, headers=headers, tablefmt="grid")


def format_list(data: Any) -> str:
    """Format data as a compact list suitable for 80-character console width."""
    if isinstance(data, dict):
        if "items" in data and isinstance(data["items"], list):
            # Handle paginated response
            items = data["items"]
            if items:
                return _format_items_as_list(items)
            else:
                return "No items found."
        else:
            # Handle single object
            return _format_single_item_as_list(data)
    elif isinstance(data, list):
        return _format_items_as_list(data)
    else:
        return str(data)


def _get_essential_fields(item: Dict[str, Any]) -> Dict[str, str]:
    """Get essential fields for list display based on item type."""
    # Helper function to get ID field
    def get_id_field():
        return item.get("id") or item.get("configId") or item.get("queueId") or item.get("projectId") or ""
    
    # Helper function to get name field  
    def get_name_field():
        return item.get("name") or item.get("configName") or item.get("queueName") or item.get("projectName") or ""
    
    # Detect resource type based on available fields
    if "type" in item and item.get("type") == "ray":
        # Job
        return {
            "ID": get_id_field(),
            "Name": get_name_field(),
            "Status": item.get("status", ""),
            "Image": item.get("image", ""),
            "Queue": item.get("queueId", ""),
            "Created": format_timestamp(item.get("createdAt", "")) if item.get("createdAt") else ""
        }
    elif "rayVersion" in item or "headConfig" in item or "headNodeSummary" in item or "configId" in item:
        # Compute Config
        return {
            "ID": get_id_field(),
            "Name": get_name_field(),
            "Status": item.get("status", ""),
            "Region": item.get("region", ""),
            "Description": item.get("description", ""),
            "Created": format_timestamp(item.get("createdAt", "")) if item.get("createdAt") else ""
        }
    elif "weight" in item or "flavorName" in item or "queueId" in item:
        # Queue
        return {
            "ID": get_id_field(),
            "Name": get_name_field(),
            "Weight": str(item.get("weight", "")),
            "Flavor": item.get("flavorName", ""),
            "Status": item.get("status", ""),
            "Created": format_timestamp(item.get("createdAt", "")) if item.get("createdAt") else ""
        }
    elif "region" in item or "quota" in item or "projectId" in item:
        # Project
        return {
            "ID": get_id_field(),
            "Name": get_name_field(),
            "Region": item.get("region", ""),
            "Description": item.get("description", ""),
            "Status": item.get("status", ""),
            "Created": format_timestamp(item.get("createdAt", "")) if item.get("createdAt") else ""
        }
    else:
        # Generic object - show first few fields
        essential = {}
        count = 0
        for key, value in item.items():
            if count >= 6:  # Show more fields for better information
                break
            if not isinstance(value, (dict, list)):
                field_name = key.replace("_", " ").title()
                essential[field_name] = str(value)
                count += 1
        return essential


def _format_items_as_list(items: List[Dict[str, Any]]) -> str:
    """Format list of items in well-aligned list format."""
    if not items:
        return "No items found."
    
    # Get essential fields from first item to determine headers
    first_item = items[0] if items else {}
    essential_fields = _get_essential_fields(first_item)
    headers = list(essential_fields.keys())
    
    rows = []
    for item in items:
        if isinstance(item, dict):
            essential = _get_essential_fields(item)
            row = [essential.get(header, "") for header in headers]
            rows.append(row)
        else:
            rows.append([str(item)])
    
    # Use simple format without borders for clean output
    return tabulate(rows, headers=headers, tablefmt="simple")


def _format_single_item_as_list(item: Dict[str, Any]) -> str:
    """Format single item in well-aligned list format."""
    essential = _get_essential_fields(item)
    
    # For single items, show as key-value pairs without borders
    rows = []
    for key, value in essential.items():
        rows.append([key, value])
    
    return tabulate(rows, headers=["Field", "Value"], tablefmt="simple")


def print_output(data: Any, output_format: str = "list", color: bool = True):
    """Print formatted output to console."""
    formatted = format_output(data, output_format, color)
    
    if color and output_format in ["json", "yaml"]:
        # Use rich syntax highlighting for JSON/YAML
        syntax = Syntax(formatted, output_format, theme="monokai", line_numbers=False)
        console.print(syntax)
    else:
        console.print(formatted)


def print_error(message: str, color: bool = True):
    """Print error message to console."""
    if color:
        console.print(f"[red]Error: {message}[/red]")
    else:
        console.print(f"Error: {message}")


def print_success(message: str, color: bool = True):
    """Print success message to console."""
    if color:
        console.print(f"[green]✓ {message}[/green]")
    else:
        console.print(f"✓ {message}")


def print_warning(message: str, color: bool = True):
    """Print warning message to console."""
    if color:
        console.print(f"[yellow]⚠ {message}[/yellow]")
    else:
        console.print(f"⚠ {message}")


def confirm_action(message: str, default: bool = False) -> bool:
    """Ask user for confirmation."""
    suffix = " [Y/n]" if default else " [y/N]"
    response = input(f"{message}{suffix}: ").strip().lower()
    
    if not response:
        return default
    
    return response in ['y', 'yes', 'true', '1']


def truncate_string(text: str, max_length: int = 50) -> str:
    """Truncate string if it's too long."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display."""
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, AttributeError):
        return timestamp


def format_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"