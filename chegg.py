import json

import requests

from notifications import TelegramBot
from utils import log


class Chegg:
    """
    A class that automates the process of answering ques on chegg and skip the question which are not good to answer.
    """
    URL = "https://www.chegg.com/expert-bff/graphql"
    HEADERS = {
        'authority': 'www.chegg.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'cookie': None,
        'origin': 'https://expert.chegg.com',
        'referer': 'https://expert.chegg.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'tnc-version': 'v2',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1'
    }

    FETCH_PAYLOAD = json.dumps({
        "operationName": None,
        "variables": {},
        "query": "{\n  getQuestion {\n    id\n    uuid\n    expertId\n    subjectName\n    groupId\n    bonusAnswering\n    body\n    questionAssignTime\n    bonusCount\n    answerStartTime\n    isAnswerStarted\n    routingType\n    probability\n    granularGroups {\n      id\n      name\n      __typename\n    }\n    isStructuredAnsweredEnable\n    questionGeoDetailTags {\n      id\n      experimentId\n      countryName\n      countryCode\n      languages\n      __typename\n    }\n    hasImage\n    __typename\n  }\n  getExpertStats {\n    dashboardData {\n      day {\n        answered\n        skipped\n        __typename\n      }\n      month {\n        answered\n        skipped\n        __typename\n      }\n      week {\n        answered\n        skipped\n        __typename\n      }\n      __typename\n    }\n    cfScores {\n      currentDayScore\n      currentWeekScore\n      currentMonthScore\n      __typename\n    }\n    __typename\n  }\n  getSubjectList {\n    id\n    name\n    __typename\n  }\n  getCurrentTime\n}\n"
    })
    SKIP_PAYLOAD = {
        "operationName": None,
        "variables": {
            "questionId": '',
            "flag": "01",
            "skipPage": "D",
            "comment": "",
            "isStructuredQnA": False
        },
        "query": "mutation ($questionId: Int!, $flag: String!, $skipPage: String!, $comment: String, $isStructuredQnA: Boolean) {\n  skipQuestion(questionId: $questionId, flag: $flag, skipPage: $skipPage, comments: $comment, isStructuredQnA: $isStructuredQnA)\n}\n"
    }
    TRANSCRIPT_PAYLOAD = {
    "operationName": "getContentTranscription",
    "variables": {
        "contentUuid": "",
        "contentType": "QUESTION",
        "katex": True
    },
    "query": "query getContentTranscription($contentUuid: String!, $contentType: String!, $katex: Boolean) {\n  getContentTranscription(contentUuid: $contentUuid, contentType: $contentType, katex: $katex) {\n    contentUuid\n    contentType\n    text\n    __typename\n  }\n}\n"
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
        self.has_images = False
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

    def create_transcript_payload(self):
        log(f'Creating transcript payload for {self.question_uuid}')
        payload = Chegg.TRANSCRIPT_PAYLOAD
        payload["variables"]["contentUuid"] = self.question_uuid
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
        ques_obj = res_data['data']['getQuestion']
        if ques_obj:
            self.question = ques_obj
            self.question_id = ques_obj['id']
            self.question_uuid = ques_obj['uuid']
            self.question_body = ques_obj['body']
            self.has_images = ques_obj['hasImage']
        return ques_obj

    def fetch_transcript(self):
        '''
            # Fetch the question images text i.e transcript
            # Returns string
            # else returns None
            # or Raise Exception
        '''
        log(f'Fetching the transcript')
        payload = self.create_transcript_payload()
        response = requests.request(
            "POST", Chegg.URL, headers=self.headers, data=payload, timeout=Chegg.TIMEOUT_FOR_REQUESTS)
        res_data = json.loads(response.text)
        return res_data['data']['getContentTranscription']['text']

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
