import json
import os
import sys
import requests
import yaml

from notifications import TelegramBot
from utils import log

config = ''
with open("config.yaml", "r", encoding="utf-8") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)

class Chegg:
    """
    A class that automates the process of answering questions on chegg and skips the questions which are not good to answer.
    """
    URL = "https://gateway.chegg.com/nestor-graph/graphql"
    DASHBOARD_URL = "https://expert.chegg.com/qna/authoring/answer"
    HEADERS = {
        'authority': 'gateway.chegg.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9',
        'apollographql-client-name': 'chegg-web-producers',
        'content-type': 'application/json',
        'cookie': None,
        'origin': 'https://expert.chegg.com',
        'referer': 'https://expert.chegg.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }

    FETCH_PAYLOAD = json.dumps({
        "operationName": "NextQuestionAnsweringAssignment",
        "variables": {},
        "query": "query NextQuestionAnsweringAssignment {\n  nextQuestionAnsweringAssignment {\n    question {\n      body\n      id\n      uuid\n      subject {\n        id\n        name\n        subjectGroup {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      imageTranscriptionText\n      lastAnswerUuid\n      __typename\n    }\n    langTranslation {\n      body\n      translationLanguage\n      __typename\n    }\n    questionGeoLocation {\n      countryCode\n      countryName\n      languages\n      __typename\n    }\n    questionRoutingDetails {\n      answeringStartTime\n      bonusCount\n      bonusTimeAllocationEnabled\n      checkAnswerStructureEnabled\n      hasAnsweringStarted\n      questionAssignTime\n      questionSolvingProbability\n      routingType\n      allocationExperimentId\n      questionQualityFactor\n      __typename\n    }\n    __typename\n  }\n}"
    })
    SKIP_PAYLOAD = {
        "operationName": "SkipQuestionAssignment",
        "variables": {
            "questionId": '',
            "skipPageFlow": "DECISION",
            "skipPrimaryReason": {
                "noKnowledge": True
            }
        },
        "query": "mutation SkipQuestionAssignment($questionId: Long!, $skipPageFlow: QnaCurrentPageFlow!, $skipPrimaryReason: QuestionSkipPrimaryReasons, $newSkipReason: QuestionNewSkipReasons) {\n  skipQuestionAssignment(\n    questionId: $questionId\n    skipPageFlow: $skipPageFlow\n    skipPrimaryReason: $skipPrimaryReason\n    newSkipReason: $newSkipReason\n  ) {\n    message\n    questionId\n    __typename\n  }\n}"
    }
    TIMEOUT_FOR_REQUESTS = (10, 20)

    def __init__(self, headers=None, keywords=None, parse_images=False):
        self.question = None
        self.question_id = None
        self.question_body = None
        self.keywords = keywords or []
        self.headers = Chegg.get_headers(headers)
        self.parse_images = parse_images
        self.notify = TelegramBot()
        self.question_uuid = None
        self.transcript = ""

    @staticmethod
    def get_headers(headers):
        '''
        Add fields to headers
        '''
        global_headers = Chegg.HEADERS
        global_headers.update(headers)
        return global_headers

    def create_skip_payload(self):
        """
        Create the skip payload for the current question.
        """
        log('Creating skip payload for {}'.format(self.question_id))
        payload = Chegg.SKIP_PAYLOAD
        payload["variables"]["questionId"] = self.question_id
        return json.dumps(payload)

    def fetch_question(self):
        '''
        Fetch the latest question in the queue.
        Returns dict with question_id, body, etc. if question is present.
        Otherwise, returns None or raises an Exception.
        '''
        log('Fetching the question')
        response = requests.request(
            "POST", Chegg.URL, headers=self.headers, data=Chegg.FETCH_PAYLOAD, timeout=Chegg.TIMEOUT_FOR_REQUESTS)
        res_data = json.loads(response.text)
        if res_data.get('errors') is not None:
            log(res_data['errors'][0]['message'])
            log("Note: If you are getting unauthorized error then please give a new cookie.")
            sys.exit()
        log('HTTP Response {}'.format(response.status_code))
        ques_obj = res_data['data']['nextQuestionAnsweringAssignment']['question'] if res_data['data'] is not None else None
        if ques_obj:
            self.question = ques_obj
            self.question_id = ques_obj['id']
            self.question_uuid = ques_obj['uuid']
            self.question_body = ques_obj['body']
            if ques_obj['imageTranscriptionText'] is not None:
                self.transcript = ques_obj['imageTranscriptionText']
        return ques_obj

    def skip_question(self):
        '''
        Skip the question with the current question_id.
        '''
        log('Skipping the question')
        payload = self.create_skip_payload()
        requests.request(
            "POST", Chegg.URL, headers=Chegg.HEADERS, data=payload, timeout=Chegg.TIMEOUT_FOR_REQUESTS)

    def answer_question(self):
        """
        Answer the current question.
        """
        log("Hurray!! You got a suitable question to answer -> {}".format(Chegg.DASHBOARD_URL))
        # Play the alert sound on terminal
        os.system("afplay {}".format(config.get('notification_sound_path')))
        message = "Hurray!! You got a suitable question to answer " + self.question_body
        self.notify.send_notification(
            repr(message))

    def __repr__(self):
        return str(self.__dict__)
