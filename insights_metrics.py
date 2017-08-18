from azure.monitor import MonitorClient
from azure.common.credentials import UserPassCredentials
import sys

# Replace this with your subscription id
subscription_id = "39ac48fb-fea0-486a-ba84-e0ae9b06c663"

# See above for details on creating different types of AAD credentials
credentials = UserPassCredentials(
    sys.argv[1],  # Your user
    sys.argv[2],      # Your password
)

client = MonitorClient(
    credentials,
    subscription_id
)

import datetime

# Get the ARM id of your resource. You might chose to do a "get"
# using the according management or to build the URL directly
# Example for a ARM VM

resource_group_name = "jzimmerman-con-rg"
vmss_name = "jzimmerman-test-ss"
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
earlier = now - datetime.timedelta(hours=1) #datetime objects
#Have to eliminate microseconds
now = now.strftime("%Y-%m-%dT%H:%M:%SZ") #string objects
earlier = earlier.strftime("%Y-%m-%dT%H:%M:%SZ")


filter = " and ".join([
    "name.value eq 'Percentage CPU'",
    "aggregationType eq 'Average'",
    "startTime eq {}".format(earlier),
    "endTime eq {}".format(now),
    "timeGrain eq duration'PT1M'"
])

metrics_data = client.metrics.list(
    resource_id,
    filter=filter
)

for item in metrics_data:
    # azure.monitor.models.Metric
    print("{} ({})".format(item.name.localized_value, item.unit.name))
    for data in item.data:
        # azure.monitor.models.MetricData
        print("{}: {}".format(data.time_stamp, data.average))
        #print("{}: {} MB".format(data.time_stamp, data.average/1000000 if isinstance(data.average, float) else data.average))

# Example of result:
# Percentage CPU (percent)
# 2016-11-16 00:00:00+00:00: 72.0
# 2016-11-16 01:00:00+00:00: 90.59
# 2016-11-16 02:00:00+00:00: 60.58
# 2016-11-16 03:00:00+00:00: 65.78
# 2016-11-16 04:00:00+00:00: 43.96
# 2016-11-16 05:00:00+00:00: 43.96
# 2016-11-16 06:00:00+00:00: 114.9
# 2016-11-16 07:00:00+00:00: 45.4
# 2016-11-16 08:00:00+00:00: 57.59
# 2016-11-16 09:00:00+00:00: 67.85
# 2016-11-16 10:00:00+00:00: 76.36
# 2016-11-16 11:00:00+00:00: 87.41
# 2016-11-16 12:00:00+00:00: 67.53
# 2016-11-16 13:00:00+00:00: 64.78
# 2016-11-16 14:00:00+00:00: 66.55
# 2016-11-16 15:00:00+00:00: 69.82
# 2016-11-16 16:00:00+00:00: 96.02
# 2016-11-16 17:00:00+00:00: 272.52
# 2016-11-16 18:00:00+00:00: 96.41
# 2016-11-16 19:00:00+00:00: 83.92
# 2016-11-16 20:00:00+00:00: 95.57
# 2016-11-16 21:00:00+00:00: 146.73
# 2016-11-16 22:00:00+00:00: 73.86
# 2016-11-16 23:00:00+00:00: 84.7