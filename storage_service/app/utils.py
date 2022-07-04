import random
import string
import uuid
from io import BytesIO

import requests
from PIL import Image
from requests.exceptions import RequestException

from storage_service.global_variables import SUPPORTED_FORMATS
from storage_service.logger import Logger

logger = Logger(__name__)
log = logger.log()


class Utils:
    @staticmethod
    def generate_id():
        random_letter = random.choice(string.ascii_letters)
        uuid_hex = str(uuid.uuid4().hex)
        return f'{random_letter}{uuid_hex}'.lower()

    @staticmethod
    async def save_file(file, location, is_file=True):
        with Image.open(file) if is_file else Image.open(BytesIO(file)) as fd:
            fd.save(location)
            return location

    @staticmethod
    async def request_url(url):
        try:
            response = requests.get(url)
            return response.content
        except RequestException as e:
            log.error(e)

    @staticmethod
    def convert(filepath):
        converted_files = []
        for format in SUPPORTED_FORMATS:
            try:
                image = Image.open(filepath)
                image = image.convert('RGB')
                new_filepath = filepath.split(".")[0]
                new_filepath = f'{new_filepath}.{format}'
                image.save(new_filepath)
                converted_files.append(new_filepath)
            except OSError as e:
                log.error(e)
        return converted_files
