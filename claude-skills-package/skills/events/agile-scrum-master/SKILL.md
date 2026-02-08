# Agile & Scrum Master - Sprint Excellence

## Agile Manifesto
```
VALUES:
- Individuals and interactions OVER processes and tools
- Working software OVER comprehensive documentation
- Customer collaboration OVER contract negotiation
- Responding to change OVER following a plan

PRINCIPLES (12):
1. Highest priority: Satisfy customer through early and continuous delivery
2. Welcome changing requirements, even late in development
3. Deliver working software frequently
4. Business and developers work together daily
5. Build projects around motivated individuals
6. Face-to-face conversation is the most efficient communication
7. Working software is the primary measure of progress
8. Sustainable development pace
9. Continuous attention to technical excellence
10. Simplicity - maximizing work not done
11. Self-organizing teams produce best results
12. Regular reflection and adjustment
```

---

## Scrum Framework

### Scrum Roles
```
PRODUCT OWNER (PO):
Responsibilities:
- Owns the product backlog
- Defines and prioritizes features
- Accepts or rejects work
- Represents customer/stakeholders
- Available to answer questions

NOT Responsible For:
- Telling team HOW to build
- Managing the team
- Attending every standup

---

SCRUM MASTER (SM):
Responsibilities:
- Facilitates Scrum ceremonies
- Removes impediments
- Coaches team on Scrum
- Protects team from distractions
- Helps improve processes

NOT Responsible For:
- Managing the team
- Assigning work
- Making product decisions

---

DEVELOPMENT TEAM:
Responsibilities:
- Self-organizing
- Cross-functional
- Delivers potentially shippable increment
- Estimates work
- Commits to sprint goals

Characteristics:
- 3-9 members
- No titles (just "developers")
- Accountable as a team
```

### Scrum Events (Ceremonies)

#### Sprint Planning
```
WHEN: Start of sprint
DURATION: 2-4 hours for 2-week sprint
WHO: Whole Scrum team

INPUTS:
- Prioritized product backlog
- Team capacity/velocity
- Definition of Done

OUTPUTS:
- Sprint Goal
- Sprint Backlog
- Team commitment

AGENDA:
1. PO presents top backlog items (30 min)
2. Team asks clarifying questions (30 min)
3. Team selects items based on capacity (30 min)
4. Team breaks down into tasks (60 min)
5. Team confirms sprint goal (15 min)

SPRINT GOAL TEMPLATE:
"By the end of this sprint, [user] will be able to [capability],
enabling [business value]."
```

#### Daily Standup
```
WHEN: Same time every day
DURATION: 15 minutes (max)
WHO: Development team (+ optional observers)

EACH PERSON ANSWERS:
1. What did I do yesterday?
2. What will I do today?
3. Are there any blockers?

RULES:
- Stand up (keeps it short)
- Same time, same place
- Start on time, even if people missing
- Not a status report - it's for the team
- Take discussions offline

ANTI-PATTERNS:
✗ Reporting to Scrum Master
✗ Problem-solving in standup
✗ Going over 15 minutes
✗ Side conversations
✗ Checking phones
```

#### Sprint Review (Demo)
```
WHEN: End of sprint
DURATION: 1-2 hours for 2-week sprint
WHO: Scrum team + stakeholders

PURPOSE:
- Demonstrate completed work
- Get feedback
- Adapt backlog based on feedback

AGENDA:
1. Sprint goal recap (5 min)
2. Demo completed items (45-60 min)
3. Stakeholder feedback (30 min)
4. Backlog discussion (15 min)

TIPS:
- Demo WORKING software, not slides
- Let team members demo their work
- Encourage questions
- Note feedback for backlog
```

#### Sprint Retrospective
```
WHEN: End of sprint, after review
DURATION: 1-1.5 hours
WHO: Scrum team only (no stakeholders)

PURPOSE:
- Inspect how sprint went
- Identify improvements
- Create action plan

BASIC FORMAT:
1. What went well? (Keep doing)
2. What didn't go well? (Stop doing)
3. What can we improve? (Try next sprint)

RETROSPECTIVE FORMATS:

START/STOP/CONTINUE:
- Start: Things to begin doing
- Stop: Things to cease doing
- Continue: Things working well

4 L's:
- Liked: What did we like?
- Learned: What did we learn?
- Lacked: What was missing?
- Longed for: What do we wish we had?

SAILBOAT:
- Wind (what pushed us forward)
- Anchor (what held us back)
- Rocks (risks ahead)
- Island (our goal)

MAD/SAD/GLAD:
- Mad: What frustrated us?
- Sad: What disappointed us?
- Glad: What made us happy?

OUTPUT:
- 1-3 specific action items
- Owners assigned
- Review at next retro
```

### Sprint Backlog Management
```
BACKLOG ITEM STATES:
To Do → In Progress → In Review → Done

DEFINITION OF READY (DoR):
Item is ready for sprint when:
□ User story written with acceptance criteria
□ Dependencies identified
□ Estimated by team
□ Small enough for one sprint
□ No blockers

DEFINITION OF DONE (DoD):
Item is done when:
□ Code complete
□ Code reviewed
□ Unit tests written and passing
□ Integration tests passing
□ Documentation updated
□ Deployed to staging
□ PO accepted
```

---

## User Story Best Practices

### Story Format
```
AS A [user type]
I WANT TO [action]
SO THAT [benefit]

ACCEPTANCE CRITERIA:
Given [context]
When [action]
Then [result]
```

### INVEST Criteria
```
I - Independent: Can be developed separately
N - Negotiable: Details can be discussed
V - Valuable: Delivers value to user
E - Estimable: Team can estimate effort
S - Small: Fits in a sprint
T - Testable: Can verify it works
```

### Story Splitting Techniques
```
When story is too big, split by:

1. WORKFLOW STEPS
   "User can checkout" →
   - User can add payment method
   - User can review order
   - User can confirm purchase

2. BUSINESS RULES
   "User can search" →
   - Basic search
   - Search with filters
   - Search with sorting

3. OPERATIONS (CRUD)
   "Manage contacts" →
   - Add contact
   - View contacts
   - Edit contact
   - Delete contact

4. HAPPY/UNHAPPY PATHS
   "User can login" →
   - Successful login
   - Failed login (wrong password)
   - Account locked

5. INPUT METHODS
   "User can upload file" →
   - Upload from computer
   - Upload from URL
   - Drag and drop
```

---

## Estimation

### Story Points
```
WHAT THEY MEASURE:
- Complexity
- Uncertainty
- Effort
- NOT time

FIBONACCI SCALE:
1, 2, 3, 5, 8, 13, 21

1 = Trivial (text change)
2 = Simple (well-understood small task)
3 = Moderate (some complexity)
5 = Complex (multiple components)
8 = Very complex (significant work)
13 = Epic-level (probably should split)
21 = Too big (definitely split)

PLANNING POKER:
1. PO reads story
2. Team discusses
3. Everyone votes simultaneously
4. Discuss outliers
5. Re-vote if needed
6. Agree on estimate
```

### Velocity
```
VELOCITY = Story points completed per sprint

CALCULATING:
- Track completed points each sprint
- Use average of last 3-5 sprints
- Don't count incomplete stories

USING VELOCITY:
Sprint capacity = Velocity × (available days / sprint days)

EXAMPLE:
Average velocity: 40 points
Team has 8 of 10 days available
Capacity: 40 × (8/10) = 32 points

DON'T:
- Compare velocity across teams
- Use velocity as a performance metric
- Pressure team to increase velocity
```

---

## Kanban (Alternative/Complement)

### Kanban Principles
```
1. Visualize work
2. Limit work in progress (WIP)
3. Manage flow
4. Make policies explicit
5. Implement feedback loops
6. Improve collaboratively

KANBAN VS SCRUM:
| Aspect | Scrum | Kanban |
|--------|-------|--------|
| Cadence | Fixed sprints | Continuous |
| Roles | PO, SM, Team | Flexible |
| Change | End of sprint | Anytime |
| WIP Limits | Sprint capacity | Per column |
| Estimation | Story points | Optional |
```

### Kanban Board Setup
```
BASIC COLUMNS:
Backlog → To Do → In Progress → Review → Done

WITH WIP LIMITS:
| Backlog | To Do (5) | In Progress (3) | Review (2) | Done |

WIP LIMIT GUIDELINES:
- Start with team size + 1
- Adjust based on flow
- When limit hit, focus on finishing before starting
```

### Flow Metrics
```
LEAD TIME:
Time from request to delivery
- Measures responsiveness to customer

CYCLE TIME:
Time from work started to done
- Measures process efficiency

THROUGHPUT:
Items completed per time period
- Measures capacity

WORK IN PROGRESS:
Items currently being worked
- Should match WIP limits
```

---

## Scaling Agile

### SAFe (Scaled Agile Framework)
```
LEVELS:
1. Team Level: Scrum/Kanban teams
2. Program Level: Agile Release Train (ART)
3. Large Solution: Multiple ARTs
4. Portfolio: Strategy and investment

KEY CONCEPTS:
- PI (Program Increment): 8-12 week planning cycle
- ART: 5-12 teams working together
- PI Planning: 2-day event to align teams
- Inspect & Adapt: End of PI retrospective
```

### Spotify Model
```
SQUADS: Small, cross-functional teams (like Scrum teams)
TRIBES: Collection of squads in same area
CHAPTERS: People with same skills across squads
GUILDS: Communities of interest across organization

PRINCIPLES:
- Autonomy over alignment
- High trust environment
- Fail fast, learn fast
```

---

## Retrospective Activities

### Quick Retro Formats
```
PLUS/DELTA (15 min):
+ What went well?
Δ What would we change?

ONE WORD (10 min):
Each person shares one word to describe sprint.
Discuss themes that emerge.

DOT VOTING (20 min):
1. Everyone writes issues on stickies
2. Group similar items
3. Everyone gets 3 dots to vote
4. Discuss top voted items
```

### Deeper Retrospectives
```
TIMELINE (45 min):
1. Draw sprint timeline on wall
2. Add events (good/bad) as stickies
3. Discuss patterns
4. Identify actions

5 WHYS (30 min):
For each problem:
Why did X happen? → Because Y
Why did Y happen? → Because Z
(Continue until root cause found)

STARFISH (45 min):
- Keep doing (center)
- Less of (shrinking)
- More of (growing)
- Stop doing (one arm)
- Start doing (other arm)
```

### Retrospective Anti-Patterns
```
AVOID:
✗ Same format every time (gets stale)
✗ No action items
✗ Action items never followed up
✗ Blame sessions
✗ Manager dominates discussion
✗ Same people always talk
✗ Skipping when "things are fine"

ENSURE:
✓ Safe space (Vegas rule)
✓ Everyone participates
✓ Concrete actions with owners
✓ Follow up on previous actions
✓ Vary the format
✓ Celebrate wins
```

---

## Agile Metrics Dashboard
```markdown
## Sprint Dashboard

### Velocity
| Sprint | Committed | Completed | Velocity |
|--------|-----------|-----------|----------|
| S1 | 40 | 35 | 35 |
| S2 | 38 | 38 | 38 |
| S3 | 42 | 40 | 40 |
**Average: 38**

### Sprint Burndown
[Chart showing remaining work vs. time]

### Cumulative Flow
[Chart showing work items in each state over time]

### Cycle Time
Average: X days
Target: Y days

### Sprint Health
- Scope changes: 0-2 ✓
- Unfinished stories: 0-1 ✓
- Blockers resolved: All ✓
- Team happiness: 4/5 ✓
```
