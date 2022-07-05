import contextlib
import os
import unittest

import environ
from celery import Celery

from storage_service.global_variables import SUPPORTED_FORMATS

env = environ.Env()

BROKER_URL = env('REDIS_URL', default="redis://redis:6379/0")
REDIS = env('REDIS_URL', default="redis://redis:6379/0")

app = Celery('test', broker=BROKER_URL, backend=REDIS)


TMP_TEST_FILES = env(
    'TMP_TEST_FILES', default="storage_service/tests/test_files")


class TestCeleryTasks(unittest.TestCase):
    def setUp(self):

        self.task = app.send_task('format_converter', args=[f"{TMP_TEST_FILES}/test.png"])
        self.result = self.task.get()

    def test_format_converter_state(self):
        self.assertEqual(self.task.state, 'SUCCESS')

    def test_format_converter_result_success(self):
        self.assertEqual(type(self.task.result), list)
        self.assertEqual(len(self.task.result), len(SUPPORTED_FORMATS))

    def tearDown(self):
        with contextlib.suppress(ValueError):
            delete_created_file_formats = SUPPORTED_FORMATS[:]
            delete_created_file_formats.remove('png')
            for format in delete_created_file_formats:
                if os.path.exists(f"{TMP_TEST_FILES}/test.{format}"):
                    os.remove(f"{TMP_TEST_FILES}/test.{format}")
