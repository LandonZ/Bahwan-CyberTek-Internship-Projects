# code segment for the main retrieval of the gps

import tokenRetrieve as t
import gpsRetrieve as g

token_api_key = "REDACTED"
id_token = t.get_id_token(token_api_key)
print(id_token)
print()
gps = g.get_gps(id_token)
print(gps)