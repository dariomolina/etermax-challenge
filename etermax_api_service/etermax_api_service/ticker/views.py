from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from services.buenbit.buenbit import BuenbitApiHandle
from ticker.serializers import TickerSerializer
from ticker.ticker import Ticker


class TickerView(APIView):

    def get(self, request):
        """
        Return a list of all tickers.
        """
        key = request
        ticker = Ticker.get()
        usernames = ["hola get"]
        return Response(usernames)


class TickerPriceView(APIView):
    def get(self, request, timestamp):
        market_identifier = request.data

        ticker_serializer = TickerSerializer(data)
        return Response(ticker_serializer.data)


class AveragePriceView(APIView):
    def get(self, request, start_timestamp, end_timestamp):
        data = TickerData.objects.filter(timestamp__range=[start_timestamp, end_timestamp])
        avg_price = data.aggregate(models.Avg('btc_ars'))['btc_ars__avg']
        return Response({'average_price': avg_price})