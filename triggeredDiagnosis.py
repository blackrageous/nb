import requests
import json

# NetBrain API endpoint for running the Triggered Diagnosis Path function
tdp_url = "http://<NetBrain_Server>/ServicesAPI/API/Operations/TriggeredDiagnosisPath"

# NetBrain API authentication credentials
username = "<username>"
password = "<password>"

# NetBrain API HTTP request headers
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# NetBrain API HTTP request payload
payload = {
    "domain": "<domain_name>",
    "pathID": "<path_id>",
    "triggerCondition": "<trigger_condition>",
    "parameterValues": {
        "<parameter_name_1>": "<parameter_value_1>",
        "<parameter_name_2>": "<parameter_value_2>",
        "<parameter_name_3>": "<parameter_value_3>",
        # Add more parameters as needed
    }
}

# Send HTTP POST request to authenticate and start session
response = requests.post(tdp_url + "/Login", headers=headers, auth=(username, password))

# Check HTTP status code of response
if response.status_code != 200:
    raise Exception("Failed to authenticate with NetBrain API")

# Extract session ID from response
session_id = response.json()["sessionID"]

# Update HTTP headers with session ID
headers["Session-Token"] = session_id

# Send HTTP POST request to run the Triggered Diagnosis Path function
response = requests.post(tdp_url + "/RunDiagnosisPath", headers=headers, data=json.dumps(payload))

# Check HTTP status code of response
if response.status_code != 200:
    raise Exception("Failed to run Triggered Diagnosis Path in NetBrain API")

# Extract job ID from response
job_id = response.json()["jobID"]

# Send HTTP GET request to check status of job
response = requests.get(tdp_url + "/GetJobStatus?jobID=" + job_id, headers=headers)

# Check HTTP status code of response
if response.status_code != 200:
    raise Exception("Failed to get job status from NetBrain API")

# Extract status of job from response
status = response.json()["status"]

# Wait for job to complete
while status == "Pending" or status == "Running":
    # Send HTTP GET request to check status of job
    response = requests.get(tdp_url + "/GetJobStatus?jobID=" + job_id, headers=headers)

    # Check HTTP status code of response
    if response.status_code != 200:
        raise Exception("Failed to get job status from NetBrain API")

    # Extract status of job from response
    status = response.json()["status"]

# Check if job completed successfully
if status == "Success":
    print("Triggered Diagnosis Path completed successfully")
else:
    raise Exception("Triggered Diagnosis Path failed with status: " + status)
