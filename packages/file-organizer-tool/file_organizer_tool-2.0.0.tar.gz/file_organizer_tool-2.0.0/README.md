# File Organizer Tool

A powerful Python tool to organize files in directories based on their extensions. Features include dry-run preview, undo capability, recursive organization, and custom configuration.

## Installation

```bash
pip install file-organizer-tool
```

For YAML config support:
```bash
pip install file-organizer-tool[yaml]
```

For development:
```bash
pip install file-organizer-tool[dev]
```

## Quick Start

### Command Line

```bash
# Basic usage - organize current directory
file-organizer-tool .

# Preview changes without moving files
file-organizer-tool /path/to/folder --dry-run

# Organize with detailed output
file-organizer-tool /downloads --verbose

# Organize subdirectories recursively
file-organizer-tool /messy-folder --recursive

# Undo the last organization
file-organizer-tool /organized-folder --undo
```

### Python Script

```python
from file_organizer_tool import organize_files

# Basic organization
result = organize_files("/path/to/directory")
print(result.summary())

# With options
result = organize_files(
    "/downloads",
    dry_run=True,
    verbose=True,
    recursive=True,
    on_conflict='rename'  # or 'skip', 'overwrite'
)
```

## CLI Options

| Option | Short | Description |
|--------|-------|-------------|
| `--dry-run` | `-n` | Preview changes without moving files |
| `--verbose` | `-v` | Show detailed output for each file |
| `--recursive` | `-r` | Organize files in subdirectories |
| `--dest` | `-d` | Custom destination directory |
| `--config` | `-c` | Path to custom config file (JSON/YAML) |
| `--exclude` | `-e` | Glob patterns to exclude |
| `--on-conflict` | | Handle duplicates: skip, rename, overwrite |
| `--undo` | | Undo previous organization |
| `--log-file` | | Path to write log file |

## File Categories

Files are organized into these categories by default:

- **images**: jpg, png, gif, svg, webp, ico, etc.
- **documents**: pdf, docx, txt, xlsx, md, csv, etc.
- **scripts**: py, js, ts, sh, bat, go, rs, etc.
- **archives**: zip, tar, gz, rar, 7z, etc.
- **videos**: mp4, avi, mov, mkv, webm, etc.
- **audio**: mp3, wav, flac, aac, ogg, etc.
- **data**: json, xml, yaml, sql, db, etc.
- **fonts**: ttf, otf, woff, woff2, etc.
- **executables**: exe, msi, dmg, deb, apk, etc.
- **others**: unrecognized extensions

## Custom Configuration

Create a `config.json` or `config.yaml`:

```json
{
    "projects": [".sln", ".csproj", ".xcodeproj"],
    "ebooks": [".epub", ".mobi", ".azw3"]
}
```

Use it:
```bash
file-organizer-tool /folder --config config.json
```

## Development

```bash
# Clone and install
git clone https://github.com/albizzy/file_organizer
cd file_organizer
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=file_organizer_tool
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

Albert Mwasisoba ([@albizzy](https://github.com/albizzy))
