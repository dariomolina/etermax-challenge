import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Union

import requests
from requests import RequestException


class ApiService(ABC):
    """
    Abstract base class for API services.
    """

    @abstractmethod
    def get(self) -> Dict:
        """
        Abstract method to perform a GET request.

        This method should be implemented by subclasses to define the specific
        logic for making a GET request to an API.

        Returns:
            dict: The response from the API in JSON format.
        """
        raise NotImplementedError


class BuenbitApiService(ApiService):
    """
    Service class to interact with the Buenbit API.
    """

    def __init__(self):
        """
        Initializes the BuenbitApiService with the API URL and headers.
        """
        self.url = os.environ.get("BUENBIT_URL", "")
        self.headers = {
            "content-type": "application/json"
        }

    def get(self) -> Dict:
        """
        Perform a GET request to the Buenbit API.

        Returns:
            dict: The response from the API in JSON format.

        Raises:
            requests.exceptions.RequestException: If there's
            a problem with the request.
        """
        try:
            response = requests.get(
                url=self.url,
                headers=self.headers
            )
            response.raise_for_status()  # Raise an error for non-2xx responses
            return response.json()
        except RequestException as error:
            raise error  # Reraise the exception for handling at a higher level


class BuenbitApiHandle:
    """
    Handler class to process data from the Buenbit API.

    This class handles the retrieval and processing of data from the Buenbit API,
    specifically for market data identified by market_identifier.
    """

    def __init__(self):
        """
        Initialize the BuenbitApiHandle.

        This method initializes the BuenbitApiHandle by creating an instance of
        BuenbitApiService for making API requests.
        """
        self.buenbit_service = BuenbitApiService()

    def handle(self, market_identifier: str) -> Dict[str, Union[int, float]]:
        """
        Handle the Buenbit API response.

        Args:
            market_identifier (str): The identifier for the market data.

        Returns:
            dict: A dictionary containing timestamp and price data.

        Raises:
            requests.exceptions.RequestException: If there's a
            problem with the API request.

            KeyError: If the response data does not contain the
            expected structure.
        """
        data = self.buenbit_service.get()
        try:
            btc_ars_data = data['object'][market_identifier]

            ticker_data = {
                'timestamp': int(datetime.now().timestamp()),
                'price': float(btc_ars_data['selling_price'])
            }
        except KeyError as error:
            raise KeyError(f"Unexpected response structure: {error}")

        return ticker_data
