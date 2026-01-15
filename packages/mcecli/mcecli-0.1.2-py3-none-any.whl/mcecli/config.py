"""Configuration management for MCE CLI."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for MCE CLI."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self._config = self._load_config()
    
    def _get_default_config_path(self) -> str:
        """Get default config file path."""
        home = Path.home()
        config_dir = home / ".mcecli"
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / "config.yaml")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if not os.path.exists(self.config_path):
            return self._get_default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "server": {
                "url": "http://localhost:8080",
                "timeout": 30
            },
            "output": {
                "format": "list",  # list, table, json, yaml
                "color": True
            },
            "auth": {
                "owner_appid": "",
                "owner_uin": "",
                "owner_sub_uin": ""
            },
            "project": {
                "default_id": ""
            },
            "cos": {
                "region": "",
                "secret_id": "",
                "secret_key": "",
                "bucket": "",
                "sub_path": ""
            }
        }
    
    def save(self):
        """Save configuration to file."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
    
    def get(self, key: str, default=None):
        """Get configuration value by key."""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value by key."""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    @property
    def server_url(self) -> str:
        """Get server URL."""
        return self.get("server.url", "http://localhost:8080")
    
    @property
    def timeout(self) -> int:
        """Get request timeout."""
        return self.get("server.timeout", 30)
    
    @property
    def output_format(self) -> str:
        """Get output format."""
        return self.get("output.format", "list")
    
    @property
    def color_enabled(self) -> bool:
        """Check if color output is enabled."""
        return self.get("output.color", True)
    
    @property
    def auth_info(self) -> Dict[str, str]:
        """Get authentication information."""
        return {
            "OwnerAppid": self.get("auth.owner_appid", ""),
            "OwnerUin": self.get("auth.owner_uin", ""),
            "OwnerSubUin": self.get("auth.owner_sub_uin", "")
        }
    
    @property
    def default_project_id(self) -> str:
        """Get default project ID."""
        return self.get("project.default_id", "")
    
    @property
    def cos_config(self) -> Dict[str, str]:
        """Get COS configuration."""
        return {
            "region": self.get("cos.region", ""),
            "secret_id": self.get("cos.secret_id", ""),
            "secret_key": self.get("cos.secret_key", ""),
            "bucket": self.get("cos.bucket", ""),
            "sub_path": self.get("cos.sub_path", "")
        }
    
    def is_cos_configured(self) -> bool:
        """Check if COS is properly configured."""
        cos_config = self.cos_config
        required_fields = ["region", "secret_id", "secret_key", "bucket"]
        return all(cos_config.get(field) for field in required_fields)