# file_organizer_tool/organizer.py
"""Main file organizer module with enhanced functionality."""

import argparse
import fnmatch
import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Optional

from .config import DEFAULT_FILE_TYPES, DEFAULT_EXCLUDES, load_config, get_category_for_extension
from .models import FileMove, OrganizationResult
from .undo import save_organization_log, undo_organization

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False, log_file: Optional[Path] = None) -> None:
    """Configure logging based on user preferences."""
    level = logging.DEBUG if verbose else logging.INFO
    
    # Update root logger level
    logging.getLogger().setLevel(level)
    
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        logging.getLogger().addHandler(file_handler)


def should_exclude(filename: str, exclude_patterns: list[str]) -> bool:
    """Check if a file should be excluded based on patterns."""
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(filename.lower(), pattern.lower()):
            return True
    return False


def validate_directory(path: Path) -> None:
    """Validate that the path exists and is a directory."""
    if not path.exists():
        raise FileNotFoundError(f"Directory does not exist: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")
    if not os.access(path, os.R_OK | os.W_OK):
        raise PermissionError(f"Insufficient permissions for directory: {path}")


def scan_directory(
    src_dir: Path, 
    file_types: dict[str, list[str]],
    exclude_patterns: list[str],
    recursive: bool = False
) -> tuple[dict[str, bool], list[Path]]:
    """
    Scan directory and identify which file types are present.
    
    Args:
        src_dir: Source directory to scan
        file_types: Dictionary mapping categories to extensions
        exclude_patterns: Patterns for files to exclude
        recursive: Whether to scan subdirectories
        
    Returns:
        Tuple of (available types dict, list of files to process)
    """
    available_types: dict[str, bool] = {key: False for key in file_types.keys()}
    files_to_process: list[Path] = []
    
    if recursive:
        iterator = src_dir.rglob('*')
    else:
        iterator = src_dir.iterdir()
    
    for item in iterator:
        if not item.is_file():
            continue
            
        # Skip files in category folders we created
        if not recursive and item.parent != src_dir:
            continue
            
        if should_exclude(item.name, exclude_patterns):
            logger.debug(f"Excluding: {item.name}")
            continue
            
        files_to_process.append(item)
        
        ext = item.suffix.lower()
        for folder, exts in file_types.items():
            if ext in exts:
                available_types[folder] = True
                break
    
    return available_types, files_to_process


def handle_duplicate(
    source: Path, 
    dest_dir: Path, 
    on_conflict: str
) -> tuple[Path, str]:
    """
    Handle duplicate file names at destination.
    
    Args:
        source: Source file path
        dest_dir: Destination directory
        on_conflict: Strategy - 'skip', 'rename', or 'overwrite'
        
    Returns:
        Tuple of (final destination path, status)
    """
    dest_path = dest_dir / source.name
    
    if not dest_path.exists():
        return dest_path, 'moved'
    
    if on_conflict == 'skip':
        return dest_path, 'skipped'
    elif on_conflict == 'overwrite':
        return dest_path, 'moved'
    elif on_conflict == 'rename':
        counter = 1
        stem = source.stem
        suffix = source.suffix
        while dest_path.exists():
            new_name = f"{stem}_{counter}{suffix}"
            dest_path = dest_dir / new_name
            counter += 1
        return dest_path, 'moved'
    
    return dest_path, 'skipped'


def organize_files(
    src_dir: str | Path,
    dest_dir: Optional[str | Path] = None,
    dry_run: bool = False,
    verbose: bool = False,
    recursive: bool = False,
    config_path: Optional[Path] = None,
    exclude_patterns: Optional[list[str]] = None,
    on_conflict: str = 'rename'
) -> OrganizationResult:
    """
    Organize files in a directory by their extensions.
    
    Args:
        src_dir: Source directory to organize
        dest_dir: Destination directory (defaults to src_dir)
        dry_run: If True, only preview changes without moving files
        verbose: If True, show detailed output
        recursive: If True, process subdirectories
        config_path: Path to custom config file
        exclude_patterns: Additional patterns to exclude
        on_conflict: How to handle duplicates - 'skip', 'rename', 'overwrite'
        
    Returns:
        OrganizationResult with details of all operations
    """
    src_path = Path(src_dir).resolve()
    dest_path = Path(dest_dir).resolve() if dest_dir else src_path
    
    # Validate directories
    validate_directory(src_path)
    if dest_dir and not dest_path.exists():
        if not dry_run:
            dest_path.mkdir(parents=True, exist_ok=True)
    
    # Setup logging
    setup_logging(verbose)
    
    # Load configuration
    file_types = load_config(config_path)
    
    # Combine exclude patterns
    all_excludes = DEFAULT_EXCLUDES.copy()
    if exclude_patterns:
        all_excludes.extend(exclude_patterns)
    
    result = OrganizationResult()
    
    if dry_run:
        logger.info("=== DRY RUN MODE - No files will be moved ===")
    
    # Scan directory
    available_types, files_to_process = scan_directory(
        src_path, file_types, all_excludes, recursive
    )
    
    logger.info(f"Found {len(files_to_process)} files to process")
    
    # Create only necessary folders (unless dry run)
    if not dry_run:
        for folder, needed in available_types.items():
            if needed:
                folder_path = dest_path / folder
                folder_path.mkdir(exist_ok=True)
    
    # Process files
    for file_path in files_to_process:
        category = get_category_for_extension(file_path.suffix, file_types)
        
        if category is None:
            category = 'others'
            if not dry_run:
                (dest_path / 'others').mkdir(exist_ok=True)
        
        target_dir = dest_path / category
        final_dest, status = handle_duplicate(file_path, target_dir, on_conflict)
        
        move = FileMove(
            source=file_path,
            destination=final_dest,
            category=category,
            status=status
        )
        
        if status == 'skipped':
            logger.debug(f"Skipping (duplicate): {file_path.name}")
            result.add_move(move)
            continue
        
        if dry_run:
            logger.info(f"[DRY RUN] Would move: {file_path.name} -> {category}/")
            move.status = 'moved'  # Mark as would-be-moved for reporting
            result.add_move(move)
        else:
            try:
                shutil.move(str(file_path), str(final_dest))
                logger.debug(f"Moved: {file_path.name} -> {category}/")
                result.add_move(move)
            except (shutil.Error, OSError) as e:
                move.status = 'error'
                move.error_message = str(e)
                logger.error(f"Error moving {file_path.name}: {e}")
                result.add_move(move)
    
    # Save undo log if not dry run and files were moved
    if not dry_run and result.moved > 0:
        save_organization_log(dest_path, result)
    
    logger.info(result.summary())
    return result


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='Organize files in a directory based on their extensions.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  file-organizer-tool /path/to/messy/folder
  file-organizer-tool . --dry-run --verbose
  file-organizer-tool /downloads -r --exclude "*.part" --exclude "*.crdownload"
  file-organizer-tool /source --dest /organized --on-conflict skip
        """
    )
    
    parser.add_argument(
        'src_dir', 
        type=str, 
        help='The source directory to organize'
    )
    parser.add_argument(
        '--dest', '-d',
        type=str,
        default=None,
        help='Destination directory (default: same as source)'
    )
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Preview changes without moving files'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output for each file'
    )
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Organize files in subdirectories recursively'
    )
    parser.add_argument(
        '--config', '-c',
        type=str,
        default=None,
        help='Path to custom config file (JSON or YAML)'
    )
    parser.add_argument(
        '--exclude', '-e',
        action='append',
        default=[],
        help='Glob patterns to exclude (can be used multiple times)'
    )
    parser.add_argument(
        '--on-conflict',
        choices=['skip', 'rename', 'overwrite'],
        default='rename',
        help='How to handle duplicate filenames (default: rename)'
    )
    parser.add_argument(
        '--log-file',
        type=str,
        default=None,
        help='Path to write log file'
    )
    parser.add_argument(
        '--undo',
        action='store_true',
        help='Undo a previous organization operation'
    )
    
    args = parser.parse_args()
    
    try:
        # Handle undo operation
        if args.undo:
            setup_logging(args.verbose)
            result = undo_organization(
                directory=args.src_dir,
                dry_run=args.dry_run
            )
            return 1 if result.errors > 0 else 0
        
        result = organize_files(
            src_dir=args.src_dir,
            dest_dir=args.dest,
            dry_run=args.dry_run,
            verbose=args.verbose,
            recursive=args.recursive,
            config_path=Path(args.config) if args.config else None,
            exclude_patterns=args.exclude,
            on_conflict=args.on_conflict
        )
        
        if result.errors > 0:
            return 1
        return 0
        
    except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
        logger.error(str(e))
        return 1
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 130


if __name__ == "__main__":
    sys.exit(main())