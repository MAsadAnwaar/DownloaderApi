from io import BytesIO
import httpx
import asyncio
from rest_framework.views import APIView
from rest_framework.response import Response
from snapsave import Fb, DownloadCallback

from .serializers import facebookurlSerializer

class Download(DownloadCallback):
    def __init__(self, length: int, downloadables: list, quality: int, quality_label: str) -> None:
        super().__init__()
        self.io = BytesIO()
        self.length = length
        self.clength = 0
        self.downloadables = downloadables
        self.quality = quality
        self.quality_label = quality_label.split("::")[2]

    async def on_open(self, client: httpx.AsyncClient, response: httpx.Response):
        self.downloadables.append({'quality': self.quality_label, 'url': str(response.url).split("=1")[0], 'size': int(response.headers.get('content-length'))})
        print("Downloadable URL", response.url, "with quality", self.quality_label, "and size", int(response.headers.get('content-length')))



async def download_facebook_video(url):
    vid = await Fb().from_url(url)
    try:
        thumbnail = vid.cover
        print("Thumbnail",thumbnail)
    except:
        thumbnail=[]    
    downloadables = []
    for i, quality in reversed(list(enumerate(vid))):
        print(vid)

        quality_label = str(quality)
        dd = Download(await quality.get_size(), downloadables, quality=i, quality_label=quality_label)
        print(f"Trying quality {i}: {quality}")
        try:
            await quality.download(dd)
            content = dd.io.getvalue()
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
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                video_data = loop.run_until_complete(download_facebook_video(url))
                if video_data:
                    status = True
                    response = Response({'status': status, 'thumbnail': video_data['thumbnail'], 'downloadables': video_data['downloadables']})
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
