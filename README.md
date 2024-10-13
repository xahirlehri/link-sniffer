# Domain Explorer

Domain Explorer is a command-line tool designed for cybersecurity professionals, researchers, and developers to gather detailed information about a target domain. The script automates the discovery of subdomains and resolves their IP addresses, helping users gain insights into the structure of websites.

## Features

- **Subdomain Discovery:** Automatically retrieves a comprehensive list of subdomains linked to the target domain using Certificate Transparency logs.
- **IP Address Resolution:** Resolves the corresponding IP addresses for discovered domains and subdomains.
- **Timestamped CSV Export:** Generates a CSV file named after the target domain with a timestamp to ensure unique filenames.
- **User-Friendly Interface:** Prompts users for the target domain and displays results clearly.

## Requirements

- Python 3.x
- `requests` library
- `colorama` library

You can install the required libraries using pip:

```bash
pip install requests colorama

git clone https://github.com/yourusername/domain-explorer.git
