# Project Management PMP - PMBOK Certified Methodologies

## PMP/PMBOK Overview
```
PMBOK = Project Management Body of Knowledge
PMP = Project Management Professional (Certification)

PMBOK 7th Edition (2021):
- 12 Project Management Principles
- 8 Project Performance Domains
- Focus on value delivery
```

---

## Project Initiation

### Project Charter Template
```markdown
# Project Charter: [Project Name]

## Project Information
| Field | Value |
|-------|-------|
| Project Name | |
| Project Manager | |
| Sponsor | |
| Start Date | |
| Target End Date | |
| Budget | |

## Business Case
### Problem/Opportunity
[Why is this project needed?]

### Objectives
1. [Objective 1 - SMART]
2. [Objective 2 - SMART]

### Success Criteria
- [Measurable outcome 1]
- [Measurable outcome 2]

## Scope Overview
### In Scope
- [Deliverable 1]
- [Deliverable 2]

### Out of Scope
- [Exclusion 1]
- [Exclusion 2]

## High-Level Timeline
| Milestone | Target Date |
|-----------|-------------|
| Project Kickoff | |
| Phase 1 Complete | |
| Phase 2 Complete | |
| Go-Live | |
| Project Close | |

## Budget Summary
| Category | Estimate |
|----------|----------|
| Labor | $ |
| Technology | $ |
| External | $ |
| Contingency | $ |
| **Total** | **$** |

## Key Stakeholders
| Name | Role | Interest |
|------|------|----------|
| | | |

## Risks & Assumptions
### Key Risks
1. [Risk 1]

### Assumptions
1. [Assumption 1]

## Approvals
| Name | Role | Signature | Date |
|------|------|-----------|------|
| | Sponsor | | |
| | PM | | |
```

### Stakeholder Register
```markdown
## Stakeholder Register

| Name | Organization | Role | Interest | Influence | Strategy |
|------|--------------|------|----------|-----------|----------|
| [Name] | [Dept] | Sponsor | High | High | Manage Closely |
| [Name] | [Dept] | User | High | Low | Keep Informed |
| [Name] | [Dept] | IT Lead | Medium | High | Keep Satisfied |
| [Name] | [Dept] | Affected | Low | Low | Monitor |

### Stakeholder Matrix
        HIGH INFLUENCE
             │
  Keep       │   Manage
  Satisfied  │   Closely
─────────────┼─────────────
  Monitor    │   Keep
             │   Informed
             │
        LOW INFLUENCE
    LOW INTEREST ─────► HIGH INTEREST
```

---

## Scope Management

### Work Breakdown Structure (WBS)
```
WBS = Hierarchical decomposition of project scope

RULES:
- 100% Rule: Each level = 100% of parent
- Mutually exclusive (no overlap)
- Outcome-focused (deliverables, not activities)
- 3-4 levels deep typically

EXAMPLE WBS:
1.0 Website Redesign
├── 1.1 Project Management
│   ├── 1.1.1 Project Planning
│   ├── 1.1.2 Status Reporting
│   └── 1.1.3 Project Closure
├── 1.2 Discovery & Design
│   ├── 1.2.1 Requirements Gathering
│   ├── 1.2.2 Wireframes
│   └── 1.2.3 Visual Design
├── 1.3 Development
│   ├── 1.3.1 Frontend Development
│   ├── 1.3.2 Backend Development
│   └── 1.3.3 Integration
├── 1.4 Testing
│   ├── 1.4.1 Unit Testing
│   ├── 1.4.2 UAT
│   └── 1.4.3 Performance Testing
└── 1.5 Deployment
    ├── 1.5.1 Staging Deployment
    ├── 1.5.2 Production Deployment
    └── 1.5.3 Training
```

### Scope Statement Template
```markdown
## Project Scope Statement

### Project Objectives
[Specific, measurable outcomes]

### Deliverables
1. [Deliverable 1]
   - Description:
   - Acceptance Criteria:

2. [Deliverable 2]
   - Description:
   - Acceptance Criteria:

### Requirements
| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| R1 | | Must Have | |
| R2 | | Should Have | |

### Boundaries
**In Scope:**
- [Item]

**Out of Scope:**
- [Item]

### Constraints
- [Time, budget, resource constraints]

### Assumptions
- [Things assumed to be true]
```

---

## Schedule Management

### Creating the Schedule
```
STEPS:
1. Define activities (from WBS work packages)
2. Sequence activities (dependencies)
3. Estimate durations
4. Develop schedule (critical path)
5. Control schedule (ongoing)

DEPENDENCY TYPES:
FS - Finish to Start (most common)
    Task A must finish before Task B starts
FF - Finish to Finish
    Task A and B must finish together
SS - Start to Start
    Task A and B must start together
SF - Start to Finish (rare)
    Task A must start before Task B finishes
```

### Critical Path Method (CPM)
```
Critical Path = Longest path through network
              = Minimum project duration
              = Zero float activities

CALCULATING:
1. Forward Pass: Calculate Early Start (ES), Early Finish (EF)
2. Backward Pass: Calculate Late Start (LS), Late Finish (LF)
3. Float = LS - ES (or LF - EF)
4. Critical Path = Activities with Float = 0

EXAMPLE:
Task A: Duration 5 days, ES=0, EF=5
Task B: Duration 3 days, depends on A, ES=5, EF=8
Task C: Duration 4 days, depends on A, ES=5, EF=9
Task D: Duration 2 days, depends on B&C, ES=9, EF=11

Critical Path: A → C → D (11 days)
```

### Gantt Chart Elements
```
INCLUDE:
- Task name
- Duration
- Start/End dates
- Dependencies (arrows)
- Milestones (diamonds)
- Resource assignments
- Progress bars
- Critical path highlighting
- Today line

TOOLS:
- Microsoft Project
- Smartsheet
- TeamGantt
- Monday.com
- Asana Timeline
```

### Schedule Compression
```
CRASHING:
Adding resources to reduce duration
- Works on critical path activities
- Increases cost
- Diminishing returns

FAST TRACKING:
Doing activities in parallel that were planned sequentially
- Higher risk
- May cause rework
- Limited by dependencies

EXAMPLE:
Original: Design (10d) → Develop (20d) → Test (10d) = 40 days

Crashed: Add developers to reduce Develop to 15 days = 35 days

Fast-tracked: Start development before design complete = 32 days
(But may cause rework if design changes)
```

---

## Cost Management

### Estimation Techniques
```
ANALOGOUS (Top-Down):
Use similar past projects
- Quick but less accurate
- Good for early estimates

PARAMETRIC:
Use statistical relationships
- Cost per unit × number of units
- Example: $50/sq ft × 1000 sq ft = $50,000

BOTTOM-UP:
Estimate each work package, sum up
- Most accurate
- Most time-consuming

THREE-POINT:
(Optimistic + 4×Most Likely + Pessimistic) / 6
- Accounts for uncertainty
- PERT estimate
```

### Budget Template
```markdown
## Project Budget

| WBS | Category | Estimate | Contingency | Total |
|-----|----------|----------|-------------|-------|
| 1.1 | Project Management | $X | 10% | $X |
| 1.2 | Discovery & Design | $X | 15% | $X |
| 1.3 | Development | $X | 20% | $X |
| 1.4 | Testing | $X | 10% | $X |
| 1.5 | Deployment | $X | 15% | $X |
| | **Subtotal** | **$X** | | **$X** |
| | Management Reserve | | 10% | $X |
| | **TOTAL** | | | **$X** |

### Assumptions
- [Rate assumptions]
- [Duration assumptions]
- [Vendor assumptions]
```

### Earned Value Management (EVM)
```
KEY TERMS:
PV = Planned Value (Budgeted cost of work scheduled)
EV = Earned Value (Budgeted cost of work performed)
AC = Actual Cost (Actual cost of work performed)

VARIANCES:
SV = Schedule Variance = EV - PV
    Positive = ahead of schedule
    Negative = behind schedule

CV = Cost Variance = EV - AC
    Positive = under budget
    Negative = over budget

PERFORMANCE INDICES:
SPI = Schedule Performance Index = EV / PV
    >1 = ahead, <1 = behind

CPI = Cost Performance Index = EV / AC
    >1 = under budget, <1 = over budget

FORECASTS:
EAC = Estimate at Completion = BAC / CPI
ETC = Estimate to Complete = EAC - AC
VAC = Variance at Completion = BAC - EAC

EXAMPLE:
Project Budget (BAC): $100,000
Planned to date (PV): $50,000
Actually spent (AC): $55,000
Work completed worth (EV): $45,000

SV = $45K - $50K = -$5K (behind schedule)
CV = $45K - $55K = -$10K (over budget)
SPI = $45K / $50K = 0.9 (90% schedule efficiency)
CPI = $45K / $55K = 0.82 (82% cost efficiency)
EAC = $100K / 0.82 = $122K (projected total cost)
```

---

## Quality Management

### Quality Planning
```
QUALITY = Conformance to requirements
        = Fitness for use

COST OF QUALITY:
1. Prevention Costs (training, planning)
2. Appraisal Costs (testing, inspection)
3. Internal Failure (rework before delivery)
4. External Failure (warranty, returns)

PRINCIPLE: Invest in prevention to reduce failure costs
```

### Quality Metrics
```
DEFECT DENSITY: Defects per unit (e.g., per 1000 lines of code)
FIRST PASS YIELD: % passing quality check first time
CUSTOMER SATISFACTION: NPS, CSAT scores
ON-TIME DELIVERY: % of deliverables on schedule
REWORK RATE: % of work requiring revision
```

### Quality Checklist Template
```markdown
## Quality Checklist: [Deliverable]

### Before Review
□ Requirements documented
□ Acceptance criteria defined
□ Stakeholders identified

### During Development
□ Standards followed
□ Code/work reviewed
□ Tests created and passed

### Before Delivery
□ Acceptance criteria verified
□ Documentation complete
□ Training materials ready

### Sign-off
- Reviewed by: _______________
- Date: _______________
- Status: Pass / Fail / Conditional
```

---

## Change Management

### Change Control Process
```
1. SUBMIT: Change request documented
2. REVIEW: PM assesses impact
3. ANALYZE: Impact on scope, schedule, cost, quality
4. DECIDE: CCB approves/rejects/defers
5. IMPLEMENT: If approved, update plans
6. COMMUNICATE: Notify stakeholders
7. TRACK: Monitor implementation
```

### Change Request Template
```markdown
## Change Request

| Field | Value |
|-------|-------|
| CR Number | CR-XXX |
| Date Submitted | |
| Submitted By | |
| Priority | High/Medium/Low |

### Description of Change
[What is being requested?]

### Reason for Change
[Why is this needed?]

### Impact Analysis
| Area | Current | With Change | Impact |
|------|---------|-------------|--------|
| Scope | | | |
| Schedule | | | +X days |
| Cost | | | +$X |
| Quality | | | |
| Risk | | | |

### Options
1. Approve as-is
2. Approve with modifications
3. Defer
4. Reject

### Recommendation
[PM recommendation]

### Approvals
| Role | Name | Decision | Date |
|------|------|----------|------|
| PM | | | |
| Sponsor | | | |
| CCB | | | |
```

---

## Project Closure

### Closure Checklist
```markdown
## Project Closure Checklist

### Deliverable Acceptance
□ All deliverables completed
□ Acceptance signed by sponsor
□ Outstanding items documented

### Administrative Closure
□ Final status report issued
□ Budget reconciled
□ Contracts closed
□ Resources released

### Documentation
□ Project files archived
□ Lessons learned documented
□ Final report completed

### Celebration
□ Team recognized
□ Stakeholders thanked
```

### Lessons Learned Template
```markdown
## Lessons Learned: [Project Name]

### Project Summary
- Duration: [X months]
- Budget: $X (actual vs. planned)
- Team Size: [X]
- Final Status: [Completed/Partial]

### What Went Well
1. [Success 1 - what and why]
2. [Success 2 - what and why]

### What Could Be Improved
1. [Challenge 1 - what happened and recommendation]
2. [Challenge 2 - what happened and recommendation]

### Recommendations for Future Projects
1. [Recommendation]
2. [Recommendation]

### Key Metrics
| Metric | Planned | Actual |
|--------|---------|--------|
| Duration | | |
| Budget | | |
| Scope Changes | | |
| Defects | | |

### Team Feedback
[Summary of team retrospective]

### Stakeholder Feedback
[Summary of stakeholder input]
```
