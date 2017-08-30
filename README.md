Step 1:
Edit creds.py template to use your azure username and password. This is how the Python SDK interacts and queries your azure resources.
This should only be stored locally on your machine. Use good judgement!

Usage:
bash$ python3 insights_metrics.py
  => reads Percentage CPU of a VMSS every minute starting now and in real time
bash$ python3 better_metrics.py
  => reads Percentage CPU of a VMSS over the past hour
bash$ python3 instance_numbers.py
  => counts number of active VMSS instances every 15 seconds and in real time for 20 minutes
