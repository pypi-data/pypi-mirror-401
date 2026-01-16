# tests/test_config.py
"""Tests for the configuration module."""

import json
import pytest
from pathlib import Path

from file_organizer_tool.config import (
    DEFAULT_FILE_TYPES,
    load_config,
    get_category_for_extension,
)


class TestDefaultConfig:
    """Tests for default configuration."""
    
    def test_default_has_all_categories(self):
        """Test default config has expected categories."""
        expected_categories = [
            'images', 'documents', 'scripts', 'archives', 
            'videos', 'audio', 'data', 'fonts', 'executables'
        ]
        
        for category in expected_categories:
            assert category in DEFAULT_FILE_TYPES
    
    def test_extensions_have_dots(self):
        """Test all extensions start with a dot."""
        for category, extensions in DEFAULT_FILE_TYPES.items():
            for ext in extensions:
                assert ext.startswith('.'), f"{ext} in {category} missing dot"


class TestLoadConfig:
    """Tests for config loading."""
    
    def test_load_none_returns_default(self):
        """Test None path returns default config."""
        config = load_config(None)
        assert config == DEFAULT_FILE_TYPES
    
    def test_load_missing_file_returns_default(self, temp_dir):
        """Test missing file returns default with warning."""
        config = load_config(temp_dir / "nonexistent.json")
        assert config == DEFAULT_FILE_TYPES
    
    def test_load_json_config(self, temp_dir):
        """Test loading custom JSON config."""
        config_path = temp_dir / "custom.json"
        custom_config = {
            "custom_category": [".custom", ".test"]
        }
        
        with open(config_path, 'w') as f:
            json.dump(custom_config, f)
        
        config = load_config(config_path)
        
        # Should have custom category merged with defaults
        assert "custom_category" in config
        assert "images" in config  # Default still present
    
    def test_load_invalid_json(self, temp_dir):
        """Test invalid JSON returns default."""
        config_path = temp_dir / "invalid.json"
        config_path.write_text("{ not valid json }")
        
        config = load_config(config_path)
        assert config == DEFAULT_FILE_TYPES


class TestGetCategoryForExtension:
    """Tests for extension to category lookup."""
    
    def test_known_extension(self):
        """Test looking up known extension."""
        category = get_category_for_extension('.jpg', DEFAULT_FILE_TYPES)
        assert category == 'images'
    
    def test_unknown_extension(self):
        """Test unknown extension returns None."""
        category = get_category_for_extension('.xyz123', DEFAULT_FILE_TYPES)
        assert category is None
    
    def test_case_insensitive(self):
        """Test extension lookup is case insensitive."""
        category = get_category_for_extension('.JPG', DEFAULT_FILE_TYPES)
        assert category == 'images'
    
    def test_without_dot(self):
        """Test extension without leading dot."""
        category = get_category_for_extension('png', DEFAULT_FILE_TYPES)
        assert category == 'images'
