# Advanced NEXUS OSINT Usage Guide

## Using as Python Library

### Import Core Module
```python
import asyncio
from osint_framework import NexusOSINT, DomainIntelligence, NetworkIntelligence

async def main():
    # Initialize framework
    nexus = NexusOSINT()
    await nexus.initialize()
    
    # Run reconnaissance
    results = await nexus.full_domain_recon('example.com')
    
    # Save results
    nexus.save_results(results, 'output.json')
    
    # Cleanup
    await nexus.cleanup()

# Run async function
asyncio.run(main())
```

---

## Advanced Module Examples

### 1. Custom Domain Analysis
```python
import asyncio
from osint_framework import DomainIntelligence

async def custom_domain_analysis():
    domain_intel = DomainIntelligence()
    await domain_intel.setup()
    
    domain = 'example.com'
    
    # Individual checks
    dns = await domain_intel.dns_enumeration(domain)
    ssl = await domain_intel.ssl_certificate_info(domain)
    whois = await domain_intel.whois_lookup(domain)
    subdomains = await domain_intel.subdomain_enumeration(domain)
    
    # Process results
    print(f"DNS Records: {dns}")
    print(f"SSL Issuer: {ssl['issuer']}")
    print(f"Subdomains Found: {len(subdomains['subdomains'])}")
    
    await domain_intel.cleanup()

asyncio.run(custom_domain_analysis())
```

### 2. Network Scanning
```python
import asyncio
from osint_framework import NetworkIntelligence

async def network_scan():
    net_intel = NetworkIntelligence()
    await net_intel.setup()
    
    target = '8.8.8.8'
    
    # Scan common ports
    ports = await net_intel.port_scanner(target, [80, 443, 22, 21, 3306, 5432])
    
    # Get location
    geo = await net_intel.ip_geolocation(target)
    
    # Trace route
    trace = await net_intel.traceroute(target)
    
    print(f"Open Ports: {ports['open_ports']}")
    print(f"Location: {geo['country']} - {geo['city']}")
    print(f"ASN: {geo['asn']}")
    
    await net_intel.cleanup()

asyncio.run(network_scan())
```

### 3. Social Media Reconnaissance
```python
import asyncio
from osint_framework import SocialMediaReconnaissance

async def social_recon():
    social = SocialMediaReconnaissance()
    await social.setup()
    
    username = 'john_doe'
    
    # Search across platforms
    results = await social.username_search(username)
    
    # Print found accounts
    print(f"Found {len(results['found_accounts'])} accounts:")
    for account in results['found_accounts']:
        print(f"  - {account['platform']}: {account['url']}")
    
    # Access all platform results
    for platform, data in results['detailed_results'].items():
        if data['found']:
            print(f"✓ {platform}: {data['url']}")
    
    await social.cleanup()

asyncio.run(social_recon())
```

---

## Using Advanced Modules

### Web Scraping and Crawling
```python
import asyncio
from advanced_modules import WebScrapingAndCrawling

async def web_analysis():
    scraper = WebScrapingAndCrawling()
    await scraper.setup()
    
    url = 'https://example.com'
    
    # Extract links and data
    links = await scraper.extract_links(url)
    metadata = await scraper.extract_metadata(url)
    tech = await scraper.technology_detection(url)
    
    print(f"Found {len(links['links'])} links")
    print(f"Emails: {links['emails']}")
    print(f"Phone Numbers: {links['phone_numbers']}")
    print(f"Technologies: {tech['technologies']}")
    
    await scraper.cleanup()

asyncio.run(web_analysis())
```

### Metadata Extraction
```python
from advanced_modules import MetadataExtraction

# Extract from image
image_meta = MetadataExtraction.extract_image_metadata('photo.jpg')
print(f"Image Size: {image_meta['size']}")
print(f"EXIF: {image_meta['exif']}")

# Extract from PDF
pdf_meta = MetadataExtraction.extract_pdf_metadata('document.pdf')
print(f"Pages: {pdf_meta['pages']}")
print(f"Author: {pdf_meta['metadata'].author}")

# Extract from Office documents
doc_meta = MetadataExtraction.extract_document_metadata('report.docx')
print(f"Title: {doc_meta['title']}")
print(f"Author: {doc_meta['author']}")
```

### GitHub Intelligence
```python
import asyncio
from advanced_modules import GithubIntelligence

async def github_recon():
    github = GithubIntelligence(api_token="your_github_token_here")
    await github.setup()
    
    # Analyze user
    user = await github.user_recon('torvalds')
    print(f"User: {user['name']}")
    print(f"Repos: {user['repositories']['count']}")
    
    # Search for sensitive files
    findings = await github.search_sensitive_files('torvalds')
    print(f"Potentially exposed files: {len(findings['findings'])}")
    
    await github.cleanup()

asyncio.run(github_recon())
```

### Anomaly Detection
```python
from advanced_modules import AnomalyDetection

# IP anomaly detection
ip_data = [
    {'ip': '1.1.1.1', 'org': 'Cloudflare', 'type': 'datacenter'},
    {'ip': '8.8.8.8', 'org': 'Google VPN', 'type': 'residential'},
    {'ip': '123.45.67.89', 'org': 'AWS', 'type': 'residential'},
]

anomalies = AnomalyDetection.detect_ip_anomalies(ip_data)
print(f"Anomalies found: {anomalies['anomalies_found']}")
for anomaly in anomalies['anomalies']:
    print(f"  - {anomaly['ip']}: {anomaly['anomaly']}")

# Domain anomaly detection
domain_data = {
    'domain': 'example.com',
    'dns': {
        'A': ['1.1.1.1', '2.2.2.2', '3.3.3.3', '4.4.4.4', '5.5.5.5', '6.6.6.6'],
        'NS': ['ns1.example.com', 'ns2.example.com', 'ns3.example.com', 'ns4.example.com', 'ns5.example.com']
    }
}

domain_anomalies = AnomalyDetection.detect_domain_anomalies(domain_data)
print(f"Domain anomalies: {domain_anomalies['anomalies']}")
```

### Caching
```python
from advanced_modules import CacheManager
import json

cache = CacheManager('my_cache.json')

# Check cache
cached_data = cache.get('example.com')
if cached_data:
    print("Using cached data")
else:
    print("No cached data, fetching new...")
    # Fetch data
    new_data = {'dns': {'A': ['1.2.3.4']}}
    cache.set('example.com', new_data)

# Clear cache
cache.clear('example.com')  # Clear specific
cache.clear()  # Clear all
```

---

## Batch Processing

### Process Multiple Domains
```python
import asyncio
from osint_framework import NexusOSINT

async def batch_domain_scan():
    domains = ['google.com', 'github.com', 'amazon.com']
    nexus = NexusOSINT()
    await nexus.initialize()
    
    results = {}
    for domain in domains:
        print(f"Scanning {domain}...")
        result = await nexus.full_domain_recon(domain)
        results[domain] = result
    
    # Save all results
    import json
    with open('batch_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    await nexus.cleanup()

asyncio.run(batch_domain_scan())
```

### Process Multiple IPs
```python
import asyncio
from osint_framework import NexusOSINT

async def batch_ip_scan():
    ips = ['8.8.8.8', '1.1.1.1', '9.9.9.9']
    nexus = NexusOSINT()
    await nexus.initialize()
    
    for ip in ips:
        print(f"Scanning {ip}...")
        results = await nexus.full_network_recon(ip)
        nexus.save_results(results, f"{ip}_report.json")
    
    await nexus.cleanup()

asyncio.run(batch_ip_scan())
```

---

## Error Handling

### Robust Error Handling
```python
import asyncio
from osint_framework import NexusOSINT

async def safe_scan():
    nexus = NexusOSINT()
    
    try:
        await nexus.initialize()
        
        results = await nexus.full_domain_recon('example.com')
        
        if results.get('error'):
            print(f"Error occurred: {results['error']}")
        else:
            print("Scan successful")
            nexus.save_results(results)
    
    except asyncio.TimeoutError:
        print("Request timed out")
    
    except ConnectionError:
        print("Connection error - check internet")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    finally:
        await nexus.cleanup()

asyncio.run(safe_scan())
```

---

## Parallel Processing

### Concurrent Scans
```python
import asyncio
from osint_framework import NexusOSINT

async def parallel_scan():
    nexus = NexusOSINT()
    await nexus.initialize()
    
    domains = ['google.com', 'github.com', 'amazon.com']
    
    # Create tasks for parallel execution
    tasks = [
        nexus.full_domain_recon(domain)
        for domain in domains
    ]
    
    # Run all simultaneously
    results = await asyncio.gather(*tasks)
    
    for domain, result in zip(domains, results):
        nexus.save_results(result, f"{domain}_report.json")
    
    await nexus.cleanup()

asyncio.run(parallel_scan())
```

---

## Data Aggregation

### Combine Results
```python
import json
from pathlib import Path

def aggregate_results():
    result_dir = Path('results')
    all_results = {}
    
    # Load all JSON files
    for json_file in result_dir.glob('*.json'):
        with open(json_file) as f:
            domain = json_file.stem
            all_results[domain] = json.load(f)
    
    # Create summary
    summary = {
        'total_domains': len(all_results),
        'domains': list(all_results.keys()),
        'timestamp': datetime.now().isoformat()
    }
    
    # Save aggregated report
    with open('aggregated_report.json', 'w') as f:
        json.dump({
            'summary': summary,
            'results': all_results
        }, f, indent=2)

aggregate_results()
```

---

## Integration with Other Tools

### Export to CSV
```python
import json
import csv

def export_to_csv(json_file):
    with open(json_file) as f:
        data = json.load(f)
    
    # Extract DNS records
    dns_records = data['results']['dns']['records']
    
    with open('dns_records.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Record Type', 'Value'])
        
        for record_type, values in dns_records.items():
            for value in values:
                writer.writerow([record_type, value])

export_to_csv('osint_results.json')
```

### Export to HTML Report
```python
from datetime import datetime

def create_html_report(domain, results):
    html = f"""
    <html>
    <head>
        <title>OSINT Report - {domain}</title>
        <style>
            body {{ font-family: Arial; margin: 20px; }}
            .section {{ margin: 20px 0; border: 1px solid #ddd; padding: 10px; }}
            h2 {{ color: #333; }}
            pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <h1>OSINT Report: {domain}</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="section">
            <h2>DNS Records</h2>
            <pre>{json.dumps(results['results']['dns'], indent=2)}</pre>
        </div>
        
        <div class="section">
            <h2>SSL Certificate</h2>
            <pre>{json.dumps(results['results']['ssl'], indent=2)}</pre>
        </div>
        
        <div class="section">
            <h2>Subdomains</h2>
            <pre>{json.dumps(results['results']['subdomains'], indent=2)}</pre>
        </div>
    </body>
    </html>
    """
    
    with open(f'{domain}_report.html', 'w') as f:
        f.write(html)
```

---

## Monitoring & Alerting

### Monitor Domain Changes
```python
import asyncio
import json
from datetime import datetime
from osint_framework import NexusOSINT

async def monitor_domain(domain, interval_hours=24):
    """Monitor domain for changes"""
    nexus = NexusOSINT()
    await nexus.initialize()
    
    previous_results = None
    
    while True:
        print(f"Checking {domain} at {datetime.now()}")
        results = await nexus.full_domain_recon(domain)
        
        if previous_results:
            # Compare results
            if results != previous_results:
                print(f"⚠️  Changes detected in {domain}!")
                print(f"Previous: {json.dumps(previous_results, indent=2)}")
                print(f"Current: {json.dumps(results, indent=2)}")
                
                # Alert (email, webhook, etc)
                # send_alert(domain, previous_results, results)
        
        previous_results = results
        
        # Wait for next check
        await asyncio.sleep(interval_hours * 3600)
    
    await nexus.cleanup()

# Run monitoring
# asyncio.run(monitor_domain('example.com'))
```

---

## Performance Tips

### 1. Async Optimization
```python
# Use gather for concurrent requests
tasks = [
    domain_intel.dns_enumeration('domain1.com'),
    domain_intel.dns_enumeration('domain2.com'),
    domain_intel.dns_enumeration('domain3.com'),
]
results = await asyncio.gather(*tasks)
```

### 2. Connection Pooling
```python
# The framework already uses connection pooling
# But you can control it:
connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
session = aiohttp.ClientSession(connector=connector)
```

### 3. Caching Strategy
```python
from advanced_modules import CacheManager

cache = CacheManager()

# Check cache first
cached = cache.get('example.com', max_age_hours=168)  # 1 week
if cached:
    results = cached
else:
    results = await fetch_data('example.com')
    cache.set('example.com', results)
```

---

## Debugging

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now run your code with debug output
asyncio.run(main())
```

### Print Detailed Results
```python
import json

results = await nexus.full_domain_recon('example.com')
print(json.dumps(results, indent=2))
```

---

## Security Best Practices

1. **Secure API Keys**
   ```python
   import os
   api_key = os.environ.get('GITHUB_TOKEN')  # Use env vars
   ```

2. **Rate Limiting**
   ```json
   {
     "settings": {
       "rate_limit_requests_per_second": 1
     }
   }
   ```

3. **Verify SSL**
   ```python
   # Keep verify_ssl: true in config
   # Only disable when testing own systems
   ```

---

**Happy Advanced Hacking! 🚀**
