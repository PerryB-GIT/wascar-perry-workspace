#!/bin/bash
# Claude Skills Package Installer for Wascar
# AI Implementation & Business Automation Toolkit

echo "=========================================="
echo "Claude Skills Package Installer"
echo "=========================================="
echo ""

# Check if Claude Code is installed
if ! command -v claude &> /dev/null; then
    echo "❌ Claude Code CLI not found"
    echo "   Please install Claude Code first:"
    echo "   npm install -g @anthropic-ai/claude-code"
    exit 1
fi

echo "✓ Claude Code found"
echo ""

# Create directories
echo "Creating directories..."
mkdir -p ~/.claude/skills
mkdir -p ~/SuperClaude_Framework

# Copy SuperClaude Framework
echo "Installing SuperClaude Framework..."
cp -r superclaude/* ~/SuperClaude_Framework/
echo "✓ SuperClaude installed to ~/SuperClaude_Framework"

# Copy Skills
echo ""
echo "Installing Skills..."

echo "  - Financial skills (5)..."
cp -r skills/financial/* ~/.claude/skills/

echo "  - Web Development skills (4)..."
cp -r skills/web-dev/* ~/.claude/skills/

echo "  - Event/Organization skills (4)..."
cp -r skills/events/* ~/.claude/skills/

echo "  - Business Operations skills (6)..."
cp -r skills/business/* ~/.claude/skills/

echo "  - Cloud/DevOps skills (4)..."
cp -r skills/cloud/* ~/.claude/skills/

echo "  - Executive Assistant (1)..."
cp -r skills/executive/* ~/.claude/skills/

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""

# Count skills
SKILL_COUNT=$(ls -1 ~/.claude/skills/ | wc -l)
echo "✓ Installed $SKILL_COUNT skills total"
echo "✓ SuperClaude Framework ready"
echo ""

echo "Available Skills:"
echo "  Financial: /creating-financial-models, /managing-finances, /invoice-generator"
echo "  Web Dev: /back-end-dev-guidelines, /senior-backend, /webapp-security"
echo "  Business: /client-intake, /creating-proposals, /negotiator"
echo "  Cloud: /cloud-costs, /aws-cost-optimizer, /incident-response"
echo "  Executive: /executive-assistant"
echo ""

echo "SuperClaude Commands:"
echo "  /sc:pm - Project management"
echo "  /sc:implement - Feature implementation"
echo "  /sc:research - Deep research"
echo "  /sc:build - Build & compile"
echo ""

echo "To verify:"
echo "  claude --version"
echo "  ls ~/.claude/skills/"
echo ""

echo "Ready to use! Open Claude Code and try a skill!"
