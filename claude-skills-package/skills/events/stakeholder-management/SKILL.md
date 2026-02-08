# Stakeholder Management - Communication & Alignment

## Stakeholder Management Philosophy
```
"Projects don't fail because of technology. They fail because of people."

KEY PRINCIPLES:
1. Identify stakeholders early and completely
2. Understand their interests and influence
3. Communicate proactively and consistently
4. Manage expectations relentlessly
5. Build relationships before you need them
```

---

## Stakeholder Identification

### Stakeholder Categories
```
INTERNAL STAKEHOLDERS:
- Executive sponsors
- Project team members
- Department heads
- End users
- IT/Security
- Finance
- Legal/Compliance
- HR

EXTERNAL STAKEHOLDERS:
- Customers
- Vendors/Partners
- Regulators
- Investors
- Industry analysts
- Media
```

### Stakeholder Register Template
```markdown
## Stakeholder Register

| Name | Organization | Role | Contact | Interest | Influence | Strategy |
|------|--------------|------|---------|----------|-----------|----------|
| Jane Smith | Executive | Sponsor | email | High | High | Manage Closely |
| Bob Jones | IT | Tech Lead | email | High | Medium | Keep Informed |
| Sue Lee | Finance | Budget Owner | email | Medium | High | Keep Satisfied |
| Mike Chen | Users | End User Rep | email | High | Low | Keep Informed |

### Classification Key
**Interest**: Level of concern about project outcomes
**Influence**: Power to affect project decisions
**Strategy**: Engagement approach (see matrix below)
```

### Stakeholder Matrix
```
        HIGH INFLUENCE
             │
  Keep       │    Manage
  Satisfied  │    Closely
  (High power│  (Key players)
   low int.) │
─────────────┼─────────────
  Monitor    │    Keep
  (Minimal   │    Informed
   effort)   │  (Show consid.)
             │
        LOW INFLUENCE
    LOW ──────────► HIGH
       INTEREST

STRATEGIES:
Manage Closely: Regular meetings, involve in decisions
Keep Satisfied: Keep informed, address concerns quickly
Keep Informed: Regular updates, answer questions
Monitor: Minimal communication, watch for changes
```

---

## RACI Matrix

### RACI Definitions
```
R - RESPONSIBLE: Does the work
    - One or more people
    - Executes the task

A - ACCOUNTABLE: Owns the outcome
    - Only ONE person
    - Makes final decisions
    - Cannot be delegated

C - CONSULTED: Provides input
    - Two-way communication
    - Opinion is sought before decisions

I - INFORMED: Kept in the loop
    - One-way communication
    - Notified after decisions
```

### RACI Template
```markdown
## RACI Matrix: [Project Name]

| Activity | Sponsor | PM | Dev Lead | Dev Team | QA | Users |
|----------|---------|-----|----------|----------|-----|-------|
| Define requirements | A | R | C | I | C | C |
| Approve budget | A | R | I | I | I | I |
| Create designs | I | A | R | C | C | C |
| Develop features | I | A | C | R | C | I |
| Test functionality | I | A | I | C | R | C |
| Approve release | A | R | C | I | C | I |
| Train users | I | A | C | I | I | R |
| Go-live decision | A | R | C | I | C | I |

### Rules
- Every row has exactly ONE "A"
- Every row has at least one "R"
- Too many C's = decision paralysis
- Inform vs. Consult: Do they need to provide input?
```

### RACI Best Practices
```
DO:
✓ One Accountable per activity
✓ Define at project start
✓ Review when roles change
✓ Use for key decisions/deliverables

DON'T:
✗ Too granular (major activities only)
✗ Everyone is C or I
✗ No clear Responsible
✗ Forget to update
```

---

## Communication Planning

### Communication Plan Template
```markdown
## Communication Plan

### Project Information
- Project Name:
- Project Manager:
- Date:

### Communication Matrix
| Audience | Message | Method | Frequency | Owner | Notes |
|----------|---------|--------|-----------|-------|-------|
| Exec Sponsor | Project status | 1:1 Meeting | Weekly | PM | Focus on decisions |
| Steering Committee | Progress report | Meeting | Bi-weekly | PM | 30 min max |
| Project Team | Task updates | Standup | Daily | SM | 15 min |
| Stakeholders | Status summary | Email | Weekly | PM | Friday send |
| End Users | Milestone updates | Email/Intranet | Monthly | PM | High-level |

### Communication Channels
| Channel | Use For | Response Time |
|---------|---------|---------------|
| Email | Formal updates, decisions | 24 hours |
| Slack/Teams | Quick questions, FYI | 4 hours |
| Meeting | Discussion, decisions | N/A |
| Status Report | Progress updates | N/A |

### Escalation Path
Issue → PM → Sponsor → Steering Committee

### Meeting Schedule
| Meeting | Cadence | Day/Time | Duration | Attendees |
|---------|---------|----------|----------|-----------|
| Standup | Daily | 9:00 AM | 15 min | Dev team |
| Sprint Review | Bi-weekly | Fri 2 PM | 1 hour | Team + stakeholders |
| Exec Update | Weekly | Mon 10 AM | 30 min | PM + Sponsor |
```

### Status Report Template
```markdown
## Project Status Report
**Project**: [Name]
**Date**: [Date]
**PM**: [Name]

### Overall Status: 🟢 Green / 🟡 Yellow / 🔴 Red

### Summary
[2-3 sentence executive summary]

### Progress This Week
| Milestone | Due Date | Status | Notes |
|-----------|----------|--------|-------|
| [Milestone 1] | [Date] | 🟢 | On track |
| [Milestone 2] | [Date] | 🟡 | At risk |

### Accomplishments
1. [What was completed]
2. [What was completed]

### Upcoming (Next 2 Weeks)
1. [What's planned]
2. [What's planned]

### Issues & Blockers
| Issue | Impact | Owner | ETA |
|-------|--------|-------|-----|
| [Issue] | [H/M/L] | [Name] | [Date] |

### Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk] | H/M/L | H/M/L | [Plan] |

### Decisions Needed
| Decision | Needed By | From |
|----------|-----------|------|
| [Decision] | [Date] | [Who] |

### Budget Status
| Category | Budget | Spent | Remaining |
|----------|--------|-------|-----------|
| Total | $XXX | $XXX | $XXX |
```

---

## Executive Communication

### Executive Summary Principles
```
KEEP IT:
- Brief (1 page max)
- High-level (outcomes, not tasks)
- Visual (dashboards, charts)
- Action-oriented (decisions needed)

LEAD WITH:
1. Status (Red/Yellow/Green)
2. Key message/headline
3. What they need to do
4. Supporting details

AVOID:
- Technical jargon
- Long narratives
- Excuses without solutions
- Surprises (warn early)
```

### Executive Update Template
```markdown
## Executive Update: [Project Name]
**Date**: [Date]

### The Headline
[One sentence summary of most important thing to know]

### Status: 🟢/🟡/🔴
[Brief explanation if not green]

### Key Metrics
| Metric | Target | Actual | Trend |
|--------|--------|--------|-------|
| Schedule | On track | +3 days | 🟡 |
| Budget | $100K | $95K | 🟢 |
| Quality | 95% | 97% | 🟢 |

### Decisions Required
1. [Decision] - Need by [Date]

### Help Needed
1. [Ask/Resource/Support]

### Next Milestone
[Milestone] - [Date]
```

### Presenting to Executives
```
PREPARE:
- Know the numbers cold
- Anticipate questions
- Have backup slides
- Know your ask

PRESENT:
- Start with bottom line
- Keep it high-level
- Be confident, not defensive
- Listen more than talk

HANDLE QUESTIONS:
- Answer directly
- "I'll get back to you" is okay
- Don't guess or speculate
- Follow up promptly
```

---

## Change Management

### Change Impact Assessment
```markdown
## Change Impact Assessment

### Change Description
[What is changing?]

### Stakeholder Impact
| Group | Impact Level | Nature of Impact | Concerns |
|-------|--------------|------------------|----------|
| [Group 1] | High | New process | Training needs |
| [Group 2] | Medium | Minor workflow | Adoption |
| [Group 3] | Low | Minimal | Awareness |

### Readiness Assessment
| Factor | Current State | Desired State | Gap |
|--------|---------------|---------------|-----|
| Awareness | Low | High | Training plan |
| Desire | Medium | High | Communication |
| Knowledge | Low | High | Documentation |
| Ability | Low | High | Practice time |
| Reinforcement | N/A | Ongoing | Support plan |
```

### Change Communication Plan
```
ADKAR MODEL:

A - AWARENESS: Why is the change happening?
    - Communicate the business case
    - Explain the "why"

D - DESIRE: What's in it for me?
    - Personal benefits
    - Address concerns

K - KNOWLEDGE: How do I change?
    - Training
    - Documentation
    - Examples

A - ABILITY: Can I do it?
    - Practice time
    - Support/coaching
    - Gradual rollout

R - REINFORCEMENT: Keep doing it
    - Celebrate wins
    - Feedback loops
    - Remove old ways
```

---

## Conflict Resolution

### Conflict Levels
```
LEVEL 1 - Problem to Solve
- Disagreement on facts/methods
- Focus on solution

LEVEL 2 - Disagreement
- Personal protection mode
- Positions hardening

LEVEL 3 - Contest
- Win/lose mentality
- Sides forming

LEVEL 4 - Crusade
- Protecting the group
- Other side is "enemy"

LEVEL 5 - World War
- Destruction of other side
- No resolution possible
```

### Conflict Resolution Strategies
```
COLLABORATING (Win-Win):
When: Important issues, time available
How: Work together to find solution both parties accept

COMPROMISING (Win Some/Lose Some):
When: Moderate importance, need quick resolution
How: Each side gives something up

ACCOMMODATING (Lose-Win):
When: Issue more important to other party
How: Yield to maintain relationship

COMPETING (Win-Lose):
When: Emergency, critical decision needed
How: Push through your position

AVOIDING (Lose-Lose):
When: Issue is trivial, need cool-off time
How: Postpone or sidestep
```

### Difficult Conversation Framework
```
PREPARE:
1. What happened? (Facts only)
2. What's my story? (My interpretation)
3. What's their story? (Their likely view)
4. What do I want? (Outcome)

HAVE THE CONVERSATION:
1. State purpose: "I'd like to discuss..."
2. Share observation: "What I've noticed is..."
3. Ask for their view: "How do you see it?"
4. Listen actively: Understand their perspective
5. Find common ground: "We both want..."
6. Agree on action: "What can we do?"
7. Follow up: "Let's check in on..."
```

---

## Meeting Management

### Effective Meeting Checklist
```
BEFORE:
□ Is a meeting necessary?
□ Clear objective defined
□ Right people invited
□ Agenda sent in advance
□ Materials prepared
□ Time allocated appropriately

DURING:
□ Start on time
□ State objective
□ Follow agenda
□ Capture decisions/actions
□ Manage participation
□ End on time

AFTER:
□ Send notes within 24 hours
□ List decisions made
□ List action items with owners/dates
□ Schedule follow-ups if needed
```

### Meeting Notes Template
```markdown
## Meeting Notes
**Meeting**: [Name]
**Date**: [Date]
**Attendees**: [Names]
**Absent**: [Names]

### Objective
[What we aimed to accomplish]

### Key Discussion Points
1. [Topic 1]
   - [Key point]
   - [Key point]
2. [Topic 2]
   - [Key point]

### Decisions Made
1. [Decision 1] - Made by [Name]
2. [Decision 2] - Made by [Name]

### Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| [Action 1] | [Name] | [Date] |
| [Action 2] | [Name] | [Date] |

### Next Meeting
Date: [Date]
Agenda: [Topics]
```

### Meeting Types & Duration
```
| Type | Purpose | Duration | Frequency |
|------|---------|----------|-----------|
| Standup | Quick sync | 15 min | Daily |
| Working Session | Problem solve | 1-2 hours | As needed |
| Status Update | Share progress | 30-60 min | Weekly |
| Decision Meeting | Make decision | 30-60 min | As needed |
| Brainstorm | Generate ideas | 60-90 min | As needed |
| Review | Evaluate work | 1-2 hours | Milestone |
| Retrospective | Improve process | 1-1.5 hours | Sprint end |
```
