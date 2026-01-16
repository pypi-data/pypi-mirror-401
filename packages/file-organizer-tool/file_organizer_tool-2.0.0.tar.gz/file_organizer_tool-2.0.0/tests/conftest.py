# tests/conftest.py
"""Pytest fixtures for file organizer tests."""

import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_files(temp_dir):
    """Create sample files of different types for testing."""
    files = {
        'photo.jpg': 'images',
        'document.pdf': 'documents',
        'script.py': 'scripts',
        'archive.zip': 'archives',
        'movie.mp4': 'videos',
        'song.mp3': 'audio',
        'data.json': 'data',
        'unknown.xyz': 'others',
    }
    
    created_files = []
    for filename in files.keys():
        file_path = temp_dir / filename
        file_path.write_text(f"Test content for {filename}")
        created_files.append(file_path)
    
    return temp_dir, files, created_files


@pytest.fixture
def nested_files(temp_dir):
    """Create nested directory structure for recursive testing."""
    # Create subdirectories
    subdir1 = temp_dir / "subdir1"
    subdir2 = temp_dir / "subdir2"
    subdir1.mkdir()
    subdir2.mkdir()
    
    # Root files
    (temp_dir / "root.txt").write_text("root file")
    
    # Subdirectory files
    (subdir1 / "nested1.jpg").write_text("nested image")
    (subdir2 / "nested2.pdf").write_text("nested document")
    
    return temp_dir
