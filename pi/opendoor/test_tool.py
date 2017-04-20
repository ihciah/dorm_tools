import requests
import json

mac = "00:00:00:00:00:00"

url = "http://192.168.1.111:5000/wifi"
post_data = json.dumps([{"MAC": mac, "DBM": -90}])

print requests.post(url, {"users": post_data}).content
