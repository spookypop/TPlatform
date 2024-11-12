from rest_framework import serializers


class PostmanSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    collection_name = serializers.CharField()
    file_type = serializers.CharField()
    file_name = serializers.CharField()
    file_path = serializers.CharField()
    upload_time = serializers.CharField()
