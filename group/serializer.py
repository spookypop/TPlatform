from rest_framework import serializers


class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    create_time = serializers.CharField()
