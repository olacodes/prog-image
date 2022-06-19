import os
from os import listdir
from os.path import isfile, join


from config.celery_app import app
from celery import shared_task
from PIL import Image
import time
import glob

from pathlib import Path
import boto3


def list_files(dir):
    cwd = str(Path.cwd())
    my_dirs = list(Path(dir).glob('**'))
    files = []
    for my_dir in my_dirs:
        file_names = glob.glob(os.path.join(my_dir, '**'))
        file_names = [f for f in file_names if not Path(f).is_dir()]

        for file_name in file_names:
            file_name = str(file_name).replace(f'{str(dir)}/', '')
            files.append(file_name)
    return files


@app.task(name="create_task")
def create_task(task_type):
    # time.sleep(int(task_type) * 10)
    return True


SUPPORTED_FORMATS = ['png', 'jpeg', 'webp']
UNCONVERTED_FILE_DIR = 'tmp/files'


# Send to S3 bucket

@app.task(name='format_converter')
def format_converter():
    # Delete the file/folder

    files = list_files(UNCONVERTED_FILE_DIR)

    for file in files:
        filename = file.split('.')[0]
        file_dir = f'tmp/img/{filename}'
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)

        for format in SUPPORTED_FORMATS:
            image = Image.open(f'tmp/files/{file}')
            image = image.convert('RGB')
            image = image.save(f'tmp/img/{filename}/{filename}.{format}')
        # except Exception as e:
        #     print(e)
        # return True


@app.task(name='background_upload')
def upload_file_celery(file_paths, bucket):
    s3 = boto3.resource('s3')
    for file_path in file_paths:
        file_upload_response = s3.meta.client.upload_file(
            f'tmp/img/{file_path}', bucket, Key=file_path)
