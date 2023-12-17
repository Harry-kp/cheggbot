"""
This module contains the TelegramBot class for sending notifications to a
Telegram chat via the Telegram API. Configuration data is loaded from
'config.yaml'.
"""

import requests
import yaml
from utils import log

with open("config.yaml", "r", encoding="utf-8") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)


class TelegramBot:
    '''
    A class for sending messages to a Telegram chat.

    Attributes:
        TIMEOUT_FOR_REQUESTS (tuple): A tuple representing the timeout values for requests.
        TOKEN (str): The token for accessing the Telegram API.
        CHAT_ID (str): The ID of the chat to which messages will be sent.

    Methods:
        __init__(): Initializes the TelegramBot object.
        send_notification(message): Sends a message to the Telegram chat.
    '''

    TIMEOUT_FOR_REQUESTS = (10, 20)
    TOKEN = config.get('telegram').get('token')
    CHAT_ID = config.get('telegram').get('chat_id')

    def __init__(self):
        '''
        Initializes the TelegramBot object.

        The API URL for sending messages is constructed using the TOKEN and CHAT_ID attributes.
        '''
        self.api_url = (
            f'https://api.telegram.org/bot{TelegramBot.TOKEN}/sendMessage'
            f'?chat_id={TelegramBot.CHAT_ID}&text='
        )

    def send_notification(self, message):
        '''
        Sends a message to the group in Telegram.

        Args:
            message (str): The message to be sent.

        Raises:
            Exception: If the chat_id or token is absent in the config.yaml file.

        Returns:
            None
        '''
        try:
            message = repr(message)
            url = self.api_url + message
            requests.get(url, timeout=TelegramBot.TIMEOUT_FOR_REQUESTS)
        except Exception:
            log("No telegram notification was sent as chat_id or token is absent in config.yaml")
