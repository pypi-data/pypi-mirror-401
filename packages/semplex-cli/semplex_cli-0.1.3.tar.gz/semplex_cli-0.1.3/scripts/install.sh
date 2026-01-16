#!/usr/bin/env bash
# Semplex CLI Installer
# Usage: curl -LsSf https://semplex.simage.ai/install.sh | sh

set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

info() { echo -e "${GREEN}info${NC}: $1"; }
warn() { echo -e "${YELLOW}warn${NC}: $1"; }
error() { echo -e "${RED}error${NC}: $1"; exit 1; }

echo -e "${BOLD}Semplex CLI Installer${NC}"
echo ""

# Check for Python 3.11+
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
        MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

        if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 11 ]; then
            info "Found Python $PYTHON_VERSION"
            return 0
        else
            warn "Python $PYTHON_VERSION found, but 3.11+ is required"
            return 1
        fi
    else
        warn "Python 3 not found"
        return 1
    fi
}

# Check for pipx
check_pipx() {
    if command -v pipx &> /dev/null; then
        info "Found pipx"
        return 0
    else
        return 1
    fi
}

# Install pipx
install_pipx() {
    info "Installing pipx..."
    if command -v brew &> /dev/null; then
        brew install pipx
        pipx ensurepath
    elif command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y pipx
        pipx ensurepath
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y pipx
        pipx ensurepath
    else
        python3 -m pip install --user pipx
        python3 -m pipx ensurepath
    fi
}

# Main installation
main() {
    # Check Python
    if ! check_python; then
        error "Python 3.11 or higher is required. Please install Python first:
  - macOS: brew install python@3.12
  - Ubuntu/Debian: sudo apt install python3.12
  - Fedora: sudo dnf install python3.12"
    fi

    # Check/install pipx
    if ! check_pipx; then
        install_pipx
    fi

    # Install semplex-cli
    info "Installing semplex-cli..."
    pipx install semplex-cli --force

    echo ""
    echo -e "${GREEN}✓${NC} ${BOLD}Semplex CLI installed successfully!${NC}"
    echo ""
    echo "Get started:"
    echo "  semplex --help     Show available commands"
    echo "  semplex init       Initialize configuration"
    echo "  semplex login      Authenticate with Semplex"
    echo "  semplex start      Start the file watcher"
    echo ""
}

main "$@"
