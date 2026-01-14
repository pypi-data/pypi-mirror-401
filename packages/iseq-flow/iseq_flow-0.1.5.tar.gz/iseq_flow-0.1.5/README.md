# iseq-flow

CLI tool for IntelliSeq Flow - cloud file management.

## Installation

```bash
pip install iseq-flow
```

## Usage

### Authentication

Login using OAuth Device Flow:

```bash
flow login
```

This will open a browser for authentication. Your credentials are stored securely in your system keyring.

Check login status:

```bash
flow status
```

Logout:

```bash
flow logout
```

### File Operations

List files in a project:

```bash
flow files ls --project PROJECT_ID
flow files ls --project PROJECT_ID --path data/raw/
```

Download a file:

```bash
flow files download --project PROJECT_ID --path data/file.txt
flow files download --project PROJECT_ID --path data/file.txt -o local_file.txt
```

Upload a file:

```bash
flow files upload --project PROJECT_ID --path data/uploaded.txt local_file.txt
```

## Configuration

Configure the Flow service URL:

```bash
flow config set api_url https://files.flow.intelliseq.com
```

View current configuration:

```bash
flow config show
```

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
ruff format .
ruff check --fix .
```
