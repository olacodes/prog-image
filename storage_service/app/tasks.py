from config.celery_app import app
from storage_service.app.utils import Utils
from storage_service.s3.s3_service import S3Service


@app.task(name='format_converter')
def format_converter(filepath):
    return Utils.convert(filepath)


@app.task(name='upload_files')
def upload_files_s3_celery(files):
    return S3Service.upload_file_s3(files)
