from django.test import TestCase
import json
# Create your tests here.
import requests

url = "https://www.ahmadhusnainfabrics.com/instaapis/"

# Create a dictionary with the data to be sent in the request body
data = {
    "url": "https://www.instagram.com/reel/Cm35eWjKcQ8/?utm_source=ig_web_copy_link"
}

# Send the POST request
response = requests.post(url, data=data)

# Check the response status code
if response.status_code == 200:
    data = json.loads(response.text)
    # print(data)
    captions = data['title']
    thumbnails = data['image_url']
    downloadables = data['downloadables']
    print(captions)
    print(thumbnails)
    print(downloadables)

else:
    print("Error:", response.status_code)
