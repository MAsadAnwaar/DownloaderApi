from rest_framework import serializers


class threatappurlSerializer(serializers.Serializer):
    url=serializers.CharField(label="Enter URL")