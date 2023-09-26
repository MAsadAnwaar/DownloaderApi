from rest_framework import serializers


class dailymotionurlSerializer(serializers.Serializer):
    url=serializers.CharField(label="Enter URL")