import json
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import*
from .serializers import*
import os
import time
# Create your views here.
class Aio_Video_DownloaderView(APIView):
    serializer_class=Aio_Video_DownloaderurlSerializer 
    def get(self,request):
        return Response()
    def post(self,request):
        serializer_obj=Aio_Video_DownloaderurlSerializer(data=request.data)
       
        url = request.POST.get("url")
        
        try:
            downloadables=[]
            
            import requests
            import json
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
                    else:
                           subname = 'N/A'

                    # url = item['url'] 
                    try :
                        import requests
    
                        url = item['url']
                        api_url = f'http://tinyurl.com/api-create.php?url={url}'
    
                        response = requests.get(api_url)
    
                        if response.status_code == 200:
                            short_url = response.text
                    except:
                        url = item['url']
                        short_url = url
                    downloadables.append({'quality': subname, 'url': short_url})

            platform = hosting.split(".")[0]
            try:
                image_url =thumb  
                
                api_urli = f'http://tinyurl.com/api-create.php?url={image_url}'

                response = requests.get(api_urli)

                
                short_urli = response.text
                image = short_urli
                if image == "Error":
                    image = "N/A"
            except:
                short_urli = thumb  
            # image = short_urli    
            status = True
            return Response({"status": status,"title":title,"downloadables": downloadables,"image_url":image ,"platform":platform })    
        except Exception as e:
            error_message = [ValueError]
            status = False
            return Response({"status": status , "error_message": e.args })
       