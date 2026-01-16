# tests/test_undo.py
"""Tests for the undo functionality."""

import json
import pytest
from pathlib import Path

from file_organizer_tool import organize_files
from file_organizer_tool.undo import (
    save_organization_log,
    load_organization_log,
    undo_organization,
    LOG_FILENAME,
)


class TestOrganizationLog:
    """Tests for log save/load functionality."""
    
    def test_log_created_after_organize(self, sample_files):
        """Test that organizing creates an undo log."""
        temp_dir, _, _ = sample_files
        
        organize_files(temp_dir)
        
        log_path = temp_dir / LOG_FILENAME
        assert log_path.exists()
    
    def test_log_contains_moves(self, sample_files):
        """Test log file contains move information."""
        temp_dir, expected, _ = sample_files
        
        organize_files(temp_dir)
        
        log_data = load_organization_log(temp_dir)
        
        assert log_data is not None
        assert 'timestamp' in log_data
        assert 'moves' in log_data
        assert len(log_data['moves']) == len(expected)
    
    def test_load_missing_log(self, temp_dir):
        """Test loading from directory without log returns None."""
        result = load_organization_log(temp_dir)
        assert result is None


class TestUndoOrganization:
    """Tests for undo functionality."""
    
    def test_undo_restores_files(self, sample_files):
        """Test undo moves files back to original location."""
        temp_dir, expected, original_files = sample_files
        
        # Organize files
        organize_files(temp_dir)
        
        # Verify files were moved
        assert not (temp_dir / "photo.jpg").exists()
        assert (temp_dir / "images" / "photo.jpg").exists()
        
        # Undo
        result = undo_organization(temp_dir)
        
        # Files should be back
        assert (temp_dir / "photo.jpg").exists()
        assert result.moved > 0
    
    def test_undo_removes_empty_folders(self, sample_files):
        """Test undo removes empty category folders."""
        temp_dir, _, _ = sample_files
        
        organize_files(temp_dir)
        undo_organization(temp_dir)
        
        # Category folders should be removed if empty
        # (some might remain if they contained subfolders)
        images_dir = temp_dir / "images"
        if images_dir.exists():
            assert any(images_dir.iterdir())  # Not empty
    
    def test_undo_dry_run(self, sample_files):
        """Test undo dry run doesn't move files."""
        temp_dir, _, _ = sample_files
        
        organize_files(temp_dir)
        
        # Dry run undo
        result = undo_organization(temp_dir, dry_run=True)
        
        # Files should still be in organized locations
        assert (temp_dir / "images" / "photo.jpg").exists()
        assert not (temp_dir / "photo.jpg").exists()
    
    def test_undo_without_log(self, temp_dir):
        """Test undo on directory without log."""
        result = undo_organization(temp_dir)
        
        assert result.total_files == 0
    
    def test_undo_removes_log_file(self, sample_files):
        """Test successful undo removes the log file."""
        temp_dir, _, _ = sample_files
        
        organize_files(temp_dir)
        log_path = temp_dir / LOG_FILENAME
        assert log_path.exists()
        
        undo_organization(temp_dir)
        assert not log_path.exists()
