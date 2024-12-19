# retrieving the gps data code segment

import requests

def get_gps(id_token):
    post_login_url = "REDACTED:id=27"
    headers = {'Authorization': f'Bearer {id_token}'}
    response = requests.get(post_login_url, headers=headers, verify=True)

    print(response.json())

    if response.status_code == 200:
        json_reponse = response.json()
        single_gps = json_reponse.get("single_gps", "")
        print(single_gps)
        return json_reponse
    else:
        print("Error:", response.json())
        return None