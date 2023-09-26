from rest_framework import serializers


class facebookurlSerializer(serializers.Serializer):
    url=serializers.CharField(label="Enter url")

from rest_framework import serializers

class FacebookDownloadSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)
    quality = serializers.CharField(required=False, allow_blank=True)



