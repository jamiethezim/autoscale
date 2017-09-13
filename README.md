Step 1: Edit creds.py template to use your azure username and password. This is how the Python SDK interacts and queries your azure resources.
This file only be stored locally on your machine. Use good judgement!

Usage:

bash$ python3 insights_metrics.py

  => reads Percentage CPU of a VMSS every minute starting now and in real time ****BROKEN**** 
  	 this script doesn't work, at least not yet!
  
bash$ python3 better_metrics.py

  => reads Percentage CPU of a VMSS over the past hour
  
bash$ python3 instance_numbers.py

  => counts number of active VMSS instances every 15 seconds and in real time for 20 minutes

---------------------------------

201-vmss-bottle-autoscale ->

	contains the ARM templates, application, and installation script to deploy the stack

jmeter-tests ->

	contains jmeter .jmx test plans, which I used in a load-testing task in VSTS