# file_organizer_tool/config.py
"""Configuration management for file organizer."""

import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Extended default file type mappings
DEFAULT_FILE_TYPES: dict[str, list[str]] = {
    'images': [
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', 
        '.ico', '.tiff', '.tif', '.raw', '.heic', '.heif'
    ],
    'documents': [
        '.pdf', '.docx', '.doc', '.txt', '.xlsx', '.xls', '.pptx', '.ppt',
        '.odt', '.ods', '.odp', '.csv', '.md', '.rtf', '.epub', '.mobi'
    ],
    'scripts': [
        '.py', '.js', '.ts', '.jsx', '.tsx', '.sh', '.bat', '.ps1',
        '.rb', '.go', '.rs', '.java', '.c', '.cpp', '.h', '.hpp',
        '.cs', '.php', '.swift', '.kt', '.scala', '.r', '.m'
    ],
    'archives': [
        '.zip', '.tar', '.gz', '.rar', '.7z', '.bz2', '.xz', '.tgz'
    ],
    'videos': [
        '.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', 
        '.m4v', '.mpeg', '.mpg', '.3gp'
    ],
    'audio': [
        '.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma', 
        '.aiff', '.alac', '.opus'
    ],
    'data': [
        '.json', '.xml', '.yaml', '.yml', '.sql', '.db', '.sqlite',
        '.parquet', '.feather', '.pickle', '.pkl'
    ],
    'fonts': [
        '.ttf', '.otf', '.woff', '.woff2', '.eot', '.fon'
    ],
    'executables': [
        '.exe', '.msi', '.dmg', '.app', '.deb', '.rpm', '.apk'
    ],
}

# Default patterns to exclude
DEFAULT_EXCLUDES: list[str] = [
    'desktop.ini',
    'Thumbs.db',
    '.DS_Store',
    '*.tmp',
    '*.temp',
    '.file_organizer_log.json',
]


def load_config(config_path: Optional[Path] = None) -> dict[str, list[str]]:
    """
    Load file type configuration from a JSON or YAML file.
    
    Args:
        config_path: Path to the config file. If None, returns default.
        
    Returns:
        Dictionary mapping category names to lists of extensions.
    """
    if config_path is None:
        return DEFAULT_FILE_TYPES.copy()
    
    config_path = Path(config_path)
    
    if not config_path.exists():
        logger.warning(f"Config file not found: {config_path}. Using defaults.")
        return DEFAULT_FILE_TYPES.copy()
    
    try:
        suffix = config_path.suffix.lower()
        
        if suffix == '.json':
            with open(config_path, 'r', encoding='utf-8') as f:
                custom_config = json.load(f)
        elif suffix in ('.yaml', '.yml'):
            try:
                import yaml
                with open(config_path, 'r', encoding='utf-8') as f:
                    custom_config = yaml.safe_load(f)
            except ImportError:
                logger.error("PyYAML not installed. Install with: pip install pyyaml")
                return DEFAULT_FILE_TYPES.copy()
        else:
            logger.warning(f"Unsupported config format: {suffix}. Using defaults.")
            return DEFAULT_FILE_TYPES.copy()
        
        # Merge with defaults (custom overrides defaults)
        merged = DEFAULT_FILE_TYPES.copy()
        merged.update(custom_config)
        
        logger.info(f"Loaded custom config from: {config_path}")
        return merged
        
    except (json.JSONDecodeError, Exception) as e:
        logger.error(f"Error loading config: {e}. Using defaults.")
        return DEFAULT_FILE_TYPES.copy()


def get_category_for_extension(ext: str, file_types: dict[str, list[str]]) -> Optional[str]:
    """
    Get the category name for a given file extension.
    
    Args:
        ext: File extension (with or without leading dot)
        file_types: Dictionary mapping categories to extensions
        
    Returns:
        Category name or None if not found
    """
    if not ext.startswith('.'):
        ext = '.' + ext
    ext = ext.lower()
    
    for category, extensions in file_types.items():
        if ext in extensions:
            return category
    return None
