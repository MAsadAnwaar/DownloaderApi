from rest_framework import serializers


class likeeSerializer(serializers.Serializer):
    url=serializers.CharField(label="Enter URL")