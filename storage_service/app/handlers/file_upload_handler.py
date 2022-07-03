import uuid
import shutil
import environ
import filetype
import boto3
import botocore

from typing import List
from fastapi import File
from PIL import Image

from storage_service.logger import Logger
from storage_service.app.utils import list_files, generate_id
from storage_service.validation import FileValidation, ImageValidation
from storage_service.app.tasks import format_converter, delete_tmp_dir, upload_file_s3
from storage_service.global_variables import SUPPORTED_FORMATS


env = environ.Env()
logger = Logger(__name__)
AWS_S3_BUCKET = env('AWS_S3_BUCKET', default=None)
AWS_S3_BASE_URL = env(
    'AWS_S3_BASE_URL', default='https://sodiqcodesbucket.s3.amazonaws.com')


class FileUploadHandler:
    def __init__(self, files: List[File]):
        self.files = files
        self.log = logger.log()

    async def handle(self):
        filepaths = await self.file_writer(env('TMP_FILES'))
        valid_filepaths = filepaths.get('valid_filepaths', [])

        # Check if their is valid file written
        if len(valid_filepaths) == 0:
            return {"error": "No valid file uploaded"}

        # Duplicate the files
        multiple_formats = await self.duplicate_format(valid_filepaths)
        if not multiple_formats:
            return {'error': 'file cannot be duplicated in different formats'}

        filepaths_list = [
            filepath for filepaths in multiple_formats for filepath in filepaths]

        # Upload files to S3
        uploaded_file = await self.upload_files_s3(filepaths_list)

        return uploaded_file

    # I/O bound operation: writing to tmp file
    async def file_writer(self, write_dir):
        valid_filepaths = []
        invalid_files = []
        for file in self.files:
            raw_file = file.file
            if ImageValidation.validate(raw_file):
                filename = generate_id()
                location = f"{write_dir}/{filename}{file.filename}"
                filepath = await self.write_file(raw_file, location)
                valid_filepaths.append(filepath)
            else:
                invalid_files.append(file.filename)
        return {"valid_filepaths": valid_filepaths, "invalid_files": invalid_files}

    async def write_file(self, file, location):
        with Image.open(file) as fd:
            fd.save(location)
            return location

    async def duplicate_format(self, filepaths):
        new_filepaths = []
        for filepath in filepaths:
            fpath = await self.convert(filepath)
            new_filepaths.append(fpath)
        return new_filepaths

    async def upload_files_s3(self, filepaths):
        uploaded_file = []
        try:
            s3 = boto3.resource('s3')
            for filepath in filepaths:
                filename = filepath.split('/')[-1]
                key = f'storage_service/{filename}'
                s3.meta.client.upload_file(
                    filepath, AWS_S3_BUCKET, Key=key)
                uploaded_file.append(f"{AWS_S3_BASE_URL}/{key}")
            return uploaded_file
        except Exception as e:
            self.log.error(e)
            return True

    # CPU Bound Operation
    async def convert(self, filepath):
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
                print(e)
                self.log.error(e)
        return converted_files

    # def chain_convert_s3_del(self):
    #     celery_chain = format_converter.apply_async(
    #         (env('TMP_FILES'), env('TMP_IMG')), link=upload_file_s3.s(env('AWS_S3_BUCKET')))
