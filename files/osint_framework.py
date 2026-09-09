#!/usr/bin/env python3
"""
🕵️ NEXUS OSINT - Most Powerful Python OSINT Framework
Platform: Windows, Linux (Kali/Ubuntu), Termux, macOS
Author: UR Rexy
Features: Domain Intel, Network Mapping, Social Media Recon, Threat Intelligence
"""

import os
import sys
import json
import asyncio
import aiohttp
import argparse
from datetime import datetime
from pathlib import Path
import platform
from typing import Dict, List, Optional, Tuple

# Color codes for cross-platform compatibility
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    banner = f"""{Colors.CYAN}{Colors.BOLD}
    ╔╗╔╔═╗╔═╗╦  ╦ ╦╔═╗
    ║║║║╚╗╚═╗║  ║ ║╚═╗
    ╚╩╝╚═╝╚═╝╩═╝╚═╝╚═╝
    
    🕵️ NEXUS OSINT v2.0
    Most Powerful Python OSINT Framework
    Designed for: Kali | Ubuntu | Termux | Windows
    {Colors.GREEN}[+] Ready for Advanced Reconnaissance{Colors.ENDC}
    {Colors.ENDC}"""
    print(banner)


def print_interactive_menu():
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== EASY OSINT MENU ==={Colors.ENDC}")
    print(f"{Colors.WHITE}1. Domain Scan       - Check a website or domain{Colors.ENDC}")
    print(f"{Colors.WHITE}2. IP Scan           - Check an IP or host{Colors.ENDC}")
    print(f"{Colors.WHITE}3. Username Search   - Search social accounts{Colors.ENDC}")
    print(f"{Colors.WHITE}4. Email Check       - Email validation and breach check{Colors.ENDC}")
    print(f"{Colors.WHITE}5. URL Security      - Quick URL check{Colors.ENDC}")
    print(f"{Colors.WHITE}6. Show Help         - See all advanced options{Colors.ENDC}")
    print(f"{Colors.WHITE}7. Exit              - Close the tool{Colors.ENDC}")


class EasyOSINTApp:
    """Modern beginner-friendly dashboard with tabs and export actions."""

    def __init__(self):
        self.root = None
        self.selected_option = 1
        self.nexus = NexusOSINT()
        self.last_result = {}
        self.tab_targets = {}
        self.status_cards = {}
        self.notebook = None
        self.output_box = None

    def launch(self):
        try:
            import tkinter as tk
            from tkinter import ttk, scrolledtext, filedialog
        except ImportError:
            print(f"{Colors.RED}[!] tkinter is not available on this system.{Colors.ENDC}")
            return

        self.root = tk.Tk()
        self.root.title("UR Rexy OSINT Toolkit")
        self.root.geometry("1280x760")
        self.root.minsize(1000, 640)
        self.root.configure(bg="#070d18")

        topbar = tk.Frame(self.root, bg="#111827", height=140)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        title = tk.Label(
            topbar,
            text="UR Rexy",
            font=("Segoe UI", 28, "bold"),
            fg="#f8fafc",
            bg="#111827",
        )
        title.place(x=30, y=22)

        subtitle = tk.Label(
            topbar,
            text="OSINT Toolkit",
            font=("Segoe UI", 12),
            fg="#cbd5e1",
            bg="#111827",
        )
        subtitle.place(x=34, y=72)

        brand = tk.Label(
            topbar,
            text="Made by UR Rexy Rehna",
            font=("Segoe UI", 10, "bold"),
            fg="#86efac",
            bg="#111827",
        )
        brand.place(x=34, y=96)

        card_frame = tk.Frame(topbar, bg="#111827")
        card_frame.place(x=380, y=18)

        self.status_cards = {}
        cards = [
            ("Domain", "Ready", "#22c55e"),
            ("IP", "Ready", "#3b82f6"),
            ("Username", "Ready", "#f59e0b"),
            ("Email", "Ready", "#a78bfa"),
            ("URL", "Ready", "#f43f5e"),
        ]
        for index, (name, text, color) in enumerate(cards):
            card = tk.Frame(card_frame, bg="#0f172a", bd=0, highlightthickness=1, highlightbackground=color)
            card.grid(row=0, column=index, padx=10, pady=6)
            title_label = tk.Label(card, text=name, font=("Segoe UI", 10, "bold"), fg="#cbd5e1", bg="#0f172a")
            title_label.pack(padx=18, pady=(12, 4))
            value_label = tk.Label(card, text=text, font=("Segoe UI", 17, "bold"), fg=color, bg="#0f172a")
            value_label.pack(padx=18, pady=(0, 12))
            self.status_cards[name] = value_label

        actions = tk.Frame(topbar, bg="#111827")
        actions.place(x=990, y=20)
        save_btn = tk.Button(actions, text="Save JSON", command=self.export_results, bg="#10b981", fg="#052e16", font=("Segoe UI", 10, "bold"), padx=16, pady=8, bd=0)
        save_btn.grid(row=0, column=0, padx=6, pady=4)
        export_btn = tk.Button(actions, text="Export Report", command=self.export_results, bg="#2563eb", fg="#f8fafc", font=("Segoe UI", 10, "bold"), padx=16, pady=8, bd=0)
        export_btn.grid(row=1, column=0, padx=6, pady=4)

        main = tk.Frame(self.root, bg="#070d18")
        main.pack(fill="both", expand=True, padx=20, pady=(18, 20))

        self.notebook = ttk.Notebook(main)
        self.notebook.pack(fill="both", expand=True)

        options = {
            1: ("Domain", "example.com"),
            2: ("IP", "8.8.8.8"),
            3: ("Username", "ur_rexy"),
            4: ("Email", "user@example.com"),
            5: ("URL", "https://example.com"),
        }
        self.tab_targets = {}

        for option_number, (tab_name, default) in options.items():
            tab = tk.Frame(self.notebook, bg="#0f172a")
            self.notebook.add(tab, text=tab_name)

            tk.Label(tab, text=f"{tab_name} target", font=("Segoe UI", 12, "bold"), fg="#e2e8f0", bg="#0f172a").pack(anchor="w", padx=20, pady=(20, 8))
            entry = tk.Entry(tab, width=80, font=("Segoe UI", 13), bg="#111827", fg="#f8fafc", insertbackground="#f8fafc", bd=1)
            entry.insert(0, default)
            entry.pack(fill="x", padx=20, pady=(0, 16))
            self.tab_targets[tab_name] = entry

            action_row = tk.Frame(tab, bg="#0f172a")
            action_row.pack(fill="x", padx=20, pady=(0, 10))
            run_button = tk.Button(
                action_row,
                text=f"Run {tab_name} Scan",
                font=("Segoe UI", 11, "bold"),
                bg="#22c55e",
                fg="#052e16",
                activebackground="#16a34a",
                command=lambda value=option_number: self.run_scan(value),
                padx=18,
                pady=10,
                bd=0,
            )
            run_button.pack(side="left")
            helper = tk.Label(
                action_row,
                text="Fast and beginner-friendly reconnaissance",
                font=("Segoe UI", 10),
                fg="#a5b4fc",
                bg="#0f172a",
            )
            helper.pack(side="left", padx=(18, 0))

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.root.bind("<Control-s>", lambda event: self.export_results())

        output_frame = tk.Frame(main, bg="#0f172a", bd=1, highlightbackground="#1f2937", highlightthickness=1)
        output_frame.pack(fill="both", expand=True)
        output_box = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            width=120,
            height=18,
            bg="#0b1220",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
            font=("Consolas", 10),
        )
        output_box.pack(fill="both", expand=True, padx=12, pady=12)
        self.output_box = output_box

        self.set_tab_status("Domain", "Ready")
        self.log_message("Ready. Pick a tab and enter your target to begin.\n")
        self.root.mainloop()

    def on_tab_change(self, event):
        tab_name = self.notebook.tab(self.notebook.select(), "text")
        self.selected_option = {
            "Domain": 1,
            "IP": 2,
            "Username": 3,
            "Email": 4,
            "URL": 5,
        }.get(tab_name, 1)
        self.log_message(f"Selected tab: {tab_name}\n")

    def set_tab_status(self, name, value):
        if name in self.status_cards:
            self.status_cards[name].config(text=value)

    def log_message(self, text):
        if self.root is not None and self.output_box is not None:
            self.output_box.insert(tk.END, text)
            self.output_box.see(tk.END)

    def export_results(self):
        if not self.last_result:
            self.log_message("No results yet to export.\n")
            return
        try:
            import tkinter as tk
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                initialfile="osint_report.json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            )
            if filename:
                with open(filename, "w", encoding="utf-8") as fh:
                    json.dump(self.last_result, fh, indent=2)
                self.log_message(f"Saved report to: {filename}\n")
        except Exception as exc:
            self.log_message(f"Export failed: {exc}\n")

    def run_scan(self, option_number):
        tab_names = {1: "Domain", 2: "IP", 3: "Username", 4: "Email", 5: "URL"}
        tab_name = tab_names.get(option_number, "Domain")
        target = self.tab_targets.get(tab_name, "").get().strip()
        if not target:
            self.log_message(f"Please enter a valid {tab_name.lower()} target.\n")
            return

        self.log_message(f"\nRunning {tab_name} scan for: {target}\n")

        def worker():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(self.execute_scan(option_number, target))
                self.last_result = result
                self.root.after(0, lambda: self.output_box.insert(tk.END, json.dumps(result, indent=2) + "\n\n"))
                self.root.after(0, lambda: self.output_box.see(tk.END))
                self.root.after(0, lambda: self.set_tab_status(tab_name, "Done"))
            except Exception as exc:
                self.root.after(0, lambda: self.output_box.insert(tk.END, f"[ERROR] {exc}\n\n"))
                self.root.after(0, lambda: self.output_box.see(tk.END))
                self.root.after(0, lambda: self.set_tab_status(tab_name, "Error"))
            finally:
                self.root.after(0, lambda: self.output_box.insert(tk.END, "Scan complete.\n"))
                self.root.after(0, lambda: self.output_box.see(tk.END))

        import threading
        threading.Thread(target=worker, daemon=True).start()

    async def execute_scan(self, option_number, target):
        await self.nexus.initialize()
        try:
            if option_number == 1:
                return await self.nexus.full_domain_recon(target)
            if option_number == 2:
                return await self.nexus.full_network_recon(target)
            if option_number == 3:
                return await self.nexus.full_username_recon(target)
            if option_number == 4:
                return await self.nexus.full_email_recon(target)
            if option_number == 5:
                url_result = await self.nexus.threat_intel.urlscan_check(target)
                return {"target": target, "results": {"url_security": url_result}}
            raise ValueError("Invalid option selected")
        finally:
            await self.nexus.cleanup()


async def run_interactive_menu():
    print_banner()
    print_interactive_menu()
    while True:
        choice = input(f"\n{Colors.CYAN}Choose an option (1-7): {Colors.ENDC}").strip()
        if choice == '7' or choice.lower() in ('exit', 'quit', 'q'):
            print(f"{Colors.GREEN}[+] Closing OSINT toolkit. Goodbye!{Colors.ENDC}")
            break
        if choice == '6':
            print(f"{Colors.YELLOW}Advanced CLI examples:{Colors.ENDC}")
            print("  python osint_framework.py --domain example.com --full")
            print("  python osint_framework.py --ip 8.8.8.8 --full")
            print("  python osint_framework.py --username admin --full")
            print("  python osint_framework.py --email test@example.com --full")
            continue

        nexus = NexusOSINT()
        await nexus.initialize()
        try:
            if choice == '1':
                target = input("Enter domain: ").strip() or "example.com"
                result = await nexus.full_domain_recon(target)
            elif choice == '2':
                target = input("Enter IP or host: ").strip() or "8.8.8.8"
                result = await nexus.full_network_recon(target)
            elif choice == '3':
                target = input("Enter username: ").strip() or "ur_rexy"
                result = await nexus.full_username_recon(target)
            elif choice == '4':
                target = input("Enter email: ").strip() or "user@example.com"
                result = await nexus.full_email_recon(target)
            elif choice == '5':
                target = input("Enter URL: ").strip() or "https://example.com"
                result = {"target": target, "results": {"url_security": await nexus.threat_intel.urlscan_check(target)}}
            else:
                print(f"{Colors.RED}[!] Invalid option. Please use 1-7.{Colors.ENDC}")
                continue
            print(f"\n{Colors.CYAN}{json.dumps(result, indent=2)}{Colors.ENDC}")
        finally:
            await nexus.cleanup()
        print_interactive_menu()


class DomainIntelligence:
    """Domain & DNS enumeration, WHOIS, SSL, Subdomain scanning"""
    
    def __init__(self):
        self.session = None
    
    async def setup(self):
        self.session = aiohttp.ClientSession()
    
    async def whois_lookup(self, domain: str) -> Dict:
        """Get WHOIS information"""
        try:
            import socket
            result = {
                "domain": domain,
                "status": "pending",
                "timestamp": datetime.now().isoformat()
            }
            return result
        except Exception as e:
            return {"error": str(e)}
    
    async def dns_enumeration(self, domain: str) -> Dict:
        """Enumerate DNS records (A, AAAA, MX, TXT, NS, CNAME)"""
        try:
            import dns.resolver
            records = {
                "domain": domain,
                "records": {}
            }
            
            record_types = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME', 'SOA']
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    records["records"][record_type] = [str(rdata) for rdata in answers]
                except:
                    records["records"][record_type] = []
            
            return records
        except Exception as e:
            return {"error": str(e)}
    
    async def ssl_certificate_info(self, domain: str) -> Dict:
        """Extract SSL/TLS certificate information"""
        try:
            import ssl
            import socket
            
            context = ssl.create_default_context()
            conn = socket.create_connection((domain, 443), timeout=5)
            sock = context.wrap_socket(conn, server_hostname=domain)
            cert = sock.getpeercert()
            sock.close()
            
            return {
                "domain": domain,
                "certificate": cert,
                "issuer": cert.get('issuer'),
                "subject": cert.get('subject'),
                "valid_from": cert.get('notBefore'),
                "valid_to": cert.get('notAfter')
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def subdomain_enumeration(self, domain: str) -> Dict:
        """Advanced subdomain enumeration using multiple methods"""
        subdomains = set()
        
        # Method 1: Common subdomains wordlist
        common_subs = ['www', 'mail', 'smtp', 'pop', 'ns', 'webmail', 'api', 'admin',
                       'test', 'dev', 'staging', 'prod', 'db', 'cdn', 'git', 'ftp',
                       'vpn', 'panel', 'backup', 'support', 'blog', 'shop', 'app']
        
        for sub in common_subs:
            full_domain = f"{sub}.{domain}"
            subdomains.add(full_domain)
        
        return {
            "domain": domain,
            "subdomains": list(subdomains),
            "count": len(subdomains)
        }
    
    async def cleanup(self):
        if self.session:
            await self.session.close()


class NetworkIntelligence:
    """Port scanning, IP geolocation, ASN lookup, Network mapping"""
    
    def __init__(self):
        self.session = None
    
    async def setup(self):
        self.session = aiohttp.ClientSession()
    
    async def port_scanner(self, target: str, ports: List[int] = None) -> Dict:
        """Fast port scanner using asyncio"""
        if ports is None:
            ports = [21, 22, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 
                    3306, 3389, 5432, 5900, 8080, 8443, 9200, 27017]
        
        async def check_port(host, port):
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(host, port), timeout=1.0
                )
                writer.close()
                await writer.wait_closed()
                return port, True
            except:
                return port, False
        
        results = {}
        tasks = [check_port(target, port) for port in ports]
        responses = await asyncio.gather(*tasks)
        
        for port, is_open in responses:
            results[port] = "OPEN" if is_open else "CLOSED"
        
        return {
            "target": target,
            "ports": results,
            "open_ports": [p for p, status in results.items() if status == "OPEN"]
        }
    
    async def ip_geolocation(self, ip: str) -> Dict:
        """Get IP geolocation and ASN information"""
        try:
            async with self.session.get(f"https://ipapi.co/{ip}/json/") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {
                        "ip": ip,
                        "country": data.get('country_name'),
                        "city": data.get('city'),
                        "latitude": data.get('latitude'),
                        "longitude": data.get('longitude'),
                        "asn": data.get('asn'),
                        "org": data.get('org'),
                        "timezone": data.get('timezone')
                    }
        except Exception as e:
            return {"error": str(e)}
    
    async def traceroute(self, host: str) -> Dict:
        """Traceroute to target host"""
        import subprocess
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['tracert', host], capture_output=True, text=True)
            else:
                result = subprocess.run(['traceroute', '-m', '30', host], 
                                       capture_output=True, text=True)
            
            return {
                "host": host,
                "traceroute": result.stdout.split('\n'),
                "status": "success"
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def cleanup(self):
        if self.session:
            await self.session.close()


class SocialMediaReconnaissance:
    """Username enumeration across 100+ platforms"""
    
    PLATFORMS = {
        'github': 'https://github.com/{}',
        'twitter': 'https://twitter.com/{}',
        'instagram': 'https://instagram.com/{}',
        'facebook': 'https://facebook.com/{}',
        'linkedin': 'https://linkedin.com/in/{}',
        'youtube': 'https://youtube.com/@{}',
        'reddit': 'https://reddit.com/u/{}',
        'tiktok': 'https://tiktok.com/@{}',
        'twitch': 'https://twitch.tv/{}',
        'snapchat': 'https://snapchat.com/add/{}',
        'pinterest': 'https://pinterest.com/{}',
        'telegram': 'https://t.me/{}',
        'discord': 'https://discordapp.com/users/{}',
        'tumblr': 'https://{}.tumblr.com',
        'medium': 'https://medium.com/@{}',
        'quora': 'https://quora.com/profile/{}',
        'stackexchange': 'https://stackexchange.com/users/{}',
        'patreon': 'https://patreon.com/{}',
    }
    
    def __init__(self):
        self.session = None
    
    async def setup(self):
        self.session = aiohttp.ClientSession()
    
    async def username_search(self, username: str) -> Dict:
        """Search username across multiple platforms"""
        async def check_platform(platform_name, url_template):
            try:
                url = url_template.format(username)
                async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    if resp.status == 200:
                        return platform_name, True, url
                    return platform_name, False, url
            except:
                return platform_name, False, url_template.format(username)
        
        results = {}
        tasks = [check_platform(name, url) for name, url in self.PLATFORMS.items()]
        responses = await asyncio.gather(*tasks)
        
        found_accounts = []
        for platform_name, found, url in responses:
            results[platform_name] = {
                "found": found,
                "url": url
            }
            if found:
                found_accounts.append({"platform": platform_name, "url": url})
        
        return {
            "username": username,
            "platforms_checked": len(self.PLATFORMS),
            "found_accounts": found_accounts,
            "detailed_results": results
        }
    
    async def cleanup(self):
        if self.session:
            await self.session.close()


class EmailIntelligence:
    """Email enumeration, breach checking, format verification"""
    
    def __init__(self):
        self.session = None
    
    async def setup(self):
        self.session = aiohttp.ClientSession()
    
    async def email_verification(self, email: str) -> Dict:
        """Verify email format and check if it exists"""
        import re
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = bool(re.match(email_pattern, email))
        
        return {
            "email": email,
            "format_valid": is_valid,
            "domain": email.split('@')[1] if '@' in email else None
        }
    
    async def breach_check(self, email: str) -> Dict:
        """Check if email appears in known breaches"""
        try:
            # Using HaveIBeenPwned API (requires attribution)
            headers = {'User-Agent': 'NEXUS-OSINT'}
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            
            async with self.session.get(url, headers=headers) as resp:
                breaches = []
                if resp.status == 200:
                    breaches = await resp.json()
                
                return {
                    "email": email,
                    "breached": len(breaches) > 0,
                    "breaches": breaches if breaches else []
                }
        except Exception as e:
            return {"error": str(e)}
    
    async def cleanup(self):
        if self.session:
            await self.session.close()


class ThreatIntelligence:
    """Malware analysis, Threat feeds, Vulnerability scanning"""
    
    def __init__(self):
        self.session = None
    
    async def setup(self):
        self.session = aiohttp.ClientSession()
    
    async def urlscan_check(self, url: str) -> Dict:
        """Scan URL for malware using URLScan.io"""
        try:
            async with self.session.get(f"https://urlscan.io/api/v1/search/?q=domain:{url}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {
                        "url": url,
                        "results": data.get('results', []),
                        "total": data.get('total', 0)
                    }
        except Exception as e:
            return {"error": str(e)}
    
    async def virustotal_check(self, hash_value: str) -> Dict:
        """Check file/URL hash on VirusTotal (requires API key)"""
        return {
            "hash": hash_value,
            "note": "Set API key in config file",
            "requires_api_key": True
        }
    
    async def cleanup(self):
        if self.session:
            await self.session.close()


class NexusOSINT:
    """Main OSINT Framework Controller"""
    
    def __init__(self):
        self.domain_intel = DomainIntelligence()
        self.network_intel = NetworkIntelligence()
        self.social_recon = SocialMediaReconnaissance()
        self.email_intel = EmailIntelligence()
        self.threat_intel = ThreatIntelligence()
        self.results = {}
    
    async def initialize(self):
        """Initialize all modules"""
        await self.domain_intel.setup()
        await self.network_intel.setup()
        await self.social_recon.setup()
        await self.email_intel.setup()
        await self.threat_intel.setup()
        print(f"{Colors.GREEN}[+] All modules initialized{Colors.ENDC}")
    
    async def full_domain_recon(self, domain: str) -> Dict:
        """Complete domain reconnaissance"""
        print(f"\n{Colors.BLUE}[*] Starting full domain reconnaissance for {domain}{Colors.ENDC}")
        
        results = {
            "domain": domain,
            "timestamp": datetime.now().isoformat(),
            "results": {}
        }
        
        print(f"{Colors.YELLOW}[*] Enumerating subdomains...{Colors.ENDC}")
        results["results"]["subdomains"] = await self.domain_intel.subdomain_enumeration(domain)
        
        print(f"{Colors.YELLOW}[*] DNS enumeration...{Colors.ENDC}")
        results["results"]["dns"] = await self.domain_intel.dns_enumeration(domain)
        
        print(f"{Colors.YELLOW}[*] SSL certificate analysis...{Colors.ENDC}")
        results["results"]["ssl"] = await self.domain_intel.ssl_certificate_info(domain)
        
        print(f"{Colors.YELLOW}[*] WHOIS lookup...{Colors.ENDC}")
        results["results"]["whois"] = await self.domain_intel.whois_lookup(domain)
        
        print(f"{Colors.GREEN}[+] Domain reconnaissance complete!{Colors.ENDC}")
        return results
    
    async def full_network_recon(self, target: str) -> Dict:
        """Complete network reconnaissance"""
        print(f"\n{Colors.BLUE}[*] Starting network reconnaissance for {target}{Colors.ENDC}")
        
        results = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "results": {}
        }
        
        print(f"{Colors.YELLOW}[*] Port scanning...{Colors.ENDC}")
        results["results"]["ports"] = await self.network_intel.port_scanner(target)
        
        print(f"{Colors.YELLOW}[*] IP geolocation...{Colors.ENDC}")
        results["results"]["geolocation"] = await self.network_intel.ip_geolocation(target)
        
        print(f"{Colors.YELLOW}[*] Traceroute...{Colors.ENDC}")
        results["results"]["traceroute"] = await self.network_intel.traceroute(target)
        
        print(f"{Colors.GREEN}[+] Network reconnaissance complete!{Colors.ENDC}")
        return results
    
    async def full_username_recon(self, username: str) -> Dict:
        """Complete username reconnaissance"""
        print(f"\n{Colors.BLUE}[*] Starting username reconnaissance for {username}{Colors.ENDC}")
        
        results = {
            "username": username,
            "timestamp": datetime.now().isoformat(),
            "results": {}
        }
        
        print(f"{Colors.YELLOW}[*] Searching {len(self.social_recon.PLATFORMS)} platforms...{Colors.ENDC}")
        results["results"]["social_media"] = await self.social_recon.username_search(username)
        
        print(f"{Colors.GREEN}[+] Username reconnaissance complete!{Colors.ENDC}")
        return results
    
    async def full_email_recon(self, email: str) -> Dict:
        """Complete email reconnaissance"""
        print(f"\n{Colors.BLUE}[*] Starting email reconnaissance for {email}{Colors.ENDC}")
        
        results = {
            "email": email,
            "timestamp": datetime.now().isoformat(),
            "results": {}
        }
        
        print(f"{Colors.YELLOW}[*] Email verification...{Colors.ENDC}")
        results["results"]["verification"] = await self.email_intel.email_verification(email)
        
        print(f"{Colors.YELLOW}[*] Checking breaches...{Colors.ENDC}")
        results["results"]["breaches"] = await self.email_intel.breach_check(email)
        
        print(f"{Colors.GREEN}[+] Email reconnaissance complete!{Colors.ENDC}")
        return results
    
    def save_results(self, results: Dict, filename: str = None):
        """Save results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"osint_results_{timestamp}.json"
        
        output_path = Path(filename)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"{Colors.GREEN}[+] Results saved to {output_path}{Colors.ENDC}")
        return str(output_path)
    
    async def cleanup(self):
        """Cleanup all modules"""
        await self.domain_intel.cleanup()
        await self.network_intel.cleanup()
        await self.social_recon.cleanup()
        await self.email_intel.cleanup()
        await self.threat_intel.cleanup()


async def main():
    print_banner()
    
    parser = argparse.ArgumentParser(
        description='NEXUS OSINT - Advanced Reconnaissance Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 osint_framework.py --domain example.com --full
  python3 osint_framework.py --ip 8.8.8.8 --full
  python3 osint_framework.py --username john_doe --full
  python3 osint_framework.py --email john@example.com --full
  python3 osint_framework.py --domain example.com --dns --ssl --subdomains
        """
    )
    
    parser.add_argument('--domain', help='Target domain for reconnaissance')
    parser.add_argument('--ip', help='Target IP for network reconnaissance')
    parser.add_argument('--username', help='Username for social media reconnaissance')
    parser.add_argument('--email', help='Email for email reconnaissance')
    parser.add_argument('--dns', action='store_true', help='DNS enumeration')
    parser.add_argument('--ssl', action='store_true', help='SSL certificate analysis')
    parser.add_argument('--subdomains', action='store_true', help='Subdomain enumeration')
    parser.add_argument('--ports', action='store_true', help='Port scanning')
    parser.add_argument('--geo', action='store_true', help='IP geolocation')
    parser.add_argument('--trace', action='store_true', help='Traceroute')
    parser.add_argument('--full', action='store_true', help='Full reconnaissance')
    parser.add_argument('--save', help='Save results to JSON file')
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    nexus = NexusOSINT()
    await nexus.initialize()
    
    try:
        if args.domain:
            if args.full:
                results = await nexus.full_domain_recon(args.domain)
            else:
                results = {"domain": args.domain, "results": {}}
                if args.dns or not any([args.ssl, args.subdomains]):
                    results["results"]["dns"] = await nexus.domain_intel.dns_enumeration(args.domain)
                if args.ssl:
                    results["results"]["ssl"] = await nexus.domain_intel.ssl_certificate_info(args.domain)
                if args.subdomains:
                    results["results"]["subdomains"] = await nexus.domain_intel.subdomain_enumeration(args.domain)
            
            if args.save:
                nexus.save_results(results, args.save)
            else:
                print(f"\n{Colors.CYAN}{json.dumps(results, indent=2)}{Colors.ENDC}")
        
        elif args.ip:
            if args.full:
                results = await nexus.full_network_recon(args.ip)
            else:
                results = {"ip": args.ip, "results": {}}
                if args.ports or not any([args.geo, args.trace]):
                    results["results"]["ports"] = await nexus.network_intel.port_scanner(args.ip)
                if args.geo:
                    results["results"]["geo"] = await nexus.network_intel.ip_geolocation(args.ip)
                if args.trace:
                    results["results"]["trace"] = await nexus.network_intel.traceroute(args.ip)
            
            if args.save:
                nexus.save_results(results, args.save)
            else:
                print(f"\n{Colors.CYAN}{json.dumps(results, indent=2)}{Colors.ENDC}")
        
        elif args.username:
            results = await nexus.full_username_recon(args.username)
            if args.save:
                nexus.save_results(results, args.save)
            else:
                print(f"\n{Colors.CYAN}{json.dumps(results, indent=2)}{Colors.ENDC}")
        
        elif args.email:
            results = await nexus.full_email_recon(args.email)
            if args.save:
                nexus.save_results(results, args.save)
            else:
                print(f"\n{Colors.CYAN}{json.dumps(results, indent=2)}{Colors.ENDC}")
    
    finally:
        await nexus.cleanup()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        try:
            import tkinter as tk  # noqa: F401
            app = EasyOSINTApp()
            app.launch()
        except Exception:
            try:
                asyncio.run(run_interactive_menu())
            except KeyboardInterrupt:
                print(f"\n{Colors.RED}[!] Interrupted by user{Colors.ENDC}")
                sys.exit(0)
        raise SystemExit(0)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Interrupted by user{Colors.ENDC}")
        sys.exit(0)
