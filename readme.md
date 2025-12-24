
# domain2ip.py

## Overview
`domain2ip.py` is a Python tool that reads a list of domains from a file, resolves each domain to its IP address, retrieves WHOIS information for the IP, and displays the results in a formatted table. The script removes duplicate domains, sorts the output by IP address, and dynamically adjusts column widths for readability.

The WHOIS lookup prioritizes the organization name (`org-name`) when available, and falls back to `network.name` or `asn_description` if necessary.

## Requirements
- Python 3.x
- `ipwhois` library

Install dependencies:
```bash
pip install ipwhois
```

## Usage
```bash
python3 domain2ip.py <file>
```

### Example
Create a file `domains.txt`:
```
google.com
microsoft.com
google.com
```

Run the script:
```bash
python3 domain2ip.py domains.txt
```

### Output
```
Domain                          IP Address       Owner
---------------------------------------------------------------
google.com                      142.250.72.14   GOOGLE
microsoft.com                   20.84.181.62    MICROSOFT-CORP
```
