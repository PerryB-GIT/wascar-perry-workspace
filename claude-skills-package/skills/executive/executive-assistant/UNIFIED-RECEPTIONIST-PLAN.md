# Unified Evie Receptionist - Integration Plan

**Date:** 2026-02-06

## Vision
Combine Evie (Executive Assistant) + GV Receptionist into one unified AI receptionist that monitors everything and proactively helps Perry.

---

## Current State

### Evie (Executive Assistant)
- **Location:** `~/.claude/skills/executive-assistant/skill.md`
- **Capabilities:**
  - Morning briefing (calendar, email, tasks, finances, AI news)
  - Email management & triage
  - Calendar management
  - Task & to-do tracking
  - Important dates tracking
  - Voice notifications
  - Desktop notifications
  - Proactive suggestions
- **Trigger:** "Good morning" or `/executive-assistant`
- **Personality:** British female, warm, flirty, professional

### GV Receptionist
- **Location:** `~/mcp-servers/gv-receptionist/gv-receptionist.js`
- **Capabilities:**
  - Monitors Google Voice (978-219-9092) voicemails
  - Monitors SMS messages
  - Perry SMS commands with authentication ("tunafish")
  - Claude Code CLI integration for task execution
  - Desktop notifications + sound alerts
  - Distinguishes Perry from external callers
- **Status:** Code written, awaiting voicemail greeting setup
- **Runs:** Background Node.js process

---

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EVIE - UNIFIED RECEPTIONIST               │
│                 (One AI, Multiple Monitoring Channels)       │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │   Gmail      │ │  Calendar    │ │ Google Voice │
      │   Monitor    │ │   Monitor    │ │   Monitor    │
      └──────────────┘ └──────────────┘ └──────────────┘
              │               │               │
              │               │               │
              ▼               ▼               ▼
      ┌─────────────────────────────────────────────┐
      │         EVIE'S KNOWLEDGE BASE               │
      │  • Email triage                             │
      │  • Calendar conflicts                       │
      │  • Voicemails from clients                  │
      │  • SMS commands from Perry                  │
      │  • Task priorities                          │
      │  • Financial tracking                       │
      │  • AI industry intel                        │
      └─────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │  Desktop     │ │    Voice     │ │     SMS      │
      │  Notification│ │  Notification│ │   Response   │
      └──────────────┘ └──────────────┘ └──────────────┘
```

---

## Unified Evie Features

### 1. **Always-On Background Monitoring**
- **Gmail**: Check every 30s for priority emails, Neuron newsletter, voicemails
- **Calendar**: Check every 60s for upcoming meetings, conflicts
- **Google Voice**: Check every 30s for voicemails and SMS
- **Uptime Monitor**: Already running (separate, but Evie can report status)
- **Cost Monitor**: Daily checks (already scheduled)

### 2. **Proactive Notifications**
Evie alerts Perry when:
- ⚡ **CRITICAL** (Immediate - Desktop + Voice + SMS):
  - Client voicemail received
  - Payment failure
  - Site down alert
  - Meeting starting in 5 minutes
  - Security alert
- 🔴 **HIGH** (Desktop + Voice):
  - Priority email from client
  - Meeting in 15 minutes
  - Payment received (large)
  - Deadline today
  - Calendar conflict
- 🟡 **MEDIUM** (Desktop):
  - Task reminders
  - Invoice due reminders
  - Goal check-ins
  - AI news (from Neuron)
- 🟢 **LOW** (Morning briefing only):
  - FYI updates
  - Background changes
  - Routine logs

### 3. **SMS Command Interface (Perry Only)**
Text Evie at **978-219-9092**:
- **"tunafish"** → Authenticate for 10 minutes (enables execution mode)
- **"What's my day?"** → Get calendar summary
- **"Check support-forge.com"** → Run site health check
- **"Any urgent emails?"** → Priority email summary
- **"Deploy vineyardvalais"** → Execute deployment (requires auth)
- **"Call [name] back"** → Creates task + reminds
- **Any command** → Claude processes and responds via notification

### 4. **Morning Briefing (Expanded)**
Triggered by "Good morning":
- Date & weather
- **Voicemails overnight** (NEW)
- Calendar for the day
- Email triage
- Today's priorities
- Financial snapshot
- AI industry intel (Neuron + web)
- Goal check-in
- Today's nudge

### 5. **Client Communication Handling**
When voicemail/SMS received from non-Perry number:
1. Evie analyzes message with Claude
2. Classifies: Sales inquiry / Support request / Spam / Emergency
3. Sends Perry desktop notification with:
   - Caller info
   - Message transcription
   - Suggested priority (High/Med/Low)
   - Recommended action
4. Drafts response email (if appropriate)
5. Creates follow-up task in calendar

### 6. **Auto-Recommendations**
Evie proactively suggests:
- "You have 3 back-to-back meetings. Should I block 15-min breaks?"
- "Invoice #123 is 7 days overdue. Draft reminder email?"
- "New AI tool trending on Product Hunt matches your stack. Review?"
- "Jessica meeting in 1 hour. Here's her last email for context."
- "Fred's birthday is next week. Gift ideas?"

---

## Technical Implementation

### Architecture Choice: **Hybrid MCP + Background Service**

**Option A: Pure MCP Integration** (Recommended)
- Create `evie-receptionist` MCP server
- Runs as background Node.js process (like uptime-monitor)
- Uses existing MCPs: Gmail, Google Calendar, Google Voice
- Claude Code invokes via MCP tools when needed
- Auto-starts via Windows Task Scheduler

**Option B: Embedded in Executive Assistant Skill**
- Skill invokes background monitors on demand
- Less autonomous, more interactive
- Simpler, but requires Perry to trigger

**Recommended: Option A** - True always-on receptionist

---

## New MCP Server: `evie-receptionist`

**Location:** `~/mcp-servers/evie-receptionist/`

### Core Components:

1. **evie-receptionist.js** (Main orchestrator)
   - Combines GV receptionist logic + new monitoring
   - Monitors Gmail, Calendar, Google Voice
   - Routes notifications by priority
   - Sends SMS responses (via Google Voice web or API)

2. **Tools Exposed via MCP:**
   ```javascript
   evie_get_status()         // Current monitoring status
   evie_check_voicemails()   // Manual voicemail check
   evie_check_calendar()     // Manual calendar check
   evie_check_emails()       // Manual email check
   evie_send_sms(to, message) // Send SMS via GV
   evie_process_command(text) // Process Perry's command
   ```

3. **Integration with Existing MCPs:**
   - `mcp__gmail__*` - Email monitoring
   - `mcp__google-calendar__*` - Calendar monitoring
   - Reuse GV receptionist code for voicemail/SMS

4. **Windows Scheduled Task:**
   - Name: `EvieReceptionist`
   - Trigger: At logon + restart on failure
   - Action: `node ~/mcp-servers/evie-receptionist/evie-receptionist.js`

---

## Updated Executive Assistant Skill

**Enhancements to `~/.claude/skills/executive-assistant/skill.md`:**

### New Sections:

**"Always-On Monitoring"**
```markdown
## Evie's Always-On Monitoring

Evie continuously monitors:
- 📧 Gmail (every 30s): Priority emails, Neuron newsletter, voicemail notifications
- 📅 Calendar (every 60s): Upcoming meetings, conflicts, prep reminders
- 📞 Google Voice (every 30s): Voicemails, SMS from clients and Perry
- 🌐 Uptime (every 60s): Client sites health (support-forge.com, etc.)
- 💰 Costs (daily): AWS/GCP/Azure spending alerts

When something needs attention, Evie alerts via:
- Desktop notification (all priorities)
- Voice notification (high/critical)
- SMS response (for Perry's commands)
```

**"SMS Command Interface"**
```markdown
## Text Evie at 978-219-9092

### Authentication
Text "tunafish" to enable execution mode for 10 minutes.

### Commands
- "What's my day?" - Calendar summary
- "Check [site]" - Health check
- "Any urgent emails?" - Email triage
- "Deploy [site]" - Execute deployment (requires auth)
- "Call [name] back" - Creates reminder task
- Any other text - Claude processes and responds

### For External Callers
Voicemails are transcribed, analyzed, and forwarded to Perry with:
- Caller info
- Message summary
- Priority level
- Recommended action
```

**"Voicemail Handling"**
```markdown
## Voicemail Protocol

When voicemail received on 978-219-9092:

1. **Gmail delivers transcription** to perry.bailes@gmail.com
2. **Evie analyzes** with Claude:
   - Classifies: Sales / Support / Spam / Emergency
   - Extracts: Caller info, callback number, intent
   - Assigns priority: High / Medium / Low
3. **Evie notifies Perry**:
   - Desktop alert with transcription
   - Suggested action (call back, email, ignore)
   - If high priority: Voice alert too
4. **Evie creates follow-up task** (if needed):
   - "Call back [Name] re: [Topic]"
   - Due: Today or tomorrow based on urgency
5. **Evie drafts response** (if appropriate):
   - Thank you email with ETA on callback
   - Boilerplate for common inquiries

### Voicemail Greeting (Support Forge)
"Hi, you've reached Support Forge, AI consulting and web development.
Please leave your name, number, and a brief message, and we'll get back to you within 24 hours.
You can also email us at perry.bailes@gmail.com or visit support-forge.com.
Thanks for calling!"
```

---

## Implementation Steps

### Phase 1: Merge GV Receptionist into Evie MCP (Today)
1. ✅ Create `~/mcp-servers/evie-receptionist/` directory
2. ✅ Copy `gv-receptionist.js` as base
3. ✅ Add Gmail monitoring (email triage logic)
4. ✅ Add Calendar monitoring (meeting prep logic)
5. ✅ Add MCP server wrapper (expose tools)
6. ✅ Update executive-assistant skill with new sections
7. ✅ Test voicemail handling
8. ✅ Test SMS command handling

### Phase 2: Enhanced Notifications (Tomorrow)
1. Voice notifications (HeyGen or Edge TTS)
2. SMS responses (send via Google Voice web or API)
3. Auto-draft responses
4. Task creation integration

### Phase 3: Auto-Recommendations (Next Week)
1. Pattern detection (busy days, overdue invoices)
2. Proactive suggestions
3. Context-aware reminders
4. Learning from Perry's responses

---

## Configuration File

**`~/mcp-servers/evie-receptionist/config.json`:**
```json
{
  "perry": {
    "email": "perry.bailes@gmail.com",
    "phone": "14782991604",
    "gv_number": "+1 978-219-9092"
  },
  "monitoring": {
    "gmail_interval": 30000,
    "calendar_interval": 60000,
    "gv_interval": 30000
  },
  "notifications": {
    "desktop": true,
    "voice": true,
    "sms_response": true
  },
  "authentication": {
    "password": "tunafish",
    "timeout_minutes": 10
  },
  "integrations": {
    "uptime_monitor": "~/mcp-servers/uptime-monitor/",
    "cost_analyzer": "~/mcp-servers/cost-analyzer/"
  }
}
```

---

## Benefits of Unified Evie

1. **Single AI Personality** - Consistent voice across all interactions
2. **Contextual Awareness** - Evie knows calendar when handling voicemail
3. **Proactive Intelligence** - Connects dots between email, calendar, calls
4. **SMS Command Center** - Control everything via text
5. **Always Monitoring** - Never miss a client inquiry
6. **Smart Prioritization** - Evie knows what's urgent based on context
7. **Reduces Cognitive Load** - Perry doesn't need to check multiple sources

---

## Next Steps

**Immediate (Today):**
1. Create evie-receptionist MCP server
2. Test voicemail monitoring
3. Test SMS commands
4. Set up Google Voice voicemail greeting

**This Week:**
1. Add voice notifications
2. Add SMS response capability
3. Integrate with uptime monitor
4. Set up auto-start task

**Next Week:**
1. Build auto-recommendation engine
2. Add pattern detection
3. Integrate with cost analyzer
4. Build learning system

---

## Commands Reference

```powershell
# Start Evie Receptionist
cd ~/mcp-servers/evie-receptionist && npm start

# Check Evie status
node ~/mcp-servers/evie-receptionist/check-status.js

# View logs
cat ~/mcp-servers/evie-receptionist/evie.log

# Stop Evie
taskkill /F /IM node.exe /FI "WINDOWTITLE eq Evie*"

# Set up auto-start
# (Run as Administrator)
~/scripts/setup-evie-autostart.ps1
```

---

## Testing Checklist

- [ ] Voicemail received → Desktop notification
- [ ] SMS from Perry with "tunafish" → Authentication success
- [ ] SMS command from Perry (authenticated) → Task executes
- [ ] SMS from external → Desktop notification only
- [ ] Priority email → Desktop notification
- [ ] Meeting in 15 min → Desktop + voice notification
- [ ] Morning briefing includes voicemails
- [ ] Calendar conflict detected → Proactive alert
- [ ] Overdue invoice → Recommendation to follow up

---

**Ready to build?** Let's start with Phase 1 and create the unified Evie Receptionist MCP server.
