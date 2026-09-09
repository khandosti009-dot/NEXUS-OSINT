#!/usr/bin/env python3
"""
NEXUS OSINT Installation Script
Supports: Windows, Kali Linux, Ubuntu, Termux, macOS
"""

import os
import sys
import platform
import subprocess
import json
from pathlib import Path
from typing import Optional

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def is_termux():
    """Check if running in Termux"""
    return 'TERMUX_VERSION' in os.environ

def is_windows():
    """Check if running on Windows"""
    return platform.system() == 'Windows'

def print_banner():
    banner = f"""{Colors.BLUE}{Colors.BOLD}
╔═══════════════════════════════════════╗
║   NEXUS OSINT Installation Script     ║
║   v2.0 - Cross Platform Support       ║
╚═══════════════════════════════════════╝
{Colors.ENDC}"""
    print(banner)

def detect_platform():
    """Detect current platform"""
    system = platform.system()
    
    if is_termux():
        return "termux"
    elif is_windows():
        return "windows"
    elif system == "Linux":
        # Try to detect distribution
        if Path("/etc/os-release").exists():
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("ID="):
                        distro = line.split("=")[1].strip().strip('"')
                        if "kali" in distro:
                            return "kali"
                        elif "ubuntu" in distro or "debian" in distro:
                            return "ubuntu"
        return "linux"
    elif system == "Darwin":
        return "macos"
    
    return "unknown"

def install_system_dependencies():
    """Install system-level dependencies based on platform"""
    platform_type = detect_platform()
    
    print(f"{Colors.YELLOW}[*] Detected platform: {platform_type}{Colors.ENDC}")
    
    if platform_type in ["kali", "ubuntu", "linux"]:
        print(f"{Colors.YELLOW}[*] Installing Linux dependencies...{Colors.ENDC}")
        
        # Update package manager
        try:
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            
            # Essential packages
            packages = [
                "python3-pip",
                "python3-dev",
                "build-essential",
                "libssl-dev",
                "libffi-dev",
                "git",
                "curl",
                "wget",
                "nmap",
                "whois",
                "traceroute",
                "dnsutils",
                "net-tools",
                "postgresql-client",
                "sqlite3",
                "libpq-dev",
            ]
            
            for package in packages:
                print(f"{Colors.YELLOW}[*] Installing {package}...{Colors.ENDC}")
                subprocess.run(["sudo", "apt-get", "install", "-y", package], check=False)
            
            print(f"{Colors.GREEN}[+] Linux dependencies installed!{Colors.ENDC}")
        
        except Exception as e:
            print(f"{Colors.RED}[-] Error installing Linux dependencies: {e}{Colors.ENDC}")
            return False
    
    elif platform_type == "termux":
        print(f"{Colors.YELLOW}[*] Installing Termux dependencies...{Colors.ENDC}")
        
        try:
            subprocess.run(["apt", "update"], check=True)
            subprocess.run(["apt", "upgrade", "-y"], check=True)
            
            packages = [
                "python",
                "python-pip",
                "git",
                "curl",
                "wget",
                "nmap",
                "whois",
                "traceroute",
                "dnsutils",
                "net-tools",
                "sqlite",
            ]
            
            for package in packages:
                print(f"{Colors.YELLOW}[*] Installing {package}...{Colors.ENDC}")
                subprocess.run(["apt", "install", "-y", package], check=False)
            
            print(f"{Colors.GREEN}[+] Termux dependencies installed!{Colors.ENDC}")
        
        except Exception as e:
            print(f"{Colors.RED}[-] Error installing Termux dependencies: {e}{Colors.ENDC}")
            return False
    
    elif platform_type == "windows":
        print(f"{Colors.YELLOW}[*] Windows detected. Please ensure Python 3.8+ is installed.{Colors.ENDC}")
        print(f"{Colors.YELLOW}[*] Recommended: Install nmap and whois for full functionality{Colors.ENDC}")
        print(f"{Colors.YELLOW}    Download from: https://nmap.org/download.html{Colors.ENDC}")
    
    elif platform_type == "macos":
        print(f"{Colors.YELLOW}[*] Installing macOS dependencies via Homebrew...{Colors.ENDC}")
        
        try:
            # Check if Homebrew is installed
            subprocess.run(["brew", "--version"], check=True, capture_output=True)
            
            packages = ["nmap", "whois", "wget", "git"]
            for package in packages:
                print(f"{Colors.YELLOW}[*] Installing {package}...{Colors.ENDC}")
                subprocess.run(["brew", "install", package], check=False)
            
            print(f"{Colors.GREEN}[+] macOS dependencies installed!{Colors.ENDC}")
        
        except:
            print(f"{Colors.YELLOW}[!] Homebrew not found. Install from: https://brew.sh{Colors.ENDC}")
    
    return True

def create_python_venv():
    """Create Python virtual environment"""
    print(f"{Colors.YELLOW}[*] Creating Python virtual environment...{Colors.ENDC}")
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "nexus_env"], check=True)
        print(f"{Colors.GREEN}[+] Virtual environment created!{Colors.ENDC}")
        return True
    
    except Exception as e:
        print(f"{Colors.RED}[-] Error creating virtual environment: {e}{Colors.ENDC}")
        return False

def get_python_executable():
    """Get the Python executable to use"""
    platform_type = detect_platform()
    
    if is_windows():
        venv_python = Path("nexus_env/Scripts/python.exe")
    else:
        venv_python = Path("nexus_env/bin/python3")
    
    if venv_python.exists():
        return str(venv_python)
    
    return sys.executable

def install_python_dependencies():
    """Install Python package dependencies"""
    print(f"{Colors.YELLOW}[*] Installing Python dependencies...{Colors.ENDC}")
    print(f"{Colors.YELLOW}[*] This may take a few minutes...{Colors.ENDC}")
    
    python_exe = get_python_executable()
    
    try:
        # Upgrade pip
        subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip"], check=False)
        
        # Install requirements
        if Path("requirements.txt").exists():
            subprocess.run([python_exe, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        else:
            print(f"{Colors.RED}[-] requirements.txt not found!{Colors.ENDC}")
            return False
        
        print(f"{Colors.GREEN}[+] Python dependencies installed!{Colors.ENDC}")
        return True
    
    except Exception as e:
        print(f"{Colors.RED}[-] Error installing Python dependencies: {e}{Colors.ENDC}")
        return False

def create_config_file():
    """Create configuration file"""
    print(f"{Colors.YELLOW}[*] Creating configuration file...{Colors.ENDC}")
    
    config = {
        "api_keys": {
            "github_token": "",
            "virustotal_api": "",
            "shodan_api": "",
            "censys_uid": "",
            "censys_secret": "",
            "twitter_bearer_token": "",
            "instagram_session": "",
        },
        "proxy": {
            "enabled": False,
            "url": "http://127.0.0.1:8080",
            "username": "",
            "password": "",
        },
        "database": {
            "type": "sqlite",
            "sqlite_path": "osint_data.db",
            "postgresql_url": "postgresql://user:password@localhost/osint",
        },
        "settings": {
            "timeout": 10,
            "max_threads": 10,
            "cache_enabled": True,
            "cache_ttl_hours": 24,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        },
        "output": {
            "format": "json",
            "save_directory": "./results/",
            "include_timestamp": True,
        }
    }
    
    try:
        config_path = Path("config.json")
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"{Colors.GREEN}[+] Configuration file created: {config_path}{Colors.ENDC}")
        print(f"{Colors.YELLOW}[!] Edit config.json to add your API keys{Colors.ENDC}")
        return True
    
    except Exception as e:
        print(f"{Colors.RED}[-] Error creating config file: {e}{Colors.ENDC}")
        return False

def create_directories():
    """Create necessary directories"""
    print(f"{Colors.YELLOW}[*] Creating directories...{Colors.ENDC}")
    
    directories = [
        "results",
        "logs",
        "cache",
        "reports",
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"{Colors.GREEN}[+] Created directory: {directory}{Colors.ENDC}")

def create_launcher_scripts():
    """Create platform-specific launcher scripts"""
    print(f"{Colors.YELLOW}[*] Creating launcher scripts...{Colors.ENDC}")
    
    platform_type = detect_platform()
    python_exe = get_python_executable()
    
    if is_windows():
        # Batch script for Windows
        batch_content = f"""@echo off
REM NEXUS OSINT Launcher for Windows
"{python_exe}" osint_framework.py %*
"""
        with open("nexus.bat", 'w') as f:
            f.write(batch_content)
        
        print(f"{Colors.GREEN}[+] Created launcher: nexus.bat{Colors.ENDC}")
    
    else:
        # Bash script for Unix-like systems
        bash_content = f"""#!/bin/bash
# NEXUS OSINT Launcher for Linux/macOS/Termux
"{python_exe}" osint_framework.py "$@"
"""
        launcher_path = Path("nexus")
        with open(launcher_path, 'w') as f:
            f.write(bash_content)
        
        # Make executable
        os.chmod(launcher_path, 0o755)
        print(f"{Colors.GREEN}[+] Created launcher: nexus{Colors.ENDC}")

def test_installation():
    """Test if installation was successful"""
    print(f"{Colors.YELLOW}[*] Testing installation...{Colors.ENDC}")
    
    python_exe = get_python_executable()
    
    try:
        result = subprocess.run([python_exe, "-c", 
                               "import aiohttp, dns.resolver, requests; print('✓ Core modules OK')"],
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"{Colors.GREEN}[+] {result.stdout.strip()}{Colors.ENDC}")
            return True
        else:
            print(f"{Colors.RED}[-] Installation test failed:{Colors.ENDC}")
            print(result.stderr)
            return False
    
    except Exception as e:
        print(f"{Colors.RED}[-] Error during installation test: {e}{Colors.ENDC}")
        return False

def main():
    print_banner()
    
    platform_type = detect_platform()
    print(f"{Colors.CYAN}Platform: {platform_type.upper()}{Colors.ENDC}\n")
    
    # Step 1: System dependencies
    if not install_system_dependencies():
        print(f"{Colors.RED}[-] Failed to install system dependencies{Colors.ENDC}")
        sys.exit(1)
    
    # Step 2: Create virtual environment
    if create_python_venv():
        print(f"{Colors.YELLOW}[*] To activate virtual environment:{Colors.ENDC}")
        if is_windows():
            print(f"    nexus_env\\Scripts\\activate")
        else:
            print(f"    source nexus_env/bin/activate")
    
    # Step 3: Install Python dependencies
    if not install_python_dependencies():
        print(f"{Colors.RED}[-] Failed to install Python dependencies{Colors.ENDC}")
        sys.exit(1)
    
    # Step 4: Create directories
    create_directories()
    
    # Step 5: Create configuration
    create_config_file()
    
    # Step 6: Create launcher scripts
    create_launcher_scripts()
    
    # Step 7: Test installation
    if test_installation():
        print(f"\n{Colors.GREEN}{Colors.BOLD}╔════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.GREEN}{Colors.BOLD}║  ✓ Installation Successful!             ║{Colors.ENDC}")
        print(f"{Colors.GREEN}{Colors.BOLD}╚════════════════════════════════════════╝{Colors.ENDC}")
        
        print(f"\n{Colors.CYAN}Quick Start:{Colors.ENDC}")
        if is_windows():
            print(f"  1. Activate venv: nexus_env\\Scripts\\activate")
            print(f"  2. Run: python osint_framework.py --help")
            print(f"  3. Or use: nexus.bat --help")
        else:
            print(f"  1. Activate venv: source nexus_env/bin/activate")
            print(f"  2. Run: python3 osint_framework.py --help")
            print(f"  3. Or use: ./nexus --help")
        
        print(f"\n{Colors.CYAN}Examples:{Colors.ENDC}")
        print(f"  Domain reconnaissance:")
        print(f"    python3 osint_framework.py --domain example.com --full")
        print(f"\n  Network reconnaissance:")
        print(f"    python3 osint_framework.py --ip 8.8.8.8 --ports --geo")
        print(f"\n  Username search:")
        print(f"    python3 osint_framework.py --username john_doe --full")
        print(f"\n  Email verification:")
        print(f"    python3 osint_framework.py --email test@example.com --full")
        
        print(f"\n{Colors.YELLOW}[!] Don't forget to configure API keys in config.json{Colors.ENDC}")
        print(f"{Colors.YELLOW}[!] Supported APIs: GitHub, VirusTotal, Shodan, Censys, etc.{Colors.ENDC}\n")
    
    else:
        print(f"{Colors.RED}[-] Installation test failed. Please check the errors above.{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Installation cancelled by user{Colors.ENDC}")
        sys.exit(0)
