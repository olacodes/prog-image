import unittest

import environ

from storage_service.validation import FileValidation

env = environ.Env()
TMP_TEST_FILES = env(
    'TMP_TEST_FILES', default="storage_service/tests/test_files")


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.file_validation = FileValidation()
        self.img_file = f"{TMP_TEST_FILES}/test.png"

    def test_validate_is_valid_image(self):
        is_valid = self.file_validation.validate(self.img_file)
        self.assertTrue(is_valid)

    def test_validate_is_invalid_image(self):
        is_valid = self.file_validation.validate(self.img_file)
        self.assertTrue(is_valid)

    def test_get_file_format(self):
        file_format = self.file_validation.get_file_format(self.img_file)
        self.assertEqual(file_format, 'png')

    def test_is_supported_file_format(self):
        file_format = self.file_validation.get_file_format(self.img_file)
        is_supported_format = self.file_validation.is_supported_format(file_format)
        self.assertTrue(is_supported_format)

    def tearDown(self):
        self.file_validation = None
