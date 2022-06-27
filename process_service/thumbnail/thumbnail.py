import environ
from PIL import Image
from io import BytesIO

env = environ.Env()
THUMBNAILED_FILES = env('THUMBNAILED_FILES',
                        default="process_service/tmp/thumbnailed")


def thumbnail(file, filename, ext, width, height, is_file=False):
    MAX_SIZE = (width, height)
    try:
        img = Image.open(file) if is_file else Image.open(BytesIO(file))
        img.thumbnail(MAX_SIZE)
        filename = f'{filename}_thumbnail.{ext}'
        img.save(f'{THUMBNAILED_FILES}/{filename}')
        return filename
    except OSError as e:
        print("Cannot filter this file", filename)
        print(e)
