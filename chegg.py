import json

import requests

from notifications import TelegramBot
from utils import log


class Chegg:
    """
    A class that automates the process of answering ques on chegg and skip the question which are not good to answer.
    """
    URL = "https://gateway.chegg.com/nestor-graph/graphql"
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

    def __init__(self, headers={}, keywords=[], parse_images=False):
        self.question = None
        self.question_id = None
        self.question_body = None
        self.keywords = keywords
        self.headers = Chegg.get_headers(headers)
        self.keywords = keywords
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
        log(f'Creating skip payload for {self.question_id}')
        payload = Chegg.SKIP_PAYLOAD
        payload["variables"]["questionId"] = self.question_id
        return json.dumps(payload)

    def fetch_question(self):
        '''
            # Fetch the lastest question in the queue
            # Returns dict with question_id, body etc if ques is present
            # else returns None
            # or Raise Exception
        '''
        log(f'Fetching the ques')
        response = requests.request(
            "POST", Chegg.URL, headers=self.headers, data=Chegg.FETCH_PAYLOAD, timeout=Chegg.TIMEOUT_FOR_REQUESTS)
        if response.status_code == 401:
            log("Unauthorised!! Cookie expired. PLease give a new cookie.")
            exit()
        res_data = json.loads(response.text)
        log(f'HTTP Response {response.status_code}')
        ques_obj = res_data['data']['nextQuestionAnsweringAssignment']['question']
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
        Skip the question with current question_id
        '''
        log(f'Skipping the question')
        payload = self.create_skip_payload()
        res = requests.request(
            "POST", Chegg.URL, headers=Chegg.HEADERS, data=payload, timeout=Chegg.TIMEOUT_FOR_REQUESTS)

    def answer_question(self):
        log(f"Hurray!! You got a suitable question to answer ")
        message = "Hurray!! You got a suitable question to answer " + self.question_body
        self.notify.send_notificaion(
            repr(message))

    def __repr__(self) -> str:
        return self.__dict__
