
import os
import re
import environ
import requests

from PIL import Image
from io import BytesIO


# IO bound operation needs celery
def compress(
    file, filename, ext,
    is_file=False, size_ratio=0.9,
    quality=90, width=None, height=None
):
    img = Image.open(file) if is_file else Image.open(BytesIO(file))
    if size_ratio < 1.0:
        img = img.resize((int(img.size[0] * size_ratio),
                          int(img.size[1] * size_ratio)), Image.LANCZOS)
    if width and height:
        img = img.resize((width, height), Image.LANCZOS)
    new_filename = f"{filename}_compressed.{ext}"
    try:
        img.save(new_filename, quality=quality, optimize=True)
    except OSError:
        img = img.convert("RGB")
        img.save(new_filename, quality=quality, optimize=True)
    return new_filename
