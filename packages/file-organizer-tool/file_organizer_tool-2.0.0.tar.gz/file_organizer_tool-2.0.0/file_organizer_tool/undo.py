# file_organizer_tool/undo.py
"""Undo functionality for file organization operations."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import FileMove, OrganizationResult

logger = logging.getLogger(__name__)

LOG_FILENAME = '.file_organizer_log.json'


def save_organization_log(
    directory: Path, 
    result: OrganizationResult
) -> Optional[Path]:
    """
    Save organization results to a log file for undo capability.
    
    Args:
        directory: Directory where the log should be saved
        result: OrganizationResult from the organize operation
        
    Returns:
        Path to the log file, or None if failed
    """
    log_path = directory / LOG_FILENAME
    
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'total_files': result.total_files,
        'moved': result.moved,
        'moves': [
            {
                'source': str(move.source),
                'destination': str(move.destination),
                'category': move.category,
                'status': move.status,
            }
            for move in result.moves
            if move.status == 'moved'
        ]
    }
    
    try:
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)
        logger.info(f"Organization log saved to: {log_path}")
        return log_path
    except (OSError, IOError) as e:
        logger.error(f"Failed to save organization log: {e}")
        return None


def load_organization_log(directory: Path) -> Optional[dict]:
    """
    Load organization log from a directory.
    
    Args:
        directory: Directory containing the log file
        
    Returns:
        Log data dict or None if not found/invalid
    """
    log_path = directory / LOG_FILENAME
    
    if not log_path.exists():
        logger.error(f"No organization log found at: {log_path}")
        return None
    
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Failed to read organization log: {e}")
        return None


def undo_organization(
    directory: str | Path,
    dry_run: bool = False,
    remove_empty_folders: bool = True
) -> OrganizationResult:
    """
    Undo a previous organization operation.
    
    Args:
        directory: Directory containing the organization log
        dry_run: If True, only preview changes without moving files
        remove_empty_folders: If True, remove category folders if empty after undo
        
    Returns:
        OrganizationResult with details of undo operations
    """
    import shutil
    
    dir_path = Path(directory).resolve()
    result = OrganizationResult()
    
    log_data = load_organization_log(dir_path)
    if log_data is None:
        logger.error("Cannot undo: no valid organization log found")
        return result
    
    logger.info(f"Found organization log from: {log_data.get('timestamp', 'unknown')}")
    logger.info(f"Attempting to undo {len(log_data.get('moves', []))} file moves")
    
    if dry_run:
        logger.info("=== DRY RUN MODE - No files will be moved ===")
    
    folders_to_check: set[Path] = set()
    
    for move_data in log_data.get('moves', []):
        source = Path(move_data['source'])
        destination = Path(move_data['destination'])
        
        # Reverse the move: destination -> source
        move = FileMove(
            source=destination,
            destination=source,
            category=move_data['category'],
            status='moved'
        )
        
        if not destination.exists():
            logger.warning(f"File not found at destination: {destination}")
            move.status = 'skipped'
            move.error_message = 'File not found'
            result.add_move(move)
            continue
        
        folders_to_check.add(destination.parent)
        
        if dry_run:
            logger.info(f"[DRY RUN] Would restore: {destination.name} -> {source.parent}")
            result.add_move(move)
        else:
            try:
                # Ensure parent directory exists
                source.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(destination), str(source))
                logger.debug(f"Restored: {destination.name} -> {source}")
                result.add_move(move)
            except (shutil.Error, OSError) as e:
                move.status = 'error'
                move.error_message = str(e)
                logger.error(f"Error restoring {destination.name}: {e}")
                result.add_move(move)
    
    # Remove empty category folders
    if not dry_run and remove_empty_folders:
        for folder in folders_to_check:
            try:
                if folder.exists() and not any(folder.iterdir()):
                    folder.rmdir()
                    logger.debug(f"Removed empty folder: {folder.name}")
            except OSError:
                pass  # Folder not empty or other error
    
    # Remove the log file after successful undo
    if not dry_run and result.errors == 0:
        log_path = dir_path / LOG_FILENAME
        try:
            log_path.unlink()
            logger.info("Organization log removed")
        except OSError:
            pass
    
    logger.info(f"Undo complete: {result.moved} restored, {result.skipped} skipped, {result.errors} errors")
    return result
