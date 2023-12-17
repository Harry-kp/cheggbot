"""
Image to Text Conversion Service
"""

# No longer used. As chegg has started giving transcript of the image in the response.

import json
from concurrent.futures import ThreadPoolExecutor

import requests

from utils import log

IMAGE_TO_TEXT_API_URL = None
IMAGE_TO_TEXT_API_KEY = None
IMAGE_TO_TEXT_API_PAYLOAD = {'language': 'eng',
                             'isOverlayRequired': 'false',
                             'url': '',
                             'iscreatesearchablepdf': 'false',
                             'issearchablepdfhidetextlayer': 'false'
                             }

IMAGE_TO_TEXT_API_HEADERS = {
    'apikey': ''
}


class Ocr:
    """
    Convert the image at given link into text.
    """

    TIMEOUT_FOR_REQUESTS = (10, 20)

    def __init__(self, urls=None):
        """
        Initialize the Ocr class with a list of URLs.
        """
        if urls is None:
            urls = []
        self.urls = urls

    @staticmethod
    def parse_image_to_text_response(res_data):
        """
        Parse the response data from the image to text API.
        """
        log('Parsing image to text api response.')
        res_data = json.loads(res_data)
        return res_data["ParsedResults"][0]["ParsedText"]

    @staticmethod
    def image_to_text(url):
        """
        Convert the image at the given URL to text.
        """
        log(f'Converting image to text with url -> {url}')
        payload = IMAGE_TO_TEXT_API_PAYLOAD
        payload['url'] = url
        headers = IMAGE_TO_TEXT_API_HEADERS
        headers['apikey'] = IMAGE_TO_TEXT_API_KEY
        response = requests.request("POST", IMAGE_TO_TEXT_API_URL, headers=headers,
                                    data=payload, timeout=Ocr.TIMEOUT_FOR_REQUESTS)
        return Ocr.parse_image_to_text_response(response.text)

    def analyze_images(self):
        """
        Analyze the images and return the combined text.
        """
        with ThreadPoolExecutor() as exe:
            results = exe.map(self.image_to_text, self.urls)
            return ' '.join(results).lower()
