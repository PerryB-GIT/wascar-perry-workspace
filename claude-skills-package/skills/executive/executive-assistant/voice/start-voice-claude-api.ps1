# Start Voice-to-Claude (Full AI Integration)
# Powered by Anthropic API - True conversational AI

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 58) -ForegroundColor Cyan
Write-Host " Voice-to-Claude - Full AI Integration" -ForegroundColor Yellow
Write-Host " Powered by Claude Sonnet 4.5" -ForegroundColor Magenta
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 58) -ForegroundColor Cyan
Write-Host ""
Write-Host "Features:" -ForegroundColor White
Write-Host "  - True conversational AI (remembers context)" -ForegroundColor Gray
Write-Host "  - Full Claude Sonnet 4.5 intelligence" -ForegroundColor Gray
Write-Host "  - Evie's British voice for responses" -ForegroundColor Gray
Write-Host "  - Conversation history saved automatically" -ForegroundColor Gray
Write-Host ""
Write-Host "Commands:" -ForegroundColor White
Write-Host "  - Speak naturally - Claude understands context" -ForegroundColor Gray
Write-Host "  - Say 'clear history' to reset conversation" -ForegroundColor Gray
Write-Host "  - Say 'goodbye' to exit" -ForegroundColor Gray
Write-Host ""
Write-Host "Starting..." -ForegroundColor Green
Write-Host ""

# Set API key environment variable
$env:ANTHROPIC_API_KEY = "YOUR_API_KEY_HERE"

python "$HOME/.claude/skills/executive-assistant/voice/voice-to-claude.py"
