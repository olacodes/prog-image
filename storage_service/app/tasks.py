from PIL import Image

from config.celery_app import app
from storage_service.global_variables import SUPPORTED_FORMATS
from storage_service.logger import Logger

logger = Logger(__name__)
log = logger.log()


@app.task(name='format_converter')
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
