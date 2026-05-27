#!/usr/bin/env python3
"""
Information Gathering Techniques & Tools Terminal Viewer
Displays comprehensive list of techniques with colored output

Author: Ethical Hacking Course
Version: 1.0
Usage: python tools/info_viewer.py [options]
"""

import os
import sys
import argparse
from colorama import Fore, Back, Style, init

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Initialize colorama for Windows compatibility
init(autoreset=True)

class InfoViewer:
    def __init__(self):
        self.techniques = {
            'passive': {
                'P01': {'name': 'WHOIS Lookup', 'tools': 'whois, python-whois', 'status': '✅'},
                'P02': {'name': 'DNS Enumeration', 'tools': 'dnspython, socket', 'status': '✅'},
                'P03': {'name': 'Subdomain Discovery', 'tools': 'Custom wordlist, DNS resolution', 'status': '✅'},
                'P04': {'name': 'SSL Certificate Analysis', 'tools': 'ssl, socket', 'status': '✅'},
                'P05': {'name': 'Google Dorking', 'tools': 'requests, custom queries', 'status': '✅'},
                'P06': {'name': 'Email Harvesting', 'tools': 'requests, regex', 'status': '✅'},
                'P07': {'name': 'Metadata Extraction', 'tools': 'exifread, PyPDF2', 'status': '⏳'},
                'P08': {'name': 'Social Media Intel', 'tools': 'APIs, web scraping', 'status': '⏳'},
                'P09': {'name': 'Archive Analysis', 'tools': 'Wayback Machine API', 'status': '⏳'},
                'P10': {'name': 'Code Repository Search', 'tools': 'GitHub API', 'status': '⏳'},
            },
            'active': {
                'A01': {'name': 'Port Scanning', 'tools': 'python-nmap', 'status': '✅'},
                'A02': {'name': 'Service Detection', 'tools': 'nmap, custom banners', 'status': '✅'},
                'A03': {'name': 'OS Fingerprinting', 'tools': 'nmap NSE scripts', 'status': '✅'},
                'A04': {'name': 'Web Technology Detection', 'tools': 'requests, headers analysis', 'status': '✅'},
                'A05': {'name': 'Directory Enumeration', 'tools': 'requests, threading', 'status': '✅'},
                'A06': {'name': 'Parameter Discovery', 'tools': 'custom fuzzing', 'status': '⏳'},
                'A07': {'name': 'Database Fingerprinting', 'tools': 'Custom probes', 'status': '⏳'},
                'A08': {'name': 'API Discovery', 'tools': 'requests, pattern matching', 'status': '⏳'},
                'A09': {'name': 'Network Mapping', 'tools': 'traceroute, ping', 'status': '⏳'},
                'A10': {'name': 'Vulnerability Scanning', 'tools': 'Custom checks', 'status': '⏳'},
            },
            'web': {
                'W01': {'name': 'Robots.txt Analysis', 'tools': 'requests', 'status': '✅'},
                'W02': {'name': 'Sitemap Analysis', 'tools': 'requests, XML parsing', 'status': '✅'},
                'W03': {'name': 'Source Code Analysis', 'tools': 'BeautifulSoup, regex', 'status': '✅'},
                'W04': {'name': 'Cookie Analysis', 'tools': 'requests.cookies', 'status': '✅'},
                'W05': {'name': 'Header Analysis', 'tools': 'requests.headers', 'status': '✅'},
                'W06': {'name': 'Form Discovery', 'tools': 'BeautifulSoup', 'status': '⏳'},
                'W07': {'name': 'JavaScript Analysis', 'tools': 'regex, ast parsing', 'status': '⏳'},
                'W08': {'name': 'Error Page Analysis', 'tools': 'Custom requests', 'status': '⏳'},
                'W09': {'name': 'CDN Detection', 'tools': 'DNS, headers', 'status': '⏳'},
                'W10': {'name': 'CMS Detection', 'tools': 'signatures, patterns', 'status': '✅'},
            },
            'specialized': {
                'S01': {'name': 'Cloud Storage Discovery', 'tools': 'boto3, custom enum', 'status': '⏳'},
                'S02': {'name': 'GraphQL Introspection', 'tools': 'requests, GraphQL', 'status': '⏳'},
                'S03': {'name': 'API Documentation', 'tools': 'requests, OpenAPI', 'status': '⏳'},
                'S04': {'name': 'Certificate Transparency', 'tools': 'CT logs API', 'status': '⏳'},
                'S05': {'name': 'Shodan Integration', 'tools': 'Shodan API', 'status': '⏳'},
                'S06': {'name': 'Threat Intelligence', 'tools': 'Various APIs', 'status': '⏳'},
                'S07': {'name': 'Geolocation Analysis', 'tools': 'IP geolocation APIs', 'status': '✅'},
                'S08': {'name': 'Network Range Discovery', 'tools': 'whois, CIDR', 'status': '⏳'},
                'S09': {'name': 'Email Format Discovery', 'tools': 'pattern analysis', 'status': '✅'},
                'S10': {'name': 'Technology Versioning', 'tools': 'banner analysis', 'status': '✅'},
            }
        }
        
        self.popular_tools = {
            'Reconnaissance': ['Nmap', 'theHarvester', 'Maltego', 'Recon-ng', 'SpiderFoot'],
            'DNS Analysis': ['dig', 'nslookup', 'dnsrecon', 'fierce', 'sublist3r', 'amass'],
            'Web Scanning': ['dirb', 'gobuster', 'wfuzz', 'Burp Suite', 'OWASP ZAP'],
            'OSINT': ['Shodan', 'Censys', 'Google Dorking', 'Social-Engineer Toolkit'],
            'Network Mapping': ['Nmap', 'Masscan', 'Zmap', 'Hping3', 'Unicornscan']
        }

    def print_banner(self):
        """Print colorful banner"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║                    Information Gathering Techniques                  ║
║                          & Tools Reference                           ║
║                                                                      ║
║  {Fore.YELLOW}📋 Comprehensive Index of Ethical Hacking Techniques{Fore.CYAN}          ║
║  {Fore.GREEN}🔍 40 Different Information Gathering Methods{Fore.CYAN}                 ║
║  {Fore.RED}⚠️  FOR EDUCATIONAL & AUTHORIZED TESTING ONLY{Fore.CYAN}                 ║
╚══════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)

    def print_section_header(self, title, color=Fore.YELLOW):
        """Print section header with formatting"""
        print(f"\n{color}{'='*70}")
        print(f"{title.center(70)}")
        print(f"{'='*70}{Style.RESET_ALL}")

    def print_technique_table(self, category, techniques):
        """Print formatted technique table"""
        print(f"\n{Fore.CYAN}┌─────┬─────────────────────────────┬──────────────────────────┬────────┐")
        print(f"│{Fore.WHITE} ID  {Fore.CYAN}│{Fore.WHITE} Technique Name              {Fore.CYAN}│{Fore.WHITE} Tools Used               {Fore.CYAN}│{Fore.WHITE} Status {Fore.CYAN}│")
        print(f"├─────┼─────────────────────────────┼──────────────────────────┼────────┤{Style.RESET_ALL}")
        
        for tech_id, details in techniques.items():
            name = details['name'][:27] + '...' if len(details['name']) > 27 else details['name'].ljust(27)
            tools = details['tools'][:24] + '...' if len(details['tools']) > 24 else details['tools'].ljust(24)
            status = details['status']
            
            # Color coding for status
            if status == '✅':
                status_color = Fore.GREEN
            else:
                status_color = Fore.YELLOW
                
            print(f"{Fore.CYAN}│{Fore.YELLOW} {tech_id} {Fore.CYAN}│{Fore.WHITE} {name} {Fore.CYAN}│{Fore.LIGHTBLUE_EX} {tools} {Fore.CYAN}│{status_color} {status}  {Fore.CYAN}│{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}└─────┴─────────────────────────────┴──────────────────────────┴────────┘{Style.RESET_ALL}")

    def print_statistics(self):
        """Print implementation statistics"""
        total = sum(len(cat) for cat in self.techniques.values())
        implemented = sum(1 for cat in self.techniques.values() for tech in cat.values() if tech['status'] == '✅')
        in_progress = total - implemented
        
        print(f"\n{Fore.GREEN}📊 IMPLEMENTATION STATISTICS:")
        print(f"{Fore.WHITE}   • Total Techniques: {Fore.YELLOW}{total}")
        print(f"{Fore.WHITE}   • Implemented: {Fore.GREEN}{implemented} ({implemented/total*100:.0f}%)")
        print(f"{Fore.WHITE}   • In Progress: {Fore.YELLOW}{in_progress} ({in_progress/total*100:.0f}%)")
        
        for category, techniques in self.techniques.items():
            cat_total = len(techniques)
            cat_impl = sum(1 for tech in techniques.values() if tech['status'] == '✅')
            print(f"{Fore.WHITE}   • {category.title()}: {Fore.CYAN}{cat_impl}/{cat_total} ({cat_impl/cat_total*100:.0f}%)")

    def print_popular_tools(self):
        """Print popular tools by category"""
        self.print_section_header("🛠️  POPULAR TOOLS BY CATEGORY", Fore.MAGENTA)
        
        for category, tools in self.popular_tools.items():
            print(f"\n{Fore.CYAN}🔹 {Fore.YELLOW}{category}:")
            for i, tool in enumerate(tools, 1):
                print(f"{Fore.WHITE}   {i}. {Fore.LIGHTGREEN_EX}{tool}")

    def print_quick_commands(self):
        """Print quick command examples"""
        self.print_section_header("⚡ QUICK COMMAND EXAMPLES", Fore.GREEN)
        
        commands = [
            ("Basic WHOIS Lookup", "whois example.com"),
            ("DNS Enumeration", "dig example.com ANY"),
            ("Subdomain Discovery", "nslookup -type=NS example.com"),
            ("Port Scan (Top 1000)", "nmap -T4 -F example.com"),
            ("Web Technology Detection", "curl -I https://example.com"),
            ("Directory Enumeration", "dirb https://example.com"),
            ("SSL Certificate Info", "openssl s_client -connect example.com:443"),
            ("Email Harvesting", "theharvester -d example.com -b google"),
        ]
        
        print(f"\n{Fore.CYAN}┌─────────────────────────────┬──────────────────────────────────────┐")
        print(f"│{Fore.WHITE} Technique                   {Fore.CYAN}│{Fore.WHITE} Command Example                      {Fore.CYAN}│")
        print(f"├─────────────────────────────┼──────────────────────────────────────┤{Style.RESET_ALL}")
        
        for technique, command in commands:
            tech_name = technique[:27].ljust(27)
            cmd = command[:36].ljust(36)
            print(f"{Fore.CYAN}│{Fore.YELLOW} {tech_name} {Fore.CYAN}│{Fore.LIGHTGREEN_EX} {cmd} {Fore.CYAN}│{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}└─────────────────────────────┴──────────────────────────────────────┘{Style.RESET_ALL}")

    def print_usage_guide(self):
        """Print usage guide"""
        self.print_section_header("📖 USAGE GUIDE", Fore.BLUE)
        
        usage_info = [
            ("View all techniques", "python info_viewer.py"),
            ("View specific category", "python info_viewer.py -c passive"),
            ("View technique details", "python info_viewer.py -t P01"),
            ("Show only implemented", "python info_viewer.py --implemented"),
            ("Export to file", "python info_viewer.py -o techniques.txt"),
            ("Generate PDF report", "python pdf_generator.py"),
        ]
        
        print(f"\n{Fore.WHITE}Command Line Options:")
        for description, command in usage_info:
            print(f"{Fore.CYAN}  • {Fore.YELLOW}{description}: {Fore.LIGHTGREEN_EX}{command}")

    def show_technique_details(self, tech_id):
        """Show detailed information about a specific technique"""
        found = False
        for category, techniques in self.techniques.items():
            if tech_id in techniques:
                tech = techniques[tech_id]
                found = True
                
                print(f"\n{Fore.YELLOW}{'='*50}")
                print(f"TECHNIQUE DETAILS: {tech_id}")
                print(f"{'='*50}{Style.RESET_ALL}")
                
                print(f"{Fore.CYAN}Name: {Fore.WHITE}{tech['name']}")
                print(f"{Fore.CYAN}Category: {Fore.WHITE}{category.title()}")
                print(f"{Fore.CYAN}Tools: {Fore.WHITE}{tech['tools']}")
                print(f"{Fore.CYAN}Status: {Fore.GREEN if tech['status'] == '✅' else Fore.YELLOW}{tech['status']}")
                
                # Add technique-specific details
                details = self.get_technique_details(tech_id)
                if details:
                    print(f"\n{Fore.CYAN}Description:")
                    print(f"{Fore.WHITE}{details['description']}")
                    
                    if 'examples' in details:
                        print(f"\n{Fore.CYAN}Examples:")
                        for example in details['examples']:
                            print(f"{Fore.LIGHTGREEN_EX}  • {example}")
                
                break
        
        if not found:
            print(f"{Fore.RED}Technique {tech_id} not found!")

    def get_technique_details(self, tech_id):
        """Get detailed description for a technique"""
        details_map = {
            'P01': {
                'description': 'WHOIS lookup retrieves domain registration information including registrar, creation date, expiry, and contact details.',
                'examples': ['Domain ownership information', 'Contact email addresses', 'Name server details', 'Registration timeline']
            },
            'A01': {
                'description': 'Port scanning identifies open TCP/UDP ports on target systems, revealing potentially accessible services.',
                'examples': ['Common ports: 22(SSH), 80(HTTP), 443(HTTPS), 21(FTP)', 'Service version detection', 'Operating system fingerprinting']
            },
            # Add more as needed...
        }
        
        return details_map.get(tech_id, None)

    def display_all(self):
        """Display complete information"""
        self.print_banner()
        
        self.print_section_header("🔍 PASSIVE INFORMATION GATHERING", Fore.BLUE)
        self.print_technique_table('passive', self.techniques['passive'])
        
        self.print_section_header("⚡ ACTIVE INFORMATION GATHERING", Fore.RED)
        self.print_technique_table('active', self.techniques['active'])
        
        self.print_section_header("🌐 WEB-BASED INFORMATION GATHERING", Fore.GREEN)
        self.print_technique_table('web', self.techniques['web'])
        
        self.print_section_header("🎯 SPECIALIZED TECHNIQUES", Fore.MAGENTA)
        self.print_technique_table('specialized', self.techniques['specialized'])
        
        self.print_statistics()
        self.print_popular_tools()
        self.print_quick_commands()
        self.print_usage_guide()
        
        print(f"\n{Fore.YELLOW}⚠️  LEGAL DISCLAIMER: {Fore.WHITE}Only use these techniques on systems you own or have explicit written permission to test.{Style.RESET_ALL}")

    def display_category(self, category):
        """Display specific category"""
        if category not in self.techniques:
            print(f"{Fore.RED}Category '{category}' not found!")
            return
            
        self.print_banner()
        self.print_section_header(f"{category.upper()} TECHNIQUES", Fore.CYAN)
        self.print_technique_table(category, self.techniques[category])

    def display_implemented(self):
        """Display only implemented techniques"""
        self.print_banner()
        self.print_section_header("IMPLEMENTED TECHNIQUES", Fore.GREEN)

        for category, techniques in self.techniques.items():
            implemented = {
                tech_id: details
                for tech_id, details in techniques.items()
                if details['status'] == '✅'
            }
            if implemented:
                self.print_section_header(f"{category.upper()} TECHNIQUES", Fore.CYAN)
                self.print_technique_table(category, implemented)

    def save_to_file(self, filename):
        """Save output to file"""
        # Redirect stdout to file
        original_stdout = sys.stdout
        with open(filename, 'w', encoding='utf-8') as f:
            sys.stdout = f
            # Print without colors for file output
            init(strip=True)
            self.display_all()
        
        sys.stdout = original_stdout
        init()  # Re-initialize with colors
        print(f"{Fore.GREEN}Output saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Information Gathering Techniques Viewer")
    parser.add_argument('-c', '--category', choices=['passive', 'active', 'web', 'specialized'], 
                       help="Show specific category only")
    parser.add_argument('-t', '--technique', help="Show details for specific technique (e.g., P01)")
    parser.add_argument('--implemented', action='store_true', help="Show only implemented techniques")
    parser.add_argument('-o', '--output', help="Save output to file")
    
    args = parser.parse_args()
    
    viewer = InfoViewer()
    
    if args.technique:
        viewer.show_technique_details(args.technique.upper())
    elif args.implemented:
        viewer.display_implemented()
    elif args.category:
        viewer.display_category(args.category)
    elif args.output:
        viewer.save_to_file(args.output)
    else:
        viewer.display_all()

if __name__ == "__main__":
    main()
