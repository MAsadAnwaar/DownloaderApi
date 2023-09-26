from rest_framework import serializers


class SnackvideoSerializer(serializers.Serializer):
    url=serializers.CharField(label="Enter URL")