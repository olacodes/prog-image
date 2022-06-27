

import unittest
import environ

from celery import Celery
from time import sleep
from storage_service.app.tasks import url_format_converter
from unittest.mock import patch

env = environ.Env()

BROKER_URL = env('REDIS_URL', default="redis://redis:6379/0")
REDIS = env('REDIS_URL', default="redis://redis:6379/0")

app = Celery('test', broker=BROKER_URL, backend=REDIS)

TMP_TEST_FILES = env(
    'TMP_TEST_FILES', default="storage_service/tmp/test_files")


class TestFormatConverter(unittest.TestCase):
    def setUp(self):

        self.task = app.send_task('format_converter', args=[
                                  "storage_service/app/tests/file_read", TMP_TEST_FILES])

        self.result = self.task.get()

        self.task2 = app.send_task(
            'url_format_converter',
            args=['/hello', TMP_TEST_FILES]
        )
        self.result2 = self.task2.get()

    def test_format_converter_state(self):
        self.assertEqual(self.task.state, 'SUCCESS')

    def test_format_converter_result_success(self):
        self.assertEqual(self.task.result, 'Done')

    def test_url_format_converter_result_failed(self):
        self.assertEqual(self.task2.result, False)
