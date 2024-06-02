from unittest.mock import patch, MagicMock

from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase, APIClient


class BaseTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        patch('django_redis.get_redis_connection', return_value=MagicMock())


class TestAveragePrice(BaseTest):

    @patch('redis_cache_manager.redis_client.zrangebyscore')
    def test_average_price_calculation(self, mock_zrangebyscore):
        """
        Verify that the 'average-price' view calculates the average
        price correctly.

        Mock redis 'zrangebyscore' function to simulate data and then
        send a GET request with 'since' and 'until' query parameters.
        Verify that the response has a status code of 200 and that the
        calculated average price in the view matches the expected price.
        """
        since_timestamp = "1717135270"
        until_timestamp = "1817135429"
        timestamp_prices = [
            (82000000.0, since_timestamp),
            (78000000.0, "1717135400"),
            (85000000.0, until_timestamp)
        ]
        # Calculate the expected average price based on the mocked data
        sum_prices = [price for price, _ in timestamp_prices]
        average = round(sum(sum_prices) / len(timestamp_prices), 2)

        # Mock redis 'zrangebyscore' function to return specific data
        mock_zrangebyscore.return_value = status.HTTP_200_OK
        mock_zrangebyscore.return_value = timestamp_prices

        # Send a GET request to the 'average-price' endpoint with
        # query parameters
        url = reverse_lazy("ticker:average-price")
        response = self.client.get(
            url,
            data={"since": since_timestamp, "until": until_timestamp}
        )

        # Verify that the response has a status code of 200 and the
        # calculated average price
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["average_price"], average)

    @patch('redis_cache_manager.redis_client.zrangebyscore')
    def test_average_price_calculation_with_empty_data_in_db(
        self,
        mock_zrangebyscore
    ):
        """
        Verify that the 'average-price' view calculates the average price
        correctly with empty data in redis db.

        Mock redis 'zrangebyscore' function to return specific data and then send a GET request
        with 'since' and 'until' query parameters. Verify that the response has a status
        code of 200 and that the calculated average price in the view is 0.
        """
        since_timestamp = "1717135270"
        until_timestamp = "1817135429"
        timestamp_prices = []

        average = 0

        # Mock redis 'zrangebyscore' function to return specific data
        mock_zrangebyscore.return_value = status.HTTP_200_OK
        mock_zrangebyscore.return_value = timestamp_prices

        # Send a GET request to the 'average-price' endpoint with
        # query parameters
        url = reverse_lazy("ticker:average-price")
        response = self.client.get(
            url,
            data={"since": since_timestamp, "until": until_timestamp}
        )

        # Verify that the response has a status code of 200 and the
        # calculated average price
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["average_price"], average)

    def test_bad_request_calculation_when_missing_until_parameter(self):
        """
        Verify that a bad request is returned when 'until' parameter is missing.

        Send a GET request to the 'average-price' endpoint with only 'since' parameter
        provided and verify that the response has a status code of 400 (Bad Request).
        """
        # Prepare the URL for the 'average-price' endpoint
        url = reverse_lazy("ticker:average-price")

        # Send a GET request with only 'since' parameter provided
        response = self.client.get(url, data={"since": "1717135270"})

        # Verify that the response has a status code of 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_request_calculation_when_missing_since_parameter(self):
        """
        Verify that a bad request is returned when 'since' parameter is missing.

        Send a GET request to the 'average-price' endpoint with only 'since' parameter
        provided and verify that the response has a status code of 400 (Bad Request).
        """
        # Prepare the URL for the 'average-price' endpoint
        url = reverse_lazy("ticker:average-price")

        # Send a GET request with only 'since' parameter provided
        response = self.client.get(url, data={"until": "1817135429"})

        # Verify that the response has a status code of 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_request_calculation_when_empty_query_params(self):
        """
        Verify that a bad request is returned when data is empty.

        Send a GET request to the 'average-price' endpoint with empty data
        provided and verify that the response has a status code of 400 (Bad Request).
        """
        # Prepare the URL for the 'average-price' endpoint
        url = reverse_lazy("ticker:average-price")

        # Send a GET request with empty data
        response = self.client.get(url, data={})

        # Verify that the response has a status code of 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestTickerList(BaseTest):

    @patch('redis_cache_manager.redis_client.zrangebyscore')
    def test_ticker_list_view_http_200_filter_correct_data(self, mock_zrangebyscore):
        """
        Verify that the 'ticker-list' view returns the correct data.

        Mock the 'zrangebyscore' function to return specific data and then send a GET request
        to the 'ticker-list' endpoint with 'since' and 'until' query parameters. Verify that
        the response has a status code of 200 and that the returned data matches the expected format.
        """
        since_timestamp = 1717135270
        until_timestamp = 1817135429
        timestamp_prices_db = [
            (82000000.0, since_timestamp),
            (78000000.0, 1717135400),
            (85000000.0, until_timestamp)
        ]

        # Calculate the expected ticker list
        timestamp_prices_dict = [
            {"timestamp": timestamp, "price": price}
            for price, timestamp in timestamp_prices_db
        ]

        # Mock redis 'zrangebyscore' function to return specific data
        mock_zrangebyscore.return_value = status.HTTP_200_OK
        mock_zrangebyscore.return_value = timestamp_prices_db

        # Send a GET request to the 'ticker-list' endpoint with
        # query parameters
        url = reverse_lazy("ticker:ticker-list")
        response = self.client.get(
            url,
            data={"since": since_timestamp, "until": until_timestamp}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(timestamp_prices_db))
        self.assertEqual(response.data["results"], timestamp_prices_dict)

    @patch('redis_cache_manager.redis_client.zrangebyscore')
    def test_ticker_list_view_without_params(
        self,
        mock_zrangebyscore
    ):
        """
        Verify that the 'ticker-list' view returns the correct data without query parameters.

        Mock redis 'zrangebyscore' function to return specific data and then send a GET request
        to the 'ticker-list' endpoint without query parameters. Verify that the response has
        a status code of 200 and that the returned data matches the expected format.
        """
        timestamp_prices_db = [
            (82000000.0, 1717135270),
            (78000000.0, 1717135400),
            (85000000.0, 1817135429),
            (100000000.0, 1917135429),
        ]

        # Calculate the expected ticker list
        timestamp_prices_dict = [
            {"timestamp": timestamp, "price": price}
            for price, timestamp in timestamp_prices_db
        ]

        # Mock redis 'zrangebyscore' function to return specific data
        mock_zrangebyscore.return_value = status.HTTP_200_OK
        mock_zrangebyscore.return_value = timestamp_prices_db

        # Send a GET request to the 'ticker-list' endpoint without
        # query parameters
        url = reverse_lazy("ticker:ticker-list")
        response = self.client.get(url, data={})

        # Verify that the response has a status code of 200 and the
        # returned data matches the expected format
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(timestamp_prices_db))
        self.assertEqual(response.data["results"], timestamp_prices_dict)
