#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
------------------------------------------------------------------------------
    Domain Explorer - 04.03.18.02.10.00 - Zahir Lehri
------------------------------------------------------------------------------
"""

## # LIBRARIES # ## 
import re
import requests
import socket
import csv
import datetime
from colorama import init, Fore

## # CONTEXT VARIABLES # ## 
version = 1.2

# Initialize colorama
init(autoreset=True)

## # MAIN FUNCTIONS # ## 

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=str, help="Output file.")
    return parser.parse_args()

def banner():
    global version
    b = f'''
          _    ___ _  _ _  __   ___ _  _ ___ ___ ___ ___ ___ 
         | |  |_ _| \| | |/ /__/ __| \| |_ _| __| __| __| _ \\
         | |__ | || .` | ' <___\__ \ .` || || _|| _|| _||   / 
         |____|___|_|\_|_|\_\  |___/_|\_|___|_| |_| |___|_|_\\
    
     Version {version} | GitHub: https://github.com/xahirlehri
     Created by Zahir Lehri
    '''
    print(b)

def clear_url(target):
    return re.sub('.*www\.', '', target, 1).split('/')[0].strip()

def save_subdomains(subdomain, output_file):
    with open(output_file, "a") as f:
        f.write(subdomain + '\n')

def separate_main_domains_subdomains(subdomains):
    main_domains = []
    subdomains_list = []
    for subdomain in subdomains:
        if subdomain.startswith("*.") or subdomain.count('.') == 1:
            main_domains.append(subdomain)
        else:
            subdomains_list.append(subdomain)
    return main_domains, subdomains_list

def get_ip_details(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.error:
        return "N/A"

def export_to_csv(results, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Domain', 'IP'])  # Write the header
        writer.writerows(results)  # Write all results

def main():
    banner()
    args = parse_args()

    target = input("Enter the target domain: ")  # Prompt for the domain name
    target = clear_url(target)  # Clean the target domain
    output = args.output

    # Generate CSV file name with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_output = f"{target}_{timestamp}.csv" if output is None else output  # Use provided output filename

    req = requests.get(f"https://crt.sh/?q=%.{target}&output=json")

    if req.status_code != 200:
        print("[X] Information not available!") 
        exit(1)

    subdomains = [value['name_value'] for value in req.json()]  # Extract subdomains

    print(f"\n[!] ---- TARGET: {target} ---- [!] \n")

    subdomains = sorted(set(subdomains))
    main_domains, subdomains_list = separate_main_domains_subdomains(subdomains)

    results = []

    if main_domains:
        print("\n[!] ---- MAIN DOMAINS ---- [!] \n")
        for main_domain in main_domains:
            ip = get_ip_details(main_domain)
            results.append((main_domain, ip))
            print(f"{main_domain} (IP: {ip})")

    if subdomains_list:
        print("\n[!] ---- SUBDOMAINS ---- [!] \n")
        for subdomain in subdomains_list:
            ip = get_ip_details(subdomain)
            results.append((subdomain, ip))
            print(f"{subdomain} (IP: {ip})")

    # Export to CSV if results were collected
    if results:
        print(f"\n[!]  Exporting results to CSV: {csv_output}")
        export_to_csv(results, csv_output)
    else:
        print("[X] No results to save!")

    print("\n\n[!]  Done!).")

if __name__ == "__main__":
    main()
