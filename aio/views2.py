
import json

# Create your views here.
from io import BytesIO
import httpx
import asyncio
from rest_framework.views import APIView
from rest_framework.response import Response
from snapsave import Fb, DownloadCallback


from rest_framework.views import APIView
from rest_framework.response import Response
from .models import*
from .serializers import*

import os
import time

# Create your views here.


async def download_facebook_video(url):
    vid = await Fb().from_url(url)
    try:
        thumbnail = vid.cover
        # print("Thumbnail",thumbnail)
    except:
        thumbnail=[]
    downloadables = []
    for i, quality in reversed(list(enumerate(vid))):
        # print(vid)

        quality_label = str(quality)

        # print(f"Trying quality {i}: {quality}")
        # print((quality.url_v).split("=1")[0])
        downloadables.append({'quality': quality_label.split("::")[2],'url':(quality.url_v)})
        try:
            quality.url_v()
            # downloadables.append(quality.url_v)
            # content = dd.io.getvalue()
            break
        except:
            continue
    return {'thumbnail': thumbnail, 'downloadables': downloadables}
class Aio_Video_DownloaderView(APIView):
    serializer_class=facebookurlSerializer 
    def get(self,request):
        # allurl = instaurl.objects.all().values()

        return Response()


    def post(self,request):
        # print("Request Data is  :",request.data)
        
        serializer_obj=facebookurlSerializer(data=request.data)
       
        url = request.POST.get("url")
        
        try:
      

                
                downloadables=[]
                
                import requests
                import json

                # url = input("Enter the URL: ")
                link = f"https://ssyoutube-api.sansekai.repl.co/api/youtube?url={url}"
                response = requests.get(link)

                if response.status_code == 200:
                    content = response.content
                    data = json.loads(content)

                    result = data['result']
                    url_list = result['url']
                    thumb = result['thumb']
                    title = result['meta']['title']
                    hosting = result['hosting']

                
                    for item in url_list:
                        
                        if 'subname' in item:
                            subname = item['subname']
                            # downloadables.append(subname)
                        else:
                            subname = 'N/A'
                            #    downloadables.append(subname)
                        url = item['url']
                        # downloadables.append(url)    
                        downloadables.append({'quality': subname,'url':url})
                        
                platform = hosting.split(".")[0]
                
                
                image_url =thumb   
            
            
                
            
            
                status = True
                return Response({"status": status,"title":title,"downloadables": downloadables,"image_url":image_url ,"platform":platform })    
        # except Exception as e:
        #     # print("Error Message is Here:",ValueError)
        #     error_message = [ValueError]
        #     status = False
        #     return Response({"status": status , "error_message": e.args })
        except:
            serializer_obj = facebookurlSerializer(data=request.data)
            if serializer_obj.is_valid():
                url = serializer_obj.validated_data['url']
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    video_data = loop.run_until_complete(download_facebook_video(url))
                    if video_data:
                        status = True
                        platform = 'FaceBook'
                        title = ''
                        response = Response({'status': status, 'title':title,'downloadables': video_data['downloadables'] , 'image_url': video_data['thumbnail'],'platform': platform,})
                    else:
                        status = False
                        response = Response({'status': status, 'message': 'Could not download video'})
                except:
                    status = False
                    response = Response({'status': status, 'message': 'An error occurred while downloading the video'})
            else:
                status = False
                response = Response({'status': status, 'message': 'Invalid input'})
            return response
