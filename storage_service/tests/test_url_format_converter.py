import unittest
from time import sleep
from unittest.mock import patch

import environ
from celery import Celery

from storage_service.app.tasks import url_format_converter

env = environ.Env()

BROKER_URL = env('REDIS_URL', default="redis://redis:6379/0")
REDIS = env('REDIS_URL', default="redis://redis:6379/0")
TMP_TEST_FILES = env(
    'TMP_TEST_FILES', default="storage_service/tmp/test_files")

app = Celery('test', broker=BROKER_URL, backend=REDIS)


class TestURLFormatConverter(unittest.TestCase):
    def setUp(self):

        self.task = app.send_task(
            'url_format_converter',
            args=[["https://github.com/olacodes/webscraper/raw/main/static/web-scrapper-arch.jpeg"],
                  TMP_TEST_FILES]
        )
        self.result = self.task.get()

        self.task2 = app.send_task(
            'url_format_converter',
            args=[["htt//pfsdfds.cd"], TMP_TEST_FILES]
        )
        self.result2 = self.task2.get()

    def test_url_format_converter_state(self):
        self.assertEqual(self.task.state, 'SUCCESS')
        self.assertEqual(self.task.result, 'Done')

    def test_url_format_converter_failed(self):
        self.assertEqual(self.task2.result, False)
