"""
Configuration management for Research Trends.

Handles API keys, settings, and user preferences from multiple sources:
- Environment variables
- .env files
- YAML configuration files
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml
from dotenv import load_dotenv


class Config:
    """Configuration manager for Research Trends.
    
    Loads configuration from multiple sources with the following precedence:
    1. Environment variables (highest)
    2. .env file in current directory
    3. Configuration file (~/.research_trends/config.yaml)
    4. Default values (lowest)
    
    Attributes:
        api_key: Scopus API key for authentication
        institution_token: Optional institutional token for extended access
        cache_dir: Directory for caching API responses
        cache_ttl: Cache time-to-live in seconds
        rate_limit: Maximum API requests per second
        default_max_results: Default maximum results per query
    """
    
    DEFAULT_CONFIG_DIR = Path.home() / ".research_trends"
    DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.yaml"
    DEFAULT_CACHE_DIR = DEFAULT_CONFIG_DIR / "cache"
    
    # Default configuration values
    DEFAULTS: Dict[str, Any] = {
        "api_key": None,
        "institution_token": None,
        "cache_dir": str(DEFAULT_CACHE_DIR),
        "cache_ttl": 86400,  # 24 hours
        "rate_limit": 9,  # Scopus limit is 9 requests/second
        "default_max_results": 500,
        "base_url": "https://api.elsevier.com/content/search/scopus",
        "abstract_url": "https://api.elsevier.com/content/abstract/scopus_id",
    }
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        config_file: Optional[Path] = None,
        load_env: bool = True,
    ) -> None:
        """Initialize configuration.
        
        Args:
            api_key: Scopus API key. If not provided, will be loaded from
                environment or config file.
            config_file: Path to YAML configuration file.
            load_env: Whether to load environment variables from .env file.
        """
        self._config: Dict[str, Any] = self.DEFAULTS.copy()
        
        # Load from config file
        config_path = config_file or self.DEFAULT_CONFIG_FILE
        if config_path.exists():
            self._load_config_file(config_path)
        
        # Load from environment
        if load_env:
            load_dotenv()
            self._load_environment()
        
        # Override with explicit API key
        if api_key:
            self._config["api_key"] = api_key
        
        # Ensure cache directory exists
        cache_dir = Path(self._config["cache_dir"])
        cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_config_file(self, path: Path) -> None:
        """Load configuration from YAML file.
        
        Args:
            path: Path to the YAML configuration file.
        """
        try:
            with open(path, "r") as f:
                file_config = yaml.safe_load(f)
            
            if file_config and isinstance(file_config, dict):
                # Handle nested scopus configuration
                if "scopus" in file_config:
                    scopus_config = file_config["scopus"]
                    if "api_key" in scopus_config:
                        self._config["api_key"] = scopus_config["api_key"]
                    if "institution_token" in scopus_config:
                        self._config["institution_token"] = scopus_config["institution_token"]
                
                # Handle top-level settings
                for key in ["cache_dir", "cache_ttl", "rate_limit", "default_max_results"]:
                    if key in file_config:
                        self._config[key] = file_config[key]
        except (yaml.YAMLError, IOError) as e:
            print(f"Warning: Could not load config file {path}: {e}")
    
    def _load_environment(self) -> None:
        """Load configuration from environment variables."""
        env_mapping = {
            "SCOPUS_API_KEY": "api_key",
            "SCOPUS_INSTITUTION_TOKEN": "institution_token",
            "RESEARCH_TRENDS_CACHE_DIR": "cache_dir",
            "RESEARCH_TRENDS_CACHE_TTL": "cache_ttl",
            "RESEARCH_TRENDS_RATE_LIMIT": "rate_limit",
        }
        
        for env_var, config_key in env_mapping.items():
            value = os.getenv(env_var)
            if value:
                # Convert numeric values
                if config_key in ["cache_ttl", "rate_limit"]:
                    value = int(value)
                self._config[config_key] = value
    
    @property
    def api_key(self) -> Optional[str]:
        """Get the Scopus API key."""
        return self._config.get("api_key")
    
    @property
    def institution_token(self) -> Optional[str]:
        """Get the institutional token."""
        return self._config.get("institution_token")
    
    @property
    def cache_dir(self) -> Path:
        """Get the cache directory path."""
        return Path(self._config["cache_dir"])
    
    @property
    def cache_ttl(self) -> int:
        """Get the cache time-to-live in seconds."""
        return self._config["cache_ttl"]
    
    @property
    def rate_limit(self) -> int:
        """Get the API rate limit."""
        return self._config["rate_limit"]
    
    @property
    def default_max_results(self) -> int:
        """Get the default maximum results."""
        return self._config["default_max_results"]
    
    @property
    def base_url(self) -> str:
        """Get the Scopus API base URL."""
        return self._config["base_url"]
    
    @property
    def abstract_url(self) -> str:
        """Get the Scopus abstract retrieval URL."""
        return self._config["abstract_url"]
    
    def validate(self) -> bool:
        """Validate the configuration.
        
        Returns:
            True if configuration is valid.
            
        Raises:
            ValueError: If required configuration is missing.
        """
        if not self.api_key:
            raise ValueError(
                "Scopus API key is required. Set SCOPUS_API_KEY environment "
                "variable or provide it in the configuration file."
            )
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Export configuration as dictionary.
        
        Returns:
            Dictionary containing all configuration values.
        """
        return self._config.copy()
    
    @classmethod
    def create_default_config(cls) -> Path:
        """Create a default configuration file.
        
        Returns:
            Path to the created configuration file.
        """
        cls.DEFAULT_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        default_config = {
            "scopus": {
                "api_key": "YOUR_API_KEY_HERE",
                "institution_token": None,
            },
            "cache_dir": str(cls.DEFAULT_CACHE_DIR),
            "cache_ttl": 86400,
            "rate_limit": 9,
            "default_max_results": 500,
        }
        
        with open(cls.DEFAULT_CONFIG_FILE, "w") as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        return cls.DEFAULT_CONFIG_FILE
