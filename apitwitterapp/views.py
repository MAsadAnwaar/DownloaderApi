
import json
import youtube_dl
import requests
from bs4 import BeautifulSoup
from lxml import etree
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import*
from .serializers import*

import time
# Create your views here.
class TwitterView(APIView):
    serializer_class=twitterurlSerializer 
    def get(self,request):

        return Response()


    def post(self,request):
        # print("Request Data is  :",request.data)
        
        serializer_obj=twitterurlSerializer(data=request.data)
       
        url1 = request.POST.get("url")
        
        url = "https://twdown.net/download.php"
        post_data = {
            # Your POST data here
            "URL": url1
        }
        response = requests.post(url,  data=post_data)
        mylist = []
        try:
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                title = soup.find("p")
                title_text = title.text if title else "Title not found"  # Check if title exists
                # print(title_text)

                img_tag = soup.find(class_="img-thumbnail")
                thumbnail_src = ""
                if img_tag:
                    thumbnail_src = img_tag.get("src")
                    # print(thumbnail_src)

                containers = soup.find_all("div", class_="col-md-8 col-md-offset-2")
                unique_links = set()  # To store unique URLs

                for container in containers:
                    links = container.find_all("a", href=True)
                    for link in links:
                        href = link["href"]
                        if "mp3.php" in href:
                            continue  # Skip URLs containing "mp3.php"
                        
                        if href != "#" and href not in unique_links:
                            unique_links.add(href)
                            # print(href)
                            mylist.append({'quality': "video", 'url': href})

                platform = 'Twitter'
                image_url = thumbnail_src 

                status = True
                return Response({"status": status, "title": title_text, "downloadables": mylist, "image_url": image_url, "platform": platform })    
        except Exception as e:
            error_message = str(e)  # Convert exception to string
            status = False
            return Response({"status": status, "error_message": error_message })
