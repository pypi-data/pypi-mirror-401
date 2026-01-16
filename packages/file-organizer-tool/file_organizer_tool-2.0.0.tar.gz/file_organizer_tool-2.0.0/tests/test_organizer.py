# tests/test_organizer.py
"""Tests for the main organizer module."""

import pytest
from pathlib import Path

from file_organizer_tool import organize_files, scan_directory
from file_organizer_tool.config import DEFAULT_FILE_TYPES, DEFAULT_EXCLUDES


class TestScanDirectory:
    """Tests for scan_directory function."""
    
    def test_scan_empty_directory(self, temp_dir):
        """Test scanning an empty directory."""
        available, files = scan_directory(
            temp_dir, DEFAULT_FILE_TYPES, DEFAULT_EXCLUDES
        )
        
        assert len(files) == 0
        assert all(v is False for v in available.values())
    
    def test_scan_with_files(self, sample_files):
        """Test scanning directory with various file types."""
        temp_dir, expected, _ = sample_files
        
        available, files = scan_directory(
            temp_dir, DEFAULT_FILE_TYPES, DEFAULT_EXCLUDES
        )
        
        assert len(files) == len(expected)
        assert available['images'] is True
        assert available['documents'] is True
        assert available['scripts'] is True
    
    def test_scan_excludes_patterns(self, temp_dir):
        """Test that exclude patterns work."""
        # Create a file that should be excluded
        (temp_dir / "Thumbs.db").write_text("system file")
        (temp_dir / "normal.txt").write_text("normal file")
        
        _, files = scan_directory(
            temp_dir, DEFAULT_FILE_TYPES, DEFAULT_EXCLUDES
        )
        
        filenames = [f.name for f in files]
        assert "Thumbs.db" not in filenames
        assert "normal.txt" in filenames


class TestOrganizeFiles:
    """Tests for organize_files function."""
    
    def test_organize_creates_folders(self, sample_files):
        """Test that organizing creates correct category folders."""
        temp_dir, expected, _ = sample_files
        
        result = organize_files(temp_dir)
        
        # Check folders were created
        assert (temp_dir / "images").is_dir()
        assert (temp_dir / "documents").is_dir()
        assert (temp_dir / "scripts").is_dir()
        assert (temp_dir / "others").is_dir()
    
    def test_organize_moves_files(self, sample_files):
        """Test that files are moved to correct folders."""
        temp_dir, expected, _ = sample_files
        
        result = organize_files(temp_dir)
        
        # Check files are in correct locations
        assert (temp_dir / "images" / "photo.jpg").exists()
        assert (temp_dir / "documents" / "document.pdf").exists()
        assert (temp_dir / "scripts" / "script.py").exists()
        assert (temp_dir / "others" / "unknown.xyz").exists()
    
    def test_organize_result_counts(self, sample_files):
        """Test that result counts are accurate."""
        temp_dir, expected, _ = sample_files
        
        result = organize_files(temp_dir)
        
        assert result.total_files == len(expected)
        assert result.moved == len(expected)
        assert result.errors == 0
    
    def test_dry_run_no_changes(self, sample_files):
        """Test dry run doesn't move files."""
        temp_dir, expected, created_files = sample_files
        
        result = organize_files(temp_dir, dry_run=True)
        
        # Original files should still exist
        for file_path in created_files:
            assert file_path.exists()
        
        # Category folders should not be created
        assert not (temp_dir / "images").exists()
    
    def test_duplicate_rename(self, temp_dir):
        """Test duplicate files are renamed."""
        # Create images folder with existing file
        images_dir = temp_dir / "images"
        images_dir.mkdir()
        (images_dir / "photo.jpg").write_text("existing")
        
        # Create new file with same name
        (temp_dir / "photo.jpg").write_text("new file")
        
        result = organize_files(temp_dir, on_conflict='rename')
        
        # Both files should exist
        assert (images_dir / "photo.jpg").exists()
        assert (images_dir / "photo_1.jpg").exists()
    
    def test_duplicate_skip(self, temp_dir):
        """Test duplicate files are skipped."""
        # Create images folder with existing file
        images_dir = temp_dir / "images"
        images_dir.mkdir()
        (images_dir / "photo.jpg").write_text("existing")
        
        # Create new file with same name
        (temp_dir / "photo.jpg").write_text("new file")
        
        result = organize_files(temp_dir, on_conflict='skip')
        
        assert result.skipped == 1
        # Original still in root
        assert (temp_dir / "photo.jpg").exists()
    
    def test_invalid_directory(self):
        """Test error handling for invalid directory."""
        with pytest.raises(FileNotFoundError):
            organize_files("/nonexistent/path")
    
    def test_custom_destination(self, sample_files, temp_dir):
        """Test organizing to a different destination."""
        src_dir, _, _ = sample_files
        dest_dir = temp_dir / "organized"
        
        result = organize_files(src_dir, dest_dir=dest_dir)
        
        assert dest_dir.exists()
        assert (dest_dir / "images" / "photo.jpg").exists()


class TestRecursiveOrganize:
    """Tests for recursive organization."""
    
    def test_recursive_finds_nested_files(self, nested_files):
        """Test recursive mode processes subdirectory files."""
        result = organize_files(nested_files, recursive=True)
        
        # Should find 3 files total
        assert result.total_files == 3
