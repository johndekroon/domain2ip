
#!/usr/bin/env python3
"""
domain2ip.py
Domain to IP Resolver
Reads domains from a text file, resolves them to IP addresses, and sorts by IP.


Usage:
    python3 domain2ip.py <file>

Example:
    python3 domain2ip.py domains.txt

"""

import sys
import socket
import os
from ipwhois import IPWhois
from pprint import pprint

def read_domains(file_path):
    """
    Read domains from a text file, one per line, and remove duplicates.
    """
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, 'r') as f:
        domains = [line.strip() for line in f if line.strip()]
    
    return list(dict.fromkeys(domains))  # Remove duplicates

def resolve_domain(domain):
    """
    Resolve a domain to its IP address.
    """
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None



def get_ip_owner(ip):
    """
    Perform WHOIS lookup to get the organization name for the IP.
    Prefer org-name from RDAP objects, fallback to network.name or ASN description.
    """
    try:
        obj = IPWhois(ip)
        data = obj.lookup_rdap()

        # 1. Zoek naar een object met kind == "org"
        for obj_id, obj_data in data.get('objects', {}).items():
            contact = obj_data.get('contact', {})
            if contact.get('kind') == 'org' and contact.get('name'):
                return contact['name']

        # 2. Fallback naar network.name
        if data.get('network', {}).get('name'):
            return data['network']['name']

        # 3. Fallback naar ASN description
        if data.get('asn_description'):
            return data['asn_description']

        return "Unknown"
    except Exception:
        return "Unknown"



def main():
    if len(sys.argv) != 2:
        print("Usage: python3 resolve_domains.py <file>")
        sys.exit(1)

    input_file = sys.argv[1]
    domains = read_domains(input_file)

    if not domains:
        print("No domains found in the file.")
        sys.exit(1)

    results = []
    for domain in domains:
        ip = resolve_domain(domain)
        if ip:
            owner = get_ip_owner(ip)
            results.append((domain, ip, owner))

    # Sort by IP address
    results.sort(key=lambda x: tuple(map(int, x[1].split('.'))))

    # Determine dynamic width for domain column
    max_domain_length = max(len(domain) for domain, _, _ in results)
    domain_width = max(max_domain_length, 10)  # Minimum width of 10

    # Print results
    print(f"{'Domain':<{domain_width}} {'IP Address':<15} {'Owner'}")
    print("-" * (domain_width + 15 + 20))
    for domain, ip, owner in results:
        print(f"{domain:<{domain_width}} {ip:<15} {owner}")

if __name__ == "__main__":
    main()
