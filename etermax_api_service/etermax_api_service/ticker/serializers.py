from rest_framework import serializers


class TickerAveragePriceSerializer(serializers.Serializer):
    average_price = serializers.FloatField(required=True)


class TickerSerializer(serializers.Serializer):
    timestamp = serializers.FloatField(required=True)
    price = serializers.FloatField(required=True)
