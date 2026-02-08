#!/bin/bash
# Wascar's Mac Auto-Installer
# Double-click this file to run it on Mac

cd "$(dirname "$0")"

echo "=========================================="
echo "Wascar's Mac Development Setup"
echo "=========================================="
echo ""
echo "This will install:"
echo "  - Homebrew (package manager)"
echo "  - Git & GitHub CLI"
echo "  - Python 3.12"
echo "  - VS Code"
echo "  - Node.js"
echo ""
read -p "Press ENTER to start installation..."

echo ""
echo "Installing Homebrew..."
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add Homebrew to PATH
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

echo ""
echo "Installing development tools..."
brew install git gh python@3.12
brew install --cask visual-studio-code

echo ""
echo "Configuring Git..."
git config --global user.name "Wascar Deleon"
git config --global user.email "wascaredeleon@gmail.com"
git config --global init.defaultBranch main

echo ""
echo "Creating workspace..."
mkdir -p ~/workspace

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Close and reopen Terminal"
echo "  2. Run: gh auth login"
echo "  3. Clone repositories:"
echo "     cd ~/workspace"
echo "     git clone https://github.com/PerryB-GIT/wascar-perry-workspace.git"
echo "     git clone https://github.com/PerryB-GIT/wascar-ai-implementation.git"
echo ""
read -p "Press ENTER to exit..."
