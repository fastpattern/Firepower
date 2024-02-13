import requests
import csv
import json
from getpass import getpass

# Replace these variables with your actual Firepower Management Center API details
FMC_HOST =input ("FMC Address: ")
USERNAME =input ("Firepower Username: ")
PASSWORD = getpass("Password: ")
DOMAIN_UUID = "e276abec-e0f2-11e3-8169-6d9ed49b625f"  # You may need to adjust this depending on your FMC setup

def get_auth_token():
    """Authenticate with FMC and get a token."""
    url = f"{FMC_HOST}/api/fmc_platform/v1/auth/generatetoken"
    try:
        response = requests.post(url, auth=(USERNAME, PASSWORD), verify=False)
        response.raise_for_status()
        auth_headers = response.headers
        token = auth_headers.get('X-auth-access-token')
        if not token:
            raise ValueError("Failed to get authentication token")
        return token
    except Exception as e:
        print(f"Error getting auth token: {e}")
        exit()

def get_network_groups(token):
    """Fetch all network groups."""
    url = f"{FMC_HOST}/api/fmc_config/v1/domain/{DOMAIN_UUID}/object/networkgroups?expanded=true"
    headers = {
        'X-auth-access-token': token,
    }
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()['items']
    except Exception as e:
        print(f"Error fetching network groups: {e}")
        exit()

def save_to_csv(network_groups):
    """Save network groups and their IP addresses to a CSV file."""
    with open('network_groups_with_ips.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Group Name", "IP Addresses"])
        for group in network_groups:
            ip_addresses = [literal['value'] for literal in group.get('literals', [])]
            writer.writerow([group['name'], ', '.join(ip_addresses)])

def main():
    token = get_auth_token()
    network_groups = get_network_groups(token)
    save_to_csv(network_groups)
    print("Network group details have been saved to network_groups_with_ips.csv")

if __name__ == "__main__":
    main()
