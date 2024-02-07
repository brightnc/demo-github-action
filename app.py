from base64 import b64encode
from nacl import encoding, public
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def encrypt(public_key: str, secret_value: str) -> str:
  """Encrypt a Unicode string using the public key."""
  public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
  sealed_box = public.SealedBox(public_key)
  encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
  return b64encode(encrypted).decode("utf-8")

def main():
    username = os.getenv('GITHUB_USERNAME')
    repository = os.getenv('GITHUB_REPOSITORY')
    api_key = os.getenv('GITHUB_API_KEY')
    secret_name = os.getenv('GITHUB_SECRET_NAME')
    secret_value = os.getenv('GITHUB_SECRET_VALUE')

    headers = {
        "Authorization": f"token {api_key}",
        "Accept": "application/vnd.github.v3+json"
    }


    # Get the public key to obtain the key_id and key use for encrypt value
    public_key_url = f"https://api.github.com/repos/{username}/{repository}/actions/secrets/public-key"

    public_key_response = requests.get(public_key_url, headers=headers)

    public_key_data = public_key_response.json()

    print(public_key_data )

    key_id = public_key_data["key_id"]
    key_value = public_key_data["key"]

    encryptedValue = encrypt(key_value, secret_value)

    # Create payload with the secret value and key_id
    payload = {
        "encrypted_value": encryptedValue,
        "key_id": key_id
    }


    # Convert payload to JSON
    payload_json = json.dumps(payload)

    # Generate the URL for creating a repository secret
    url = f"https://api.github.com/repos/{username}/{repository}/actions/secrets/{secret_name}"

    # Send the request to create the secret
    response = requests.put(url, headers=headers, data=payload_json)

    if response.status_code == 201:
        print(f"Secret '{secret_name}' created successfully.")
    elif response.status_code == 204:
        print(f"Secret '{secret_name}' updated successfully.")
    else:
        print(f"Failed to create secret. Status code: {response.status_code}, Response: {response.text}")


main()