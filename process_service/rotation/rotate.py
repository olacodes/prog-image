from PIL import Image
from io import BytesIO


def rotate(file, filename, ext, angle, expand, is_file=False):

    try:
        img = Image.open(file) if is_file else Image.open(BytesIO(file))
        img = img.rotate(
            angle, resample=Image.Resampling.NEAREST, expand=expand)
        filename = f'{filename}_rotate.{ext}'
        img.save(filename)
        return filename
    except OSError as e:
        print("Cannot rotate this file", filename)
        print(e)
