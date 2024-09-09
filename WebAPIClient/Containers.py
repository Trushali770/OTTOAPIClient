import logging
import os
import sys
import requests
from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
import json

# Add parent directory to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Logger.logger_setup import setup_logger


def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

config_path = os.path.join(os.path.dirname(__file__), 'apiclient_config.json')
config = load_config(config_path)

logger = setup_logger(
    __name__,
    log_dir=config.get('log_dir'),
    max_bytes=config.get('max_bytes'),
    backup_count=config.get('backup_count'),
    level=logging.getLevelName(config.get('log_level', 'INFO'))
)
class Containers:
    """_summary_

    Returns:
        _type_: _description_
    """
    BASE_URL = config.get('base_url')

    def log_request_response(self, method, url, response):
        """_summary_

        Args:
            method (_type_): _description_
            url (_type_): _description_
            response (_type_): _description_
        """
        logger.info("---------------")
        logger.info(f"Request method: {method}")
        logger.info(f"Request URL: {url}")
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response content: {response.content}")

    def getContainer(self, endpoint, params=None):
        """_summary_

        Args:
            endpoint (_type_): _description_
            params (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.log_request_response("GET", url, response)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching posts: {e}")
            raise

    def createContainer(self, endpoint, payload):
        """_summary_

        Args:
            endpoint (_type_): _description_
            payload (_type_): _description_

        Returns:
            _type_: _description_
        """
        url = f'{self.BASE_URL}{endpoint}'
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            self.log_request_response("POST", url, response)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating post: {e}")
            raise
        
    def deleteContainer(self, endpoint, payload):
        """_summary_

        Args:
            endpoint (_type_): _description_
            payload (_type_): _description_
        """
        url = f'{self.BASE_URL}{endpoint}'
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            self.log_request_response("POST", url, response)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating post: {e}")
            raise
        
    def updateContainer(self, endpoint, payload):
        """_summary_

        Args:
            endpoint (_type_): _description_
            payload (_type_): _description_
        """
        url = f'{self.BASE_URL}{endpoint}'
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            self.log_request_response("POST", url, response)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating post: {e}")
            raise

    