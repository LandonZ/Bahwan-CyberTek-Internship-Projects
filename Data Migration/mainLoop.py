# the main loop of the script

import tokenRetrieve
import gpsRetrieve
import s3Upload
import json

#loop starts at 1, ends at ?
current_index = 1
end_index = 5
template_path = "/Users/landonzheng/Documents/Intern/id-gps"
while current_index <= end_index:
    id_token_api_key = "REDACTED"
    id_token = tokenRetrieve.get_id_token(id_token_api_key)
    print(id_token)
    print()

    gps = gpsRetrieve.get_gps(id_token)
    print(gps)
    gps_json = json.dumps(gps)

    file_path = template_path + str(current_index) + ".json"
    with open(file_path, "w") as outfile:
        outfile.write(gps_json)
    
    current_index = current_index + 1
    #s3Upload.upload_file(file_path)

