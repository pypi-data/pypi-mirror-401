"""
Tests for the Configuration module.
"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch, mock_open
import tempfile
import yaml

from research_trends.config import Config


class TestConfig:
    """Tests for the Config class."""
    
    def test_defaults(self):
        """Test default configuration values."""
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(Path, 'exists', return_value=False):
                config = Config()
        
        assert config.rate_limit == 9
        assert config.cache_ttl == 86400
        assert config.default_max_results == 500
    
    def test_env_api_key(self):
        """Test loading API key from environment."""
        with patch.dict(os.environ, {"SCOPUS_API_KEY": "test_key_123"}, clear=True):
            with patch.object(Path, 'exists', return_value=False):
                config = Config()
        
        assert config.api_key == "test_key_123"
    
    def test_explicit_api_key(self):
        """Test explicit API key override."""
        with patch.dict(os.environ, {"SCOPUS_API_KEY": "env_key"}, clear=True):
            with patch.object(Path, 'exists', return_value=False):
                config = Config(api_key="explicit_key")
        
        assert config.api_key == "explicit_key"
    
    def test_validate_missing_key(self):
        """Test validation fails without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(Path, 'exists', return_value=False):
                config = Config()
        
        with pytest.raises(ValueError) as exc_info:
            config.validate()
        
        assert "API key is required" in str(exc_info.value)
    
    def test_validate_with_key(self):
        """Test validation passes with API key."""
        with patch.object(Path, 'exists', return_value=False):
            config = Config(api_key="test_key")
        
        assert config.validate() is True
    
    def test_to_dict(self):
        """Test configuration export to dict."""
        with patch.object(Path, 'exists', return_value=False):
            config = Config(api_key="test_key")
        
        config_dict = config.to_dict()
        
        assert "api_key" in config_dict
        assert "rate_limit" in config_dict
        assert "cache_ttl" in config_dict
    
    def test_load_yaml_config(self):
        """Test loading configuration from YAML file."""
        yaml_content = """
scopus:
  api_key: yaml_api_key
  institution_token: yaml_token
cache_ttl: 3600
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_path = Path(f.name)
        
        try:
            config = Config(config_file=temp_path)
            assert config.api_key == "yaml_api_key"
            assert config.institution_token == "yaml_token"
            assert config.cache_ttl == 3600
        finally:
            temp_path.unlink()
    
    def test_env_overrides_yaml(self):
        """Test that environment variables override YAML config."""
        yaml_content = """
scopus:
  api_key: yaml_key
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_path = Path(f.name)
        
        try:
            with patch.dict(os.environ, {"SCOPUS_API_KEY": "env_key"}):
                config = Config(config_file=temp_path)
            assert config.api_key == "env_key"
        finally:
            temp_path.unlink()
    
    def test_create_default_config(self):
        """Test creating default configuration file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(Config, 'DEFAULT_CONFIG_DIR', Path(tmpdir)):
                with patch.object(Config, 'DEFAULT_CONFIG_FILE', Path(tmpdir) / 'config.yaml'):
                    config_path = Config.create_default_config()
                    
                    assert config_path.exists()
                    
                    with open(config_path) as f:
                        content = yaml.safe_load(f)
                    
                    assert 'scopus' in content
                    assert 'api_key' in content['scopus']
    
    def test_properties(self):
        """Test configuration properties."""
        with patch.object(Path, 'exists', return_value=False):
            config = Config(api_key="test")
        
        assert isinstance(config.cache_dir, Path)
        assert isinstance(config.cache_ttl, int)
        assert isinstance(config.rate_limit, int)
        assert config.base_url.startswith("https://")
