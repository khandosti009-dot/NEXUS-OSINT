# 🚀 NEXUS OSINT Quick Start Guide

## 5-Minute Setup

### Step 1: Install
```bash
# Linux/macOS/Termux
python3 install.py

# Windows
python install.py
```

### Step 2: Activate
```bash
# Linux/macOS/Termux
source nexus_env/bin/activate

# Windows
nexus_env\Scripts\activate
```

### Step 3: Run
```bash
python3 osint_framework.py --domain example.com --full
```

---

## Command Reference

### Domain Reconnaissance
```bash
# Full domain recon
python3 osint_framework.py --domain example.com --full

# DNS only
python3 osint_framework.py --domain example.com --dns

# SSL analysis
python3 osint_framework.py --domain example.com --ssl

# Subdomains
python3 osint_framework.py --domain example.com --subdomains

# Save results
python3 osint_framework.py --domain example.com --full --save report.json
```

### Network Reconnaissance
```bash
# Full network recon
python3 osint_framework.py --ip 8.8.8.8 --full

# Port scan
python3 osint_framework.py --ip 192.168.1.1 --ports

# IP geolocation
python3 osint_framework.py --ip 1.1.1.1 --geo

# Traceroute
python3 osint_framework.py --ip google.com --trace

# All network checks
python3 osint_framework.py --ip 8.8.8.8 --ports --geo --trace
```

### Social Media Search
```bash
# Search username everywhere
python3 osint_framework.py --username john_doe --full

# With output
python3 osint_framework.py --username hacker123 --full --save accounts.json
```

### Email Intelligence
```bash
# Check email
python3 osint_framework.py --email user@example.com --full

# Breach check
python3 osint_framework.py --email admin@company.com --full
```

---

## Real-World Examples

### Scenario 1: Check a Competitor's Domain
```bash
python3 osint_framework.py \
  --domain competitor.com \
  --full \
  --save competitor_report.json
```

**What you get:**
- IP addresses & servers
- Subdomains
- SSL certificate info
- DNS records
- Hosting information

### Scenario 2: Find Email from LinkedIn Profile
```bash
# First: Get username
# Then: Search email patterns
python3 osint_framework.py --email firstname@company.com --full
```

### Scenario 3: Network Security Audit
```bash
# Scan your own server (with permission!)
python3 osint_framework.py \
  --ip your.server.ip \
  --full \
  --save security_audit.json
```

### Scenario 4: Hunt Similar Usernames
```bash
# Check multiple usernames
for username in admin admin1 admin123 administrator; do
  python3 osint_framework.py --username $username --full
done
```

### Scenario 5: Website Security Assessment
```bash
# Check website configuration
python3 osint_framework.py \
  --domain yoursite.com \
  --dns --ssl --subdomains \
  --save site_assessment.json
```

---

## Output Files

**Location:** `./results/` directory

**File Names:**
- `osint_results_YYYYMMDD_HHMMSS.json` - Auto-generated
- Custom name: `--save myreport.json`

**Contents:**
```json
{
  "domain": "example.com",
  "timestamp": "2024-01-15T10:30:45",
  "results": {
    "dns": { "A": ["1.2.3.4"], ... },
    "ssl": { "issuer": "...", ... },
    "subdomains": [ "www.example.com", ... ]
  }
}
```

---

## Common Errors & Fixes

### Error: "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or activate venv properly
source nexus_env/bin/activate
```

### Error: "Connection timeout"
```bash
# Check internet connection
ping google.com

# Try with longer timeout
# Edit config.json: "timeout": 15
```

### Error: "Permission denied"
```bash
# Make script executable
chmod +x nexus
chmod +x osint_framework.py

# Run with python explicitly
python3 osint_framework.py --domain example.com
```

### Error: "DNS resolution failed"
```bash
# Try with specific nameserver
# Or check config for DNS settings
```

---

## Tips & Tricks

### 1. Batch Processing
```bash
# Create domains.txt with one domain per line
while read domain; do
  python3 osint_framework.py --domain $domain --full --save "$domain.json"
done < domains.txt
```

### 2. Pipeline to Other Tools
```bash
# Export IPs for further scanning
python3 osint_framework.py --domain example.com --dns | \
  grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' > ips.txt
```

### 3. Monitor for Changes
```bash
# Run daily and compare
python3 osint_framework.py --domain example.com --dns --save dns_today.json

# Compare with yesterday
diff dns_today.json dns_yesterday.json
```

### 4. Filter Results with jq (if installed)
```bash
# Extract just subdomains
python3 osint_framework.py --domain example.com --subdomains | \
  jq '.results.subdomains.subdomains[]'

# Extract IPs
cat results.json | jq '.results.dns.A[]'
```

### 5. Parallel Scanning
```bash
# Scan multiple targets simultaneously
parallel python3 osint_framework.py --ip {} --full --save {}.json ::: 8.8.8.8 1.1.1.1 9.9.9.9
```

---

## API Keys Setup (Optional)

### GitHub
1. Go to: https://github.com/settings/tokens
2. Create token with `public_repo` scope
3. Add to config.json: `"github_token": "ghp_xxxx"`

### VirusTotal
1. Go to: https://www.virustotal.com
2. Create free account
3. Get API key from dashboard
4. Add to config.json: `"virustotal_api": "xxxx"`

### Shodan
1. Go to: https://www.shodan.io
2. Create account (free limited)
3. Get API key
4. Add to config.json: `"shodan_api": "xxxx"`

---

## Performance Tuning

### Faster Scanning
```json
// In config.json
{
  "settings": {
    "max_threads": 20,
    "timeout": 5,
    "cache_enabled": true
  }
}
```

### Better Accuracy
```json
{
  "settings": {
    "timeout": 15,
    "max_retries": 5,
    "verify_ssl": true
  }
}
```

---

## Next Steps

1. **Read Full Documentation:** `cat README.md`
2. **Configure API Keys:** Edit `config.json`
3. **Run First Scan:** `python3 osint_framework.py --help`
4. **Join Community:** Follow on Twitter/Instagram

---

## Need Help?

```bash
# Show all options
python3 osint_framework.py --help

# Show examples
python3 osint_framework.py --examples

# Check version
python3 osint_framework.py --version

# Enable debug mode
python3 osint_framework.py --debug --domain example.com
```

---

## License & Ethics

- ✅ Use only on systems you own or have permission for
- ✅ Respect terms of service of websites
- ✅ Follow local laws and regulations
- ❌ No unauthorized access
- ❌ No DoS/DDoS attacks

---

**Happy Hunting! 🕵️**

*Last Updated: January 2024*
