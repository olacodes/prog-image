import filetype
from PIL import Image
from typing import BinaryIO, Union
from io import BytesIO

from storage_service.global_variables import SUPPORTED_FORMATS
from storage_service.logger import Logger


logger = Logger(__name__)


class FileValidation:

    def __init__(self, file):
        self.file_info = filetype.guess(file)
        self.log = logger.log()

    def validate(self):
        return bool((self.is_valid_image_type()) & (self.is_supported_ext()))

    def is_valid_image_type(self):
        try:
            mime_type = self.file_info.mime
            if mime_type.split('/')[0] != 'image':
                self.log.error('Invalid image file')
                return False
            return True
        except (AttributeError, TypeError) as e:
            self.log.error(e)
            return False

    def get_extension(self):
        try:
            return self.file_info.extension
        except (AttributeError, TypeError) as e:
            self.log.error(e)
            return False

    def is_supported_ext(self):
        file_ext = self.get_extension()
        return file_ext in SUPPORTED_FORMATS


class ImageValidation:

    log = logger.log()

    @classmethod
    def validate(cls, filepath):
        file_format = cls.get_file_format(filepath)
        return cls.is_supported_format(file_format)

    @classmethod
    def get_file_format(cls, filepath):
        try:
            with Image.open(filepath) as fd:
                return str(fd.format).lower()
        except OSError as e:
            cls.log.error(e)
            return None

    @classmethod
    def is_supported_format(cls, file_format):
        if file_format in SUPPORTED_FORMATS:
            return True
        cls.log.warning(
            f"Invalid file format, supported formats are {SUPPORTED_FORMATS}")
        return False
