from django.shortcuts import render
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from services.buenbit.buenbit import BuenbitApiHandle
from ticker.serializers import TickerSerializer, TickerAveragePriceSerializer
from ticker.ticker import BuenbitTicker


class AveragePriceView(APIView):

    @staticmethod
    def get(request):
        since_timestamp = request.GET.get('since')
        until_timestamp = request.GET.get('until')

        if not since_timestamp or not until_timestamp:
            return Response(
                data={"error": "Please provide since and until timestamps."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            since_timestamp = float(since_timestamp)
            until_timestamp = float(until_timestamp)
        except ValueError:
            return Response(
                data={"error": "Timestamps must be valid numbers."},
                status=status.HTTP_400_BAD_REQUEST
            )

        ticker = BuenbitTicker()
        average_price = ticker.get_average_price(
            since_timestamp=since_timestamp,
            until_timestamp=until_timestamp
        )
        serializer = TickerAveragePriceSerializer(data=average_price)
        serializer.is_valid()  # TODO EXCEPTIONS
        return Response(serializer.data, status=status.HTTP_200_OK)


class TickerListView(APIView):

    @staticmethod
    def get(request):
        since_timestamp = request.GET.get('since')
        until_timestamp = request.GET.get('until')
        page_size = request.GET.get('page_size', 10)

        if not since_timestamp:
            since_timestamp = "-inf"
        if not until_timestamp:
            until_timestamp = "+sup"

        # except ValueError:
        #     return Response({"error": "Invalid parameters."}, status=status.HTTP_400_BAD_REQUEST)

        ticker = BuenbitTicker()
        ticker_list = ticker.get_tickers_list(
            since_timestamp=since_timestamp,
            until_timestamp=until_timestamp
        )

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(ticker_list, request)

        # Serializar los datos paginados
        serializer = TickerSerializer(data=result_page, many=True)
        serializer.is_valid()
        return paginator.get_paginated_response(serializer.data)
