from io import BytesIO
import httpx
import asyncio
from rest_framework.views import APIView
from rest_framework.response import Response
from snapsave import Fb, DownloadCallback
import requests
from bs4 import BeautifulSoup
from .serializers import facebookurlSerializer
import json

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



class FacebookView(APIView):
    serializer_class=facebookurlSerializer 
    def get(self,request):
        # allurl = twitterurl.objects.all().values()
        return Response()

    serializer_class = facebookurlSerializer
    def post(self, request):
        serializer_obj = facebookurlSerializer(data=request.data)  
        if serializer_obj.is_valid():
            url = serializer_obj.validated_data['url']
            mylist = []
        try:
            try:
                    try:
                        downloadables = []
                        url1 = "https://savefromus.com/api/convert"
                        payload = {"url": url}
                        response = requests.post(url1, data=payload)

                        if response.status_code == 200:
                            data = response.json()
                            thumbnail_url = data.get("thumb", "")
                            title = data.get("meta", {}).get("title", "")
                            video_urls = []
                            for item in data.get("url", []):
                                url_info = {
                                    "url": item.get("url", ""),
                                    "name": item.get("name", ""),
                                    "subname": item.get("subname", ""),
                                    "type": item.get("type", ""),
                                    "ext": item.get("ext", "")
                                }
                                video_urls.append(url_info)
                            for url_info in video_urls:
                                print("URL:", url_info["url"])
                                print("Quality:", url_info["name"])
                                print("Subname:", url_info["subname"])
                                print("Type:", url_info["type"])
                                print("Extension:", url_info["ext"])
                                # print()
                            
                                downloadables.append({'quality': url_info["subname"]+"1", 'url': url_info["url"]})
                            
                            thumbnail_url = thumbnail_url
                        platform = 'Facebook'
                        status = True
                        return Response({
                            "status": status,
                            "title": title,
                            "downloadables": downloadables,
                            "image_url": thumbnail_url,
                            "platform": platform
                        })
                    except:
                        downloadables = []
                        url1 = "https://x2download.app/api/ajaxSearch/facebook"
                        payload = {
                            "q": url,
                            "vt": "facebook",
                        }

                        response = requests.post(url1, data=payload)

                        if response.status_code == 200:
                            data = response.json()

                            # Extract the URLs and other information
                            sd_url = data["links"]["sd"]
                            if sd_url:
                                downloadables.append({'quality': "SD1", 'url': sd_url})

                            hd_url = data["links"]["hd"]
                            if hd_url:
                                downloadables.append({'quality': "HD1", 'url': hd_url})
                            title = data["title"]
                            thumbnail_url = data["thumbnail"]
                        platform = 'Facebook'
                        status = True
                        return Response({
                            "status": status,
                            "title": title,
                            "downloadables": downloadables,
                            "image_url": thumbnail_url,
                            "platform": platform
                        })
            except:
      
                downloadables = []
                url1 = "https://likeedownloader.com/process"
                payload = {
                    "id": url,
                }

                response = requests.post(url1, data=payload)
                data = json.loads(response.content)
                # Parse the JSON content
                template = data["template"]
                start_index = template.find("src=\"") + 5
                end_index = template.find("\"", start_index)
                img_thumb_src = template[start_index:end_index]
                
                    
                start_index = template.find("With watermark") + len("With watermark</div>")
                start_index = template.find("href=\"", start_index) + 6
                end_index = template.find("\"", start_index)
                with_watermark_href = template[start_index:end_index]
                if with_watermark_href:
                        # print(url)
                    downloadables.append({'quality': "sd", 'url': with_watermark_href})

                start_index = template.find("Without watermark") + len("Without watermark</div>")
                start_index = template.find("href=\"", start_index) + 6
                end_index = template.find("\"", start_index)
                without_watermark_href = template[start_index:end_index]
                if without_watermark_href:
                        # print(url)
                    downloadables.append({'quality': "hd", 'url': without_watermark_href})
                platform = 'Facebook'
                status = True
                return Response({
                    "status": status,
                    "title": "",
                    "downloadables": downloadables,
                    "image_url": img_thumb_src,
                    "platform": platform
                })
        except:
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
