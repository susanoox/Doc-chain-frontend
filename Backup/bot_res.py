import requests

def hit_response_api(query, namespace):
    url = "https://25a0-2405-201-e049-31-9c96-5a9e-2547-8afc.ngrok-free.app/v2/response"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "query": query,
        "namespace": namespace
    }
    response = requests.post(url, json=data, headers=headers)

    # Print the response status code and content
    print("Response status code:", response.status_code)
    print("Response content:", response.json())

# Example usage
query = "why was the leave"
namespace = "example namespace"
hit_response_api(query, namespace)
