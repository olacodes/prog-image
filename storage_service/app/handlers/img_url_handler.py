import environ

from storage_service.app.handlers.handler import Handler
from storage_service.logger import Logger

env = environ.Env()
logger = Logger(__name__)


class URLImageHandler(Handler):
    # Download the image
    def __init__(self, urls: list):
        self.urls = urls
        self.log = logger.log()

    async def handle(self):
        filepaths = await self.file_writer(
            self.urls, env('TMP_FILES'), is_file=False
        )
        valid_files = filepaths.get('valid_files', [])

        # Check if their is valid file written
        if len(valid_files) == 0:
            return {"error": "No valid file uploaded"}

        # generate different file format
        multiple_formats = await self.generate_multiple_formats(valid_files)
        if not multiple_formats:
            return {'error': 'file cannot be generated in different formats'}

        filepaths_list = [
            filepath for filepaths in multiple_formats for filepath in filepaths]

        # Upload files to S3
        uploaded_file = await self.upload_files_s3(filepaths_list)
        return {'urls': uploaded_file, 'total': len(uploaded_file)}
