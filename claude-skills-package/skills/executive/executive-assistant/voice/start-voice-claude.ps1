# Start Voice-to-Claude Interface
# Quick launcher for direct voice interaction with Claude Code

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 58) -ForegroundColor Cyan
Write-Host " Voice-to-Claude Interface" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 58) -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting Evie Bridge..." -ForegroundColor Green
Write-Host "You can now speak to Claude Code directly!" -ForegroundColor White
Write-Host ""
Write-Host "Say your questions out loud, and Claude will respond via voice." -ForegroundColor Gray
Write-Host "Say 'goodbye' or press Ctrl+C to exit." -ForegroundColor Gray
Write-Host ""

python "$HOME/.claude/skills/executive-assistant/voice/evie-bridge.py"
