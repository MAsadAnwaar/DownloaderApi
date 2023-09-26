from rest_framework import serializers


class instaurlSerializer(serializers.Serializer):
    url=serializers.CharField(label="Enter URL")