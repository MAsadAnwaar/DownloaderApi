
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
class LinkedinVideoappView(APIView):
    serializer_class=LinkedinvideoSerializer 
    def get(self,request):
        # allurl = dailymotionurl.objects.all().values()

        return Response()


    def post(self,request):
        # print("Request Data is  :",request.data)
        
        serializer_obj=LinkedinvideoSerializer(data=request.data)
       
        url = request.POST.get("url")
        mylist = []
        try:
      
            downloadables = []
            url1 = f'https://postdrips.com/scraper?url={url}'
            response = requests.get(url1)

            # Parse the JSON content
            if response.status_code == 200:
    # Parse the response content as JSON
                    data = json.loads(response.content)
                    
                    # Extract the URL from the "contentUrl" key
                    content_url = data.get("contentUrl")
                    
                    if content_url:            
                        thumbnail = content_url
                        downloadables.append({'quality': "", 'url': content_url})
            platform = 'LinkedIn'
            status = True
            return Response({
                "status": status,
                "title": "",
                "downloadables": downloadables,
                "image_url": thumbnail,
                "platform": platform
            })
        except Exception as e:
                    error_message = [ValueError]
                    status = False
                    return Response({"status": status , "error_message": e.args })
       