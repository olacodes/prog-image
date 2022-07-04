
import environ
from celery import group

from storage_service.app.tasks import format_converter, upload_files_s3_celery
from storage_service.app.utils import Utils
from storage_service.validation import FileValidation

env = environ.Env()
AWS_S3_BUCKET = env('AWS_S3_BUCKET', default=None)
AWS_S3_BASE_URL = env(
    'AWS_S3_BASE_URL', default='https://sodiqcodesbucket.s3.amazonaws.com')
AWS_S3_STORAGE_KEY = env('AWS_S3_STORAGE_KEY', default='storage_service')


class Handler:

    # CPU Bound operation [handle by celery]
    @classmethod
    async def generate_multiple_formats(cls, filepaths):
        multiple_formats = group(format_converter.s(filepath) for filepath in filepaths)()
        multiple_formats = multiple_formats.get()
        return multiple_formats

    @classmethod
    async def upload_files_s3(cls, filepaths):
        uploaded_files = group(upload_files_s3_celery.s(filepath) for filepath in filepaths)()
        uploaded_files = uploaded_files.get()
        return uploaded_files

    # I/O Bound operation [handle by async]
    @classmethod
    async def file_writer(cls, files, write_dir, is_file=True):
        valid_files = []
        invalid_files = []
        for file in files:
            file = file.file if is_file else await Utils.request_url(file)
            if bool(file and FileValidation.validate(file, is_file=is_file)):
                filename = Utils.generate_id()
                file_ext = FileValidation.get_file_format(file, is_file=is_file)
                location = f"{write_dir}/{filename}.{file_ext}"
                filepath = await Utils.save_file(file, location, is_file=is_file)
                valid_files.append(filepath)
            else:
                invalid_files.append(file)
        return {'valid_files': valid_files, 'invalid_files': invalid_files}
