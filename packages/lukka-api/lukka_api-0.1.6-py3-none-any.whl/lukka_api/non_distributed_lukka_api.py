import os
import sys
import socket
import requests
import multiprocessing
import time
import base64

import pandas as pd

from dotenv import load_dotenv
from multiprocessing import Pool
from pandas.tseries.offsets import BDay


class LukkaAPIClient:
    def __init__(self):
        self.url = "https://sso.lukka.tech/oauth2/aus1imo2fqcx5Ik4Q0h8/v1/token"
        self.session = requests.Session()  # Use a session for connection pooling

    def get_api_key(self) -> str:
        """
        Retrieve API key from Lukka using credentials from .env file.

        Returns:
            str: API key for subsequent requests

        Raises:
            ValueError: If credentials are missing or invalid
            requests.RequestException: If API request fails
        """
        # Load environment variables from .env file
        load_dotenv()

        username = os.getenv("LUKKA_USERNAME")
        password = os.getenv("LUKKA_PASSWORD")

        # Validate credentials exist
        if not username or not password:
            raise ValueError(
                "Missing credentials. Please ensure LUKKA_USERNAME and "
                "LUKKA_PASSWORD are set in your .env file"
            )

        try:
            credentials = f"{username}:{password}"
            encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

            payload = "grant_type=client_credentials&scope=pricing"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Cache-Control": "no-cache",
                "Accept": "application/json",
                "Authorization": f"Basic {encoded_credentials}",
            }
            # Make API request with timeout and proper error handling
            response = requests.request("POST", self.url, data=payload, headers=headers, timeout=30)

            # Check for successful response
            response.raise_for_status()

            # Parse JSON response to extract access token
            try:
                response_data = response.json()
                access_token = response_data.get("access_token")

                if not access_token:
                    raise ValueError("No access token received from OAuth2 response")

                # Log success without exposing the actual token
                print(
                    f"POST {self.url} {response.status_code} {response.reason} - OAuth2 token retrieved successfully"
                )

                return access_token
            except ValueError as json_error:
                raise requests.RequestException(f"Invalid JSON response: {json_error}")

        except requests.exceptions.Timeout:
            raise requests.RequestException("Request timed out while retrieving OAuth2 token")
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error {response.status_code}"
            try:
                error_detail = response.json().get("error_description", response.text)
                error_msg += f": {error_detail}"
            except:
                error_msg += f": {response.text}"
            raise requests.RequestException(error_msg)
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"Failed to retrieve OAuth2 token: {e}")


if __name__ == "__main__":
    client = LukkaAPIClient()
    try:
        token = client.get_api_key()
        print("Token retrieved successfully")
    except Exception as e:
        print(f"Error: {e}")
