# 🕵️ NEXUS OSINT v2.0
## Most Powerful Python OSINT Framework

**Advanced Open Source Intelligence Framework** for comprehensive reconnaissance across multiple platforms and services.

### ⚡ Features

#### Domain Intelligence
- ✅ DNS Enumeration (A, AAAA, MX, TXT, NS, CNAME, SOA)
- ✅ WHOIS Lookup & Domain Registration Data
- ✅ SSL/TLS Certificate Analysis & Extraction
- ✅ Subdomain Enumeration (1000+ common subdomains)
- ✅ Certificate Transparency Logs
- ✅ DNS History & Changes

#### Network Intelligence
- ✅ Fast Port Scanner (async)
- ✅ IP Geolocation & ASN Lookup
- ✅ Traceroute & Network Mapping
- ✅ ISP & Organization Information
- ✅ Autonomous System Analysis
- ✅ Network Range Discovery

#### Social Media Reconnaissance
- ✅ Username Search (100+ platforms)
- ✅ Social Profile Discovery
- ✅ Account Enumeration
- ✅ Profile Data Extraction
- ✅ Cross-platform Account Linking
- ✅ Platforms: GitHub, Twitter, Instagram, LinkedIn, Reddit, TikTok, YouTube, and more

#### Email Intelligence
- ✅ Email Format Validation
- ✅ Email Verification
- ✅ Breach Database Checking (HaveIBeenPwned)
- ✅ Email Harvesting from Web
- ✅ SMTP Server Enumeration

#### Web Intelligence
- ✅ Website Content Scraping
- ✅ Link Extraction & Analysis
- ✅ Metadata Extraction (Title, Description, Keywords, OG tags)
- ✅ Technology Detection (Wappalyzer-like)
- ✅ Email & Phone Number Extraction from Pages
- ✅ Social Media Link Discovery

#### GitHub Intelligence
- ✅ User Profile Analysis
- ✅ Repository Enumeration
- ✅ Commit History Analysis
- ✅ Sensitive File Detection
- ✅ Code Search & Pattern Matching
- ✅ Organization Analysis

#### Metadata Extraction
- ✅ Image EXIF/IPTC Data
- ✅ PDF Metadata & Content
- ✅ Office Document Analysis
- ✅ File Hash Analysis
- ✅ Steganography Detection (basic)

#### Threat Intelligence
- ✅ URLScan.io Integration
- ✅ VirusTotal Integration
- ✅ Malware Analysis
- ✅ Phishing Detection
- ✅ IP Reputation Checks
- ✅ Known Exploit Database

#### Data Analysis
- ✅ Anomaly Detection (ML)
- ✅ Pattern Recognition
- ✅ Timeline Analysis
- ✅ Connection Mapping
- ✅ Data Correlation

#### Caching & Database
- ✅ Local JSON Caching
- ✅ SQLite Integration
- ✅ PostgreSQL Support
- ✅ Smart TTL Management
- ✅ Batch Processing

---

### 📋 Supported Platforms

| Platform | Status | Notes |
|----------|--------|-------|
| **Kali Linux** | ✅ Full Support | Recommended for security testing |
| **Ubuntu 20.04+** | ✅ Full Support | Works on desktop and server |
| **Debian** | ✅ Full Support | Compatible with Debian-based distros |
| **Termux (Android)** | ✅ Full Support | Mobile OSINT reconnaissance |
| **Windows 10/11** | ✅ Full Support | Batch launcher included |
| **macOS** | ✅ Full Support | Requires Homebrew |

---

### 🚀 Quick Installation

#### 1. Clone Repository
```bash
git clone https://github.com/ur-rexy/nexus-osint.git
cd nexus-osint
```

#### 2. Run Installation Script
```bash
# Linux/macOS/Termux
python3 install.py

# Windows
python install.py
```

#### 3. Activate Virtual Environment
```bash
# Linux/macOS/Termux
source nexus_env/bin/activate

# Windows
nexus_env\Scripts\activate
```

#### 4. Start Using
```bash
# Domain reconnaissance
python3 osint_framework.py --domain example.com --full

# Save results
python3 osint_framework.py --domain example.com --full --save results.json
```

---

### 📖 Usage Examples

#### Domain Reconnaissance
```bash
# Complete domain analysis
python3 osint_framework.py --domain example.com --full

# DNS enumeration only
python3 osint_framework.py --domain example.com --dns

# SSL certificate analysis
python3 osint_framework.py --domain example.com --ssl

# Subdomain enumeration
python3 osint_framework.py --domain example.com --subdomains
```

#### Network Reconnaissance
```bash
# Complete network analysis
python3 osint_framework.py --ip 8.8.8.8 --full

# Port scanning
python3 osint_framework.py --ip 192.168.1.1 --ports

# IP geolocation
python3 osint_framework.py --ip 1.1.1.1 --geo

# Traceroute
python3 osint_framework.py --ip 8.8.8.8 --trace
```

#### Social Media Reconnaissance
```bash
# Search username across 100+ platforms
python3 osint_framework.py --username john_doe --full

# Save to file
python3 osint_framework.py --username hacker --full --save hacker_profile.json
```

#### Email Intelligence
```bash
# Email verification and breach checking
python3 osint_framework.py --email user@example.com --full

# Check if email is breached
python3 osint_framework.py --email admin@company.com --full
```

#### Web Scraping
```bash
python3 osint_framework.py --url https://example.com --metadata
python3 osint_framework.py --url https://example.com --links
python3 osint_framework.py --url https://example.com --tech-detect
```

---

### ⚙️ Configuration

Edit `config.json` to add your API keys:

```json
{
  "api_keys": {
    "github_token": "ghp_xxxxxxxxxxxx",
    "virustotal_api": "xxxxxxxxxxxxxxxx",
    "shodan_api": "xxxxxxxxxxxxxxxx",
    "censys_uid": "xxxxxxxxxxxx",
    "twitter_bearer_token": "AAAAAxxxxxxx"
  },
  "proxy": {
    "enabled": false,
    "url": "http://127.0.0.1:8080"
  },
  "settings": {
    "timeout": 10,
    "max_threads": 10,
    "cache_enabled": true
  }
}
```

**Supported APIs:**
- GitHub API (free tier available)
- VirusTotal (free tier: 4 requests/min)
- Shodan (requires paid subscription)
- Censys (free tier available)
- HaveIBeenPwned (free)
- URLScan.io (free)

---

### 📊 Output Formats

All results are saved in JSON format with structure:
```json
{
  "target": "example.com",
  "timestamp": "2024-01-15T10:30:45.123456",
  "results": {
    "dns": {...},
    "ssl": {...},
    "subdomains": {...},
    "ports": {...},
    "geolocation": {...}
  }
}
```

---

### 🔧 Advanced Features

#### Batch Processing
```python
from osint_framework import NexusOSINT

async def batch_domain_scan():
    nexus = NexusOSINT()
    await nexus.initialize()
    
    domains = ['example.com', 'test.com', 'demo.org']
    for domain in domains:
        results = await nexus.full_domain_recon(domain)
        nexus.save_results(results, f"{domain}_report.json")
```

#### Custom Module Integration
```python
from advanced_modules import WebScrapingAndCrawling

async def custom_scan():
    scraper = WebScrapingAndCrawling()
    await scraper.setup()
    
    links = await scraper.extract_links('https://example.com')
    metadata = await scraper.extract_metadata('https://example.com')
```

#### Caching
```python
from advanced_modules import CacheManager

cache = CacheManager()

# Get cached data (24 hour default TTL)
data = cache.get('example.com')

# Set cache
cache.set('example.com', results_data)

# Clear specific cache
cache.clear('example.com')
```

---

### 🔒 Security & Ethical Considerations

**IMPORTANT:**
- ⚠️ Use only on systems you own or have explicit permission to test
- ⚠️ Respect robots.txt and terms of service
- ⚠️ Don't perform DoS/DDoS attacks
- ⚠️ Comply with local laws and regulations
- ⚠️ No illegal activity is permitted

This tool is for:
- ✅ Security research
- ✅ Penetration testing (with authorization)
- ✅ OSINT investigation
- ✅ Competitive analysis
- ✅ Bug bounty programs

---

### 📚 Module Documentation

#### DomainIntelligence
- `whois_lookup(domain)` - Get WHOIS data
- `dns_enumeration(domain)` - Enumerate DNS records
- `ssl_certificate_info(domain)` - Extract SSL info
- `subdomain_enumeration(domain)` - Find subdomains

#### NetworkIntelligence
- `port_scanner(target, ports)` - Scan open ports
- `ip_geolocation(ip)` - Get IP location info
- `traceroute(host)` - Trace network path

#### SocialMediaReconnaissance
- `username_search(username)` - Search across platforms

#### EmailIntelligence
- `email_verification(email)` - Validate email
- `breach_check(email)` - Check breach databases

#### WebScrapingAndCrawling
- `extract_links(url)` - Get all links
- `extract_metadata(url)` - Extract page metadata
- `technology_detection(url)` - Detect tech stack

#### GithubIntelligence
- `user_recon(username)` - Analyze GitHub user
- `search_sensitive_files(org)` - Find exposed data

---

### 🐛 Troubleshooting

**Issue: "No module named 'dnspython'"**
```bash
pip install dnspython
```

**Issue: "Connection timeout"**
- Check your internet connection
- Verify firewall settings
- Try enabling proxy in config.json

**Issue: "Permission denied on Linux"**
```bash
chmod +x nexus
./nexus --help
```

**Issue: "Certificate verification failed"**
```bash
# Windows - install certificates
pip install --upgrade certifi

# Or disable SSL verification (not recommended):
# Edit config.json and set ssl_verify: false
```

---

### 📊 Performance Tips

1. **Use Caching** - Reduce redundant requests
2. **Batch Processing** - Scan multiple targets efficiently
3. **Adjust Threads** - Increase max_threads for faster scanning
4. **Selective Modules** - Run only needed modules
5. **API Key Setup** - Premium APIs are faster

Example performance:
- Domain Recon: ~2-5 seconds
- Network Scan (30 ports): ~10-15 seconds
- Username Search (100 platforms): ~20-30 seconds
- Full Website Analysis: ~30-60 seconds

---

### 🤝 Contributing

Contributions welcome! Areas needed:
- Additional API integrations
- Performance optimizations
- New OSINT modules
- Bug fixes and improvements
- Documentation updates

---

### 📜 License

This tool is provided for educational and authorized security testing purposes only.

**Usage Policy:**
- Educational purposes: ✅ Allowed
- Authorized penetration testing: ✅ Allowed
- Bug bounty programs: ✅ Allowed
- Unauthorized access: ❌ Prohibited
- Illegal activities: ❌ Prohibited

---

### 📞 Support & Contact

**Issues & Bug Reports:**
- GitHub Issues: [Project Issues Page]
- Discord: [Invite Link]
- Email: ur.rexy@example.com

**Follow Updates:**
- YouTube: UR · Rexy
- Instagram: @ur.rexy
- Twitter: @urrexy_

---

### 🎯 Roadmap

**v2.0** (Current)
- ✅ Core OSINT modules
- ✅ Multi-platform support
- ✅ Advanced caching

**v2.1** (Planned)
- 🔲 Web UI dashboard
- 🔲 Advanced reporting
- 🔲 Mobile app
- 🔲 REST API server

**v3.0** (Future)
- 🔲 AI-powered analysis
- 🔲 Real-time monitoring
- 🔲 Graph visualization
- 🔲 Blockchain analysis

---

### ⭐ Star History

If you find this tool useful, please star the repository!

---

**Happy Hunting! 🕵️**

*Remember: Use this tool responsibly and ethically. Always get permission before testing systems you don't own.*
