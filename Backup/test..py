import requests

# Define the base URL of your FastAPI server
base_url = "http://127.0.0.1:8000"

# Define the endpoint URL
endpoint_url = f"{base_url}/v2/summary"

# Define the request payload
payload = {
    "file_content": "Based on this error message, it seems like there might be an issue with the connection to the specified URL.",
    "language": "string",
    "num_lines": 5
}

# Define headers
headers = {
    "Content-Type": "application/json",
    "accept": "application/json"
}

# Send POST request
try:
    response = requests.post(endpoint_url, json=payload, headers=headers)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        print("Request successful!")
        print("Response:")
        print(response.json())  # Print response JSON
    else:
        print(f"Request failed with status code {response.status_code}:")
        print(response.text)  # Print response content for debugging
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
