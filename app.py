import requests
import json
import base64
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

# Replace these variables with your own values
username = "brightnc"
repository = "demo-github-action"
api_key = API_KEY
secret_name = "TEST_KEY"
secret_value = "ddd-secret-value"

# Set up headers with authentication token
headers = {
    "Authorization": f"token {api_key}",
    "Accept": "application/vnd.github.v3+json"
}


# Get the public key to obtain the key_id
public_key_url = f"https://api.github.com/repos/{username}/{repository}/actions/secrets/public-key"
public_key_response = requests.get(public_key_url, headers=headers)
public_key_data = public_key_response.json()
key_id = public_key_data["key_id"]

# Create payload with the secret value and key_id
payload = {
    "encrypted_value": base64.b64encode(secret_value.encode()).decode(),
    "key_id": key_id
}


# Convert payload to JSON
payload_json = json.dumps(payload)

# Generate the URL for creating a repository secret
url = f"https://api.github.com/repos/{username}/{repository}/actions/secrets/{secret_name}"

# Send the request to create the secret
response = requests.put(url, headers=headers, data=payload_json)

# Check the response status
if response.status_code == 201:
    print(f"Secret '{secret_name}' created successfully.")
else:
    print(f"Failed to create secret. Status code: {response.status_code}, Response: {response.text}")
