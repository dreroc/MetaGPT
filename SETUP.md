# MetaGPT Virtual Environment Setup Guide

This guide helps you set up a Python virtual environment and install all dependencies for the MetaGPT project.

## Quick Start

Run the automated setup script:

```bash
./setup_venv.sh
```

## Manual Setup

If you prefer to set up manually or the script doesn't work:

### 1. Prerequisites

- Python 3.9+ (Python 3.12+ may have some compatibility issues)
- Git (for cloning the repository)
- Node.js/npm (optional, for mermaid-cli)

Check your Python version:
```bash
python3 --version
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment (Linux/macOS)
source venv/bin/activate

# Activate virtual environment (Windows)
# venv\Scripts\activate
```

### 3. Upgrade Build Tools

```bash
pip install --upgrade pip setuptools>=78.1.1 wheel
```

### 4. Install Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Install MetaGPT in development mode
pip install -e .

# Optional: Install development tools
pip install -e ".[dev]"

# Optional: Install test dependencies
pip install -e ".[test]"
```

### 5. Configuration Setup

```bash
# Create config directory
mkdir -p ~/.metagpt

# Copy default configuration
cp config/config2.yaml ~/.metagpt/config2.yaml

# Edit configuration with your API keys
# vim ~/.metagpt/config2.yaml
```

### 6. Optional Tools

#### Mermaid CLI (for diagram generation)
```bash
# Install Node.js first if not available
# Then install mermaid-cli globally
npm install -g @mermaid-js/mermaid-cli
```

#### Playwright (for web scraping)
```bash
# Install browser dependencies
playwright install --with-deps chromium
```

## Verification

Run the verification script to check your setup:

```bash
python verify_setup.py
```

## Usage

### Activate Environment
```bash
source venv/bin/activate
```

### Run MetaGPT
```bash
metagpt "Create a 2048 game in python"
```

### Run Tests
```bash
pytest
```

### Run Linting
```bash
pre-commit run --all-files
```

### Deactivate Environment
```bash
deactivate
```

## Troubleshooting

### Network Issues
If you encounter network timeouts during installation:

1. Try installing with longer timeouts:
   ```bash
   pip install --timeout 300 --retries 3 -r requirements.txt
   ```

2. Install core dependencies first:
   ```bash
   pip install pydantic aiohttp>=3.9.4 openai numpy pandas PyYAML loguru typer rich
   ```

### Python Version Issues

- Ensure you're using Python 3.9+
- Python 3.12+ may have compatibility issues with some packages
- Consider using Python 3.10 or 3.11 for best compatibility

### Package Conflicts
If you encounter dependency conflicts:

1. Clear pip cache:
   ```bash
   pip cache purge
   ```

2. Try installing with `--no-deps` for problematic packages
3. Use `pip-tools` to resolve conflicts:
   ```bash
   pip install pip-tools
   pip-compile requirements.txt
   ```

### Security Vulnerabilities
The setup script automatically upgrades vulnerable packages:

- `aiohttp` to version >=3.9.4 (fixes DoS and directory traversal vulnerabilities)
- `setuptools` to version >=78.1.1 (fixes path traversal and command injection)

## Development Workflow

1. **Always activate the virtual environment** before working:
   ```bash
   source venv/bin/activate
   ```

2. **Install new dependencies** via requirements.txt:
   ```bash
   echo "new-package==1.0.0" >> requirements.txt
   pip install -r requirements.txt
   ```

3. **Run tests** before committing:
   ```bash
   pytest
   ```

4. **Run linting** to ensure code quality:
   ```bash
   pre-commit run --all-files
   ```

## Project Structure

```
MetaGPT/
├── venv/                   # Virtual environment (created by setup)
├── metagpt/               # Main package source code
├── tests/                 # Test files
├── config/                # Configuration files
├── docs/                  # Documentation
├── examples/              # Example scripts
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup
├── setup_venv.sh         # Setup script
├── verify_setup.py       # Verification script
└── SETUP.md              # This file
```

## Support

- Check the [official documentation](docs/)
- Review the [installation guide](docs/install/cli_install.md)
- Run `python verify_setup.py` to diagnose issues
- Check GitHub issues for known problems

## Security Notes

- Always use virtual environments to isolate dependencies
- Keep dependencies updated to avoid security vulnerabilities
- Don't commit API keys or sensitive configuration to version control
- Use environment variables or secure config files for secrets