#!/usr/bin/env python3
"""
Information Gathering Techniques PDF Report Generator
Creates comprehensive PDF documentation of all techniques and tools

Author: Ethical Hacking Course
Version: 1.0
Usage: python tools/pdf_generator.py [options]
"""

import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white, blue, green, red, orange
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import argparse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

class PDFGenerator:
    def __init__(self):
        self.techniques = {
            'Passive Information Gathering': {
                'P01': {'name': 'WHOIS Lookup', 'tools': 'whois, python-whois', 'status': '✅', 'desc': 'Retrieve domain registration information'},
                'P02': {'name': 'DNS Enumeration', 'tools': 'dnspython, socket', 'status': '✅', 'desc': 'Enumerate DNS records and configuration'},
                'P03': {'name': 'Subdomain Discovery', 'tools': 'Custom wordlist, DNS resolution', 'status': '✅', 'desc': 'Discover subdomains and virtual hosts'},
                'P04': {'name': 'SSL Certificate Analysis', 'tools': 'ssl, socket', 'status': '✅', 'desc': 'Extract SSL/TLS certificate information'},
                'P05': {'name': 'Google Dorking', 'tools': 'requests, custom queries', 'status': '✅', 'desc': 'Advanced search engine reconnaissance'},
                'P06': {'name': 'Email Harvesting', 'tools': 'requests, regex', 'status': '✅', 'desc': 'Collect email addresses from various sources'},
                'P07': {'name': 'Metadata Extraction', 'tools': 'exifread, PyPDF2', 'status': '⏳', 'desc': 'Extract metadata from documents and images'},
                'P08': {'name': 'Social Media Intel', 'tools': 'APIs, web scraping', 'status': '⏳', 'desc': 'Gather intelligence from social media platforms'},
                'P09': {'name': 'Archive Analysis', 'tools': 'Wayback Machine API', 'status': '⏳', 'desc': 'Analyze historical website content'},
                'P10': {'name': 'Code Repository Search', 'tools': 'GitHub API', 'status': '⏳', 'desc': 'Search public code repositories for information'},
            },
            'Active Information Gathering': {
                'A01': {'name': 'Port Scanning', 'tools': 'python-nmap', 'status': '✅', 'desc': 'Identify open ports and services'},
                'A02': {'name': 'Service Detection', 'tools': 'nmap, custom banners', 'status': '✅', 'desc': 'Detect service versions and configurations'},
                'A03': {'name': 'OS Fingerprinting', 'tools': 'nmap NSE scripts', 'status': '✅', 'desc': 'Identify target operating systems'},
                'A04': {'name': 'Web Technology Detection', 'tools': 'requests, headers analysis', 'status': '✅', 'desc': 'Identify web technologies and frameworks'},
                'A05': {'name': 'Directory Enumeration', 'tools': 'requests, threading', 'status': '✅', 'desc': 'Discover hidden directories and files'},
                'A06': {'name': 'Parameter Discovery', 'tools': 'custom fuzzing', 'status': '⏳', 'desc': 'Discover hidden parameters and endpoints'},
                'A07': {'name': 'Database Fingerprinting', 'tools': 'Custom probes', 'status': '⏳', 'desc': 'Identify database types and versions'},
                'A08': {'name': 'API Discovery', 'tools': 'requests, pattern matching', 'status': '⏳', 'desc': 'Discover API endpoints and documentation'},
                'A09': {'name': 'Network Mapping', 'tools': 'traceroute, ping', 'status': '⏳', 'desc': 'Map network topology and routing'},
                'A10': {'name': 'Vulnerability Scanning', 'tools': 'Custom checks', 'status': '⏳', 'desc': 'Identify potential security vulnerabilities'},
            },
            'Web-Based Information Gathering': {
                'W01': {'name': 'Robots.txt Analysis', 'tools': 'requests', 'status': '✅', 'desc': 'Analyze robots.txt for hidden paths'},
                'W02': {'name': 'Sitemap Analysis', 'tools': 'requests, XML parsing', 'status': '✅', 'desc': 'Parse XML sitemaps for site structure'},
                'W03': {'name': 'Source Code Analysis', 'tools': 'BeautifulSoup, regex', 'status': '✅', 'desc': 'Analyze HTML source code for information'},
                'W04': {'name': 'Cookie Analysis', 'tools': 'requests.cookies', 'status': '✅', 'desc': 'Analyze HTTP cookies and session management'},
                'W05': {'name': 'Header Analysis', 'tools': 'requests.headers', 'status': '✅', 'desc': 'Analyze HTTP response headers'},
                'W06': {'name': 'Form Discovery', 'tools': 'BeautifulSoup', 'status': '⏳', 'desc': 'Discover and analyze HTML forms'},
                'W07': {'name': 'JavaScript Analysis', 'tools': 'regex, ast parsing', 'status': '⏳', 'desc': 'Analyze JavaScript code for information'},
                'W08': {'name': 'Error Page Analysis', 'tools': 'Custom requests', 'status': '⏳', 'desc': 'Analyze error pages for information disclosure'},
                'W09': {'name': 'CDN Detection', 'tools': 'DNS, headers', 'status': '⏳', 'desc': 'Identify content delivery networks'},
                'W10': {'name': 'CMS Detection', 'tools': 'signatures, patterns', 'status': '✅', 'desc': 'Identify content management systems'},
            },
            'Specialized Techniques': {
                'S01': {'name': 'Cloud Storage Discovery', 'tools': 'boto3, custom enum', 'status': '⏳', 'desc': 'Discover publicly accessible cloud storage'},
                'S02': {'name': 'GraphQL Introspection', 'tools': 'requests, GraphQL', 'status': '⏳', 'desc': 'Perform GraphQL schema introspection'},
                'S03': {'name': 'API Documentation', 'tools': 'requests, OpenAPI', 'status': '⏳', 'desc': 'Discover API documentation and specifications'},
                'S04': {'name': 'Certificate Transparency', 'tools': 'CT logs API', 'status': '⏳', 'desc': 'Search certificate transparency logs'},
                'S05': {'name': 'Shodan Integration', 'tools': 'Shodan API', 'status': '⏳', 'desc': 'Integrate with Shodan search engine'},
                'S06': {'name': 'Threat Intelligence', 'tools': 'Various APIs', 'status': '⏳', 'desc': 'Correlate with threat intelligence feeds'},
                'S07': {'name': 'Geolocation Analysis', 'tools': 'IP geolocation APIs', 'status': '✅', 'desc': 'Determine geographic location of targets'},
                'S08': {'name': 'Network Range Discovery', 'tools': 'whois, CIDR', 'status': '⏳', 'desc': 'Discover network ranges and ownership'},
                'S09': {'name': 'Email Format Discovery', 'tools': 'pattern analysis', 'status': '✅', 'desc': 'Discover email naming conventions'},
                'S10': {'name': 'Technology Versioning', 'tools': 'banner analysis', 'status': '✅', 'desc': 'Identify specific technology versions'},
            }
        }
        
        self.popular_tools = {
            'Reconnaissance': ['Nmap', 'theHarvester', 'Maltego', 'Recon-ng', 'SpiderFoot'],
            'DNS Analysis': ['dig', 'nslookup', 'dnsrecon', 'fierce', 'sublist3r', 'amass'],
            'Web Scanning': ['dirb', 'gobuster', 'wfuzz', 'Burp Suite', 'OWASP ZAP'],
            'OSINT': ['Shodan', 'Censys', 'Google Dorking', 'Social-Engineer Toolkit'],
            'Network Mapping': ['Nmap', 'Masscan', 'Zmap', 'Hping3', 'Unicornscan']
        }
        
        self.styles = getSampleStyleSheet()
        self.custom_styles = self.create_custom_styles()
    
    def create_custom_styles(self):
        """Create custom paragraph styles"""
        styles = {}
        
        # Title style
        styles['CustomTitle'] = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#1f4e79'),
            alignment=1  # Center alignment
        )
        
        # Section header style
        styles['SectionHeader'] = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=HexColor('#2f5597'),
            backgroundColor=HexColor('#e8f1ff'),
            borderPadding=8
        )
        
        # Technique name style
        styles['TechniqueName'] = ParagraphStyle(
            'TechniqueName',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=6,
            textColor=HexColor('#1f4e79'),
            fontName='Helvetica-Bold'
        )
        
        # Body text style
        styles['CustomBody'] = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=black
        )
        
        return styles
    
    def create_cover_page(self, doc, elements):
        """Create PDF cover page"""
        # Title
        title = Paragraph("Information Gathering Techniques", self.custom_styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle = Paragraph("Comprehensive Ethical Hacking Reference", self.styles['Heading2'])
        elements.append(subtitle)
        elements.append(Spacer(1, 0.3*inch))
        
        # Warning box
        warning_text = """
        <para align="center" backColor="#ffebee" borderColor="#f44336" borderWidth="2" borderPadding="12">
        <b>⚠️ IMPORTANT LEGAL DISCLAIMER ⚠️</b><br/><br/>
        This documentation is for <b>EDUCATIONAL PURPOSES ONLY</b>.<br/>
        Only use these techniques on systems you <b>OWN</b> or have <b>EXPLICIT WRITTEN PERMISSION</b> to test.<br/>
        Unauthorized access to computer systems is <b>ILLEGAL</b> in most jurisdictions.
        </para>
        """
        warning = Paragraph(warning_text, self.styles['Normal'])
        elements.append(warning)
        elements.append(Spacer(1, 0.5*inch))
        
        # Statistics
        total_techniques = sum(len(cat) for cat in self.techniques.values())
        implemented = sum(1 for cat in self.techniques.values() 
                         for tech in cat.values() if tech['status'] == '✅')
        
        stats_text = f"""
        <para align="center">
        <b>Course Statistics:</b><br/>
        📊 Total Techniques: {total_techniques}<br/>
        ✅ Implemented: {implemented}<br/>
        📚 Categories: {len(self.techniques)}<br/>
        🛠️ Popular Tools: {sum(len(tools) for tools in self.popular_tools.values())}<br/>
        </para>
        """
        stats = Paragraph(stats_text, self.styles['Normal'])
        elements.append(stats)
        elements.append(Spacer(1, 0.5*inch))
        
        # Generation info
        gen_info = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                           self.styles['Normal'])
        elements.append(gen_info)
        
        elements.append(PageBreak())
    
    def create_table_of_contents(self, elements):
        """Create table of contents"""
        toc_title = Paragraph("Table of Contents", self.custom_styles['CustomTitle'])
        elements.append(toc_title)
        elements.append(Spacer(1, 0.3*inch))
        
        toc_data = [
            ['Section', 'Page'],
            ['1. Overview', '3'],
            ['2. Passive Information Gathering', '4'],
            ['3. Active Information Gathering', '6'],
            ['4. Web-Based Information Gathering', '8'],
            ['5. Specialized Techniques', '10'],
            ['6. Popular Tools Reference', '12'],
            ['7. Command Examples', '13'],
            ['8. Legal Considerations', '14'],
            ['9. Learning Resources', '15'],
        ]
        
        toc_table = Table(toc_data, colWidths=[4*inch, 1*inch])
        toc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#4472c4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f2f2f2')),
            ('GRID', (0, 0), (-1, -1), 1, black)
        ]))
        
        elements.append(toc_table)
        elements.append(PageBreak())
    
    def create_overview_section(self, elements):
        """Create overview section"""
        title = Paragraph("1. Overview", self.custom_styles['SectionHeader'])
        elements.append(title)
        
        overview_text = """
        This comprehensive reference covers 40 different information gathering techniques 
        used in ethical hacking, penetration testing, and cybersecurity assessments. 
        The techniques are organized into four main categories:
        """
        elements.append(Paragraph(overview_text, self.custom_styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Category summary
        for category, techniques in self.techniques.items():
            total = len(techniques)
            implemented = sum(1 for tech in techniques.values() if tech['status'] == '✅')
            
            cat_text = f"<b>{category}:</b> {implemented}/{total} techniques implemented"
            elements.append(Paragraph(cat_text, self.custom_styles['CustomBody']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Implementation status legend
        legend_text = """
        <b>Status Legend:</b><br/>
        ✅ Implemented and ready to use<br/>
        ⏳ Planned for future implementation
        """
        elements.append(Paragraph(legend_text, self.custom_styles['CustomBody']))
        elements.append(PageBreak())
    
    def create_techniques_section(self, category_name, techniques, elements):
        """Create a techniques section"""
        # Section title
        section_num = ['Passive', 'Active', 'Web-Based', 'Specialized'].index(category_name.split()[0]) + 2
        title = Paragraph(f"{section_num}. {category_name}", self.custom_styles['SectionHeader'])
        elements.append(title)
        
        # Create table data
        table_data = [['ID', 'Technique Name', 'Tools Used', 'Status', 'Description']]
        
        for tech_id, details in techniques.items():
            status_symbol = "Implemented" if details['status'] == '✅' else "Planned"
            table_data.append([
                tech_id,
                details['name'],
                details['tools'],
                status_symbol,
                details['desc']
            ])
        
        # Create table
        table = Table(table_data, colWidths=[0.6*inch, 2*inch, 2*inch, 0.6*inch, 2.3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#4472c4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        elements.append(PageBreak())
    
    def create_tools_section(self, elements):
        """Create popular tools section"""
        title = Paragraph("6. Popular Tools Reference", self.custom_styles['SectionHeader'])
        elements.append(title)
        
        for category, tools in self.popular_tools.items():
            cat_title = Paragraph(f"<b>{category}</b>", self.custom_styles['TechniqueName'])
            elements.append(cat_title)
            
            tools_text = "• " + "<br/>• ".join(tools)
            elements.append(Paragraph(tools_text, self.custom_styles['CustomBody']))
            elements.append(Spacer(1, 0.2*inch))
        
        elements.append(PageBreak())
    
    def create_commands_section(self, elements):
        """Create command examples section"""
        title = Paragraph("7. Quick Command Examples", self.custom_styles['SectionHeader'])
        elements.append(title)
        
        commands = [
            ("WHOIS Lookup", "whois example.com"),
            ("DNS Enumeration", "dig example.com ANY"),
            ("Subdomain Discovery", "nslookup -type=NS example.com"),
            ("Port Scan", "nmap -T4 -F example.com"),
            ("Web Headers", "curl -I https://example.com"),
            ("Directory Scan", "dirb https://example.com"),
            ("SSL Certificate", "openssl s_client -connect example.com:443"),
            ("Email Harvesting", "theharvester -d example.com -b google"),
        ]
        
        table_data = [['Technique', 'Command Example']]
        table_data.extend(commands)
        
        table = Table(table_data, colWidths=[2.5*inch, 4.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#4472c4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('FONTNAME', (1, 1), (1, -1), 'Courier'),
            ('FONTSIZE', (1, 1), (1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(PageBreak())
    
    def create_legal_section(self, elements):
        """Create legal considerations section"""
        title = Paragraph("8. Legal Considerations", self.custom_styles['SectionHeader'])
        elements.append(title)
        
        legal_text = """
        <b>Always Remember:</b><br/><br/>
        
        1. <b>Authorization Required:</b> Written permission is mandatory before conducting any security testing.<br/><br/>
        
        2. <b>Scope Limitations:</b> Stay within the authorized boundaries and scope of testing.<br/><br/>
        
        3. <b>Data Handling:</b> Ensure secure storage and proper disposal of collected data.<br/><br/>
        
        4. <b>Disclosure Process:</b> Follow responsible vulnerability disclosure practices.<br/><br/>
        
        5. <b>Legal Compliance:</b> Understand and comply with local and international laws.<br/><br/>
        
        6. <b>Professional Ethics:</b> Adhere to cybersecurity professional standards and codes of conduct.<br/><br/>
        
        <b>⚠️ Disclaimer:</b> The authors and publishers of this document are not responsible for any 
        misuse of the information provided. This content is intended solely for educational purposes 
        and authorized security testing activities.
        """
        
        elements.append(Paragraph(legal_text, self.custom_styles['CustomBody']))
        elements.append(PageBreak())
    
    def create_resources_section(self, elements):
        """Create learning resources section"""
        title = Paragraph("9. Learning Resources", self.custom_styles['SectionHeader'])
        elements.append(title)
        
        resources_text = """
        <b>Recommended Reading:</b><br/>
        • OWASP Testing Guide<br/>
        • NIST Cybersecurity Framework<br/>
        • SANS Penetration Testing Resources<br/>
        • Ethical Hacking Certifications (CEH, OSCP)<br/><br/>
        
        <b>Practice Environments:</b><br/>
        • Personal lab setups<br/>
        • VulnHub Virtual Machines<br/>
        • HackTheBox Platform<br/>
        • TryHackMe Challenges<br/>
        • PentesterLab Exercises<br/><br/>
        
        <b>Professional Certifications:</b><br/>
        • Certified Ethical Hacker (CEH)<br/>
        • Offensive Security Certified Professional (OSCP)<br/>
        • GIAC Penetration Tester (GPEN)<br/>
        • CompTIA PenTest+<br/><br/>
        
        <b>Online Communities:</b><br/>
        • Reddit: r/AskNetsec, r/HowToHack<br/>
        • Discord: Various ethical hacking servers<br/>
        • GitHub: Security tool repositories<br/>
        • Twitter: InfoSec community<br/>
        """
        
        elements.append(Paragraph(resources_text, self.custom_styles['CustomBody']))
    
    def generate_pdf(self, filename="information_gathering_reference.pdf"):
        """Generate the complete PDF document"""
        doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=72, leftMargin=72, 
                              topMargin=72, bottomMargin=18)
        
        elements = []
        
        # Build document sections
        self.create_cover_page(doc, elements)
        self.create_table_of_contents(elements)
        self.create_overview_section(elements)
        
        # Create sections for each technique category
        for category, techniques in self.techniques.items():
            self.create_techniques_section(category, techniques, elements)
        
        self.create_tools_section(elements)
        self.create_commands_section(elements)
        self.create_legal_section(elements)
        self.create_resources_section(elements)
        
        # Build PDF
        doc.build(elements)
        return filename

def main():
    parser = argparse.ArgumentParser(description="Generate Information Gathering Techniques PDF")
    parser.add_argument('-o', '--output', default="information_gathering_reference.pdf",
                       help="Output PDF filename")
    
    args = parser.parse_args()
    
    print("Generating comprehensive information gathering techniques PDF...")
    
    try:
        generator = PDFGenerator()
        filename = generator.generate_pdf(args.output)
        print(f"✅ PDF generated successfully: {filename}")
        print(f"📄 File size: {os.path.getsize(filename) / 1024:.1f} KB")
        
    except ImportError as e:
        print("❌ Missing required dependency: reportlab")
        print("Install with: pip install reportlab")
        
    except Exception as e:
        print(f"❌ Error generating PDF: {str(e)}")

if __name__ == "__main__":
    main()
