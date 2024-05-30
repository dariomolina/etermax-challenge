from rest_framework import serializers


class TickerSerializer(serializers.Serializer):
    timestamp = serializers.DateField(required=True)
    price = serializers.CharField(required=True)
