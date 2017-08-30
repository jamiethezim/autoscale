from azure.mgmt import compute
from azure.common.credentials import UserPassCredentials
import json
import datetime
from time import sleep
import creds

'''
Produced 2017 for autoscaling demo for Norton Site Reliability Engineering at Symantec

This script checks how many instances are in the provided scale set implementing the azure python SDK.
The script accesses user credentials and queries and displays the number of instances every 15 seconds
for a run-time of 20 minutes.

Usage:
bash$: python3 instance_numbers.py

Password protection is implemented using another file creds.py. The global variables are USERNAME and PASSWORD,
which are imported to this script and used to create the credential object.

'''

# Replace this with your subscription id
subscription_id = "39ac48fb-fea0-486a-ba84-e0ae9b06c663"
resource_group_name = "jzimmerman-demo"
vmss_name = "mini-vmss"

credentials = UserPassCredentials(
    creds.USERNAME,  # Your user
    creds.PASSWORD,      # Your password
)

client = compute.compute.ComputeManagementClient(credentials, subscription_id)

#print data
for i in range(80):
    print("check {} at time {} -----------------------------".format(i, datetime.datetime.now().strftime("%H:%M:%S")))
    succeeded = 0
    deleting = 0
    creating = 0
    for inst in client.virtual_machine_scale_set_vms.list(resource_group_name, vmss_name):
        if inst.provisioning_state == "Succeeded":
            succeeded += 1
        elif inst.provisioning_state == "Deleting":
            deleting += 1
        elif inst.provisioning_state == "Creating":
            creating += 1
    print("\tSucceeded {}\tDeleting {}\t Creating {}".format(succeeded, deleting, creating))
    sleep(15)