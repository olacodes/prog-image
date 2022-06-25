from PIL import Image
from io import BytesIO


def thumbnail(file, filename, ext, width, height):
    MAX_SIZE = (width, height)
    try:
        with Image.open(BytesIO(file)) as img:
            img.thumbnail(MAX_SIZE)
            filename = f'{filename}_thumbnail.{ext}'
            img.save(filename)
        return filename
    except OSError as e:
        print("Cannot filter this file", filename)
        print(e)
