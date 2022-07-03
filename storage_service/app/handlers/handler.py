from io import BytesIO

import boto3
import environ
import requests
from celery import group
from PIL import Image
from requests.exceptions import RequestException

from storage_service.app.tasks import convert
from storage_service.app.utils import generate_id
from storage_service.logger import Logger
from storage_service.validation import FileValidation

env = environ.Env()
logger = Logger(__name__)
AWS_S3_BUCKET = env('AWS_S3_BUCKET', default=None)
AWS_S3_BASE_URL = env(
    'AWS_S3_BASE_URL', default='https://sodiqcodesbucket.s3.amazonaws.com')
AWS_S3_STORAGE_KEY = env('AWS_S3_STORAGE_KEY', default='storage_service')


class Handler:
    log = logger.log()

    # CPU Bound operation [handle by celery]
    @classmethod
    async def generate_multiple_formats(cls, filepaths):
        multiple_formats = group(convert.s(filepath)
                                 for filepath in filepaths)()
        multiple_formats = multiple_formats.get()
        return multiple_formats

    # I/O Bound operation [handle by async]
    @classmethod
    async def file_writer(cls, files, write_dir, is_file=True):
        valid_files = []
        invalid_files = []
        for file in files:
            file = file.file if is_file else await cls.get_file(file)
            if bool(file and FileValidation.validate(file, is_file=is_file)):
                filename = generate_id()
                file_ext = FileValidation.get_file_format(
                    file, is_file=is_file)
                location = f"{write_dir}/{filename}.{file_ext}"
                filepath = await cls.write_file(file, location, is_file=is_file)
                valid_files.append(filepath)
            else:
                invalid_files.append(file)
        return {'valid_files': valid_files, 'invalid_files': invalid_files}

    @classmethod
    async def write_file(cls, file, location, is_file=True):
        with Image.open(file) if is_file else Image.open(BytesIO(file)) as fd:
            fd.save(location)
            return location

    @classmethod
    async def upload_files_s3(cls, filepaths):
        uploaded_file = []
        try:
            s3 = boto3.resource('s3')
            for filepath in filepaths:
                filename = filepath.split('/')[-1]
                key = f'{AWS_S3_STORAGE_KEY}/{filename}'
                s3.meta.client.upload_file(
                    filepath, AWS_S3_BUCKET, Key=key)
                uploaded_file.append(f"{AWS_S3_BASE_URL}/{key}")
            return uploaded_file
        except Exception as e:
            cls.log.error(e)

    @classmethod
    async def get_file(cls, url):
        try:
            response = requests.get(url, stream=True)
            return response.content
        except RequestException as e:
            cls.log.error(e)
