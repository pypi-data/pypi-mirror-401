# file_organizer_tool/__init__.py
"""File Organizer Tool - Organize files by extension."""

from .organizer import organize_files, scan_directory
from .config import DEFAULT_FILE_TYPES, DEFAULT_EXCLUDES, load_config, get_category_for_extension
from .models import FileMove, OrganizationResult

__version__ = "2.0.0"
__all__ = [
    "organize_files",
    "scan_directory", 
    "DEFAULT_FILE_TYPES",
    "DEFAULT_EXCLUDES",
    "load_config",
    "get_category_for_extension",
    "FileMove",
    "OrganizationResult",
    "__version__",
]