
from PIL import Image
from io import BytesIO


def mask(file, filename, ext):
    try:
        with Image.open(BytesIO(file)) as img:
            mask = Image.new("RGB", img.size, 128)
            img = Image.composite(img, img, mask)
            filename = f'{filename}_mask.{ext}'
            img.save(filename)
        return filename
    except OSError as e:
        print("Cannot filter this file", filename)
        print(e)
