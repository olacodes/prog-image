from typing import List

import environ
from fastapi import File

from storage_service.app.handlers.handler import Handler
from storage_service.logger import Logger

env = environ.Env()
logger = Logger(__name__)
AWS_S3_BUCKET = env('AWS_S3_BUCKET', default=None)
AWS_S3_BASE_URL = env(
    'AWS_S3_BASE_URL', default='https://sodiqcodesbucket.s3.amazonaws.com')


class FileUploadHandler(Handler):
    def __init__(self, files: List[File]):
        self.files = files
        self.log = logger.log()

    async def handle(self):
        filepaths = await self.file_writer(self.files, env('TMP_FILES'))
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
