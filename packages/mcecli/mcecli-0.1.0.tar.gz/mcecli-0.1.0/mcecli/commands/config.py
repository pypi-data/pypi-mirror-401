"""Configuration management commands."""

import click
from ..config import Config
from ..utils import print_output, print_error, print_success


@click.group()
def config():
    """Manage CLI configuration."""
    pass


@config.command()
@click.option('--owner-appid', help='Owner App ID')
@click.option('--owner-uin', help='Owner UIN')
@click.option('--owner-sub-uin', help='Owner Sub UIN')
@click.option('--default-project', help='Default project ID')
@click.pass_context
def login(ctx, owner_appid: str, owner_uin: str, owner_sub_uin: str, default_project: str):
    """Configure authentication and default project."""
    try:
        config = ctx.obj['config']
        
        # Interactive input if not provided
        if not owner_appid:
            owner_appid = click.prompt('Owner App ID', default=config.get('auth.owner_appid', ''))
        if not owner_uin:
            owner_uin = click.prompt('Owner UIN', default=config.get('auth.owner_uin', ''))
        if not owner_sub_uin:
            owner_sub_uin = click.prompt('Owner Sub UIN', default=config.get('auth.owner_sub_uin', ''))
        if not default_project:
            current_default = config.get('project.default_id', '')
            default_project = click.prompt('Default Project ID (optional)', 
                                         default=current_default, 
                                         show_default=True if current_default else False)
        
        # Update configuration
        config.set('auth.owner_appid', owner_appid)
        config.set('auth.owner_uin', owner_uin)
        config.set('auth.owner_sub_uin', owner_sub_uin)
        if default_project:
            config.set('project.default_id', default_project)
        
        config.save()
        
        print_success("Authentication configured successfully")
        if default_project:
            print_success(f"Default project ID set to: {default_project}")
        
    except Exception as e:
        print_error(f"Failed to configure authentication: {str(e)}")
        ctx.exit(1)


@config.command()
@click.pass_context
def show(ctx):
    """Show current configuration."""
    config = ctx.obj['config']
    print_output(config._config, config.output_format, config.color_enabled)


@config.command()
@click.argument('key')
@click.argument('value')
@click.pass_context
def set(ctx, key: str, value: str):
    """Set configuration value."""
    try:
        config = ctx.obj['config']
        
        # Handle boolean values
        if value.lower() in ['true', 'false']:
            value = value.lower() == 'true'
        # Handle numeric values
        elif value.isdigit():
            value = int(value)
        
        config.set(key, value)
        config.save()
        
        print_success(f"Configuration '{key}' set to '{value}'")
        
    except Exception as e:
        print_error(f"Failed to set configuration: {str(e)}")
        ctx.exit(1)


@config.command()
@click.argument('key')
@click.pass_context
def get(ctx, key: str):
    """Get configuration value."""
    config = ctx.obj['config']
    value = config.get(key)
    
    if value is not None:
        click.echo(f"{key}: {value}")
    else:
        print_error(f"Configuration key '{key}' not found")
        ctx.exit(1)


@config.command()
@click.option('--force', '-f', is_flag=True, help='Force reset without confirmation')
@click.pass_context
def reset(ctx, force: bool):
    """Reset configuration to defaults."""
    try:
        if not force:
            from ..utils import confirm_action
            if not confirm_action("Are you sure you want to reset all configuration to defaults?"):
                click.echo("Operation cancelled.")
                return
        
        config = ctx.obj['config']
        config._config = config._get_default_config()
        config.save()
        
        print_success("Configuration reset to defaults")
        
    except Exception as e:
        print_error(f"Failed to reset configuration: {str(e)}")
        ctx.exit(1)


@config.command()
@click.pass_context
def path(ctx):
    """Show configuration file path."""
    config = ctx.obj['config']
    click.echo(config.config_path)


@config.command()
@click.option('--region', help='COS region (e.g., ap-beijing, ap-shanghai)')
@click.option('--secret-id', help='COS Secret ID')
@click.option('--secret-key', help='COS Secret Key')
@click.option('--bucket', help='COS bucket name')
@click.option('--sub-path', help='Sub path in bucket (optional)', default='')
@click.pass_context
def cos(ctx, region: str, secret_id: str, secret_key: str, bucket: str, sub_path: str):
    """Configure COS (Cloud Object Storage) settings.
    
    Configure Tencent Cloud COS settings for code upload functionality.
    
    Examples:
    \b
    # Interactive configuration
    mcecli config cos
    
    # Direct configuration
    mcecli config cos --region ap-beijing --secret-id YOUR_ID --secret-key YOUR_KEY --bucket my-bucket --sub-path code/
    """
    try:
        config = ctx.obj['config']
        
        # Interactive input if not provided
        if not region:
            current_region = config.get('cos.region', '')
            region = click.prompt('COS Region (e.g., ap-beijing, ap-shanghai)', 
                                default=current_region if current_region else 'ap-beijing',
                                show_default=True)
        
        if not secret_id:
            current_secret_id = config.get('cos.secret_id', '')
            secret_id = click.prompt('COS Secret ID', 
                                   default=current_secret_id,
                                   show_default=bool(current_secret_id))
        
        if not secret_key:
            current_secret_key = config.get('cos.secret_key', '')
            secret_key = click.prompt('COS Secret Key', 
                                    default=current_secret_key,
                                    hide_input=True,
                                    show_default=bool(current_secret_key))
        
        if not bucket:
            current_bucket = config.get('cos.bucket', '')
            bucket = click.prompt('COS Bucket Name', 
                                default=current_bucket,
                                show_default=bool(current_bucket))
        
        if sub_path is None:  # Only prompt if not provided (including empty string)
            current_sub_path = config.get('cos.sub_path', '')
            sub_path = click.prompt('Sub Path (optional, e.g., code/)', 
                                  default=current_sub_path,
                                  show_default=bool(current_sub_path))
        
        # Validate region format
        valid_regions = [
            'ap-beijing', 'ap-shanghai', 'ap-guangzhou', 'ap-chengdu', 'ap-chongqing',
            'ap-nanjing', 'ap-tianjin', 'ap-shenzhen-fsi', 'ap-beijing-fsi', 'ap-shanghai-fsi',
            'ap-hongkong', 'ap-singapore', 'ap-mumbai', 'ap-seoul', 'ap-bangkok',
            'ap-tokyo', 'na-siliconvalley', 'na-ashburn', 'eu-frankfurt'
        ]
        
        if region and region not in valid_regions:
            click.echo(f"Warning: '{region}' is not a standard COS region.")
            click.echo(f"Valid regions include: {', '.join(valid_regions[:10])}...")
            if not click.confirm("Continue with this region?"):
                return
        
        # Ensure sub_path ends with / if not empty
        if sub_path and not sub_path.endswith('/'):
            sub_path += '/'
        
        # Update configuration
        config.set('cos.region', region)
        config.set('cos.secret_id', secret_id)
        config.set('cos.secret_key', secret_key)
        config.set('cos.bucket', bucket)
        config.set('cos.sub_path', sub_path)
        
        config.save()
        
        print_success("COS configuration saved successfully")
        print_success(f"Region: {region}")
        print_success(f"Bucket: {bucket}")
        if sub_path:
            print_success(f"Sub Path: {sub_path}")
        
        # Test configuration
        if click.confirm("Test COS connection?", default=True):
            _test_cos_connection(config)
        
    except Exception as e:
        print_error(f"Failed to configure COS: {str(e)}")
        ctx.exit(1)


@config.command()
@click.pass_context
def cos_show(ctx):
    """Show current COS configuration."""
    config = ctx.obj['config']
    cos_config = config.cos_config
    
    # Mask sensitive information
    masked_config = cos_config.copy()
    if masked_config['secret_key']:
        masked_config['secret_key'] = '*' * 8 + masked_config['secret_key'][-4:]
    
    # Format for display
    display_data = [
        {'Field': 'Region', 'Value': masked_config['region']},
        {'Field': 'Secret ID', 'Value': masked_config['secret_id']},
        {'Field': 'Secret Key', 'Value': masked_config['secret_key']},
        {'Field': 'Bucket', 'Value': masked_config['bucket']},
        {'Field': 'Sub Path', 'Value': masked_config['sub_path']},
    ]
    
    print_output(display_data, config.output_format, config.color_enabled)
    
    if config.is_cos_configured():
        print_success("✓ COS is properly configured")
    else:
        print_error("✗ COS configuration is incomplete")


@config.command()
@click.pass_context
def cos_test(ctx):
    """Test COS connection and permissions."""
    config = ctx.obj['config']
    
    if not config.is_cos_configured():
        print_error("COS is not properly configured. Run 'mcecli config cos' first.")
        ctx.exit(1)
    
    _test_cos_connection(config)


def _test_cos_connection(config):
    """Test COS connection and basic operations."""
    try:
        # Import COS SDK (we'll need to add this dependency)
        try:
            from qcloud_cos import CosConfig, CosS3Client
        except ImportError:
            print_error("COS SDK not installed. Install with: pip install cos-python-sdk-v5")
            return
        
        cos_config_obj = config.cos_config
        
        # Initialize COS client
        cos_config = CosConfig(
            Region=cos_config_obj['region'],
            SecretId=cos_config_obj['secret_id'],
            SecretKey=cos_config_obj['secret_key']
        )
        client = CosS3Client(cos_config)
        
        # Test bucket access
        bucket = cos_config_obj['bucket']
        response = client.head_bucket(Bucket=bucket)
        
        print_success("✓ COS connection successful")
        print_success(f"✓ Bucket '{bucket}' is accessible")
        
        # Test upload permission with a small test file
        test_key = f"{cos_config_obj['sub_path']}test_upload.txt"
        test_content = "MCE CLI test upload"
        
        client.put_object(
            Bucket=bucket,
            Key=test_key,
            Body=test_content.encode('utf-8')
        )
        print_success("✓ Upload permission verified")
        
        # Clean up test file
        client.delete_object(Bucket=bucket, Key=test_key)
        print_success("✓ Delete permission verified")
        
    except Exception as e:
        print_error(f"COS connection test failed: {str(e)}")
        print_error("Please check your COS configuration and permissions")