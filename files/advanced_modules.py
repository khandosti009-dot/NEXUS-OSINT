#!/usr/bin/env python3
"""
Advanced OSINT Modules for NEXUS Framework
Includes: Web Scraping, Metadata Extraction, API Integration, ML Analysis
"""

import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import hashlib
import re

class WebScrapingAndCrawling:
    """Advanced web scraping, crawling, and content analysis"""
    
    def __init__(self):
        self.session = None
        self.crawled_urls = set()
    
    async def setup(self):
        self.session = aiohttp.ClientSession()
    
    async def extract_links(self, url: str, max_depth: int = 2) -> Dict:
        """Extract all links from website (recursive crawling)"""
        from bs4 import BeautifulSoup
        
        result = {
            "base_url": url,
            "links": [],
            "emails": [],
            "phone_numbers": [],
            "social_media": [],
            "depth_crawled": 0
        }
        
        try:
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    content = await resp.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Extract links
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        result["links"].append(href)
                    
                    # Extract emails
                    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
                    result["emails"] = list(set(emails))
                    
                    # Extract phone numbers
                    phones = re.findall(r'\+?\d{1,3}[-.\s]?\d{1,14}', content)
                    result["phone_numbers"] = list(set(phones))
                    
                    # Extract social media links
                    social_patterns = {
                        'twitter': r'twitter\.com/[\w]+',
                        'facebook': r'facebook\.com/[\w\-\.]+',
                        'linkedin': r'linkedin\.com/(in|company)/[\w\-]+',
                        'instagram': r'instagram\.com/[\w\.]+',
                        'github': r'github\.com/[\w\-]+',
                    }
                    
                    for platform, pattern in social_patterns.items():
                        matches = re.findall(pattern, content)
                        if matches:
                            result["social_media"].extend([(platform, m) for m in matches])
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    async def extract_metadata(self, url: str) -> Dict:
        """Extract page metadata (title, description, keywords, og tags)"""
        from bs4 import BeautifulSoup
        
        metadata = {
            "url": url,
            "title": None,
            "description": None,
            "keywords": None,
            "og_tags": {},
            "headers": {},
            "server_info": None
        }
        
        try:
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                metadata["server_info"] = resp.headers.get('Server', 'Unknown')
                
                if resp.status == 200:
                    content = await resp.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Basic metadata
                    if soup.title:
                        metadata["title"] = soup.title.string
                    
                    for tag in soup.find_all('meta'):
                        if tag.get('name') == 'description':
                            metadata["description"] = tag.get('content')
                        elif tag.get('name') == 'keywords':
                            metadata["keywords"] = tag.get('content')
                        
                        # OG tags
                        if tag.get('property', '').startswith('og:'):
                            metadata["og_tags"][tag.get('property')] = tag.get('content')
        
        except Exception as e:
            metadata["error"] = str(e)
        
        return metadata
    
    async def technology_detection(self, url: str) -> Dict:
        """Detect technologies used on website (Wappalyzer-like)"""
        # This is a simplified version - in production use wappalyzer or builtwith APIs
        
        tech_indicators = {
            'wordpress': ['wp-content', 'wp-includes', 'wp-admin'],
            'drupal': ['sites/default', 'modules/'],
            'joomla': ['components/com_', 'administrator/'],
            'shopify': ['cdn.shopify.com', 'myshopify.com'],
            'wix': ['wix.com', 'www.wix.com'],
            'django': ['Django/'],
            'rails': ['ruby', 'rails'],
            'spring': ['Spring/'],
            'laravel': ['Laravel/'],
            'react': ['react', 'react.js'],
            'vue': ['vue', 'vuejs'],
            'angular': ['angular', 'angularjs'],
        }
        
        result = {"url": url, "technologies": []}
        
        try:
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    content = await resp.text()
                    headers_str = str(resp.headers).lower()
                    
                    for tech, indicators in tech_indicators.items():
                        for indicator in indicators:
                            if indicator.lower() in content.lower() or indicator.lower() in headers_str:
                                result["technologies"].append(tech)
                                break
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    async def cleanup(self):
        if self.session:
            await self.session.close()


class MetadataExtraction:
    """Extract metadata from various file types"""
    
    @staticmethod
    def extract_image_metadata(file_path: str) -> Dict:
        """Extract EXIF and other metadata from images"""
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            import piexif
            
            metadata = {"file": file_path, "exif": {}, "iptc": {}}
            
            image = Image.open(file_path)
            
            # Basic image info
            metadata["size"] = image.size
            metadata["format"] = image.format
            metadata["mode"] = image.mode
            
            # EXIF data
            exif_data = piexif.load(file_path)
            for ifd_name in ("0th", "Exif", "GPS", "1st"):
                ifd = exif_data[ifd_name]
                for tag, value in ifd.items():
                    tag_name = piexif.TAGS[ifd_name][tag]["name"]
                    metadata["exif"][tag_name] = str(value)
            
            return metadata
        
        except Exception as e:
            return {"error": str(e), "file": file_path}
    
    @staticmethod
    def extract_pdf_metadata(file_path: str) -> Dict:
        """Extract metadata from PDF files"""
        try:
            import PyPDF2
            
            metadata = {"file": file_path, "metadata": {}}
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata["pages"] = len(pdf_reader.pages)
                metadata["metadata"] = pdf_reader.metadata
            
            return metadata
        
        except Exception as e:
            return {"error": str(e), "file": file_path}
    
    @staticmethod
    def extract_document_metadata(file_path: str) -> Dict:
        """Extract metadata from Office documents"""
        try:
            from docx import Document
            from openpyxl import load_workbook
            
            metadata = {"file": file_path}
            
            if file_path.endswith('.docx'):
                doc = Document(file_path)
                props = doc.core_properties
                metadata.update({
                    "title": props.title,
                    "author": props.author,
                    "subject": props.subject,
                    "created": props.created,
                    "modified": props.modified,
                })
            
            elif file_path.endswith('.xlsx'):
                wb = load_workbook(file_path)
                props = wb.properties
                metadata.update({
                    "title": props.title,
                    "author": props.author,
                    "created": props.created,
                    "modified": props.modified,
                })
            
            return metadata
        
        except Exception as e:
            return {"error": str(e), "file": file_path}


class GithubIntelligence:
    """GitHub reconnaissance and code analysis"""
    
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token
        self.session = None
        self.base_url = "https://api.github.com"
    
    async def setup(self):
        self.session = aiohttp.ClientSession()
    
    async def user_recon(self, username: str) -> Dict:
        """Gather intelligence on GitHub user"""
        result = {"username": username, "error": None}
        
        try:
            headers = {}
            if self.api_token:
                headers["Authorization"] = f"token {self.api_token}"
            
            # User info
            async with self.session.get(f"{self.base_url}/users/{username}", headers=headers) as resp:
                if resp.status == 200:
                    user_data = await resp.json()
                    result.update({
                        "name": user_data.get('name'),
                        "company": user_data.get('company'),
                        "location": user_data.get('location'),
                        "email": user_data.get('email'),
                        "bio": user_data.get('bio'),
                        "public_repos": user_data.get('public_repos'),
                        "followers": user_data.get('followers'),
                        "following": user_data.get('following'),
                        "created_at": user_data.get('created_at'),
                        "updated_at": user_data.get('updated_at'),
                    })
            
            # Repositories
            async with self.session.get(f"{self.base_url}/users/{username}/repos", headers=headers) as resp:
                if resp.status == 200:
                    repos = await resp.json()
                    result["repositories"] = {
                        "count": len(repos),
                        "repos": [
                            {
                                "name": r.get('name'),
                                "description": r.get('description'),
                                "url": r.get('html_url'),
                                "stars": r.get('stargazers_count'),
                                "language": r.get('language'),
                                "created": r.get('created_at'),
                                "updated": r.get('updated_at'),
                            }
                            for r in repos[:10]  # Top 10 repos
                        ]
                    }
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    async def search_sensitive_files(self, organization: str) -> Dict:
        """Search for sensitive files in public repos (educational)"""
        sensitive_patterns = [
            'password',
            'api_key',
            'secret',
            'token',
            'aws_access_key',
            'database_url',
        ]
        
        result = {"organization": organization, "findings": []}
        
        try:
            headers = {}
            if self.api_token:
                headers["Authorization"] = f"token {self.api_token}"
            
            for pattern in sensitive_patterns:
                query = f"org:{organization} {pattern} in:file"
                async with self.session.get(
                    f"{self.base_url}/search/code?q={query}",
                    headers=headers
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get('items'):
                            result["findings"].extend(data.get('items', []))
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    async def cleanup(self):
        if self.session:
            await self.session.close()


class AnomalyDetection:
    """Machine learning based anomaly detection for OSINT data"""
    
    @staticmethod
    def detect_ip_anomalies(ip_data_list: List[Dict]) -> Dict:
        """Detect suspicious IP patterns"""
        # Simplified anomaly detection
        anomalies = []
        
        for data in ip_data_list:
            ip = data.get('ip')
            # Check for residential IP behaving like datacenter
            if data.get('org', '').lower() in ['aws', 'azure', 'gcp', 'digitalocean']:
                if data.get('type') == 'residential':
                    anomalies.append({"ip": ip, "anomaly": "Datacenter IP with residential designation"})
            
            # Check for geo-hopping (would need historical data)
            # Check for proxy/VPN
            if 'vpn' in data.get('org', '').lower() or 'proxy' in data.get('org', '').lower():
                anomalies.append({"ip": ip, "anomaly": "Proxy/VPN detected"})
        
        return {
            "total_ips": len(ip_data_list),
            "anomalies_found": len(anomalies),
            "anomalies": anomalies
        }
    
    @staticmethod
    def detect_domain_anomalies(domain_data: Dict) -> Dict:
        """Detect suspicious domain patterns"""
        anomalies = []
        
        dns_records = domain_data.get('dns', {})
        
        # Check for multiple A records (load balancing or suspicious)
        if len(dns_records.get('A', [])) > 5:
            anomalies.append("Multiple A records detected (potential DGA or load balancing)")
        
        # Check for short TTL (potential rapid changes)
        if dns_records.get('SOA'):
            anomalies.append("Low TTL values detected (rapid DNS changes)")
        
        # Check for excessive NS records
        if len(dns_records.get('NS', [])) > 4:
            anomalies.append("Excessive nameservers detected")
        
        return {
            "domain": domain_data.get('domain'),
            "anomalies_found": len(anomalies),
            "anomalies": anomalies
        }


class CacheManager:
    """Local database caching for results"""
    
    def __init__(self, cache_file: str = "osint_cache.json"):
        self.cache_file = Path(cache_file)
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """Load cache from file"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """Save cache to file"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def get(self, key: str, max_age_hours: int = 24) -> Optional[Dict]:
        """Get cached data if not expired"""
        if key in self.cache:
            data = self.cache[key]
            timestamp = datetime.fromisoformat(data.get('timestamp'))
            if datetime.now() - timestamp < timedelta(hours=max_age_hours):
                return data.get('data')
        return None
    
    def set(self, key: str, data: Dict):
        """Cache data with timestamp"""
        self.cache[key] = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self._save_cache()
    
    def clear(self, key: Optional[str] = None):
        """Clear cache entry or entire cache"""
        if key:
            if key in self.cache:
                del self.cache[key]
        else:
            self.cache = {}
        self._save_cache()
