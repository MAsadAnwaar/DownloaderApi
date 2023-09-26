
import json
import youtube_dl

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import*
from .serializers import*

import time
# Create your views here.
class DailymotionView(APIView):
    serializer_class=dailymotionurlSerializer 
    def get(self,request):
        # allurl = dailymotionurl.objects.all().values()

        return Response()


    def post(self,request):
        # print("Request Data is  :",request.data)
        
        serializer_obj=dailymotionurlSerializer(data=request.data)
       
        url = request.POST.get("url")
        mylist = []
        try:
      

            # with youtube_dl.YoutubeDL() as ydl:
            #     info_dict = ydl.extract_info(url, download=False)
            #     video_url = info_dict.get("url", None)
            #     # for item in info_dict:
            #         # if not item['url'].endswith('fmp4'):
            #     mylist.append({'quality': info_dict['format'], 'url': info_dict['url']})
            with youtube_dl.YoutubeDL() as ydl:
                info_dict = ydl.extract_info(url, download=False)
                video_url = info_dict.get("url", None)
                for item in info_dict['formats']:
                    if  item['url'].endswith('.mp4'):
                        mylist.append({'quality': item['format_id'], 'url': item['url']})
            platform = 'dailymotion'
            try:
                title = info_dict.get("title", None)
            except:
                title = ''
            try:    
                image_url = info_dict.get("thumbnail", None)
            except:
                image_url = ''    
           
         
            jsonreturn=  json.dumps(mylist)
            object = json.loads(jsonreturn)
           
           
            status = True
            return Response({"status": status,"title":title,"downloadables": object,"image_url":image_url ,"platform":platform })    
        except Exception as e:
            # print("Error Message is Here:",ValueError)
            error_message = [ValueError]
            status = False
            return Response({"status": status , "error_message": e.args })
       