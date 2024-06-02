import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import requests
from rest_framework import status

from services.buenbit.buenbit import BuenbitApiService, BuenbitApiHandle


class TestBuenbitApiService(unittest.TestCase):
    """
    Test suite for the BuenbitApiService class.
    """

    def setUp(self):
        self.response_api_data = {
            "object": {
                "btcars": {
                    "currency": "ars",
                    "bid_currency": "btc",
                    "ask_currency": "ars",
                    "purchase_price": "82781100.0",
                    "selling_price": "84436700.0",
                    "open_price": "83439260.1561159577375675",
                    "market_identifier": "btcars"
                }
            }
        }

    @patch('requests.get')
    def test_get_successful_response(self, mock_get):
        """
        Test the get method for a successful API response.
        """
        # Mock the response to buenbit api from the requests.get call
        mock_response = MagicMock()
        mock_response.json.return_value = self.response_api_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = BuenbitApiService()
        result = service.get()

        # Assert that the mock response was used
        self.assertEqual(result, self.response_api_data)
        mock_get.assert_called_once_with(url=service.url, headers=service.headers)

    @patch('requests.get')
    def test_get_raises_exception(self, mock_get):
        """
        Test the get method to ensure it raises an exception for an error response.
        """
        # Mock the response to raise a RequestException
        mock_get.side_effect = requests.RequestException("Error")

        service = BuenbitApiService()
        with self.assertRaises(requests.RequestException):
            service.get()


class TestBuenbitApiHandle(unittest.TestCase):
    """
    Test suite for the BuenbitApiHandle class.
    """

    def setUp(self):
        self.response_api_data = {
            "object": {
                "btcars": {
                    "currency": "ars",
                    "bid_currency": "btc",
                    "ask_currency": "ars",
                    "purchase_price": "82781100.0",
                    "selling_price": "84436700.0",
                    "open_price": "83439260.1561159577375675",
                    "market_identifier": "btcars"
                }
            }
        }

    @patch.object(BuenbitApiService, 'get')
    def test_handle_successful_response(self, mock_get):
        """
        Test the handle method for a successful data retrieval and processing.
        """
        response_price = float(
            self.response_api_data['object']['btcars']['selling_price']
        )

        # Mock the response to buenbit api from the requests.get call
        mock_get.return_value = self.response_api_data
        mock_get.status_code = status.HTTP_200_OK

        handler = BuenbitApiHandle()
        result = handler.handle(market_identifier='btcars')

        # Assert the result contains the correct timestamp and price
        self.assertIn('timestamp', result)
        self.assertIn('price', result)
        self.assertIsInstance(result['price'], float)
        self.assertIsInstance(result['timestamp'], int)
        self.assertEqual(
            result['price'],
            response_price
        )

    @patch.object(BuenbitApiService, 'get', return_value={})
    def test_handle_key_error(self, mock_get):
        """
        Test the handle method to ensure it raises a KeyError for unexpected
        response structure in the buenbit api.
        """
        handler = BuenbitApiHandle()
        with self.assertRaises(KeyError):
            handler.handle('btc_ars')


if __name__ == '__main__':
    unittest.main()
