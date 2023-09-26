
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
class SnackVideoappView(APIView):
    serializer_class=SnackvideoSerializer 
    def get(self,request):
        # allurl = dailymotionurl.objects.all().values()

        return Response()


    def post(self,request):
        # print("Request Data is  :",request.data)
        
        serializer_obj=SnackvideoSerializer(data=request.data)
       
        url = request.POST.get("url")
        mylist = []
        try:
      
            downloadables = []
            url1 = "https://getsnackvideo.com/results"
            payload = {
                "id": url,
            }
            response = requests.post(url1, data=payload)
            content = response.content

            # Parse the JSON content
            soup = BeautifulSoup(content, "html.parser")
            img_tags = soup.find_all(class_="img_thumb")
            src_list = [img.find('img')['src'] for img in img_tags]
            for src in src_list:
                thumbnail = src
                # print(src)

            a_tags = soup.find_all("a", class_="btn btn-primary download_link without_watermark")

            print("Href values:")
            for tag in a_tags:
                href = tag.get("href")
                if href:
                    # print(href)
                    # print(url)
                    downloadables.append({'quality': "Without watermark", 'url': href})
            platform = 'SnackVideo'
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
       