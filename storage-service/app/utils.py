import os
import glob
from pathlib import Path
from os.path import isfile, isdir


def get_content_type(request):
    types = {'multipart/form-data;': 'form_data', 'application/json;': 'json'}
    content_type = request.headers['content-type']
    return types[content_type.split(" ")[0]]


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
