from azure.monitor import MonitorClient
from azure.common.credentials import UserPassCredentials
from time import sleep
import datetime
import creds


# Replace this with your subscription id
subscription_id = "39ac48fb-fea0-486a-ba84-e0ae9b06c663"

# See above for details on creating different types of AAD credentials
credentials = UserPassCredentials(
    creds.USERNAME,  # Your user
    creds.PASSWORD,      # Your password
)

client = MonitorClient(
    credentials,
    subscription_id
)

import datetime

# Get the ARM id of your resource. You might chose to do a "get"
# using the according management or to build the URL directly
# Example for a ARM VM

resource_group_name = "jzimmerman-demo"
vmss_name = "mini-vmss"
resource_id = (
    "subscriptions/{}/"
    "resourceGroups/{}/"
    "providers/Microsoft.Compute/virtualMachineScaleSets/{}"
).format(subscription_id, resource_group_name, vmss_name)

# You can get the available metrics of this specific resource
'''
for metric in client.metric_definitions.list(resource_id):
    # azure.monitor.models.MetricDefinition
    print("{}: id={}, unit={}".format(
        metric.name.localized_value,
        metric.name.value,
        metric.unit
    ))
'''

# Get CPU total of yesterday for this VM, by hour

now = datetime.datetime.now()
earlier = now - datetime.timedelta(minutes=1) #datetime objects
#Have to eliminate microseconds
now = now.strftime("%Y-%m-%dT%H:%M:%SZ") #string objects
earlier = earlier.strftime("%Y-%m-%dT%H:%M:%SZ")

print("Percentage CPU (percent)")
for i in range(80):
    #Set start and end times to be 1 minute in the past and now
    ender = datetime.datetime.now()
    starter = ender - datetime.timedelta(minutes=1)
    ender = ender.strftime("%Y-%m-%dT%H:%M:%SZ")
    starter = starter.strftime("%Y-%m-%dT%H:%M:%SZ")

    #Set up filter parms
    _filter = " and ".join([
    "name.value eq 'Percentage CPU'",
    "aggregationType eq 'Average'",
    "startTime eq {}".format(starter),
    "endTime eq {}".format(ender),
    "timeGrain eq duration'PT1M'"
    ])
    #Query for the data
    the_data = client.metrics.list(resource_id, filter=_filter)

    for item in the_data:
        for data in item.data:
            # azure.monitor.models.MetricData
            print("{}: {}".format(data.time_stamp, data.average))
    #Wait - the time stamps need to turn over
    sleep(60)