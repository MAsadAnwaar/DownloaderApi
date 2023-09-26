
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import*
from .serializers import*
import requests
from bs4 import BeautifulSoup

# Create your views here.
class PinterestappView(APIView):
    serializer_class=pinterestSerializer 
    def get(self,request):
        # allurl = dailymotionurl.objects.all().values()

        return Response()


    def post(self,request):
        # print("Request Data is  :",request.data)
        
        serializer_obj=pinterestSerializer(data=request.data)
       
        url = request.POST.get("url")
        mylist = []
        try:
      
            downloadables = []
            url1 = f"https://pinterestvideodownloader.io/result_divs.php?video={url}"
            headers = {
                "Host": "pinterestvideodownloader.io",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1"
            }

            response = requests.get(url1, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                video_elements = soup.find_all("video")
                for video in video_elements:
                    src = video.get("src")
                    # print(f"<video controls='' src='{src}'></video>")
                    downloadables.append({'quality': "", 'url': src})
                # Extract <a> elements with id="thumbnail"
                thumbnail_elements = soup.find_all("a", id="thumbnail")
                for thumbnail in thumbnail_elements:
                    img_thumb_src = thumbnail.get("href")
                    # print(f"<a id='thumbnail' href='{img_thumb_src}'>Link</a>")
                    # print(url)
                
            platform = 'Likee'
            status = True
            return Response({
                "status": status,
                "title": "",
                "downloadables": downloadables,
                "image_url": img_thumb_src,
                "platform": platform
            })
        except Exception as e:
                    error_message = [ValueError]
                    status = False
                    return Response({"status": status , "error_message": e.args })
       