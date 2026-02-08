---
name: incident-response
description: Runbook for diagnosing and resolving website downtime, server issues, and deployment failures. Quick triage steps for Perry's client sites.
version: 1.0.0
author: Perry
---

# Incident Response Skill

You are a site reliability engineer helping Perry quickly diagnose and resolve incidents affecting his websites.

## Perry's Site Infrastructure

| Site | Type | Host | Quick Check |
|------|------|------|-------------|
| support-forge.com | EC2 Docker | {LEGACY_EC2_IP} | `ssh -i ~/.ssh/support-forge-key.pem ubuntu@{LEGACY_EC2_IP}` |
| vineyardvalais.com | Amplify | dq... | `aws amplify list-apps` |
| witchsbroomcleaning.com | S3/CloudFront | S3 | `aws s3 ls s3://witchsbroomcleaning.com` |
| sweetmeadow-bakery.com | Amplify | dqa0p0t9xllsd | `aws amplify get-app --app-id dqa0p0t9xllsd --profile sweetmeadow` |
| homebasevet.com | S3 | homebasevet-staging | `aws s3 ls s3://homebasevet-staging` |

## Incident Triage Flowchart

```
Site Down?
    │
    ├─→ Can you reach the domain? (ping/curl)
    │       │
    │       ├─ No → DNS issue or server unreachable
    │       │       → Check Route53/GoDaddy DNS
    │       │       → Check if server is running
    │       │
    │       └─ Yes but error → Application issue
    │               → Check error code (502, 503, 500)
    │               → Check application logs
    │
    └─→ Is it slow?
            │
            ├─ Yes → Performance issue
            │       → Check server resources (CPU, memory)
            │       → Check database connections
            │       → Check CDN status
            │
            └─ No → Specific feature broken
                    → Check browser console
                    → Check API endpoints
                    → Check recent deployments
```

## Quick Diagnostic Commands

### Step 1: Is it reachable?

```bash
# Basic connectivity
ping -c 3 support-forge.com
curl -I https://support-forge.com
curl -sS -o /dev/null -w "%{http_code}" https://support-forge.com

# DNS resolution
nslookup support-forge.com
dig support-forge.com

# SSL certificate check
echo | openssl s_client -servername support-forge.com -connect support-forge.com:443 2>/dev/null | openssl x509 -noout -dates
```

### Step 2: Server Status (EC2 - Support Forge)

```bash
# SSH into server
ssh -i ~/.ssh/support-forge-key.pem ubuntu@{LEGACY_EC2_IP}

# Once connected:
# Check Docker containers
docker ps -a
docker logs web --tail 100

# Check resources
htop
df -h
free -m

# Check recent deployments
docker-compose logs --tail 50

# Restart if needed
cd /home/ubuntu/support-forge-app
docker-compose restart web
```

### Step 3: Amplify Status

```bash
# List recent builds
aws amplify list-jobs --app-id <app-id> --branch-name main --max-items 5

# Get build logs
aws amplify get-job --app-id <app-id> --branch-name main --job-id <job-id>

# Trigger redeploy
aws amplify start-job --app-id <app-id> --branch-name main --job-type RELEASE
```

### Step 4: S3/CloudFront Status

```bash
# Check S3 bucket
aws s3 ls s3://bucket-name --recursive | head -20

# Check CloudFront distribution
aws cloudfront list-distributions --query 'DistributionList.Items[*].[Id,DomainName,Status]'

# Invalidate CloudFront cache (if stale content)
aws cloudfront create-invalidation --distribution-id <dist-id> --paths "/*"
```

## Error Code Quick Reference

| Code | Meaning | Likely Cause | Fix |
|------|---------|--------------|-----|
| 500 | Internal Server Error | Application crash, bad code | Check app logs |
| 502 | Bad Gateway | Backend not responding | Restart container/server |
| 503 | Service Unavailable | Server overloaded | Scale up or restart |
| 504 | Gateway Timeout | Backend too slow | Check DB, increase timeout |
| 403 | Forbidden | Permissions issue | Check S3 policy, file permissions |
| 404 | Not Found | Missing file/route | Check deployment, routing |
| SSL Error | Certificate issue | Expired/misconfigured cert | Renew cert, check ACM |

## Incident Response Template

```markdown
# Incident Report: [Site Name]

## Timeline
- **Detected**: [Time] by [who/how]
- **Acknowledged**: [Time]
- **Resolved**: [Time]
- **Total Duration**: [X] minutes

## Impact
- **Affected**: [What users/functionality]
- **Severity**: [Critical/High/Medium/Low]

## Root Cause
[Brief description of what caused the incident]

## Resolution
[Steps taken to resolve]

## Action Items
- [ ] [Preventive measure 1]
- [ ] [Preventive measure 2]
```

## Common Scenarios

### Scenario 1: Support Forge is down

```bash
# 1. Check if reachable
curl -I https://support-forge.com

# 2. SSH in
ssh -i ~/.ssh/support-forge-key.pem ubuntu@{LEGACY_EC2_IP}

# 3. Check Docker
docker ps -a
# If container is stopped/restarting:
docker logs web --tail 100

# 4. Restart
cd ~/support-forge-app
docker-compose down
docker-compose up -d

# 5. Verify
curl -I https://support-forge.com
```

### Scenario 2: Amplify build failing

```bash
# 1. Check build status
aws amplify list-jobs --app-id <app-id> --branch-name main --max-items 3

# 2. Get error details
aws amplify get-job --app-id <app-id> --branch-name main --job-id <job-id> \
  --query 'job.steps[?status==`FAILED`]'

# 3. Common fixes:
# - Check package.json for dependency issues
# - Verify environment variables in Amplify console
# - Check build settings in amplify.yml

# 4. Trigger rebuild
aws amplify start-job --app-id <app-id> --branch-name main --job-type RELEASE
```

### Scenario 3: SSL Certificate expired

```bash
# 1. Check certificate expiry
echo | openssl s_client -servername domain.com -connect domain.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# 2. If using ACM (Amplify/CloudFront):
aws acm list-certificates --query 'CertificateSummaryList[*].[DomainName,Status]'

# ACM auto-renews, but may need validation
aws acm describe-certificate --certificate-arn <arn> --query 'Certificate.DomainValidationOptions'

# 3. If using Let's Encrypt on EC2:
sudo certbot renew
sudo systemctl reload nginx
```

### Scenario 4: Site slow/high latency

```bash
# 1. Check response time
curl -o /dev/null -s -w 'Total: %{time_total}s\nTTFB: %{time_starttransfer}s\n' https://site.com

# 2. On server - check resources
ssh user@server
htop  # CPU/Memory
iostat -x 1 5  # Disk I/O
netstat -tuln  # Connection count

# 3. Check database (if applicable)
# PostgreSQL:
psql -c "SELECT * FROM pg_stat_activity WHERE state = 'active';"

# 4. Check for runaway processes
ps aux --sort=-%mem | head -10
ps aux --sort=-%cpu | head -10
```

## Monitoring Setup (TODO)

### Quick Health Check Script

```bash
#!/bin/bash
# save as ~/scripts/site-health.sh

SITES=(
  "https://support-forge.com"
  "https://vineyardvalais.com"
  "https://witchsbroomcleaning.com"
  "https://sweetmeadow-bakery.com"
  "https://homebasevet.com"
)

for site in "${SITES[@]}"; do
  status=$(curl -o /dev/null -s -w "%{http_code}" "$site")
  if [ "$status" != "200" ]; then
    echo "❌ $site - Status: $status"
  else
    echo "✅ $site - OK"
  fi
done
```

## Emergency Contacts

- **AWS Support**: Console → Support Center
- **GoDaddy DNS**: https://dcc.godaddy.com
- **Amplify Console**: https://console.aws.amazon.com/amplify/
- **CloudFront**: https://console.aws.amazon.com/cloudfront/

## Post-Incident Checklist

- [ ] Incident documented
- [ ] Client notified (if applicable)
- [ ] Root cause identified
- [ ] Preventive measures planned
- [ ] Monitoring improved (if gap found)
