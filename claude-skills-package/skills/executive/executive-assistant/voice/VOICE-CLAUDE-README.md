# Voice-to-Claude - Full AI Integration

True conversational AI powered by Claude Sonnet 4.5 via Anthropic API.

---

## 🎯 What You Get

**Full Claude AI Intelligence via Voice:**
- Natural conversation with context retention
- Can answer ANY question Claude can answer
- Remembers conversation history
- Evie's warm British voice for responses
- Automatic conversation saving

**This is NOT a simple voice assistant** - this is the full power of Claude Sonnet 4.5 accessible by voice!

---

## 🚀 Quick Start

### For Perry (Regular Use)

**Start the voice AI:**
```powershell
powershell ~/.claude/skills/executive-assistant/voice/start-voice-claude-api.ps1
```

**Then just speak naturally:**
- "What's the best way to deploy a Next.js app?"
- "Explain quantum entanglement in simple terms"
- "Write a bash script to backup my files"
- "What's the meaning of life?"

Claude will respond via Evie's voice!

---

## 💡 Features

### 1. **True Conversational AI**
Not pre-programmed responses - actual Claude Sonnet 4.5 intelligence:
```
You: "Explain Docker containers"
Claude: [Full intelligent explanation]

You: "How do they compare to VMs?"
Claude: [Remembers Docker context, gives comparison]

You: "Give me a Docker Compose example"
Claude: [Provides relevant example based on conversation]
```

### 2. **Context Retention**
Conversation history is automatically saved and loaded:
- Remembers past 20 messages (10 exchanges)
- Resumes where you left off
- Say "clear history" to start fresh

### 3. **Smart Response Handling**
- Short answers spoken in full
- Long answers summarized for speech (full text on screen)
- Code examples printed but not spoken (too hard to follow by voice)

### 4. **Evie Personality**
Claude responds as Evie, your executive assistant:
- Professional yet warm
- Direct and concise
- British voice
- Occasional terms of endearment

---

## 📋 Commands

| Say This | What Happens |
|----------|--------------|
| Any question | Claude answers intelligently |
| "Clear history" | Resets conversation memory |
| "Goodbye" | Exits the program |
| (Ctrl+C) | Emergency exit |

---

## 🎛️ Advanced Usage

### Use Different Claude Models

**Claude Opus 4.6** (Most capable):
```bash
python ~/.claude/skills/executive-assistant/voice/voice-to-claude.py --model claude-opus-4-6
```

**Claude Haiku 4.5** (Fastest, cheapest):
```bash
python ~/.claude/skills/executive-assistant/voice/voice-to-claude.py --model claude-haiku-4-5-20251001
```

**Default is Sonnet 4.5** (best balance)

### Clear History on Start
```bash
python ~/.claude/skills/executive-assistant/voice/voice-to-claude.py --clear-history
```

### View Conversation History
```bash
cat ~/.voice-claude-history.json
```

---

## 💰 Cost Information

**API Pricing (Anthropic):**
- **Sonnet 4.5**: $3 per million input tokens, $15 per million output tokens
- **Opus 4.6**: $15 per million input tokens, $75 per million output tokens
- **Haiku 4.5**: $0.25 per million input tokens, $1.25 per million output tokens

**Typical Usage:**
- Short question/answer: ~$0.001-0.005 (less than a penny)
- Complex coding question: ~$0.01-0.03 (1-3 cents)
- Long conversation (10 exchanges): ~$0.05-0.15 (5-15 cents)

**Your API key is already configured in the script.**

---

## 🔧 How It Works

```
1. You speak
   ↓
2. Whisper transcribes (local, free)
   ↓
3. Sent to Claude via Anthropic API
   ↓
4. Claude processes with full intelligence
   ↓
5. Response printed to screen
   ↓
6. Evie speaks the response (Edge TTS, free)
   ↓
7. Conversation saved to history
```

---

## 🎤 Example Conversations

### Coding Help
```
You: "How do I create a REST API in Express?"
Claude: "To create a REST API in Express, you'll need three main components:
        the Express server, route handlers, and middleware..."
        [Full detailed explanation with code examples on screen]
```

### General Knowledge
```
You: "What causes the Northern Lights?"
Claude: "The Northern Lights, or Aurora Borealis, are caused by charged particles
        from the sun colliding with gases in Earth's atmosphere..."
```

### Creative Tasks
```
You: "Write a haiku about programming"
Claude: "Code flows like water,
        Bugs hide in silent branches,
        Tests reveal the truth."
```

### Complex Analysis
```
You: "Explain the Byzantine Generals Problem"
Claude: [Full explanation of distributed consensus]

You: "How does blockchain solve this?"
Claude: [Explanation building on previous context]
```

---

## 📁 Files & Locations

| File | Purpose |
|------|---------|
| `voice-to-claude.py` | Main script |
| `start-voice-claude-api.ps1` | Quick launcher |
| `~/.voice-claude-history.json` | Conversation history |
| `evie-listen.py` | Microphone input (Whisper) |
| `evie-speak-edge.py` | Voice output (Edge TTS) |

---

## 🆚 Comparison: Voice Interfaces

| Feature | Voice-to-Claude (API) | Accessible CLI | Evie Simple |
|---------|----------------------|----------------|-------------|
| **AI Intelligence** | ✅ Full Claude Sonnet | ❌ No AI | ❌ No AI |
| **Context Memory** | ✅ Yes | ❌ No | ❌ No |
| **Complex Questions** | ✅ Any question | ❌ Commands only | ❌ Basic commands |
| **Coding Help** | ✅ Full assistance | ❌ No | ❌ No |
| **Cost** | ~$0.01-0.05 per exchange | Free | Free |
| **Speed** | ~2-5 seconds | Instant | Instant |
| **Best For** | Conversations, learning | File management | Quick tasks |

---

## 🐛 Troubleshooting

### "API Error: Invalid API key"
- Check that your Anthropic API key is valid
- Get new key at: https://console.anthropic.com/

### "anthropic module not found"
```bash
pip install anthropic
```

### Microphone not working
- Run test: `python ~/.claude/skills/executive-assistant/voice/evie-listen.py`
- Check Windows microphone permissions
- Verify mic index is 18 (Logitech C525)

### Speaker not working
- Run test: `python ~/.claude/skills/executive-assistant/voice/evie-speak-edge.py "test" --play`
- Check speaker volume
- Verify Edge TTS is installed

### Slow responses
- Use Haiku model for faster (but simpler) answers
- Check internet connection
- Reduce conversation history with "clear history"

### High API costs
- Use Haiku instead of Sonnet ($10-30x cheaper)
- Keep questions concise
- Clear history regularly to reduce token usage
- Monitor usage at: https://console.anthropic.com/

---

## 🎓 Tips for Best Results

### Speaking
- **Speak clearly** but naturally
- **Pause** 1 second before speaking
- **Wait** for Evie to finish before next question
- **Rephrase** if she misunderstands

### Questions
- **Be specific** - "Explain Docker containers for beginners"
- **Provide context** - "I'm building a Next.js app..."
- **Ask follow-ups** - Claude remembers the conversation
- **Request examples** - "Show me code examples"

### Managing Conversation
- Say **"clear history"** when changing topics
- Long conversations use more tokens (cost)
- Keep exchanges under 10 for better context
- History auto-saves - resume anytime

---

## 🚀 Next Steps

### For Daily Use
Add to PowerShell profile:
```powershell
function Ask-Claude {
    powershell ~/.claude/skills/executive-assistant/voice/start-voice-claude-api.ps1
}
```

Then just type: `Ask-Claude`

### Auto-Start on Login
Use Windows Task Scheduler to start on login (optional)

### Integrate with Other Tools
- Combine with `/morning` briefing skill
- Use with accessibility CLI for your friend
- Chain with Google Calendar/Gmail MCPs

---

## 📊 System Requirements

- ✅ Windows (with PowerShell)
- ✅ Python 3.9+ (you have 3.13)
- ✅ Working microphone (Logitech C525)
- ✅ Internet connection (for API calls)
- ✅ Anthropic API key (already configured)

**Everything is ready to use!**

---

## 🎉 You're All Set!

Just run:
```powershell
powershell ~/.claude/skills/executive-assistant/voice/start-voice-claude-api.ps1
```

And start having intelligent conversations with Claude via voice!

---

*Built with Claude Code*
*Powered by Anthropic API + Claude Sonnet 4.5*
