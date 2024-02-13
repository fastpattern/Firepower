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

def get_network_objects(fmc_client):
    """Fetch all network objects from FMC."""
    return fmc_client.object.network.get()

def find_network_object_by_name(fmc_client, object_name):
    """Find a network object by name on the FMC."""
    network_objects = fmc_client.object.network.get()
    for obj in network_objects:
        if obj['name'] == object_name:
            return obj
    return None

def create_or_update_network_object(fmc_client, object_name, object_value):
    """Create or update a network object based on existence."""
    existing_object = find_network_object_by_name(fmc_client, object_name)
    
    if existing_object:
        # Prepare the existing object with updated value for an update
        existing_object['value'] = object_value
        try:
            fmc_client.object.network.update(data=existing_object)
            print(f"Network object '{object_name}' updated on the destination FMC.")
        except Exception as e:
            print(f"Error updating network object '{object_name}': {e}")
    else:
        # Create a new network object
        object_data = {
            'name': object_name,
            'type': 'Network',  # Adjust this as necessary for your object types (e.g., Host, Network, Range)
            'value': object_value
        }
        try:
            fmc_client.object.network.create(data=object_data)
            print(f"Network object '{object_name}' created on the destination FMC.")
        except Exception as e:
            print(f"Error creating network object '{object_name}': {e}")

def sync_network_objects(src_fmc_client, dst_fmc_client):
    """Synchronize network objects from source FMC to destination FMC."""
    src_network_objects = get_network_objects(src_fmc_client)
    for obj in src_network_objects:
        object_name = obj['name']
        object_value = obj.get('value', '')
        create_or_update_network_object(dst_fmc_client, object_name, object_value)

def main():
    print("Starting synchronization of network objects...")
    sync_network_objects(src_fmc, dst_fmc)
    print("Synchronization completed.")

if __name__ == '__main__':
    main()
