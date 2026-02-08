---
name: invoice-generator
description: Generate professional invoices for client work. Supports hourly, fixed-price, and retainer billing with PDF export capability.
version: 1.0.0
author: Perry
---

# Invoice Generator Skill

You are a billing assistant helping Perry create professional invoices for his web development clients.

## Perry's Business Info

```
{YOUR_NAME}
Web Development Services
Email: {YOUR_EMAIL}
```

## Invoice Template (Markdown → PDF)

```markdown
# INVOICE

**Invoice #**: INV-[YYYY]-[###]
**Date**: [Invoice Date]
**Due Date**: [Due Date - typically Net 15 or Net 30]

---

**From:**
{YOUR_NAME}
Web Development Services
{YOUR_EMAIL}

**To:**
[Client Name]
[Client Company]
[Client Email]
[Client Address - if known]

---

## Project: [Project Name]

| Description | Quantity | Rate | Amount |
|-------------|----------|------|--------|
| [Line item 1] | [X hrs/units] | $[rate] | $[total] |
| [Line item 2] | [X hrs/units] | $[rate] | $[total] |
| [Line item 3] | [X hrs/units] | $[rate] | $[total] |

---

| | |
|---|---|
| **Subtotal** | $[subtotal] |
| **Tax (0%)** | $0.00 |
| **Total Due** | **$[total]** |

---

## Payment Details

**Payment Methods Accepted:**
- Venmo: @[handle]
- PayPal: {YOUR_EMAIL}
- Zelle: {YOUR_EMAIL}
- Check: Made payable to {YOUR_NAME}

**Terms**: Net [15/30] - Due by [Due Date]

---

*Thank you for your business!*
```

## Line Item Templates

### Hourly Work

```markdown
| Description | Hours | Rate | Amount |
|-------------|-------|------|--------|
| Website development - homepage | 4 | $100 | $400 |
| Website development - contact page | 2 | $100 | $200 |
| Bug fixes and revisions | 1.5 | $100 | $150 |
| Client meeting (Jan 15) | 0.5 | $100 | $50 |
```

### Fixed Price Project

```markdown
| Description | Quantity | Rate | Amount |
|-------------|----------|------|--------|
| Website design and development (5 pages) | 1 | $3,500 | $3,500 |
| SEO optimization setup | 1 | $500 | $500 |
| Content migration | 1 | $250 | $250 |
```

### Retainer/Maintenance

```markdown
| Description | Quantity | Rate | Amount |
|-------------|----------|------|--------|
| Monthly maintenance retainer - January 2026 | 1 | $300 | $300 |
| - Security updates and backups | included | - | - |
| - Content updates (up to 2 hours) | included | - | - |
| - Performance monitoring | included | - | - |
| Additional development work (3 hrs) | 3 | $75 | $225 |
```

### Milestone Billing

```markdown
| Description | Milestone | Rate | Amount |
|-------------|-----------|------|--------|
| Project: [Name] - Milestone 2 of 4 | 25% | $8,000 | $2,000 |
| - Design approval completed | ✓ | - | - |
| - Homepage development | ✓ | - | - |
| - Responsive implementation | ✓ | - | - |
```

## Invoice Number System

Format: `INV-YYYY-###`

Examples:
- `INV-2026-001` - First invoice of 2026
- `INV-2026-002` - Second invoice of 2026

Track invoices in a simple log:

```markdown
## Invoice Log 2026

| Invoice # | Date | Client | Amount | Status | Paid Date |
|-----------|------|--------|--------|--------|-----------|
| INV-2026-001 | 01/10 | Vineyard Valais | $1,500 | Paid | 01/18 |
| INV-2026-002 | 01/15 | Support Forge | $2,500 | Pending | - |
| INV-2026-003 | 01/20 | Witch's Broom | $300 | Pending | - |
```

## Standard Rate Card

| Service | Rate |
|---------|------|
| **Hourly Rate** | $75-125/hr |
| **Rush Rate** (< 48hr turnaround) | $150/hr |
| **Consulting/Strategy** | $125/hr |
| **Maintenance Retainer** | $200-500/mo |

| Project Type | Range |
|--------------|-------|
| Landing Page | $500-1,500 |
| Small Business Site (5-7 pages) | $2,000-5,000 |
| E-commerce Site | $5,000-15,000 |
| Custom Web Application | $10,000+ |
| Site Redesign | 60-80% of new build |

## Payment Terms

### Standard Terms

```markdown
**Net 15**: Payment due within 15 days of invoice date
**Net 30**: Payment due within 30 days of invoice date
```

### Late Payment Policy

```markdown
Invoices not paid within [30] days of the due date will incur a late fee of [1.5%] per month on the outstanding balance.
```

### Deposit Policy

```markdown
A [50%] deposit is required before work begins on fixed-price projects.
Remaining balance due upon project completion.
```

## Email Templates

### Sending Invoice

```markdown
Subject: Invoice INV-[####] - [Project Name]

Hi [Name],

Please find attached the invoice for [project/work description].

**Invoice #**: INV-[####]
**Amount Due**: $[amount]
**Due Date**: [date]

Payment can be made via:
- Venmo: @[handle]
- PayPal: {YOUR_EMAIL}
- Zelle: {YOUR_EMAIL}

Let me know if you have any questions!

Thanks,
Perry
```

### Payment Reminder (Friendly)

```markdown
Subject: Friendly Reminder - Invoice INV-[####]

Hi [Name],

Just a quick reminder that invoice INV-[####] for $[amount] was due on [date].

If you've already sent payment, please disregard this message. Otherwise, please let me know if you have any questions or need alternative payment arrangements.

Thanks!
Perry
```

### Payment Reminder (Past Due)

```markdown
Subject: Past Due Notice - Invoice INV-[####]

Hi [Name],

I wanted to follow up regarding invoice INV-[####] for $[amount], which was due on [date] and is now [X] days past due.

Please arrange payment at your earliest convenience. If there are any issues or you'd like to discuss payment arrangements, please let me know.

Best regards,
Perry
```

### Payment Received

```markdown
Subject: Payment Received - Thank You!

Hi [Name],

This confirms receipt of your payment of $[amount] for invoice INV-[####].

Thank you for your prompt payment! Looking forward to continuing to work with you.

Best,
Perry
```

## Quick Invoice Generation

When asked to create an invoice, gather:

1. **Client name and email**
2. **Project/work description**
3. **Line items with hours/quantities and rates**
4. **Payment terms** (Net 15, Net 30, etc.)
5. **Any notes or special terms**

Then generate:
1. Invoice in Markdown format
2. Optionally convert to PDF using document skills
3. Draft email to send with invoice

## Integration with Financial Models

Link to `/creating-financial-models` for:
- Revenue tracking
- Cash flow projections
- Client lifetime value
- Monthly recurring revenue from retainers
