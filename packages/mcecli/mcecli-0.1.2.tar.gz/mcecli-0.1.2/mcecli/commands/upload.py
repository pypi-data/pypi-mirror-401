"""Code upload commands."""

import os
import click
import hashlib
import tarfile
from pathlib import Path
from typing import Optional, List
from datetime import datetime

from ..config import Config
from ..utils import print_output, print_error, print_success, print_warning


@click.group()
def upload():
    """Upload local code to COS."""
    pass


@upload.command()
@click.argument('source_path', type=click.Path(exists=True))
@click.option('--name', '-n', help='Custom name for the uploaded code package')
@click.option('--exclude', '-e', multiple=True, help='Exclude patterns (e.g., *.pyc, __pycache__)')
@click.option('--include-hidden', is_flag=True, help='Include hidden files and directories')
@click.option('--dry-run', is_flag=True, help='Show what would be uploaded without actually uploading')
@click.option('--force', '-f', is_flag=True, help='Overwrite existing files without confirmation')
@click.pass_context
def code(ctx, source_path: str, name: Optional[str], exclude: tuple, 
         include_hidden: bool, dry_run: bool, force: bool):
    """Upload local code directory or file to COS.
    
    This command packages your local code into a tar.gz file and uploads it to COS.
    The uploaded code can then be referenced in job configurations.
    
    Examples:
    \b
    # Upload current directory
    mcecli upload code .
    
    # Upload specific directory with custom name
    mcecli upload code ./my-project --name my-training-code
    
    # Upload with exclusions
    mcecli upload code . --exclude "*.pyc" --exclude "__pycache__" --exclude ".git"
    
    # Dry run to see what would be uploaded
    mcecli upload code . --dry-run
    """
    try:
        config = ctx.obj['config'] if ctx.obj else Config()
        
        # Check COS configuration
        if not config.is_cos_configured():
            print_error("COS is not configured. Run 'mcecli config cos' first.")
            ctx.exit(1)
        
        source_path = Path(source_path).resolve()
        
        # Generate package name if not provided
        if not name:
            if source_path.is_file():
                name = source_path.stem
            else:
                name = source_path.name
            
            # Add timestamp to make it unique
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"{name}_{timestamp}"
        
        # Default exclude patterns
        default_excludes = [
            '*.pyc', '*.pyo', '*.pyd', '__pycache__',
            '.git', '.gitignore', '.DS_Store', '*.log',
            '.pytest_cache', '.coverage', 'htmlcov',
            'node_modules', '.npm', '.yarn',
            '*.egg-info', 'dist', 'build'
        ]
        
        exclude_patterns = list(exclude) + default_excludes
        
        print_success(f"Preparing to upload: {source_path}")
        print_success(f"Package name: {name}")
        
        if dry_run:
            print_warning("DRY RUN MODE - No files will be uploaded")
        
        # Create temporary tar.gz file
        tar_path = _create_code_package(
            source_path, name, exclude_patterns, include_hidden, dry_run
        )
        
        if dry_run:
            print_success("Dry run completed. Use --dry-run=false to actually upload.")
            return
        
        # Upload to COS (only if not dry run)
        cos_key = _upload_to_cos(config, tar_path, name, force)
        
        # Clean up temporary file
        if tar_path.exists():
            tar_path.unlink()
        
        print_success(f"Code uploaded successfully!")
        print_success(f"COS Key: {cos_key}")
        print_success(f"Use this in your job configuration:")
        print_success(f"  volumeMounts:")
        print_success(f"    - type: COS")
        print_success(f"      remotePath: cos://{config.cos_config['bucket']}/{cos_key}")
        print_success(f"      mountPath: /code")
        
    except Exception as e:
        print_error(f"Upload failed: {str(e)}")
        ctx.exit(1)


@upload.command(name='list')
@click.pass_context
def list_packages(ctx):
    """List uploaded code packages in COS."""
    try:
        config = ctx.obj['config'] if ctx.obj else Config()
        
        if not config.is_cos_configured():
            print_error("COS is not configured. Run 'mcecli config cos' first.")
            ctx.exit(1)
        
        packages = _list_cos_packages(config)
        
        if not packages:
            print_warning("No code packages found in COS.")
            return
        
        # Format for display
        formatted_packages = []
        for pkg in packages:
            formatted_packages.append({
                'Name': pkg['name'],
                'Size': _format_size(pkg['size']),
                'Modified': pkg['modified'],
                'Key': pkg['key']
            })
        
        print_output(formatted_packages, config.output_format, config.color_enabled)
        
    except Exception as e:
        print_error(f"Failed to list packages: {str(e)}")
        ctx.exit(1)


@upload.command()
@click.argument('package_name')
@click.option('--force', '-f', is_flag=True, help='Delete without confirmation')
@click.pass_context
def delete(ctx, package_name: str, force: bool):
    """Delete a code package from COS."""
    try:
        config = ctx.obj['config'] if ctx.obj else Config()
        
        if not config.is_cos_configured():
            print_error("COS is not configured. Run 'mcecli config cos' first.")
            ctx.exit(1)
        
        if not force:
            from ..utils import confirm_action
            if not confirm_action(f"Are you sure you want to delete package '{package_name}'?"):
                click.echo("Operation cancelled.")
                return
        
        _delete_cos_package(config, package_name)
        print_success(f"Package '{package_name}' deleted successfully.")
        
    except Exception as e:
        print_error(f"Failed to delete package: {str(e)}")
        ctx.exit(1)


def _create_code_package(source_path: Path, name: str, exclude_patterns: List[str], 
                        include_hidden: bool, dry_run: bool) -> Path:
    """Create a tar.gz package from source code."""
    import fnmatch
    
    # Create temporary tar.gz file
    temp_dir = Path.home() / ".mcecli" / "temp"
    temp_dir.mkdir(exist_ok=True)
    tar_path = temp_dir / f"{name}.tar.gz"
    
    files_to_include = []
    total_size = 0
    
    if source_path.is_file():
        # Single file
        if not _should_exclude(source_path.name, exclude_patterns):
            files_to_include.append((source_path, source_path.name))
            total_size += source_path.stat().st_size
    else:
        # Directory
        for root, dirs, files in os.walk(source_path):
            root_path = Path(root)
            
            # Filter directories
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not _should_exclude(d, exclude_patterns)]
            
            for file in files:
                if not include_hidden and file.startswith('.'):
                    continue
                
                if _should_exclude(file, exclude_patterns):
                    continue
                
                file_path = root_path / file
                relative_path = file_path.relative_to(source_path)
                
                files_to_include.append((file_path, str(relative_path)))
                total_size += file_path.stat().st_size
    
    print_success(f"Found {len(files_to_include)} files to include ({_format_size(total_size)})")
    
    if dry_run:
        print_success("Files that would be included:")
        for _, rel_path in files_to_include[:20]:  # Show first 20 files
            print_success(f"  {rel_path}")
        if len(files_to_include) > 20:
            print_success(f"  ... and {len(files_to_include) - 20} more files")
        return Path()  # Return empty path for dry run
    
    # Create tar.gz file
    with tarfile.open(tar_path, 'w:gz') as tar:
        for file_path, arc_name in files_to_include:
            tar.add(file_path, arcname=arc_name)
    
    tar_size = tar_path.stat().st_size
    print_success(f"Created package: {tar_path} ({_format_size(tar_size)})")
    
    return tar_path


def _should_exclude(filename: str, exclude_patterns: List[str]) -> bool:
    """Check if file should be excluded based on patterns."""
    import fnmatch
    
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False


def _upload_to_cos(config: Config, tar_path: Path, name: str, force: bool) -> str:
    """Upload tar.gz file to COS."""
    try:
        from qcloud_cos import CosConfig, CosS3Client
    except ImportError:
        raise Exception("COS SDK not installed. Install with: pip install cos-python-sdk-v5")
    
    cos_config_obj = config.cos_config
    
    # Initialize COS client
    cos_config = CosConfig(
        Region=cos_config_obj['region'],
        SecretId=cos_config_obj['secret_id'],
        SecretKey=cos_config_obj['secret_key']
    )
    client = CosS3Client(cos_config)
    
    # Generate COS key
    cos_key = f"{cos_config_obj['sub_path']}{name}.tar.gz"
    bucket = cos_config_obj['bucket']
    
    # Check if file already exists
    try:
        client.head_object(Bucket=bucket, Key=cos_key)
        if not force:
            if not click.confirm(f"Package '{name}' already exists. Overwrite?"):
                raise Exception("Upload cancelled by user")
    except Exception as e:
        if "NoSuchKey" not in str(e):
            # File exists but we got a different error
            pass
    
    # Upload file
    print_success(f"Uploading to COS: {cos_key}")
    
    with open(tar_path, 'rb') as f:
        client.put_object(
            Bucket=bucket,
            Key=cos_key,
            Body=f
        )
    
    return cos_key


def _list_cos_packages(config: Config) -> List[dict]:
    """List code packages in COS."""
    try:
        from qcloud_cos import CosConfig, CosS3Client
    except ImportError:
        raise Exception("COS SDK not installed. Install with: pip install cos-python-sdk-v5")
    
    cos_config_obj = config.cos_config
    
    # Initialize COS client
    cos_config = CosConfig(
        Region=cos_config_obj['region'],
        SecretId=cos_config_obj['secret_id'],
        SecretKey=cos_config_obj['secret_key']
    )
    client = CosS3Client(cos_config)
    
    bucket = cos_config_obj['bucket']
    prefix = cos_config_obj['sub_path']
    
    # List objects
    response = client.list_objects(Bucket=bucket, Prefix=prefix)
    
    packages = []
    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            if key.endswith('.tar.gz'):
                name = Path(key).stem.replace('.tar', '')  # Remove .tar from .tar.gz
                if prefix and key.startswith(prefix):
                    name = key[len(prefix):].replace('.tar.gz', '')
                
                packages.append({
                    'name': name,
                    'key': key,
                    'size': int(obj['Size']),
                    'modified': obj['LastModified']
                })
    
    return packages


def _delete_cos_package(config: Config, package_name: str):
    """Delete a code package from COS."""
    try:
        from qcloud_cos import CosConfig, CosS3Client
    except ImportError:
        raise Exception("COS SDK not installed. Install with: pip install cos-python-sdk-v5")
    
    cos_config_obj = config.cos_config
    
    # Initialize COS client
    cos_config = CosConfig(
        Region=cos_config_obj['region'],
        SecretId=cos_config_obj['secret_id'],
        SecretKey=cos_config_obj['secret_key']
    )
    client = CosS3Client(cos_config)
    
    # Generate COS key
    cos_key = f"{cos_config_obj['sub_path']}{package_name}.tar.gz"
    bucket = cos_config_obj['bucket']
    
    # Delete object
    client.delete_object(Bucket=bucket, Key=cos_key)


def _format_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"