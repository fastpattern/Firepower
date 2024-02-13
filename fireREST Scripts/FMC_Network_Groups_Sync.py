#script that synchronises network object groups from a source FMC to a destination FMC
#if a network group already exists, it will be updated. Otherwise, a new network group will be created.
#be warned that if a network group exist in both locations it will be overwritten with the contents from the source fmc
#all contents will be destroyed/overwritten without warning. suggest taking a backup on the FMC before running.

import csv
from fireREST import FMC
from getpass import getpass

# Configure your source FMC connection details
src_hostname =input ("Source FMC IP Address: ")
src_username =input ("Source FMC Username: ")
src_password =getpass("Source FMC Password: ")
#src_domain = 'your_source_domain_uuid' ##not needed if global

# Configure your destination FMC connection details
dst_hostname =input ("Dest FMC IP Address: ")
dst_username =input ("Dest FMC Username: ")
dst_password =getpass("Dest FMC Password: ")

# Initialize the FMC clients
src_fmc = FMC(hostname=src_hostname, username=src_username, password=src_password, domain='Global')
dst_fmc = FMC(hostname=dst_hostname, username=dst_username, password=dst_password, domain='Global')

def get_network_groups(fmc_client):
    """Fetch all network groups from FMC."""
    return fmc_client.object.networkgroup.get()

def find_network_group_by_name(fmc_client, group_name):
    """Find a network group by name on the FMC."""
    network_groups = fmc_client.object.networkgroup.get()
    for group in network_groups:
        if group['name'] == group_name:
            return group
    return None

def create_or_update_network_group(fmc_client, group_name, literals):
    """Create or update a network group based on existence."""
    existing_group = find_network_group_by_name(fmc_client, group_name)
    
    if existing_group:
        # Prepare the existing group with updated literals for an update
        existing_group['literals'] = literals
        try:
            fmc_client.object.networkgroup.update(data=existing_group)
            print(f"Network group '{group_name}' updated on the destination FMC.")
        except Exception as e:
            print(f"Error updating network group '{group_name}': {e}")
    else:
        # Create a new network group
        group_data = {
            'name': group_name,
            'type': 'NetworkGroup',
            'literals': literals
        }
        try:
            fmc_client.object.networkgroup.create(data=group_data)
            print(f"Network group '{group_name}' created on the destination FMC.")
        except Exception as e:
            print(f"Error creating network group '{group_name}': {e}")

def sync_network_groups(src_fmc_client, dst_fmc_client):
    """Synchronize network groups from source FMC to destination FMC."""
    src_network_groups = get_network_groups(src_fmc_client)
    for group in src_network_groups:
        group_name = group['name']
        literals = group.get('literals', [])
        create_or_update_network_group(dst_fmc_client, group_name, literals)

def main():
    print("Starting synchronization of network groups...")
    sync_network_groups(src_fmc, dst_fmc)
    print("Synchronization completed.")

if __name__ == '__main__':
    main()
