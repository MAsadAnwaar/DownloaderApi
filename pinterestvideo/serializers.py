from rest_framework import serializers


class pinterestSerializer(serializers.Serializer):
    url=serializers.CharField(label="Enter URL")