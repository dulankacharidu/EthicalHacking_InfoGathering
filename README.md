# Ethical Hacking - Information Gathering Course

## Course Overview

This course covers ethical hacking information-gathering techniques used in cybersecurity, penetration testing, and bug bounty learning.

## Important Disclaimer

This course is for educational purposes and authorized testing only.

- Only use these techniques on systems you own or have explicit written permission to test.
- Practice in controlled lab environments whenever possible.
- Keep scans within the written scope of an authorized engagement.
- Never use these techniques against systems without permission.

## Project Structure

```text
EthicalHacking_InfoGathering/
├── docs/                  # Additional documentation
├── tools/                 # Python tools and report generator
├── README.md              # Project overview
├── requirements.txt       # Python dependencies
└── view_techniques.bat    # Windows helper launcher
```

## Tools

- `tools/infogather_pro.py` - Main information-gathering scanner.
- `tools/info_viewer.py` - Terminal reference viewer for techniques.
- `tools/pdf_generator.py` - PDF reference generator.

## Getting Started

1. Install Python 3.7 or newer.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. View available techniques:

   ```bash
   python tools/info_viewer.py
   ```

4. Run an authorized passive scan:

   ```bash
   python tools/infogather_pro.py example.com --passive --yes
   ```

5. Generate the PDF reference:

   ```bash
   python tools/pdf_generator.py
   ```

## Notes

- The scanner prompts for authorization by default. Use `--yes` only when you already have permission to test the target.
- `python-nmap` requires Nmap to be installed on the system for port scanning.
- Generated scan JSON files and the default PDF report are ignored by git.

## Learning Path

1. Introduction to information gathering.
2. Passive reconnaissance techniques.
3. Active reconnaissance techniques.
4. Network-based information gathering.
5. Web-based information gathering.
6. Combining techniques for useful reporting.
7. Legal and ethical considerations.
