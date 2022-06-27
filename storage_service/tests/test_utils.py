import os
import environ
import unittest
from storage_service.app.utils import create_dir, list_files


env = environ.Env()
TMP_TEST_FILES = env(
    'TMP_TEST_FILES', default="storage_service/tmp/test_files")
class TestUtils(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_create_dir(self):
        dir_created = create_dir(f"{TMP_TEST_FILES}/{create_dir}")
        self.assertTrue(os.path.exists(dir_created))
        
    def test_list_files(self):
        files = list_files('storage_service/tests/file_read')
        self.assertEqual(len(files), 1)
