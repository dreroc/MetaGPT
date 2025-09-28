#!/bin/bash

# MetaGPT Virtual Environment Setup Script
# This script creates a virtual environment and installs all dependencies

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}MetaGPT Virtual Environment Setup${NC}"
echo "======================================"

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "Python version: $python_version"

# Extract major and minor version numbers
major_version=$(echo $python_version | cut -d'.' -f1)
minor_version=$(echo $python_version | cut -d'.' -f2)

# Check if Python version is >= 3.9
if [ "$major_version" -lt 3 ] || ([ "$major_version" -eq 3 ] && [ "$minor_version" -lt 9 ]); then
    echo -e "${RED}Error: Python 3.9+ is required. Current version: $python_version${NC}"
    exit 1
fi

if [ "$major_version" -eq 3 ] && [ "$minor_version" -ge 12 ]; then
    echo -e "${YELLOW}Warning: Python 3.12+ detected. Some packages may have compatibility issues.${NC}"
fi

echo -e "${GREEN}✓ Python version check passed${NC}"

# Set virtual environment directory
VENV_DIR="venv"

# Check if virtual environment already exists
if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment already exists at $VENV_DIR${NC}"
    read -p "Do you want to remove it and create a new one? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Removing existing virtual environment...${NC}"
        rm -rf "$VENV_DIR"
    else
        echo -e "${BLUE}Using existing virtual environment${NC}"
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}✓ Virtual environment created at $VENV_DIR${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Upgrade pip, setuptools, and wheel
echo -e "${YELLOW}Upgrading pip, setuptools, and wheel...${NC}"
pip install --upgrade pip setuptools>=78.1.1 wheel

# Function to install with retry and timeout
install_with_retry() {
    local package="$1"
    local max_attempts=3
    local timeout=300
    
    for attempt in $(seq 1 $max_attempts); do
        echo -e "${YELLOW}Installing $package (attempt $attempt/$max_attempts)...${NC}"
        if timeout $timeout pip install --timeout $timeout --retries 3 "$package"; then
            echo -e "${GREEN}✓ Successfully installed $package${NC}"
            return 0
        else
            echo -e "${RED}Failed to install $package (attempt $attempt/$max_attempts)${NC}"
            if [ $attempt -eq $max_attempts ]; then
                echo -e "${RED}Error: Failed to install $package after $max_attempts attempts${NC}"
                return 1
            fi
            sleep 5
        fi
    done
}

# Install core dependencies first
echo -e "${YELLOW}Installing core dependencies...${NC}"
CORE_DEPS=(
    "setuptools>=78.1.1"
    "wheel"
    "pydantic>=2.5.3"
    "aiohttp>=3.9.4"
    "openai~=1.64.0"
    "numpy~=1.26.4"
    "pandas==2.1.1"
    "PyYAML==6.0.1"
    "loguru==0.6.0"
    "typer==0.9.0"
    "rich==13.6.0"
)

for dep in "${CORE_DEPS[@]}"; do
    if ! install_with_retry "$dep"; then
        echo -e "${YELLOW}Warning: Failed to install $dep, continuing with other packages...${NC}"
    fi
done

# Try to install from requirements file with better error handling
echo -e "${YELLOW}Installing remaining dependencies from requirements.txt...${NC}"
if [ -f "requirements.txt" ]; then
    if timeout 600 pip install --timeout 300 --retries 3 -r requirements.txt; then
        echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
    else
        echo -e "${YELLOW}Warning: Some dependencies may have failed to install due to network issues${NC}"
        echo -e "${YELLOW}You can retry later by running: pip install -r requirements.txt${NC}"
    fi
else
    echo -e "${RED}Error: requirements.txt not found${NC}"
    exit 1
fi

# Install the package in development mode
echo -e "${YELLOW}Installing MetaGPT in development mode...${NC}"
if timeout 300 pip install --timeout 300 -e .; then
    echo -e "${GREEN}✓ MetaGPT installed in development mode${NC}"
else
    echo -e "${YELLOW}Warning: MetaGPT installation may be incomplete${NC}"
fi

# Install development and test dependencies (optional)
echo ""
read -p "Install development and test dependencies? (recommended for development) (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Installing development dependencies...${NC}"
    if timeout 300 pip install --timeout 300 ".[dev]"; then
        echo -e "${GREEN}✓ Development dependencies installed${NC}"
    else
        echo -e "${YELLOW}Warning: Some dev dependencies may not be installed${NC}"
    fi
    
    echo -e "${YELLOW}Installing test dependencies...${NC}"
    if timeout 300 pip install --timeout 300 ".[test]"; then
        echo -e "${GREEN}✓ Test dependencies installed${NC}"
    else
        echo -e "${YELLOW}Warning: Some test dependencies may not be installed${NC}"
    fi
fi

# Show installed packages summary
echo -e "${BLUE}Installation Summary${NC}"
echo "===================="
echo "Virtual environment: $(pwd)/$VENV_DIR"
if command -v python &> /dev/null; then
    echo "Python version: $(python --version)"
    echo "Pip version: $(pip --version)"
    echo "Installed packages: $(pip list | wc -l) packages"
else
    echo "Python environment not properly activated"
fi

# Verify core installation
echo -e "${YELLOW}Verifying core installation...${NC}"
if python -c "import sys; print('Python path:', sys.executable)" 2>/dev/null; then
    echo -e "${GREEN}✓ Python environment verified${NC}"
else
    echo -e "${RED}✗ Python environment verification failed${NC}"
fi

# Check if metagpt module can be imported
if python -c "import metagpt; print('MetaGPT version: 1.0.0')" 2>/dev/null; then
    echo -e "${GREEN}✓ MetaGPT module can be imported${NC}"
else
    echo -e "${YELLOW}Warning: MetaGPT module cannot be imported yet${NC}"
fi

# Provide usage instructions
echo -e "${GREEN}Setup completed!${NC}"
echo ""
echo -e "${BLUE}Usage Instructions:${NC}"
echo "To activate the virtual environment:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "To deactivate the virtual environment:"
echo "  deactivate"
echo ""
echo "To run MetaGPT (after setting up config):"
echo "  metagpt \"Your requirements here\""
echo ""
echo "To run tests:"
echo "  pytest"
echo ""
echo "To run linting:"
echo "  pre-commit run --all-files"

# Configuration setup reminder
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "1. Configure your LLM API keys:"
echo "   mkdir -p ~/.metagpt"
echo "   cp config/config2.yaml ~/.metagpt/config2.yaml"
echo "   # Edit ~/.metagpt/config2.yaml with your API keys"
echo ""
echo "2. Optional: Install mermaid-cli for diagram generation:"
echo "   npm install -g @mermaid-js/mermaid-cli"
echo ""
echo "3. Optional: Install Playwright browsers for web scraping:"
echo "   playwright install --with-deps chromium"

# Optional: Check if Node.js/npm is available for mermaid-cli
if command -v npm &> /dev/null; then
    echo ""
    echo -e "${YELLOW}Optional: Install mermaid-cli for diagram generation?${NC}"
    read -p "Install mermaid-cli globally? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Installing mermaid-cli...${NC}"
        if npm install -g @mermaid-js/mermaid-cli; then
            echo -e "${GREEN}✓ mermaid-cli installed${NC}"
        else
            echo -e "${YELLOW}Warning: mermaid-cli installation failed${NC}"
        fi
    fi
else
    echo -e "${YELLOW}Note: npm not found. mermaid-cli installation skipped.${NC}"
    echo "To install npm, visit: https://nodejs.org/"
fi

echo -e "${GREEN}All done! 🎉${NC}"