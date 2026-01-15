"""
Configuration management for OffCall CLI.

Config file location: ~/.offcall/config.yaml

Example config:
    default:
      api_url: https://api.offcallai.com/api/v1
      api_key: ofc_xxxxxxxxxxxx

    staging:
      api_url: https://staging-api.offcallai.com/api/v1
      api_key: ofc_staging_key
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import yaml


CONFIG_DIR = Path.home() / ".offcall"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
DEFAULT_API_URL = "https://api.offcallai.com/api/v1"


class Config:
    """CLI configuration manager."""

    def __init__(self, profile: str = "default"):
        self.profile = profile
        self._config: Dict[str, Any] = {}
        self._load()

    def _load(self):
        """Load configuration from file."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE) as f:
                    self._config = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Warning: Failed to load config: {e}")
                self._config = {}

        # Override with environment variables
        if os.environ.get("OFFCALL_API_KEY"):
            if self.profile not in self._config:
                self._config[self.profile] = {}
            self._config[self.profile]["api_key"] = os.environ["OFFCALL_API_KEY"]

        if os.environ.get("OFFCALL_API_URL"):
            if self.profile not in self._config:
                self._config[self.profile] = {}
            self._config[self.profile]["api_url"] = os.environ["OFFCALL_API_URL"]

    def _save(self):
        """Save configuration to file."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(self._config, f, default_flow_style=False)

    @property
    def api_url(self) -> str:
        """Get API URL for current profile."""
        profile_config = self._config.get(self.profile, {})
        return profile_config.get("api_url", DEFAULT_API_URL)

    @property
    def api_key(self) -> Optional[str]:
        """Get API key for current profile."""
        profile_config = self._config.get(self.profile, {})
        return profile_config.get("api_key")

    def set_api_key(self, api_key: str):
        """Set API key for current profile."""
        if self.profile not in self._config:
            self._config[self.profile] = {}
        self._config[self.profile]["api_key"] = api_key
        self._save()

    def set_api_url(self, api_url: str):
        """Set API URL for current profile."""
        if self.profile not in self._config:
            self._config[self.profile] = {}
        self._config[self.profile]["api_url"] = api_url
        self._save()

    def get_profiles(self) -> list:
        """Get list of configured profiles."""
        return list(self._config.keys())

    def is_configured(self) -> bool:
        """Check if CLI is configured with API key."""
        return self.api_key is not None


def get_config(profile: str = "default") -> Config:
    """Get configuration for profile."""
    return Config(profile)


def init_config(api_key: str, api_url: str = None, profile: str = "default"):
    """Initialize configuration with API key."""
    config = Config(profile)
    config.set_api_key(api_key)
    if api_url:
        config.set_api_url(api_url)
    return config
