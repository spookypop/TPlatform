from rest_framework import serializers
from SprintList.models import sprints, cases


class SprintSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    sprint_name = serializers.CharField()
    state = serializers.CharField()

    def create(self, validated_data):
        return sprints.objects.create(**validated_data)


class CaseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    app_name = serializers.CharField()
    module_name = serializers.CharField()
    case_description = serializers.CharField()
    case_data =serializers.CharField()
    sprint_name_id = serializers.CharField()
    user = serializers.CharField()
    result = serializers.CharField()

    def create(self, validated_data):
        return cases.objects.create(**validated_data)
