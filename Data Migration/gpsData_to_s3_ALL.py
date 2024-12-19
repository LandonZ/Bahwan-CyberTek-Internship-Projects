# the full, combined code in migrating GPS data into a S3 Bucket for the software to use.
# Note: some information, such as the URL links and tokens are redacted for confidentiality purposes.

import requests
import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import re
import os

bucket_name = "staging-ride-life-path-info"
access_key = "REDACTED"
secret_key = "REDACTED"
api_key = "REDACTED"

s3 = boto3.client(service_name="s3", 
            aws_access_key_id=access_key, 
            aws_secret_access_key=secret_key
    )

def get_id_token(api_key):
    post_login_url = f"REDACTED"\
                     f"REDACTED"
    headers = {'x-api-key': api_key}
    data = {
        "username": "REDACTED",
        "password": "REDACTED"
    }
    response = requests.post(post_login_url, headers=headers, json=data, verify=True)

    if response.status_code == 200:
        json_response = response.json()
        location = json_response.get("location", "")
        #print(location)
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

        token_response = requests.post(token_url, data=body, 
            headers={"Content-Type": "application/x-www-form-urlencoded"})
        #print("token", token_response)

        if token_response.status_code == 200:
            json_response = token_response.json()
            id_token = json_response.get("id_token", "")
            return id_token
        else:
            print("Error getting token:", token_response.json())
            return None
    else:
        print("Login Error:", response.text)
        return None
    
def get_gps(id_token, start_id, end_id):

    temp_url = "REDACTED:id={id}"
    headers = {'Authorization': f'Bearer {id_token}'}
    results = []

    temp_folder = "temp" #"/Users/landonzheng/Documents/Intern/temp"
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    
    for id in range(start_id, end_id + 1):
        url = temp_url.replace(':id={id}', f'{id}')
        response = requests.get(url, headers=headers, verify=False)

    #print(response.json())
        print(f"ID: {id}, HTTP Status Code: {response.status_code}")

        if response.status_code == 200:
            json_reponse = response.json()
            results.append(json_reponse)

            file_name = f"{id}-gps.json"
            file_path = os.path.join(temp_folder, file_name)
            with open(file_path, "w") as outfile:
                json.dump(json_reponse, outfile)
        
            upload_success = upload_to_s3(file_path, bucket_name)
            if upload_success:
                os.remove(file_path)
                print(f"Local File '{file_path}' removed after successful upload.")
            else:
                print(f"Local file '{file_path}' retained due to upload failure.")
        else:
            print(f"Failed to get data for ID: {id}, Status Code: {response.status_code}")
    return results

def upload_to_s3(file_path, bucket_name, object_name=None):

    if object_name is None:
        object_name = os.path.basename(file_path)
    
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"File '{file_path}' uploaded to '{bucket_name}/{object_name}'")
        return True
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
        return False
    except NoCredentialsError:
        print("Credentials not available.")
        return False
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

id_token = get_id_token(api_key)

if id_token:
    start_id = 1
    end_id = 10
    data = get_gps(id_token, start_id, end_id)
else:
    print("Failed to obtain id_token.")
