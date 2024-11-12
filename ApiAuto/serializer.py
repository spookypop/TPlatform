from rest_framework import serializers
from .models import apiauto


class ApiSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name_id = serializers.CharField()
    api_module = serializers.CharField()
    scene = serializers.CharField()
    api_name = serializers.CharField()
    assertion_rule = serializers.CharField()
    assertion = serializers.CharField()
    state = serializers.CharField()
    result_desc = serializers.CharField()

    def create(self, validated_data):
        # username = validated_data['username']
        # password = validated_data['password']
        return apiauto.objects.create(**validated_data)
