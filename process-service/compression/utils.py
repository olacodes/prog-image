
import os
import re
import environ
import requests

from PIL import Image
from io import BytesIO


def fetch_url(url):
    try:
        fname = url.split("/")[-1]
        fname, ext = fname.split(".")[0], fname.split(".")[-1]
        filename = re.sub('[^A-Za-z0-9]+', '', fname)
        res = requests.get(url, stream=True)
        file = res.content
        return file, filename, ext
    except Exception as e:
        filename, file, ext = None
        return file, filename, ext


def resize(
    file, filename, ext,
    file_type=None, size_ratio=0.9,
    quality=90, width=None, height=None
):
    img = Image.open(BytesIO(file)) if file_type else Image.open(file)
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
