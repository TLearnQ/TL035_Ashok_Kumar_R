import requests
import json

api_url = "https://httpbin.org/put"
TOKEN = "mytoken"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "status": "active"
}

# Send PUT request
response = requests.put(api_url, headers=headers, json=payload)

if response.status_code == 200:
    response_json = response.json()
    
    if response_json.get("json") == payload:
        print(True)
    else:
        print(False)
else:
    print(False)
