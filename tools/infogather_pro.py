#!/usr/bin/env python3
"""
InfoGather Pro - Comprehensive Information Gathering Tool
Educational Ethical Hacking Tool for Authorized Testing Only

Author: Ethical Hacking Course
Version: 1.0
License: Educational Use Only

WARNING: This tool is for educational purposes and authorized testing only!
Only use on systems you own or have explicit written permission to test.
"""

import socket
import subprocess
import requests
import ssl
import threading
import json
import re
import sys
import argparse
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
import os
import tempfile
import urllib3

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import dns.resolver
except ImportError:
    dns = None

try:
    import whois
except ImportError:
    whois = None

try:
    import nmap
except ImportError:
    nmap = None

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class InfoGatherPro:
    def __init__(self):
        self.results = {}
        self.target = None
        self.verbose = False
        
    def banner(self):
        """Display tool banner"""
        banner_text = """
==================================================================
                   ⚠️  InfoHub Toolkit  ⚠️
            !~  Developed by Dulanka Charidu  ~
==================================================================          
╔══════════════════════════════════════════════════════════════╗
║                    InfoGather Pro v1.0                       ║
║              Comprehensive Information Gathering             ║
║                                                              ║
║  ⚠️  FOR EDUCATIONAL & AUTHORIZED TESTING ONLY ⚠️           ║
║                                                              ║
║  Only use on systems you OWN or have WRITTEN PERMISSION!     ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(banner_text)
    
    def log(self, message, level="INFO"):
        """Logging function"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def save_results(self, filename=None):
        """Save results to JSON file"""
        if not filename:
            safe_target = re.sub(r"[^A-Za-z0-9_.-]+", "_", self.target or "scan_results").strip("_")
            filename = Path("reports") / f"infogather_{safe_target}_{int(time.time())}.json"

        output_path = Path(filename)
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with output_path.open('w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, default=str)
        except OSError as e:
            fallback_path = Path(tempfile.gettempdir()) / output_path.name
            self.log(f"Cannot write to {output_path}: {e}. Saving to {fallback_path} instead.", "WARNING")
            with fallback_path.open('w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, default=str)
            output_path = fallback_path

        self.log(f"Results saved to {output_path}")
    
    # ============================================================
    # PASSIVE INFORMATION GATHERING METHODS
    # ============================================================
    
    def whois_lookup(self, domain):
        """WHOIS information gathering"""
        self.log(f"Performing WHOIS lookup for {domain}")
        if whois is None:
            self.log("python-whois is not installed. Skipping WHOIS lookup.", "WARNING")
            self.results['whois'] = {'error': 'python-whois is not installed'}
            return None

        try:
            w = whois.whois(domain)
            whois_data = {
                'domain_name': w.domain_name,
                'registrar': w.registrar,
                'creation_date': w.creation_date,
                'expiration_date': w.expiration_date,
                'name_servers': w.name_servers,
                'emails': w.emails,
                'country': w.country
            }
            self.results['whois'] = whois_data
            return whois_data
        except Exception as e:
            self.log(f"WHOIS lookup failed: {str(e)}", "ERROR")
            return None
    
    def dns_enumeration(self, domain):
        """DNS enumeration and subdomain discovery"""
        self.log(f"Performing DNS enumeration for {domain}")
        dns_results = {}

        if dns is None:
            self.log("dnspython is not installed. Skipping DNS record lookup.", "WARNING")
            self.results['dns'] = {'error': 'dnspython is not installed'}
            return dns_results
        
        # Common DNS record types
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                dns_results[record_type] = [str(answer) for answer in answers]
            except Exception as e:
                dns_results[record_type] = f"No {record_type} records found"
        
        # Common subdomains to check
        common_subdomains = ['www', 'mail', 'ftp', 'admin', 'test', 'dev', 'api', 
                           'blog', 'shop', 'secure', 'vpn', 'remote', 'support']
        
        found_subdomains = []
        for subdomain in common_subdomains:
            try:
                full_domain = f"{subdomain}.{domain}"
                socket.gethostbyname(full_domain)
                found_subdomains.append(full_domain)
                self.log(f"Found subdomain: {full_domain}")
            except:
                pass
        
        dns_results['subdomains'] = found_subdomains
        self.results['dns'] = dns_results
        return dns_results
    
    def ssl_certificate_info(self, domain, port=443):
        """SSL/TLS certificate information"""
        self.log(f"Gathering SSL certificate info for {domain}:{port}")
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    ssl_info = {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'version': cert['version'],
                        'serial_number': cert['serialNumber'],
                        'not_before': cert['notBefore'],
                        'not_after': cert['notAfter'],
                        'san': cert.get('subjectAltName', [])
                    }
                    
                    self.results['ssl_certificate'] = ssl_info
                    return ssl_info
        except Exception as e:
            self.log(f"SSL certificate gathering failed: {str(e)}", "ERROR")
            return None
    
    # ============================================================
    # ACTIVE INFORMATION GATHERING METHODS
    # ============================================================
    
    def port_scan(self, target, port_range="1-1000"):
        """TCP port scanning"""
        self.log(f"Scanning ports {port_range} on {target}")

        if nmap is None:
            self.log("python-nmap is not installed. Skipping port scan.", "WARNING")
            self.results['port_scan'] = {
                'target': target,
                'open_ports': [],
                'error': 'python-nmap is not installed'
            }
            return []
        
        nm = nmap.PortScanner()
        try:
            scan_result = nm.scan(target, port_range)
            
            open_ports = []
            for host in scan_result['scan']:
                for port in scan_result['scan'][host]['tcp']:
                    if scan_result['scan'][host]['tcp'][port]['state'] == 'open':
                        service = scan_result['scan'][host]['tcp'][port]['name']
                        version = scan_result['scan'][host]['tcp'][port].get('version', '')
                        open_ports.append({
                            'port': port,
                            'service': service,
                            'version': version
                        })
            
            self.results['port_scan'] = {
                'target': target,
                'open_ports': open_ports,
                'scan_time': str(datetime.now())
            }
            
            self.log(f"Found {len(open_ports)} open ports")
            return open_ports
            
        except Exception as e:
            self.log(f"Port scan failed: {str(e)}", "ERROR")
            return []
    
    def web_technology_detection(self, url):
        """Detect web technologies and frameworks"""
        self.log(f"Detecting web technologies for {url}")
        
        try:
            response = requests.get(url, timeout=10, verify=False)
            
            tech_info = {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'server': response.headers.get('Server', 'Unknown'),
                'technologies': []
            }
            
            # Check for common technologies in headers and content
            content = response.text.lower()
            headers_str = str(response.headers).lower()
            
            # Technology detection patterns
            tech_patterns = {
                'WordPress': ['wp-content', 'wp-includes', 'wordpress'],
                'Drupal': ['drupal', 'sites/default'],
                'Joomla': ['joomla', 'option=com_'],
                'Apache': ['apache'],
                'Nginx': ['nginx'],
                'PHP': ['x-powered-by: php', '.php'],
                'ASP.NET': ['x-aspnet-version', 'viewstate'],
                'jQuery': ['jquery'],
                'Bootstrap': ['bootstrap'],
                'Angular': ['ng-'],
                'React': ['react']
            }
            
            for tech, patterns in tech_patterns.items():
                if any(pattern in content or pattern in headers_str for pattern in patterns):
                    tech_info['technologies'].append(tech)
            
            self.results['web_technology'] = tech_info
            return tech_info
            
        except Exception as e:
            self.log(f"Web technology detection failed: {str(e)}", "ERROR")
            return None
    
    def directory_enumeration(self, url, wordlist=None):
        """Web directory and file enumeration"""
        self.log(f"Performing directory enumeration on {url}")
        
        if not wordlist:
            # Common directories and files to check
            wordlist = [
                'admin', 'administrator', 'login', 'panel', 'dashboard',
                'wp-admin', 'phpmyadmin', 'cpanel', 'webmail',
                'backup', 'backups', 'test', 'dev', 'staging',
                'api', 'v1', 'v2', 'rest', 'graphql',
                'robots.txt', 'sitemap.xml', '.htaccess', 'web.config',
                'readme.txt', 'changelog.txt', 'version.txt'
            ]
        
        found_paths = []
        
        def check_path(path):
            try:
                test_url = urljoin(url, path)
                response = requests.get(test_url, timeout=5, allow_redirects=False)
                if response.status_code in [200, 301, 302, 403]:
                    found_paths.append({
                        'path': path,
                        'url': test_url,
                        'status_code': response.status_code,
                        'size': len(response.content)
                    })
                    self.log(f"Found: {test_url} [{response.status_code}]")
            except:
                pass
        
        # Use threading for faster enumeration
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(check_path, wordlist)
        
        self.results['directory_enumeration'] = {
            'url': url,
            'found_paths': found_paths
        }
        
        return found_paths
    
    def email_harvesting(self, domain):
        """Email address harvesting from various sources"""
        self.log(f"Harvesting email addresses for {domain}")
        
        emails = set()
        
        # Search patterns
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        try:
            # Check main domain website
            response = requests.get(f"http://{domain}", timeout=10)
            found_emails = re.findall(email_pattern, response.text)
            emails.update(found_emails)
            
            # Check common pages
            common_pages = ['contact', 'about', 'team', 'staff', 'directory']
            for page in common_pages:
                try:
                    response = requests.get(f"http://{domain}/{page}", timeout=5)
                    found_emails = re.findall(email_pattern, response.text)
                    emails.update(found_emails)
                except:
                    continue
            
            # Filter emails related to the domain
            domain_emails = [email for email in emails if domain in email]
            
            self.results['email_harvesting'] = {
                'domain': domain,
                'emails_found': list(domain_emails),
                'total_count': len(domain_emails)
            }
            
            self.log(f"Found {len(domain_emails)} email addresses")
            return list(domain_emails)
            
        except Exception as e:
            self.log(f"Email harvesting failed: {str(e)}", "ERROR")
            return []
    
    # ============================================================
    # MAIN EXECUTION METHODS
    # ============================================================
    
    def run_passive_scan(self, target):
        """Run all passive information gathering techniques"""
        self.target = target
        self.results['target'] = target
        self.results['scan_start_time'] = str(datetime.now())
        self.log("Starting passive information gathering...")
        
        # WHOIS lookup
        self.whois_lookup(target)
        
        # DNS enumeration
        self.dns_enumeration(target)
        
        # SSL certificate info
        self.ssl_certificate_info(target)
        
        # Email harvesting
        self.email_harvesting(target)
        self.results['scan_end_time'] = str(datetime.now())
    
    def run_active_scan(self, target):
        """Run all active information gathering techniques"""
        self.target = target
        self.results['target'] = target
        self.results['scan_start_time'] = str(datetime.now())
        self.log("Starting active information gathering...")
        
        # Resolve domain to IP
        try:
            ip_address = socket.gethostbyname(target)
            self.log(f"Resolved {target} to {ip_address}")
        except:
            ip_address = target
        
        # Port scanning
        self.port_scan(ip_address)
        
        # Web technology detection
        for protocol in ['http', 'https']:
            self.web_technology_detection(f"{protocol}://{target}")
        
        # Directory enumeration
        for protocol in ['http', 'https']:
            try:
                response = requests.get(f"{protocol}://{target}", timeout=5)
                if response.status_code == 200:
                    self.directory_enumeration(f"{protocol}://{target}")
                    break
            except:
                continue
        self.results['scan_end_time'] = str(datetime.now())
    
    def run_full_scan(self, target):
        """Run complete information gathering scan"""
        self.target = target
        self.results['target'] = target
        self.results['scan_start_time'] = str(datetime.now())
        
        self.log(f"Starting comprehensive scan of {target}")
        
        self.log("Starting passive information gathering...")
        self.whois_lookup(target)
        self.dns_enumeration(target)
        self.ssl_certificate_info(target)
        self.email_harvesting(target)

        self.log("Starting active information gathering...")
        try:
            ip_address = socket.gethostbyname(target)
            self.log(f"Resolved {target} to {ip_address}")
        except:
            ip_address = target

        self.port_scan(ip_address)

        for protocol in ['http', 'https']:
            self.web_technology_detection(f"{protocol}://{target}")

        for protocol in ['http', 'https']:
            try:
                response = requests.get(f"{protocol}://{target}", timeout=5)
                if response.status_code == 200:
                    self.directory_enumeration(f"{protocol}://{target}")
                    break
            except:
                continue
        
        self.results['scan_end_time'] = str(datetime.now())
        self.log("Scan completed!")
    
    def print_results(self):
        """Print formatted results"""
        print("\n" + "="*60)
        print(f"INFORMATION GATHERING RESULTS FOR: {self.target}")
        print("="*60)
        
        for category, data in self.results.items():
            if category in ['target', 'scan_start_time', 'scan_end_time']:
                continue
                
            print(f"\n[{category.upper().replace('_', ' ')}]")
            print("-" * 40)
            
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        print(f"{key}: {len(value)} items")
                        for item in value[:5]:  # Show first 5 items
                            print(f"  - {item}")
                        if len(value) > 5:
                            print(f"  ... and {len(value) - 5} more")
                    else:
                        print(f"{key}: {value}")
            else:
                print(str(data))

def main():
    parser = argparse.ArgumentParser(description="InfoGather Pro - Comprehensive Information Gathering Tool")
    parser.add_argument("target", help="Target domain or IP address")
    parser.add_argument("-p", "--passive", action="store_true", help="Run only passive techniques")
    parser.add_argument("-a", "--active", action="store_true", help="Run only active techniques")
    parser.add_argument("-o", "--output", help="Output file for results (JSON)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--yes", action="store_true",
                       help="Confirm you are authorized to test the target")
    
    args = parser.parse_args()
    
    # Create InfoGather instance
    scanner = InfoGatherPro()
    scanner.verbose = args.verbose
    
    # Display banner
    scanner.banner()
    
    # Legal warning
    print("\n⚠️  LEGAL WARNING:")
    print("This tool should only be used on systems you own or have explicit permission to test.")
    print("Unauthorized access to computer systems is illegal in most jurisdictions.")
    response = "yes" if args.yes else input("\nDo you have authorization to test this target? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("Exiting. Only use this tool on authorized targets.")
        sys.exit(1)
    
    # Run appropriate scan type
    if args.passive:
        scanner.run_passive_scan(args.target)
    elif args.active:
        scanner.run_active_scan(args.target)
    else:
        scanner.run_full_scan(args.target)
    
    # Display results
    scanner.print_results()
    
    # Save results if output file specified
    if args.output:
        scanner.save_results(args.output)
    else:
        scanner.save_results()

if __name__ == "__main__":
    main()
