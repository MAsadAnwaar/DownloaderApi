import subprocess
import json
url = "https://www.tiktok.com/@abdullahhhhh010/video/7187736298701081883?is_from_webapp=1&sender_device=pc"
tiktokurl = url.split("?")[0]
cmd = f'python -m tiktok_downloader --url {tiktokurl} --snaptik --json'

result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
response_json = json.loads(result.stdout)

# Check if the response is a list of objects
if isinstance(response_json, list):
    # If the response is a list, assume the first object contains the URL
    url = response_json[0]['url']
else:
    # If the response is a single object, access the URL directly
    url = response_json['url']

print(url)
