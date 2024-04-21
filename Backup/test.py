import requests

# Define the base URL of your FastAPI server
base_url = "http://127.0.0.1:8000"
# http://13.211.152.131:8080
# Define the endpoint URL
endpoint_url = f"{base_url}/v2/summary"

# Define the request payload
payload = {'file_content': "The Principal\nDelhi Public School\nNoida, UP - 201XXX\n\n25th March, 20XX\nSubject: Leave on [Leave Date] for Doctor's Appointment\n\nDear Sir/Madam,\n\nThis is to inform you that |, Ananth Nath Sharma, a Student of\nStandard 10 of your esteemed institution, would have to visit the\nphysician urgently with the consent of my parents. | have been\ngetting a fever on and off for the past two days. Hence, will not\nbe possible to attend school on [Leave Date].\n\n[Elaborate the reason with important pointers highlighting the\nimportance of the event.]\n\nKindly look into the matter. | will be gladly obliged to your kind\nconsent to allow me a leave for one day.\n\nThanking you,\n\nYours Sincerely,\nAnanth Nath Sharma\nStandard 10\n\nRoll no. 011\n\x0c", 'language': 'eng', 'num_lines': 10}
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
