import unittest
import environ

from celery import Celery
from time import sleep
from storage_service.app.tasks import url_format_converter
from unittest.mock import patch

env = environ.Env()

BROKER_URL = env('REDIS_URL')
REDIS = env('REDIS_URL')

app = Celery('test', broker=BROKER_URL, backend=REDIS)


class TestURLFormatConverter(unittest.TestCase):
    def setUp(self):

        self.task = app.send_task(
            'url_format_converter', 
            args=[["https://github.com/olacodes/webscraper/raw/main/static/web-scrapper-arch.jpeg"], env('TMP_TEST_FILES')]
        )
        self.result = self.task.get()
        
        self.task2 = app.send_task(
            'url_format_converter', 
            args=[["htt//pfsdfds.cd"], env('TMP_TEST_FILES')]
        )
        self.result2 = self.task2.get()
        
    def test_url_format_converter_state(self):
        self.assertEqual(self.task.state, 'SUCCESS')
        self.assertEqual(self.task.result, 'Done')
        
    def test_url_format_converter_failed(self):
        self.assertEqual(self.task2.result, False)
