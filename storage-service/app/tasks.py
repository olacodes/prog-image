import re
import os
import time
import boto3
import shutil
import environ
import requests

from PIL import Image
from io import BytesIO

from config.celery_app import app
from app.utils import remove_file_dir, list_files

env = environ.Env()
SUPPORTED_FORMATS = ['png', 'jpeg', 'webp']


@app.task(name='format_converter')
def format_converter():
    files = list_files(env('TMP_IMG'))

    for file in files:
        filename = file.split('.')[0]
        file_dir = f'tmp/img/{filename}'
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)

        for format in SUPPORTED_FORMATS:
            image = Image.open(f'tmp/files/{file}')
            image = image.convert('RGB')
            image = image.save(f'tmp/img/{filename}/{filename}.{format}')


@app.task(name='url_format_converter')
def url_format_converter(urls):
    for url in urls:
        response = requests.get(url)
        filename = re.sub('[^A-Za-z0-9]+', '', response.url)
        file_dir = f'tmp/img/{filename}'
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)

        for format in SUPPORTED_FORMATS:
            image = Image.open(BytesIO(response.content))
            image = image.convert('RGB')
            image = image.save(f'tmp/img/{filename}/{filename}.{format}')


@app.task(name='background_upload')
def upload_file_s3(link_p, bucket):
    file_paths = list_files('tmp/img')
    # wait for file creation
    if len(file_paths) == 0:
        time.sleep(10)
    file_paths = list_files('tmp/img')
    s3 = boto3.resource('s3')
    for file_path in file_paths:
        file_upload_response = s3.meta.client.upload_file(
            f'tmp/img/{file_path}', bucket, Key=file_path)


@app.task(name='delete_tmp')
def delete_tmp_dir(dirs):
    # wait 1 minutes before remove
    time.sleep(60)
    for dir in dirs:
        remove_file_dir(dir)
