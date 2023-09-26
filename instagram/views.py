
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import*
from .serializers import*
import os
import time
import requests
from bs4 import BeautifulSoup

import re
class InstaView(APIView):
    serializer_class=instaurlSerializer 
    def get(self,request):
        return Response()
    def jls_extract_def(self):
        
        return 

    def post(self,request):
        try:
            serializer_obj=instaurlSerializer(data=request.data)
            serializer_obj.is_valid(raise_exception=True)
            url = serializer_obj.validated_data['url']
            urlsp = url.split("?")[0]
            video_id = urlsp.split("/")[-2]
            regex_pattern = r"(https:\/\/instagram\.com\/stories)"
            regex_pattern1 = r"(https:\/\/www\.instagram\.com\/stories)"
            
            match = re.search(regex_pattern, url) or re.search(regex_pattern1, url)
            if match:
                    
                    downloadables = []
                    url1 = f"https://igram.world/api/ig/story?url={url}"

                    # Send a GET request to the URL
                    response = requests.get(url1)
                    if response.status_code == 200:
                    # Parse the JSON content
                        data = json.loads(response.text)
                        results = data['result']
                            
                        for result in results:
                            image_url = result['image_versions2']['candidates'][0]['url']
                            video_versions = result.get('video_versions', [])
                            
                            for video in video_versions:
                                video_url = video['url']
                                width = video['width']
                                height = video['height']
                                quality = f"{width}x{height}"
                                downloadables.append({'quality': quality, 'url': video_url})

                    platform = "instagram"
                    status = True
                    if downloadables == []:
                        results = data['result']
            
                        for result in results:
                            image_versions = result.get('image_versions2', {}).get('candidates', [])
                            # video_versions = result.get('video_versions', [])
                            
                            for image in image_versions:
                                video_url = image['url']
                                width = image['width']
                                height = image['height']
                                quality = f"{width}x{height}"
                                downloadables.append({'quality': quality, 'url': video_url})

                    return Response({
                        "status": status,
                        "title": "",
                        "downloadables": downloadables,
                        "image_url": image_url,
                        "platform": platform
                    })
            if not match:
                regex_pattern = r"(https:\/\/instagram\.com\/p)"
                regex_pattern1 = r"(https:\/\/www\.instagram\.com\/p)"
                
                match = re.search(regex_pattern, url) or re.search(regex_pattern1, url)
                if match:
                    downloadables = []
                    apiurl = "https://fastdl.app/c/"
                    payload = {
                        "url": url,
                        "lang_code": "en",
                        "token": ""
                    }
                    headers = {
                        "Host": "fastdl.app",
                        "Accept": "*/*",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Referer": "https://fastdl.app/",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "Origin": "https://fastdl.app",
                        "Connection": "keep-alive",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-origin",
                        "TE": "trailers"
                    }
                    response = requests.post(apiurl, data=payload, headers=headers)
                    soup = BeautifulSoup(response.content, "html.parser")
                    # href_element = soup.find(class_="mt-1 rounded-md border-b-4 border-blue-800 bg-blue-600 py-2 ring-1 ring-blue-500 hover:bg-blue-700")

                    # thumbnail = ""
                    title = ""
                    success = True
                    src_element = soup.find(class_="w-full")
                    if src_element:
                        src_value = src_element.get("src")
                    href_elements = soup.find_all(class_="mt-1 rounded-md border-b-4 border-blue-800 bg-blue-600 py-2 ring-1 ring-blue-500 hover:bg-blue-700")
                    for element in href_elements:
                        href = element.get('href')
                        data_mediatype = element.get('data-mediatype')
                        if href and data_mediatype:
                            # print(href)
                            downloadables.append({'quality': data_mediatype, 'url': href})
                    platform = "instagram"
                    return Response({
                        "status": success,
                        "title": title,
                        "downloadables": downloadables,
                        "image_url": src_value,
                        "platform": platform
                    })
                if not match:
                    downloadables = []
                    url1 = "https://snapinsta.tools/action.php"
                    payload = {
                            "url": url
                        }
                    
                    response = requests.post(url1, data=payload)
                    # Parse the HTML response using BeautifulSoup
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # href_element = soup.find(class_="mt-1 rounded-md border-b-4 border-blue-800 bg-blue-600 py-2 ring-1 ring-blue-500 hover:bg-blue-700")

                    # thumbnail = ""
                    title = ""
                    success = True
                    img_elements = soup.find_all('img')
                    for img_element in img_elements:
                        img_url = img_element['src']
                        # print("Image URL:", img_url)

                    # Find the elements with the 'a' tag and extract the 'href' attribute
                    video_elements = soup.find_all('a', href=True)
                    for video_element in video_elements:
                        video_url = video_element['href']
                        # Check if the div with class 'text-2xl tracking-wide uppercase' contains 'mp4' text
                        quality_element = video_element.find('div', class_='text-2xl tracking-wide uppercase')
                        # if quality_element and 'mp4' in quality_element.text.lower():
                            # Get the quality from the next sibling div tag
                        quality = quality_element.find_next('div').text.strip()
                        # print("Video URL:", video_url)
                        # print("Quality:", quality)
                            # print(href)
                        downloadables.append({'quality': quality, 'url': video_url})
                    platform = "instagram"
                    return Response({
                        "status": success,
                        "title": title,
                        "downloadables": downloadables,
                        "image_url": video_url,
                        "platform": platform
                    })
                    
            
        except:
            try:
                downloadables = []
                apiurl = "https://www.w3toys.com/"
                data = {
                        "link": url,
                        "submit": "DOWNLOAD",
                        # Add more key-value pairs as needed
                    }
                response = requests.post(apiurl,  data=data)
                # href_element = soup.find(class_="mt-1 rounded-md border-b-4 border-blue-800 bg-blue-600 py-2 ring-1 ring-blue-500 hover:bg-blue-700")

                # thumbnail = ""
                title = ""
                success = True
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Find all <img> tags
                    img_tags = soup.find_all("img")

                    if img_tags:
                        # Print all the image URLs found within <img> tags
                        for img in img_tags:
                            if "src" in img.attrs:
                                img_url = img["src"]
                                # print(f"Image URL: {img_url}, Type: Image")
                                downloadables.append({'quality': 'Image', 'url': img_url})

                    # Find the <div> with class 'dlsection'
                    dlsection_div = soup.find("div", class_="dlsection")

                    if dlsection_div:
                        # Print all the video URLs and their types found within <video> tags
                        video_tags = dlsection_div.find_all("video")
                        for video in video_tags:
                            source_tag = video.find("source")
                            if source_tag and "src" in source_tag.attrs and "type" in source_tag.attrs:
                                video_url = source_tag["src"]
                                video_type = source_tag["type"]
                                # print(f"Video URL: {video_url}, Type: {video_type}")
                                downloadables.append({'quality': video_type, 'url': video_url})
                                img_url = video_url

                        
                platform = "instagram"
                return Response({
                    "status": success,
                    "title": title,
                    "downloadables": downloadables,
                    "image_url": img_url,
                    "platform": platform
                })
            
            except Exception as e:
            # print("Error Message is Here:",ValueError)
                error_message = [ValueError]
                status = False
                return Response({"status": status , "error_message": e.args })   