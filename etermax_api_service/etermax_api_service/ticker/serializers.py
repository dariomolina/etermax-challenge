from rest_framework import serializers


class TickerAveragePriceSerializer(serializers.Serializer):
    """
    Serializer for the average price of tickers.

    Fields:
        average_price (float): The average price of the tickers.
    """
    average_price = serializers.FloatField(required=True)


class TickerSerializer(serializers.Serializer):
    """
    Serializer for individual ticker data.

    Fields:
        timestamp (int): The timestamp of the ticker.
        price (float): The price of the ticker.
    """
    timestamp = serializers.IntegerField(required=True)
    price = serializers.FloatField(required=True)


class TickerPriceSerializer(serializers.Serializer):
    """
    Serializer for the price of tickers.

    Fields:
        price (float): The price of the tickers.
    """
    price = serializers.FloatField(required=True)
