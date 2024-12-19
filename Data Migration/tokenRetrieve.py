# retrieving the two tokens needed from the api

import requests
import re

def get_id_token(api_key):
    post_login_url = f"REDACTED" \
                     f"redirect_uri=ridelife2://auth-callback"
    headers = {'x-api-key': api_key}
    data = {
        "username": "REDACTED",
        "password": "REDACTED"
    }
    response = requests.post(post_login_url, headers=headers, json=data, verify=True)

    if response.status_code == 200:
        json_response = response.json()
        location = json_response.get("location", "")
        print(location)
        code_match = re.search(r'code=([^&]+)', location)
        if code_match:
            code_value = code_match.group(1)
            print("Code:", code_value)
        else:
            print("Code not found in the location URL.")
            return None

        token_url = f"REDACTED"
        body = {
            "grant_type": "authorization_code",
            "client_id": "REDACTED",
            "code": code_value ,
            "redirect_uri": "REDACTED"
        }

        token_response = requests.post(token_url, data=body)
        print("token", token_response)

        if token_response.status_code == 200:
            json_response = token_response.json()
            id_token = json_response.get("id_token", "")
            return id_token
        else:
            print("Error:", token_response.json())
            return None
    else:
        print("Error:", response.text)
        return None