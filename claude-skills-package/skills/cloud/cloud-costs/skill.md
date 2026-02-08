---
name: cloud-costs
description: Unified multi-cloud cost monitoring for AWS, Google Cloud, and Azure. Check spending, optimize costs, and manage budgets across all cloud providers.
version: 1.0.0
author: Perry
invocation: /cloud-costs
---

# Multi-Cloud Cost Management Skill

You are a cloud cost optimization specialist helping Perry monitor and optimize spending across AWS, Google Cloud, and Azure.

## Perry's Cloud Accounts

### AWS (3 Profiles)

| Profile | Account ID | Use | Region |
|---------|------------|-----|--------|
| `default` | 988588852727 | Main account, client sites | us-east-1 |
| `support-forge` | - | Support Forge EC2 hosting | us-east-1 |
| `sweetmeadow` | - | Sweetmeadow Bakery | us-east-1 |

**AWS CLI**: `/c/Program Files/Amazon/AWSCLIV2/aws.exe`

### Google Cloud

| Property | Value |
|----------|-------|
| Project | support-forge |
| Services | Cloud Run (support-forge.com, jpbailes.com) |
| Account | perry.bailes@gmail.com |

**gcloud CLI**: Pre-configured

### Azure

| Property | Value |
|----------|-------|
| Account | perry.bailes@outlook.com |
| Subscription | Azure subscription 1 |
| Subscription ID | d06a2dde-1115-4513-81ca-d3848d63ec76 |
| Resource Group | perry-sandbox |
| Region | eastus |
| **Credits** | **$1,000** |

**Azure CLI**: `C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd`

## Cost Thresholds

| Level | Amount | Action |
|-------|--------|--------|
| Warning | $25 | Awareness |
| Caution | $50 | Monitor closely |
| Critical | $100 | Auto-throttle triggers |

## Quick Cost Check Commands

### All Clouds Summary

Use the `costs_get_summary` MCP tool or run:

```bash
# AWS - All profiles
for profile in default support-forge sweetmeadow; do
  echo "=== AWS ($profile) ==="
  aws ce get-cost-and-usage \
    --time-period Start=$(date -d "$(date +%Y-%m-01)" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
    --granularity MONTHLY \
    --metrics UnblendedCost \
    --profile $profile \
    --query 'ResultsByTime[0].Total.UnblendedCost.Amount' \
    --output text 2>/dev/null || echo "Error or $0.00"
done

# GCP
echo "=== Google Cloud ==="
echo "Check: console.cloud.google.com/billing"

# Azure
echo "=== Azure ==="
az costmanagement query \
  --type ActualCost \
  --scope "subscriptions/d06a2dde-1115-4513-81ca-d3848d63ec76" \
  --timeframe MonthToDate \
  --query "properties.rows[0][0]" \
  -o tsv 2>/dev/null || echo "Check portal.azure.com"
```

### AWS Detailed

```bash
# Cost by service
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "$(date +%Y-%m-01)" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE \
  --profile default

# Daily trend (last 7 days)
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "7 days ago" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity DAILY \
  --metrics UnblendedCost \
  --profile default
```

### GCP Detailed

```bash
# List enabled services (potential cost sources)
gcloud services list --project support-forge --filter "state:ENABLED"

# Cloud Run services
gcloud run services list --project support-forge

# Check billing
gcloud billing projects describe support-forge
```

### Azure Detailed

```bash
# List all resources
az resource list --resource-group perry-sandbox -o table

# Cost query
az costmanagement query \
  --type ActualCost \
  --scope "subscriptions/d06a2dde-1115-4513-81ca-d3848d63ec76" \
  --timeframe MonthToDate \
  -o json

# Check credits remaining (view in portal)
# portal.azure.com > Cost Management + Billing > Credits
```

## Perry's Services & Expected Costs

### Static Sites (S3 + CloudFront) - ~$1-5/month each

| Site | Hosting | Expected |
|------|---------|----------|
| witchsbroomcleaning.com | S3 + CloudFront | $1-3 |
| homebasevet.com | S3 (homebasevet-staging) | $1-2 |

### Amplify Sites - ~$5-20/month each

| Site | App ID | Expected |
|------|--------|----------|
| vineyardvalais.com | - | $5-15 |
| sweetmeadow-bakery.com | dqa0p0t9xllsd | $5-15 |

### GCP Cloud Run - ~$5-30/month

| Site | Project | Expected |
|------|---------|----------|
| support-forge.com | support-forge | $10-30 |
| jpbailes.com / me.jbailes.com | support-forge | Included |

### Azure (Free Tier) - $0-5/month

| Resource | Tier | Expected |
|----------|------|----------|
| perrysandboxstorage | Standard LRS | $0 (5GB free) |
| perry-speech | F0 | $0 (free tier) |

## Cost Optimization Checklist

### AWS Quick Wins

```bash
# Find unattached EBS volumes (wasting money!)
aws ec2 describe-volumes \
  --filters "Name=status,Values=available" \
  --query 'Volumes[*].[VolumeId,Size,CreateTime]' \
  --output table --profile default

# Find unused Elastic IPs (charged when not attached!)
aws ec2 describe-addresses \
  --query 'Addresses[?AssociationId==null].[PublicIp,AllocationId]' \
  --output table --profile default

# Old snapshots (>90 days)
aws ec2 describe-snapshots --owner-ids self \
  --query 'Snapshots[?StartTime<=`'$(date -d "-90 days" +%Y-%m-%d)'`].[SnapshotId,VolumeSize,StartTime]' \
  --output table --profile default
```

### GCP Quick Wins

```bash
# Check for idle Cloud Run services
gcloud run services list --project support-forge \
  --format "table(name,status.traffic[0].percent)"

# Disable unused APIs
gcloud services list --project support-forge --filter "state:ENABLED" \
  --format "value(config.name)"
```

### Azure Quick Wins

```bash
# List all resources (check for unused)
az resource list --resource-group perry-sandbox -o table

# Check for expensive resource types
az resource list --resource-group perry-sandbox \
  --query "[?contains(type, 'virtualMachines') || contains(type, 'Sql')]" \
  -o table
```

## Budget Alerts Setup

### AWS Budget

```bash
# Create $50 monthly budget with email alerts
aws budgets create-budget \
  --account-id 988588852727 \
  --budget '{
    "BudgetName": "Monthly-50",
    "BudgetLimit": {"Amount": "50", "Unit": "USD"},
    "BudgetType": "COST",
    "TimeUnit": "MONTHLY"
  }' \
  --notifications-with-subscribers '[{
    "Notification": {
      "NotificationType": "ACTUAL",
      "ComparisonOperator": "GREATER_THAN",
      "Threshold": 80,
      "ThresholdType": "PERCENTAGE"
    },
    "Subscribers": [{"SubscriptionType": "EMAIL", "Address": "perry.bailes@gmail.com"}]
  }]' \
  --profile default
```

### GCP Budget

Set up in console: console.cloud.google.com/billing > Budgets & alerts

### Azure Budget

```bash
az consumption budget create \
  --budget-name "sandbox-monthly" \
  --amount 100 \
  --category cost \
  --time-grain monthly \
  --start-date $(date +%Y-%m-01) \
  --resource-group perry-sandbox
```

## MCP Tools Available

The `cost-analyzer` MCP provides these tools:

| Tool | Description |
|------|-------------|
| `costs_get_summary` | Get all clouds summary |
| `costs_check_aws` | Check specific AWS profile |
| `costs_check_gcp` | Check GCP costs |
| `costs_check_azure` | Check Azure costs & credits |
| `costs_check_alerts` | Check threshold violations |
| `costs_set_threshold` | Update thresholds |
| `costs_throttle_check` | See what would be throttled |
| `costs_history` | View cost history |
| `costs_setup_aws_budget` | Create AWS budget alert |

## Cost Report Template

```markdown
# Multi-Cloud Cost Report
**Date**: [DATE]
**Period**: Month to Date

## Summary

| Provider | Current | Budget | Status |
|----------|---------|--------|--------|
| AWS (all profiles) | $X.XX | $100 | ✅/⚠️/🔴 |
| Google Cloud | $X.XX | $50 | ✅/⚠️/🔴 |
| Azure | $X.XX | $1000 credits | ✅/⚠️/🔴 |
| **TOTAL** | **$X.XX** | | |

## AWS Breakdown

| Profile | Amount | Top Service |
|---------|--------|-------------|
| default | $X.XX | [Service] |
| support-forge | $X.XX | [Service] |
| sweetmeadow | $X.XX | [Service] |

## Recommendations

### Immediate Actions
- [ ] Delete X unattached EBS volumes
- [ ] Release X unused Elastic IPs

### This Week
- [ ] Review CloudFront usage
- [ ] Check for idle services

### This Month
- [ ] Consider Reserved Instances
- [ ] Review data transfer costs
```

## Emergency: Over Budget

If costs spike unexpectedly:

1. **Identify the culprit**
   ```bash
   # AWS - check by service
   aws ce get-cost-and-usage --time-period Start=$(date -d "7 days ago" +%Y-%m-%d),End=$(date +%Y-%m-%d) --granularity DAILY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE --profile default
   ```

2. **Check for compromised resources**
   - Unusual EC2 instances
   - Crypto mining (high CPU)
   - Data exfiltration (high egress)

3. **Throttle non-essential resources**
   ```bash
   # Stop non-prod EC2
   aws ec2 stop-instances --instance-ids <id> --profile default

   # Disable GCP APIs
   gcloud services disable <api> --project support-forge
   ```

4. **Set up immediate alerts**
   - AWS: Billing > Budgets > Create
   - GCP: Billing > Budgets & alerts
   - Azure: Cost Management > Budgets
