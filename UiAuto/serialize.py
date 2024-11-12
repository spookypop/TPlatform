from rest_framework import serializers


class Uiserializer(serializers.Serializer):
    id = serializers.IntegerField()
    ui_name = serializers.CharField()
    state = serializers.CharField()
    result = serializers.CharField()
    update_time = serializers.CharField()


class Suitserializer(serializers.Serializer):
    ui_id_id = serializers.IntegerField()
    id = serializers.IntegerField()
    action_type = serializers.IntegerField()
    actions = serializers.CharField()
    location_fun = serializers.CharField()
    location = serializers.CharField()
    value = serializers.CharField()
