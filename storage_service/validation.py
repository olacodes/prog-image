from io import BytesIO

from PIL import Image

from storage_service.global_variables import SUPPORTED_FORMATS
from storage_service.logger import Logger

logger = Logger(__name__)


class FileValidation:

    log = logger.log()

    @classmethod
    def validate(cls, filepath, is_file=True):
        file_format = cls.get_file_format(filepath, is_file=is_file)
        return cls.is_supported_format(file_format)

    @classmethod
    def get_file_format(cls, file, is_file=True):
        try:
            with Image.open(file) if is_file else \
                    Image.open(BytesIO(file)) as fd:
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
