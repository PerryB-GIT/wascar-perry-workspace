# Start Accessible CLI - Voice-Controlled Terminal
# For users who cannot use keyboard/mouse

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 58) -ForegroundColor Cyan
Write-Host " Accessible CLI - Voice-Controlled Terminal" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 58) -ForegroundColor Cyan
Write-Host ""
Write-Host "Perfect for users who cannot use keyboard or mouse!" -ForegroundColor Green
Write-Host ""
Write-Host "Features:" -ForegroundColor White
Write-Host "  - Full voice control of file system" -ForegroundColor Gray
Write-Host "  - Audio confirmation of all actions" -ForegroundColor Gray
Write-Host "  - Safety confirmations for destructive commands" -ForegroundColor Gray
Write-Host "  - Command history logging" -ForegroundColor Gray
Write-Host ""
Write-Host "Essential Commands:" -ForegroundColor White
Write-Host "  'help' - Hear all available commands" -ForegroundColor Gray
Write-Host "  'list files' - See what's in current folder" -ForegroundColor Gray
Write-Host "  'read file [name]' - Have a file read to you" -ForegroundColor Gray
Write-Host "  'repeat that' - Hear last response again" -ForegroundColor Gray
Write-Host "  'goodbye' - Exit" -ForegroundColor Gray
Write-Host ""
Write-Host "Starting in beginner mode (extra guidance)..." -ForegroundColor Green
Write-Host "Press Ctrl+C to exit anytime" -ForegroundColor Gray
Write-Host ""

python "$HOME/.claude/skills/executive-assistant/voice/accessible-cli.py" --beginner
