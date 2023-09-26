from rest_framework import serializers


class LinkedinvideoSerializer(serializers.Serializer):
    url=serializers.CharField(label="Enter URL")