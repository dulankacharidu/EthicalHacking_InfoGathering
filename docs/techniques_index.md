# Information Gathering Techniques & Tools Index

## 📋 **QUICK REFERENCE INDEX**

### **PASSIVE TECHNIQUES**
| Index | Technique | Tools Used | Implemented |
|-------|-----------|------------|-------------|
| P01 | WHOIS Lookup | whois, python-whois | ✅ |
| P02 | DNS Enumeration | dnspython, socket | ✅ |
| P03 | Subdomain Discovery | Custom wordlist, DNS resolution | ✅ |
| P04 | SSL Certificate Analysis | ssl, socket | ✅ |
| P05 | Google Dorking | requests, custom queries | ✅ |
| P06 | Email Harvesting | requests, regex | ✅ |
| P07 | Metadata Extraction | exifread, PyPDF2 | ⏳ |
| P08 | Social Media Intel | APIs, web scraping | ⏳ |
| P09 | Archive Analysis | Wayback Machine API | ⏳ |
| P10 | Code Repository Search | GitHub API | ⏳ |

### **ACTIVE TECHNIQUES**
| Index | Technique | Tools Used | Implemented |
|-------|-----------|------------|-------------|
| A01 | Port Scanning | python-nmap | ✅ |
| A02 | Service Detection | nmap, custom banners | ✅ |
| A03 | OS Fingerprinting | nmap NSE scripts | ✅ |
| A04 | Web Technology Detection | requests, headers analysis | ✅ |
| A05 | Directory Enumeration | requests, threading | ✅ |
| A06 | Parameter Discovery | custom fuzzing | ⏳ |
| A07 | Database Fingerprinting | Custom probes | ⏳ |
| A08 | API Discovery | requests, pattern matching | ⏳ |
| A09 | Network Mapping | traceroute, ping | ⏳ |
| A10 | Vulnerability Scanning | Custom checks | ⏳ |

### **WEB-BASED TECHNIQUES**
| Index | Technique | Tools Used | Implemented |
|-------|-----------|------------|-------------|
| W01 | Robots.txt Analysis | requests | ✅ |
| W02 | Sitemap Analysis | requests, XML parsing | ✅ |
| W03 | Source Code Analysis | BeautifulSoup, regex | ✅ |
| W04 | Cookie Analysis | requests.cookies | ✅ |
| W05 | Header Analysis | requests.headers | ✅ |
| W06 | Form Discovery | BeautifulSoup | ⏳ |
| W07 | JavaScript Analysis | regex, ast parsing | ⏳ |
| W08 | Error Page Analysis | Custom requests | ⏳ |
| W09 | CDN Detection | DNS, headers | ⏳ |
| W10 | CMS Detection | signatures, patterns | ✅ |

### **SPECIALIZED TECHNIQUES**
| Index | Technique | Tools Used | Implemented |
|-------|-----------|------------|-------------|
| S01 | Cloud Storage Discovery | boto3, custom enum | ⏳ |
| S02 | GraphQL Introspection | requests, GraphQL | ⏳ |
| S03 | API Documentation | requests, OpenAPI | ⏳ |
| S04 | Certificate Transparency | CT logs API | ⏳ |
| S05 | Shodan Integration | Shodan API | ⏳ |
| S06 | Threat Intelligence | Various APIs | ⏳ |
| S07 | Geolocation Analysis | IP geolocation APIs | ✅ |
| S08 | Network Range Discovery | whois, CIDR | ⏳ |
| S09 | Email Format Discovery | pattern analysis | ✅ |
| S10 | Technology Versioning | banner analysis | ✅ |

## 📊 **IMPLEMENTATION STATISTICS**
- **Total Techniques**: 40
- **Implemented**: 20 (50%)
- **In Progress**: 20 (50%)
- **Core Passive**: 6/10 (60%)
- **Core Active**: 5/10 (50%)
- **Web-Based**: 5/10 (50%)
- **Specialized**: 4/10 (40%)

## 🔧 **TOOL DEPENDENCIES**

### **Core Python Libraries**
```
requests>=2.25.1
dnspython>=2.1.0
python-whois>=0.7.3
python-nmap>=0.6.4
beautifulsoup4>=4.9.3
colorama>=0.4.4
```

### **Optional Libraries (Advanced Features)**
```
shodan>=1.25.0
exifread>=2.3.2
PyPDF2>=2.0.0
boto3>=1.17.0
selenium>=3.141.0
```

### **System Requirements**
- Python 3.7+
- Nmap (for port scanning)
- Internet connection
- Windows/Linux/macOS compatible

## 🎯 **USAGE PATTERNS**

### **Quick Scan (Passive Only)**
```
python tools/infogather_pro.py example.com -p
```

### **Full Comprehensive Scan**
```
python tools/infogather_pro.py example.com -f
```

### **Specific Technique**
```
python tools/infogather_pro.py example.com -t P01,A01,W01
```

## 📝 **OUTPUT FORMATS**

| Format | Extension | Description |
|--------|-----------|-------------|
| JSON | .json | Structured data format |
| HTML | .html | Web-based report |
| TXT | .txt | Plain text summary |
| CSV | .csv | Spreadsheet format |
| XML | .xml | Structured markup |

## 🔍 **TECHNIQUE DETAILS**

### **Passive Techniques (P01-P10)**
- **P01**: Domain registration information
- **P02**: DNS records and configuration  
- **P03**: Subdomain enumeration and discovery
- **P04**: SSL/TLS certificate information
- **P05**: Search engine intelligence gathering
- **P06**: Email address collection
- **P07**: File metadata extraction
- **P08**: Social media profiling
- **P09**: Historical content analysis
- **P10**: Source code repository searches

### **Active Techniques (A01-A10)**
- **A01**: Network port identification
- **A02**: Service version detection
- **A03**: Operating system identification
- **A04**: Web server and framework detection
- **A05**: Hidden directory and file discovery
- **A06**: Input parameter identification
- **A07**: Database service identification
- **A08**: API endpoint discovery
- **A09**: Network topology mapping
- **A10**: Basic vulnerability identification

### **Web-Based Techniques (W01-W10)**
- **W01**: Robots.txt file analysis
- **W02**: XML sitemap analysis
- **W03**: HTML source code examination
- **W04**: HTTP cookie analysis
- **W05**: HTTP response header analysis
- **W06**: HTML form discovery and analysis
- **W07**: JavaScript code analysis
- **W08**: Error message information gathering
- **W09**: Content delivery network detection
- **W10**: Content management system detection

### **Specialized Techniques (S01-S10)**
- **S01**: Cloud storage bucket enumeration
- **S02**: GraphQL schema introspection
- **S03**: API documentation discovery
- **S04**: Certificate transparency log analysis
- **S05**: Shodan database integration
- **S06**: Threat intelligence correlation
- **S07**: Geographic location analysis
- **S08**: Network range identification
- **S09**: Email format pattern discovery
- **S10**: Technology version analysis