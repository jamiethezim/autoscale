from azure.mgmt import compute
from azure.common.credentials import UserPassCredentials
import json
import sys
import datetime
from time import sleep

# Replace this with your subscription id
subscription_id = "39ac48fb-fea0-486a-ba84-e0ae9b06c663"
resource_group_name = "jzimmerman-con-rg"
vmss_name = "jzimmerman-test-ss"

credentials = UserPassCredentials(
    sys.argv[1],  # Your user
    sys.argv[2],      # Your password
)

client = compute.compute.ComputeManagementClient(credentials, subscription_id)

#the_instances = client.virtual_machine_scale_set_vms.list(resource_group_name, vmss_name)
#print("the type of the_instances is {}, dir is {}, nexting {}".format(type(the_instances), dir(the_instances), the_instances.next()))

def get_active():
    '''
    returns -> tuple of lists. first list is active vms instances, second list is deleting
    '''
    succeeded = []
    deleting = []
    creating = []
    the_instances = client.virtual_machine_scale_set_vms.list(resource_group_name, vmss_name)
    for inst in the_instances:
        if inst.provisioning_state == "Succeeded":
            succeeded.append(inst)
        elif inst.provisioning_state == "Deleting":
            deleting.append(inst)
        elif inst.provisioning_state == "Creating":
            creating.append(inst)
    return succeeded, deleting, creating


#print data
for i in range(40):
    print("check {}--------------------------------------------------------------------".format(i))

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
        print("\tSucceeded {}\tCreating {}\t Deleting {}".format(succeeded, deleting, creating))
    #data = get_active()
    #print(data)
    #print("{} Active: {} Dead: {} Creating: {}".format(datetime.datetime.now(), len(data[0]), len(data[1]), len(data[2])))
    sleep(30)