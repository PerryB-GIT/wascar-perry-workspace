# Voice Interfaces for Claude Code

Three voice interface options for different use cases:

## 1. Evie Bridge - Direct Voice to Claude Code
**Use for:** Having conversations with Claude Code via voice

```bash
# Start voice bridge
python ~/.claude/skills/executive-assistant/voice/evie-bridge.py

# With wake word (say "hey claude" before each query)
python ~/.claude/skills/executive-assistant/voice/evie-bridge.py --wake-word "hey claude"

# Skip confirmation sounds (faster)
python ~/.claude/skills/executive-assistant/voice/evie-bridge.py --no-confirm
```

**How it works:**
1. You speak your question/command
2. Evie transcribes it
3. Sends to Claude Code
4. Claude responds (text on screen)
5. Evie speaks the response back to you

**Example conversation:**
- You: "What files are in my current directory?"
- Evie: "Let me think about that..."
- Claude: [Lists files]
- Evie: [Speaks the list]

---

## 2. Accessible CLI - Voice-Controlled Terminal
**Use for:** Users who cannot use keyboard/mouse (accessibility)

```bash
# Start accessible CLI
python ~/.claude/skills/executive-assistant/voice/accessible-cli.py

# Beginner mode (extra guidance)
python ~/.claude/skills/executive-assistant/voice/accessible-cli.py --beginner

# Advanced mode (skip confirmations)
python ~/.claude/skills/executive-assistant/voice/accessible-cli.py --no-confirm
```

**Voice Commands:**

| Category | Commands |
|----------|----------|
| **Navigation** | "list files", "change directory to [path]", "go to home", "go back" |
| **Files** | "create file [name]", "delete file [name]", "read file [name]" |
| **Shell** | "run [command]" (e.g., "run git status") |
| **Email** | "check email", "send email to [person]..." |
| **Calendar** | "what's on my calendar", "schedule meeting..." |
| **Help** | "help", "what can i do", "repeat that" |

**Safety Features:**
- Audio confirmation for all actions
- Requires confirmation for destructive commands (delete, rm, etc.)
- All commands logged to history
- "Repeat that" command to hear last response again

**Example workflow:**
```
You: "list files"
System: "Found 3 folders and 5 files. Folders: Documents, Pictures, Downloads..."

You: "change directory to Documents"
System: "Changed to Documents"

You: "read file readme.txt"
System: "Contents of readme.txt: Welcome to my project..."

You: "run git status"
System: "Command completed. On branch main, nothing to commit..."
```

---

## 3. Evie Interactive - Standalone Assistant
**Use for:** Quick tasks without Claude Code integration

```bash
python ~/.claude/skills/executive-assistant/voice/evie-interactive.py
```

Handles:
- Time/date queries
- Calendar checks
- Email summaries
- Basic questions

---

## Quick Start Commands

### For Perry (Regular Use)
```bash
# Talk to Claude Code via voice
python ~/.claude/skills/executive-assistant/voice/evie-bridge.py
```

### For Your Friend (Accessibility)
```bash
# Full voice-controlled terminal
python ~/.claude/skills/executive-assistant/voice/accessible-cli.py --beginner
```

---

## Requirements

All scripts use:
- **Microphone**: Index 18 (Logitech C525 HD WebCam) - automatically configured
- **Speech Recognition**: OpenAI Whisper (already installed)
- **Text-to-Speech**: Microsoft Edge TTS (free, British female voice)

No additional installation needed - everything is ready to go!

---

## Troubleshooting

### No audio output
- Check speaker volume
- Verify Edge TTS is working:
  ```bash
  python ~/.claude/skills/executive-assistant/voice/evie-speak-edge.py "test" --play
  ```

### Microphone not picking up speech
- Check microphone permissions (Windows Settings → Privacy → Microphone)
- Test mic:
  ```bash
  python ~/.claude/skills/executive-assistant/voice/evie-listen.py
  ```

### Claude Code connection fails (Evie Bridge only)
- Make sure `claude` is in your PATH
- Test: `claude --version`

---

## Customization

### Change voice speed
Edit the scripts and adjust `rate` parameter:
- `rate="+0%"` - Normal speed
- `rate="+20%"` - 20% faster
- `rate="-20%"` - 20% slower

### Change wake word
```bash
python evie-bridge.py --wake-word "hey jarvis"
```

### Use different microphone
Find your mic index:
```bash
python -c "import speech_recognition as sr; print([sr.Microphone.list_microphone_names().index(x) for x in sr.Microphone.list_microphone_names()])"
```

Then use:
```bash
python accessible-cli.py --mic-index [YOUR_INDEX]
```

---

## For Your Friend - Getting Started Guide

**Share this with your friend:**

### First Time Setup (One Time Only)

1. **Open PowerShell** (ask someone to help launch it)
2. **Navigate to the voice folder:**
   ```bash
   cd ~/.claude/skills/executive-assistant/voice
   ```

### Daily Use

1. **Start the accessible CLI:**
   ```bash
   python accessible-cli.py --beginner
   ```

2. **Wait for greeting:**
   - You'll hear: "Accessible CLI started. Say help for commands or goodbye to exit."

3. **Start giving voice commands!**

### Essential Commands to Remember

- **"help"** - Hear list of all commands
- **"repeat that"** - Hear the last response again
- **"list files"** - See what's in current folder
- **"read file [filename]"** - Have a file read to you
- **"run [any command]"** - Execute any terminal command
- **"goodbye"** - Exit the program

### Safety Features

- The system will **always confirm** before doing anything destructive (delete, remove, etc.)
- You must say **"yes"** to confirm, or **"no"** to cancel
- All your commands are saved to history for review

### Example First Session

```
System: "Accessible CLI started. Say help for commands or goodbye to exit."

You: "help"
System: [Lists all available commands]

You: "what directory am i in"
System: "You are in C:\Users\YourName"

You: "list files"
System: "Found 3 folders and 8 files. Folders: Documents, Downloads, Pictures..."

You: "change directory to Documents"
System: "Changed to Documents"

You: "list files"
System: "Found 2 folders and 12 files. Folders: Work, Personal..."

You: "goodbye"
System: "Goodbye. Take care."
```

---

## PowerShell Shortcuts (Optional)

Add these to your PowerShell profile for easy access:

```powershell
# Talk to Claude via voice
function Start-VoiceClaude {
    python ~/.claude/skills/executive-assistant/voice/evie-bridge.py
}

# Accessible CLI for your friend
function Start-AccessibleCLI {
    python ~/.claude/skills/executive-assistant/voice/accessible-cli.py --beginner
}

# Quick test
function Test-VoiceSetup {
    Write-Host "Testing microphone..."
    python ~/.claude/skills/executive-assistant/voice/evie-listen.py

    Write-Host "`nTesting speakers..."
    python ~/.claude/skills/executive-assistant/voice/evie-speak-edge.py "Voice test successful" --play
}
```

Then use:
- `Start-VoiceClaude`
- `Start-AccessibleCLI`
- `Test-VoiceSetup`

---

## Support

- **Issues with voice recognition**: Speak clearly, pause between commands
- **Too fast/slow**: Adjust rate parameter in scripts
- **Need help**: Say "help" anytime for command list
- **Emergency exit**: Press Ctrl+C to force quit
