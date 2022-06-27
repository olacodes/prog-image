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

TMP_FILES = env('TMP_FILES')
TMP_IMG = env('TMP_IMG')

@app.task(name='format_converter')
def format_converter(read_dir, write_dir):
    try:
        files = list_files(read_dir)
        for file in files:
            filename = file.split('.')[0]
            file_dir = f'{write_dir}/{filename}'
            create_dir(file_dir)
            for format in SUPPORTED_FORMATS:
                image = Image.open(f'{read_dir}/{file}')
                image = image.convert('RGB')
                image = image.save(f'{write_dir}/{filename}/{filename}.{format}')
        return 'Done'
    except Exception as e:
        print(e)
        return False


@app.task(name='url_format_converter')
def url_format_converter(urls, dir):
    for url in urls:
        try:
            response = requests.get(url, stream=True)
            fname = url.split("/")[-1]
            fname = fname.split(".")[0]
            filename = re.sub('[^A-Za-z0-9]+', '', fname)
            file_dir = f'{dir}/{filename}'
            file = response.content
            create_dir(file_dir)
            for format in SUPPORTED_FORMATS:
                image = Image.open(BytesIO(file))
                image = image.convert('RGB')
                image = image.save(f'{dir}/{filename}/{filename}.{format}')
            return "Done"
        except Exception as e:
            print(e)
            # Todo: Write the exception to log file
            # write to log
            return False


@app.task(name='upload_files_s3')
def upload_file_s3(link_p, bucket):
    try:
        time.sleep(10)
        file_paths = list_files(TMP_IMG)
        # wait for file creation
        if len(file_paths) == 0:
            time.sleep(10)
        file_paths = list_files(TMP_IMG)
        s3 = boto3.resource('s3')
        for file_path in file_paths:
            file_upload_response = s3.meta.client.upload_file(
                f'{TMP_IMG}/{file_path}', bucket, Key=file_path)
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
