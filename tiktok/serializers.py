from rest_framework import serializers


class tiktokurlSerializer(serializers.Serializer):
    url=serializers.CharField(label="Enter URL")