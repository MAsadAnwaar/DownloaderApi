      
import json
import tiktok_downloader

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import*
from .serializers import*
from tiktok_downloader import snaptik , ttdownloader, mdown , tikdown , ttdownloader , tikwm , VideoInfo ,VideoInfo
import time
# Create your views here.




class TikTokView(APIView):
    serializer_class = tiktokurlSerializer

    def get(self, request):
        return Response()

    def post(self, request):
        serializer_obj = tiktokurlSerializer(data=request.data)
        url = request.POST.get("url")
        mylist = []

        try:
            downloadables = []
            tiktok_url = url.split("?")[0]

            media_list = snaptik(tiktok_url)

            for media in media_list:
                response = media.json
                quality1=media.type
                url = response.split("=1")[0]
                # url = response

                if url != "https://play.google.com/store/apps/details?id=com.snaptik.tt.downloader.nologo.nowatermark":
                    downloadables.append({'quality': quality1, 'url': url})

            platform = 'tiktok'
            title = ''
            image_url = ''
            status = True

            return Response({
                "status": status,
                "title": title,
                "downloadables": downloadables,
                "image_url": image_url,
                "platform": platform
            })

        except Exception as e:
            error_message = [ValueError]
            status = False
            return Response({"status": status, "error_message": e.args})
