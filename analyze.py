import re

from bs4 import BeautifulSoup

from ocr import Ocr
from utils import log


class Analyze:
    def __init__(self, question, keywords, parse_images=False,transcript = "") -> None:
        self.question = question
        self.keywords = keywords
        self.parse_images = parse_images
        self.transcript = transcript

    def check_keyword_present(self, text):
        if any(word in text for word in self.keywords):
            return True
        return False

    def get_question_body(self) :
        '''
        Fetch question body from the ques dict
        Parse the raw text and image urls from html content
        Returns the image_urls and raw_text
        '''
        log(f'Getting question body from api response')
        body = self.question['body']
        image_urls = re.findall(r'(https?://\S+)', body)
        image_urls = [url.strip('""') for url in image_urls]
        clean_text = ' '.join(BeautifulSoup(
            body, "html.parser").stripped_strings).lower()
        return image_urls, clean_text

    def is_ques_good(self):
        '''
        Checks if question is answerable
        Return Boolean Value
        '''
        log(f'Checking if question is suitable to answer.')
        image_urls, ques_text = self.get_question_body()

        ques_text = ques_text + ' ' + self.transcript
        # Prior Chegg doesn't have functionality of transcripts
        # so I made custom handling of image to text
        if self.parse_images:
            ocr = Ocr(urls=image_urls)
            images_text = ocr.analyze_images()
            ques_text = ques_text + ' ' + images_text
        if any([self.check_keyword_present(ques_text)]):
            return True
        return False
