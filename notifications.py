import requests
import yaml
from  utils import log

with open("config.yaml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)

class TelegramBot:
    '''
    Send message to telegram chat
    '''
    TIMEOUT_FOR_REQUESTS = (10, 20)
    TOKEN = config.get('telegram').get('token')
    CHAT_ID = config.get('telegram').get('chat_id')

    def __init__(self):
        self.api_url = f'https://api.telegram.org/bot{TelegramBot.TOKEN}/sendMessage?chat_id={TelegramBot.CHAT_ID}&text='

    def send_notificaion(self, message):
        '''
        Send message to the group  in Telegram.
        '''
        try:
            message = repr(message)
            url = self.api_url+message
            requests.get(url, timeout=TelegramBot.TIMEOUT_FOR_REQUESTS)
        except:
            log("No telegram notification was sent as chat_id or token is absent in config.yaml")
