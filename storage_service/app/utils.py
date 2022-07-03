import os
import uuid
import glob
import shutil
import string
import random
from pathlib import Path
from os.path import isfile, isdir
from PIL import Image


def convert(format, filename, file=None):
    image = Image.open(f'tmp/files/{file}')
    image = image.convert('RGB')
    image = image.save(f'tmp/img/{filename}/{filename}.{format}')


def generate_id():
    random_letter = random.choice(string.ascii_letters)
    uuid_hex = str(uuid.uuid4().hex)
    return f'{random_letter}{uuid_hex}'.lower()


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    return dir_name


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


def remove_file_dir(dir_name):
    dirs = os.listdir(dir_name)
    for dir in dirs:
        file_dir = f'{dir_name}/{dir}'
        if isfile(file_dir):
            os.remove(file_dir)
        elif isdir(file_dir):
            shutil.rmtree(file_dir)
