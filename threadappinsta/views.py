
import json
import youtube_dl

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import*
from .serializers import*
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

# Create your views here.
class ThreadappView(APIView):
    serializer_class=threatappurlSerializer 
    def get(self,request):
        # allurl = dailymotionurl.objects.all().values()

        return Response()


    def post(self,request):
        # print("Request Data is  :",request.data)
        
        serializer_obj=threatappurlSerializer(data=request.data)
       
        url = request.POST.get("url")
        mylist = []
        try:
            try:
      
                downloadables = []
                url1 = f'https://api.threadsphotodownloader.com/v2/media?url={url}'

                response = requests.post(url1)
                data = response.json()
                # Parse the JSON content
                image_urls = data["image_urls"]
                video_urls = data["video_urls"]
                image_url = ""
                
                    
                for url in video_urls:
                    # print(url["download_url"])
                    downloadables.append({'quality': "Video", 'url': url["download_url"]})
                if downloadables == []:
                    image_url = data["image_urls"][0]
                    for url in image_urls:
                        # print(url)
                        downloadables.append({'quality': "Image", 'url': url})
                platform = 'threads.net'
                status = True
                return Response({
                    "status": status,
                    "title": "",
                    "downloadables": downloadables,
                    "image_url": image_url,
                    "platform": platform
                })
            except:
                url = f"https://download-thread-video.dhr.wtf/api/getUrl?url={url}"

                response = requests.get(url)
                # response = requests.get(url, headers=headers)
                data = json.loads(response.content)
                url2 = data["url"]
                # print(url2)
                
                mylist.append({'quality': "video", 'url': url2})
                platform = 'threads.net'
                try:
                    title = response.get("title", None)
                except:
                    title = ''
                try:    
                    image_url = response.get("thumbnail", None)
                except:
                    image_url = ''    
            
            
                jsonreturn=  json.dumps(mylist)
                object = json.loads(jsonreturn)
            
            
                status = True
                return Response({"status": status,"title":title,"downloadables": object,"image_url":image_url ,"platform":platform })    
        except Exception as e:
                    error_message = [ValueError]
                    status = False
                    return Response({"status": status , "error_message": response.status_code })
       