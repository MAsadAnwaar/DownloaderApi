from rest_framework import serializers


class twitterurlSerializer(serializers.Serializer):
    url=serializers.CharField(label="Enter URL")