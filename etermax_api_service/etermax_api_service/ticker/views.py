from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from common import convert_to_float
from ticker.serializers import TickerSerializer, TickerAveragePriceSerializer
from ticker.ticker import BuenbitTicker


class AveragePriceView(APIView):
    """
    API view to get the average price of tickers within
    a specified timestamp range.
    """

    def get(self, request):
        """
        Handle GET requests to retrieve the average price
        of tickers.

        Query Parameters:
            since (str): The start of the time range.
            until (str): The end of the time range.

        Returns:
            Response: A response containing the average price
            or an error message.
        """
        since_timestamp = request.GET.get('since')
        until_timestamp = request.GET.get('until')

        try:
            self.check_timestamps_presence(timestamp=since_timestamp)
            self.check_timestamps_presence(timestamp=until_timestamp)

            since_timestamp = convert_to_float(value=since_timestamp)
            until_timestamp = convert_to_float(value=until_timestamp)

            ticker = BuenbitTicker()
            average_price = ticker.get_average_price(
                since_timestamp=since_timestamp,
                until_timestamp=until_timestamp
            )
            serializer = TickerAveragePriceSerializer(data=average_price)
            serializer.is_valid()

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as error:
            return Response(
                data={"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as error:
            return Response(
                data={"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def check_timestamps_presence(timestamp):
        if not timestamp:
            raise Exception("Please provide since and until timestamps.")


class TickerListView(APIView):
    """
    API view to get a list of tickers within a specified
    timestamp range with pagination.
    """

    @staticmethod
    def get(request):
        """
        Handle GET requests to retrieve a list of tickers.

        Query Parameters:
            since (str, optional): The start of the timestamp
            range. Defaults to "-inf".

            until (str, optional): The end of the timestamp
            range. Defaults to "+inf".

            page (int, optional): The page number to retrieve.
            Defaults to 1.

            page_size (int, optional): The number of items
            per page. Defaults to 10.

        Returns:
            Response: A paginated response containing the list
            of tickers or an error message.
        """
        since_timestamp = request.GET.get('since')
        until_timestamp = request.GET.get('until')
        page_size = request.GET.get('page_size', 10)

        if not since_timestamp:
            since_timestamp = float("-inf")
        if not until_timestamp:
            until_timestamp = float("+inf")

        ticker = BuenbitTicker()

        try:
            ticker_list = ticker.get_tickers_list(
                since_timestamp=since_timestamp,
                until_timestamp=until_timestamp
            )

            # Pagination
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            result_page = paginator.paginate_queryset(ticker_list, request)

            # Serialize the paginated data
            serializer = TickerSerializer(data=result_page, many=True)
            serializer.is_valid()
            return paginator.get_paginated_response(serializer.data)

        except ValidationError as error:
            return Response(
                data=str(error),
                status=status.HTTP_400_BAD_REQUEST)
        except RuntimeError as error:
            return Response(
                data=str(error),
                status=status.HTTP_408_REQUEST_TIMEOUT)
