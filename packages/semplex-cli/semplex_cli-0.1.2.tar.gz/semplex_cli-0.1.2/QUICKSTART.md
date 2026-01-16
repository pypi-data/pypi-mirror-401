# Semplex CLI - Quick Start Guide

## Installation

### Using uv (recommended)

```bash
# Navigate to the cli directory
cd cli

# Install with uv
uv pip install -e .

# Or install in a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Using pip

```bash
cd cli
pip install -e .
```

## Quick Start

### 1. Initialize Configuration

Run the interactive configuration wizard:

```bash
semplex config init
```

Or use the alias:

```bash
semplex init
```

You'll be prompted to:
- Add directories to watch
- Specify file types (.xlsx, .csv, .tsv)
- Configure recursive watching
- Set the backend API URL
- Enable/disable debug mode

### 2. Start Watching

Start the file watcher in the background:

```bash
semplex start
```

Or run in foreground (useful for debugging):

```bash
semplex start --foreground
```

### 3. Check Status

Check if the watcher is running:

```bash
semplex status
```

### 4. Stop Watching

Stop the file watcher:

```bash
semplex stop
```

## Debug Mode

Debug mode writes all API requests to a file instead of sending them to the backend. This is useful for:
- Testing the CLI without a backend
- Debugging metadata extraction
- Verifying what data will be sent

Enable debug mode during configuration:

```bash
semplex config init
# Select "Yes" for debug mode
# Specify output file (default: ~/.config/semplex/debug_output.jsonl)
```

Or set it manually:

```bash
semplex config set api.debug_mode true
semplex config set api.debug_output_file /path/to/debug.jsonl
```

## Configuration

### View Current Configuration

```bash
semplex config show
```

### Set Individual Values

```bash
# Set API URL
semplex config set api.url http://api.example.com/metadata

# Add watch directories (comma-separated)
semplex config set watch.directories /path/to/dir1,/path/to/dir2

# Set file types
semplex config set watch.file_types .xlsx,.csv,.tsv

# Enable/disable recursive watching
semplex config set watch.recursive true
```

### Reset Configuration

```bash
semplex config reset
```

## Configuration File Location

Configuration is stored at:
- **Linux/macOS**: `~/.config/semplex/config.yaml`
- **Windows**: `%USERPROFILE%\.config\semplex\config.yaml`

## Example Workflow

### Testing with Debug Mode

```bash
# 1. Initialize with debug mode
semplex init

# Follow prompts:
# - Add directory: /path/to/data
# - File types: .xlsx,.csv
# - Recursive: Yes
# - API URL: (any value, won't be used)
# - Debug mode: Yes
# - Debug file: /tmp/semplex_debug.jsonl

# 2. Start watcher
semplex start

# 3. Make changes to files in /path/to/data
# Headers will be written to /tmp/semplex_debug.jsonl

# 4. Check the debug output
cat /tmp/semplex_debug.jsonl

# 5. Stop watcher
semplex stop
```

### Production Use

```bash
# 1. Configure with real API
semplex init
# - Add directories to watch
# - Set API URL: https://api.semplex.com/metadata
# - Debug mode: No

# 2. Start watcher in background
semplex start

# 3. Check status
semplex status

# 4. Watcher runs continuously, monitoring files

# 5. Stop when needed
semplex stop
```

## What Gets Extracted?

The CLI extracts the following metadata from files:

### Excel Files (.xlsx, .xls, .xlsm)
- Filename and path
- File size
- Last modified timestamp
- Header row (first row of active sheet)
- Row count
- Column count
- Sheet names

### CSV/TSV Files
- Filename and path
- File size
- Last modified timestamp
- Header row (first line)
- Row count (total lines including header)
- Column count
- Delimiter used

### Example Output

```json
{
  "filename": "sales_data.xlsx",
  "filepath": "/home/user/data/sales_data.xlsx",
  "file_type": ".xlsx",
  "file_size": 45678,
  "modified_at": "2024-01-15T10:30:00",
  "headers": ["Date", "Product", "Quantity", "Revenue"],
  "row_count": 1523,
  "column_count": 4,
  "sheet_name": "Sales",
  "sheet_names": ["Sales", "Summary"],
  "extracted_at": "2024-01-15T10:30:15"
}
```

## Troubleshooting

### Watcher won't start
- Check configuration: `semplex config show`
- Ensure directories exist
- Check if already running: `semplex status`

### Files not being detected
- Verify file types are configured: `semplex config show`
- Check ignore patterns in config
- Ensure recursive watching is enabled if needed

### Permission errors
- Ensure you have read access to watched directories
- Check write access to config directory

### Debug output not appearing
- Verify debug mode is enabled: `semplex config show`
- Check debug file path is writable
- Look at the file after making changes to monitored files

## Advanced Usage

### Multiple Environments

Use different config files for different environments:

```bash
# Development
SEMPLEX_CONFIG_FILE=~/.config/semplex/config-dev.yaml semplex start

# Production
SEMPLEX_CONFIG_FILE=~/.config/semplex/config-prod.yaml semplex start
```

### Running as a Service

#### systemd (Linux)

Create `/etc/systemd/system/semplex.service`:

```ini
[Unit]
Description=Semplex File Watcher
After=network.target

[Service]
Type=forking
User=youruser
ExecStart=/usr/local/bin/semplex start
ExecStop=/usr/local/bin/semplex stop
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable semplex
sudo systemctl start semplex
sudo systemctl status semplex
```

## Getting Help

```bash
# General help
semplex --help

# Command-specific help
semplex config --help
semplex watch --help

# Version
semplex --version
```
