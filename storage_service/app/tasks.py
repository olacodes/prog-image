import re
import os
import time
import boto3
import environ
import requests
from PIL import Image
from io import BytesIO

from config.celery_app import app
from storage_service.app.utils import remove_file_dir, list_files, create_dir, convert

env = environ.Env()
SUPPORTED_FORMATS = ['png', 'jpeg', 'webp']


@app.task(name='format_converter')
def format_converter():
    files = list_files(env('TMP_FILES'))
    for file in files:
        filename = file.split('.')[0]
        file_dir = f'tmp/img/{filename}'
        create_dir(file_dir)
        for format in SUPPORTED_FORMATS:
            image = Image.open(f'tmp/files/{file}')
            image = image.convert('RGB')
            image = image.save(f'tmp/img/{filename}/{filename}.{format}')


@app.task(name='url_format_converter')
def url_format_converter( urls):
    for url in urls:
        try:
            response = requests.get(url, stream=True)
            fname = url.split("/")[-1]
            fname = fname.split(".")[0]
            filename = re.sub('[^A-Za-z0-9]+', '', fname)
            file_dir = f'tmp/img/{filename}'
            file = response.content
            create_dir(file_dir)
            for format in SUPPORTED_FORMATS:
                image = Image.open(BytesIO(file))
                image = image.convert('RGB')
                image = image.save(f'tmp/img/{filename}/{filename}.{format}')
        except Exception as e:
            print(e)
            # Todo: Write the exception to log file
            # write to log
            return True


@app.task(name='background_upload')
def upload_file_s3(link_p, bucket):
    try:
        time.sleep(10)
        file_paths = list_files('tmp/img')
        # wait for file creation
        if len(file_paths) == 0:
            time.sleep(10)
        file_paths = list_files('tmp/img')
        s3 = boto3.resource('s3')
        for file_path in file_paths:
            file_upload_response = s3.meta.client.upload_file(
                f'tmp/img/{file_path}', bucket, Key=file_path)
    except Exception as e:
        print(e)
        # Todo: Write the exception to log file
        # write to log
        return True


@app.task(name='delete_tmp')
def delete_tmp_dir(dirs):
    # wait 1 minutes before remove
    time.sleep(60)
    for dir in dirs:
        remove_file_dir(dir)
