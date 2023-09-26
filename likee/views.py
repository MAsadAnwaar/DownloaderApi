
import json
import youtube_dl

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import*
from .serializers import*
import requests
from bs4 import BeautifulSoup


# Create your views here.
class LikeeappView(APIView):
    serializer_class=likeeSerializer 
    def get(self,request):
        # allurl = dailymotionurl.objects.all().values()

        return Response()


    def post(self,request):
        # print("Request Data is  :",request.data)
        
        serializer_obj=likeeSerializer(data=request.data)
       
        url = request.POST.get("url")
        mylist = []
        try:
      
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

            start_index = template.find("Without watermark") + len("Without watermark</div>")
            start_index = template.find("href=\"", start_index) + 6
            end_index = template.find("\"", start_index)
            without_watermark_href = template[start_index:end_index]
                    # print(url)
            downloadables.append({'quality': "Without watermark", 'url': without_watermark_href})
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
       